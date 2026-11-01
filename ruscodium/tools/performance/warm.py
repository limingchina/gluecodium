#!/usr/bin/env python3
"""Separate persistent-process API experiment; see README for boundaries."""
import argparse, json, subprocess
from pathlib import Path
import benchmark as b

ITERATIONS = 20
WARMUPS = 10
PILOT_LIMIT_SECONDS = 3

def main():
    p = argparse.ArgumentParser(); p.add_argument('--work', type=Path, required=True); args = p.parse_args()
    work = args.work.resolve(); pilot = json.loads((work / 'pilot.json').read_text())
    current = b.environment(work)
    for key in ('native_binary_sha256', 'java_binary_sha256', 'jars_sha256', 'templates', 'runner_sha256', 'supervisor_sha256', 'supervisor_source_sha256'):
        if current[key] != pilot['environment'][key]: raise RuntimeError(f'identity changed after pilot: {key}')
    if (work / 'warm.json').exists(): raise RuntimeError('warm.json already exists; use a new work directory')
    names = [n for n in ('structs-10', 'structs-100') if pilot['workloads'][n]['parity'] and all(r['wall_seconds'] <= PILOT_LIMIT_SECONDS for r in pilot['workloads'][n]['runs'].values())]
    classes = work / 'warm-classes'; classes.mkdir(exist_ok=True)
    compile_java = [str(b.JAVA.parent / 'javac'), '-cp', str(b.LIB / '*'), '-d', str(classes), str(b.TOOL / 'WarmJvm.java')]
    compile_rust = ['cargo', 'build', '--offline', '--release', '--manifest-path', str(b.TOOL / 'warm-rust/Cargo.toml')]
    for cmd in (compile_java, compile_rust): subprocess.run(cmd, check=True, cwd=b.ROOT)
    binary = b.TOOL / 'warm-rust/target/release/ruscodium-performance-warm'
    data = {'schema': 'ruscodium.performance.persistent.v1', 'description': 'Persistent process, full load/validation/generate/write API iterations; process startup excluded; not CLI timings', 'selection_rule': '10 and 100 struct probes only, if both fresh pilot invocations each complete in at most 3 seconds with parity; 500 excluded to bound repeated cost.', 'selected': names, 'warmup_iterations': WARMUPS, 'timed_iterations': ITERATIONS-WARMUPS, 'build_commands': [compile_java, compile_rust], 'source_sha256': {'WarmJvm.java': b.digest(b.TOOL / 'WarmJvm.java'), 'warm-rust/src/main.rs': b.digest(b.TOOL / 'warm-rust/src/main.rs'), 'warm-rust/Cargo.toml': b.digest(b.TOOL / 'warm-rust/Cargo.toml'), 'warm.py': b.digest(Path(__file__))}, 'warm_binary_sha256': b.digest(binary), 'runs': {}, 'environment': b.environment(work)}
    b.write_json(work / 'warm.json', data)
    for name in names:
        spec = pilot['workloads'][name]['spec']; data['runs'][name] = {}
        if b.digest(Path(spec['input'])) != pilot['workloads'][name]['input_sha256']: raise RuntimeError(f'input changed: {name}')
        for side in ('jvm','rust'):
            output = work / 'persistent' / name / side
            if output.exists(): raise RuntimeError(f'output already exists: {output}')
            output.mkdir(parents=True)
            if side == 'jvm':
                jvm_home = output.parent / (output.name + '.jvm-home')
                if jvm_home.exists(): raise RuntimeError(f'JVM home already exists: {jvm_home}')
                jvm_home.mkdir()
                cmd = [str(b.JAVA), '-Duser.home=' + str(jvm_home), '-cp', str(classes) + ':' + str(b.LIB / '*'), 'WarmJvm', spec['input'], str(output), str(ITERATIONS)]
            else: cmd = [str(binary), spec['input'], str(output), str(ITERATIONS), str(b.TEMPLATES)]
            try:
                result = subprocess.run(cmd, cwd=b.ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)
            except subprocess.TimeoutExpired as exc:
                data['runs'][name][side] = {'argv': cmd, 'timeout_seconds': 300, 'timeout': True, 'stdout': (exc.stdout or b'').decode(errors='replace') if isinstance(exc.stdout, bytes) else exc.stdout, 'stderr': (exc.stderr or b'').decode(errors='replace') if isinstance(exc.stderr, bytes) else exc.stderr, 'valid': False}
                b.write_json(work / 'warm.json', data)
                raise
            entries = []
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts)==3 and parts[0].isdigit() and parts[1].isdigit():
                    i = int(parts[0]); out = output / str(i)
                    entries.append({'iteration': i, 'phase': 'warmup' if i < WARMUPS else 'timed', 'wall_seconds': int(parts[1])/1e9, 'success': parts[2] == 'true', 'matches_baseline': out.is_dir() and b.manifest(out) == pilot['workloads'][name]['inventories']['jvm']})
            logging_error = side == 'jvm' and ('Can\'t load log handler' in result.stderr or 'java.nio.file.FileSystemException' in result.stderr)
            ok = result.returncode==0 and not logging_error and len(entries)==ITERATIONS and all(e['success'] and e['matches_baseline'] for e in entries)
            data['runs'][name][side] = {'argv': cmd, 'exit_code': result.returncode, 'logging_error': logging_error, 'stdout': result.stdout, 'stderr': result.stderr, 'samples': entries, 'valid': ok, 'statistics': b.quantiles([e['wall_seconds'] for e in entries if e['phase']=='timed']) if ok else None}
            b.write_json(work / 'warm.json', data)
            print('persistent', name, side, 'valid', ok, flush=True)
            if not ok: raise RuntimeError(f'persistent failure {name} {side}')
        data['runs'][name]['jvm_over_rust_wall_median'] = data['runs'][name]['jvm']['statistics']['median'] / data['runs'][name]['rust']['statistics']['median']
        b.write_json(work / 'warm.json', data)

if __name__ == '__main__': main()
