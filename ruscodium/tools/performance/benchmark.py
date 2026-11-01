#!/usr/bin/env python3
"""Parity-gated, fresh-process JVM/native C++ generation benchmark (Linux)."""
import argparse, datetime, hashlib, json, os, platform, random, shutil, statistics, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = Path(__file__).resolve().parent
TEMPLATES = ROOT / 'gluecodium/src/main/resources/templates'
LIB = ROOT / 'gluecodium/build/install/gluecodium/lib'
NATIVE = ROOT / 'ruscodium/target/release/ruscodium'
JAVA = Path(os.environ.get('JAVA_HOME', '/workspace/.gluecodium-env/jdk-17.0.16+8')) / 'bin/java'
FIXTURES = ROOT / 'ruscodium/tools/cpp-generation-oracle'
SUPERVISOR = TOOL / 'supervisor'
SEED = 20261101
TIMEOUT = 60
TRIALS = 8

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p, value): p.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
def run_text(args):
    return subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout.strip()
def read(path):
    try: return Path(path).read_text().strip()
    except OSError: return None

def manifest(root):
    files = {str(p.relative_to(root)): {'sha256': digest(p), 'bytes': p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file()}
    h = hashlib.sha256()
    for name, item in files.items():
        h.update(name.encode()); h.update(b'\0'); h.update(bytes.fromhex(item['sha256'])); h.update(b'\0'); h.update(str(item['bytes']).encode()); h.update(b'\n')
    return {'files': files, 'file_count': len(files), 'bytes': sum(v['bytes'] for v in files.values()), 'sha256': h.hexdigest()}

def prepare(work):
    work.mkdir(parents=True, exist_ok=True)
    inputs = work / 'inputs'; inputs.mkdir(exist_ok=True)
    default = (FIXTURES / 'default.lime').read_text().replace('field constructor(label)', 'field constructor(label, mapping, tags)')
    (inputs / 'default-normalized.lime').write_text(default)
    shutil.copyfile(FIXTURES / 'custom.lime', inputs / 'custom.lime')
    shutil.copyfile(FIXTURES / 'aux.lime', inputs / 'aux.lime')
    for n in (10, 100, 125, 500):
        (inputs / f'structs-{n}.lime').write_text('package benchmark.scale\n\n' + ''.join(f'struct Item{i:04d} {{ value: Int }}\n' for i in range(n)))
    copyright_file = inputs / 'copyright.txt'; copyright_file.write_text('Copyright 2026 Example\nAll rights reserved.')
    options = {'schema': 'gluecodium.native-cpp-options', 'version': 1, 'root_namespace': ['acme', 'api'], 'internal_namespace': ['acme', 'detail'], 'export': 'ACME_API', 'export_common': 'ACME_COMMON', 'copyright_header': copyright_file.read_text()}
    write_json(inputs / 'custom-options.json', options)
    names = ['custom', 'default-normalized', 'structs-10', 'structs-100', 'structs-500', 'structs-125']
    return {name: {'input': str(inputs / (name + '.lime')), 'aux': str(inputs / 'aux.lime') if name == 'custom' else None, 'native_options': str(inputs / 'custom-options.json') if name == 'custom' else None, 'copyright': str(copyright_file) if name == 'custom' else None, 'declarations': {'custom': 3, 'default-normalized': 5}.get(name, int(name.split('-')[-1]) if name.startswith('structs-') else None)} for name in names}

def commands(spec, output):
    j = [str(JAVA), '-cp', str(LIB / '*'), 'com.here.gluecodium.Gluecodium', '-input', spec['input'], '-generators', 'cpp', '-output', str(output)]
    r = [str(NATIVE), 'compile-cpp', '--input', spec['input'], '--templates', str(TEMPLATES), '--output', str(output)]
    if spec['aux']: j += ['-auxinput', spec['aux']]; r += ['--auxinput', spec['aux']]
    if spec['native_options']:
        j += ['-cppnamespace', 'acme.api', '-intnamespace', 'acme.detail', '-cppexport', 'ACME_API', '-cppexportcommon', 'ACME_COMMON', '-copyright', spec['copyright']]
        r += ['--options', spec['native_options']]
    return {'jvm': j, 'rust': r}

def invoke(cmd, out, timeout=TIMEOUT):
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists(): raise RuntimeError(f'output already exists: {out}')
    log = out.parent / (out.name + '.log')
    completed = subprocess.run([str(SUPERVISOR), str(timeout), str(log)] + cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    result = json.loads(completed.stdout)
    result['cpu_seconds'] = result['user_seconds'] + result['system_seconds']
    result['argv'] = cmd
    result['log'] = log.read_text(errors='replace'); log.unlink()
    return result

def environment(work):
    templates = manifest(TEMPLATES)
    jars = {p.name: digest(p) for p in sorted(LIB.glob('*.jar'))}
    cpu = read('/proc/cpuinfo') or ''
    model = next((line.split(':',1)[1].strip() for line in cpu.splitlines() if line.startswith('model name')), None)
    return {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'git_commit': run_text(['git','rev-parse','HEAD']), 'git_status_short': run_text(['git','status','--short']), 'os': platform.platform(), 'kernel': platform.release(), 'cpu_model': model, 'logical_cpus': os.cpu_count(), 'affinity': sorted(os.sched_getaffinity(0)), 'cpu_max': read('/sys/fs/cgroup/cpu.max'), 'memory_max': read('/sys/fs/cgroup/memory.max'), 'meminfo': read('/proc/meminfo'), 'filesystem': run_text(['df','-T',str(work)]), 'java_version': run_text([str(JAVA),'-version']), 'java_binary_sha256': digest(JAVA), 'jars_sha256': jars, 'rustc_version': run_text(['rustc','--version','--verbose']), 'native_binary_sha256': digest(NATIVE), 'native_build_command': 'cargo build --offline --release', 'templates': templates, 'python': sys.version, 'environment': {k: os.environ.get(k) for k in ('JAVA_HOME','JAVA_TOOL_OPTIONS','JDK_JAVA_OPTIONS','_JAVA_OPTIONS','RUSTFLAGS','RUSTUP_TOOLCHAIN','PATH')}, 'work_dir': str(work), 'runner_sha256': digest(Path(__file__)), 'supervisor_sha256': digest(SUPERVISOR), 'supervisor_source_sha256': digest(TOOL / 'supervisor.c'), 'cc_version': run_text(['cc', '--version']).splitlines()[0]}

def pilot(work):
    if (work / 'pilot.json').exists(): raise RuntimeError('pilot.json already exists; use a new work directory')
    specs = prepare(work)
    data = {'schema': 'ruscodium.performance.pilot.v1', 'timeout_seconds': TIMEOUT, 'selection_rule': 'Include all parity-passing workloads whose JVM and Rust pilot invocations finish within 60 seconds; if 500 times out, also pilot 125 as an intermediate; retain all exclusions with diagnostics.', 'effective_defaults': {'generators': ['cpp'], 'root_namespace': [], 'internal_namespace': [], 'export': '_GLUECODIUM_CPP', 'export_common': '_GLUECODIUM_CPP', 'copyright_header': None, 'cache': False}, 'source_normalization': 'Copied default.lime: field constructor(label) changed to field constructor(label, mapping, tags) to satisfy JVM validation.', 'environment': environment(work), 'workloads': {}}
    for name, spec in specs.items():
        if name == 'structs-125' and not any(r['timeout'] for r in data['workloads']['structs-500']['runs'].values()): continue
        source = Path(spec['input'])
        entry = {'spec': spec, 'input_sha256': digest(source), 'input_bytes': source.stat().st_size, 'input_lines': len(source.read_text().splitlines()), 'runs': {}}
        if spec['aux']: entry['aux_sha256'] = digest(Path(spec['aux']))
        if spec['native_options']: entry['options_sha256'] = digest(Path(spec['native_options']))
        inventories = {}
        for side in ('jvm', 'rust'):
            out = work / 'pilot' / name / side
            result = invoke(commands(spec, out)[side], out)
            if result['exit_code'] == 0 and not result['timeout']: inventories[side] = manifest(out)
            entry['runs'][side] = result
            print('pilot', name, side, round(result['wall_seconds'], 3), result['exit_code'], flush=True)
        entry['parity'] = len(inventories) == 2 and inventories['jvm'] == inventories['rust'] and inventories['jvm']['file_count'] > 0
        entry['inventories'] = inventories
        data['workloads'][name] = entry
        write_json(work / 'pilot.json', data)
    return data

def quantiles(values):
    values = sorted(values); n = len(values)
    def q(x):
        pos = (n-1)*x; lo = int(pos); hi = min(lo+1,n-1)
        return values[lo] + (values[hi]-values[lo])*(pos-lo)
    return {'min': values[0], 'q1': q(.25), 'median': statistics.median(values), 'q3': q(.75), 'max': values[-1], 'iqr': q(.75)-q(.25)}

def measure(work):
    data = json.loads((work / 'pilot.json').read_text())
    current = environment(work)
    for key in ('native_binary_sha256', 'java_binary_sha256', 'jars_sha256', 'templates', 'runner_sha256', 'supervisor_sha256', 'supervisor_source_sha256'):
        if current[key] != data['environment'][key]: raise RuntimeError(f'identity changed after pilot: {key}')
    for name, entry in data['workloads'].items():
        spec = entry['spec']
        for field, key in (('input', 'input_sha256'), ('aux', 'aux_sha256'), ('native_options', 'options_sha256')):
            if spec[field] and digest(Path(spec[field])) != entry[key]: raise RuntimeError(f'identity changed after pilot: {name} {field}')
        if spec['copyright'] and Path(spec['copyright']).read_text() != json.loads(Path(spec['native_options']).read_text())['copyright_header']: raise RuntimeError('copyright changed')
    if (work / 'fresh.json').exists(): raise RuntimeError('fresh.json already exists; use a new work directory')
    names = [name for name,e in data['workloads'].items() if e['parity']]
    rng = random.Random(SEED)
    schedule = []
    for name in names:
        first = ['jvm']*(TRIALS//2) + ['rust']*(TRIALS//2); rng.shuffle(first)
        for round_no, side in enumerate(first, 1):
            schedule.append({'workload': name, 'round': round_no, 'order': [side, 'rust' if side == 'jvm' else 'jvm']})
    rng.shuffle(schedule)
    report = {'schema': 'ruscodium.performance.fresh.v1', 'mode': 'fresh process, warm filesystem', 'seed': SEED, 'trials': TRIALS, 'timeout_seconds': TIMEOUT, 'selected': names, 'schedule': schedule, 'warmups': [], 'samples': [], 'environment': environment(work), 'statistics': {}}
    write_json(work / 'fresh.json', report)
    for name in names:
        for side in ('jvm', 'rust'):
            out = work / 'warmup' / name / side
            result = invoke(commands(data['workloads'][name]['spec'], out)[side], out)
            result.update({'workload': name, 'implementation': side, 'matches_baseline': result['exit_code'] == 0 and manifest(out) == data['workloads'][name]['inventories']['jvm']})
            report['warmups'].append(result); write_json(work / 'fresh.json', report)
            if not result['matches_baseline']: raise RuntimeError(f'warmup failed {name} {side}')
    for pair in schedule:
        for position, side in enumerate(pair['order'], 1):
            name = pair['workload']; out = work / 'timed' / name / str(pair['round']) / side
            result = invoke(commands(data['workloads'][name]['spec'], out)[side], out)
            result.update({'workload': name, 'round': pair['round'], 'position': position, 'implementation': side, 'matches_baseline': result['exit_code'] == 0 and not result['timeout'] and manifest(out) == data['workloads'][name]['inventories']['jvm']})
            report['samples'].append(result); write_json(work / 'fresh.json', report)
            print('sample', name, pair['round'], side, round(result['wall_seconds'],3), result['matches_baseline'], flush=True)
    for name in names:
        report['statistics'][name] = {}
        for side in ('jvm', 'rust'):
            samples = [s for s in report['samples'] if s['workload']==name and s['implementation']==side and s['matches_baseline']]
            report['statistics'][name][side] = {'count': len(samples), **{key: quantiles([s[key] for s in samples]) for key in ('wall_seconds','user_seconds','system_seconds','cpu_seconds','peak_rss_kib')} } if samples else {'count': 0}
        a,b = (report['statistics'][name][s] for s in ('jvm','rust'))
        if a['count']==TRIALS and b['count']==TRIALS: report['statistics'][name]['jvm_over_rust_wall_median'] = a['wall_seconds']['median']/b['wall_seconds']['median']
    write_json(work / 'fresh.json', report)
    if any(not s['matches_baseline'] for s in report['samples']): raise RuntimeError('one or more timed samples failed parity')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('phase', choices=('pilot','measure')); parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args(); work = args.work.resolve(); work.mkdir(parents=True, exist_ok=True)
    if args.phase == 'pilot': pilot(work)
    else: measure(work)
