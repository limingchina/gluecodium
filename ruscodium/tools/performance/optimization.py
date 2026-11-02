#!/usr/bin/env python3
"""Predeclared, full-output-gated M14 fresh-process comparison (Linux)."""
import argparse
import datetime
import json
import random
from pathlib import Path

import benchmark as b

NAMES = ('custom', 'default-normalized', 'structs-10', 'structs-100', 'structs-125', 'structs-500')
SIDES = ('jvm', 'baseline', 'optimized')
SEED = 20261102
TIMEOUT = 60
COUNTS = {name: {'jvm': 8, 'optimized': 8, 'baseline': 1 if name == 'structs-500' else 3} for name in NAMES}


def schedule():
    rng = random.Random(SEED)
    groups = []
    for name in NAMES:
        order = ['jvm'] * 4 + ['optimized'] * 4
        rng.shuffle(order)
        for trial, first in enumerate(order, 1):
            second = 'optimized' if first == 'jvm' else 'jvm'
            groups.append([{'workload': name, 'side': side, 'trial': trial, 'position': i + 1, 'kind': 'sample'} for i, side in enumerate((first, second))])
        for trial in range(1, COUNTS[name]['baseline'] + 1):
            groups.append([{'workload': name, 'side': 'baseline', 'trial': trial, 'position': 1, 'kind': 'censored-pilot' if name == 'structs-500' else 'sample'}])
    rng.shuffle(groups)
    return [item for group in groups for item in group]


def success(result):
    return result['exit_code'] == 0 and not result['timeout'] and not result['logging_error']


def check_result(result, inventory, reference):
    return bool(success(result) and inventory and inventory['file_count'] and reference and inventory == reference)


def command(spec, out, side, binaries):
    commands = b.commands(spec, out)
    if side == 'jvm':
        return commands['jvm']
    cmd = commands['rust']
    cmd[0] = str(binaries[side])
    return cmd


def identities(binaries, specs):
    return {
        'binaries': {side: {'path': str(path), 'sha256': b.digest(path)} for side, path in binaries.items()},
        'java_sha256': b.digest(b.JAVA),
        'jars': {p.name: b.digest(p) for p in sorted(b.LIB.glob('*.jar'))},
        'templates': b.manifest(b.TEMPLATES),
        'inputs': {name: {key: b.digest(Path(spec[key])) for key in ('input', 'aux', 'native_options', 'copyright') if spec[key]} for name, spec in specs.items()},
        'runner_sha256': b.digest(Path(__file__)),
        'benchmark_module_sha256': b.digest(Path(b.__file__)),
        'supervisor_sha256': b.digest(b.SUPERVISOR),
        'supervisor_source_sha256': b.digest(b.TOOL / 'supervisor.c'),
    }


def save(path, data):
    tmp = path.with_suffix('.tmp')
    b.write_json(tmp, data)
    tmp.replace(path)


def invoke_attempt(item, specs, binaries, work, reference):
    name, side = item['workload'], item['side']
    out = work / item['kind'] / name / str(item['trial']) / side
    result = dict(item)
    try:
        run = b.invoke(command(specs[name], out, side, binaries), out, TIMEOUT)
        result.update(run)
        # Capture every existing tree, including partial failure output; compare all files.
        inventory = b.manifest(out) if out.is_dir() else None
        result['inventory'] = inventory
        result['matches_reference'] = check_result(run, inventory, reference)
    except Exception as exc:
        log = out.parent / (out.name + '.log')
        result.update({'harness_error': f'{type(exc).__name__}: {exc}', 'harness_stderr': getattr(exc, 'stderr', None), 'log': log.read_text(errors='replace') if log.is_file() else None, 'inventory': b.manifest(out) if out.is_dir() else None, 'matches_reference': False})
    return result


def summarize(data):
    stats = {}
    for name in NAMES:
        stats[name] = {}
        for side in SIDES:
            attempts = [x for x in data['samples'] if x['workload'] == name and x['side'] == side]
            valid = [x for x in attempts if x['matches_reference']]
            item = {'scheduled': COUNTS[name][side], 'attempted': len(attempts), 'valid': len(valid)}
            if valid and len(valid) == COUNTS[name][side] and not (name == 'structs-500' and side == 'baseline'):
                for key in ('wall_seconds', 'cpu_seconds', 'peak_rss_kib'):
                    item[key] = b.quantiles([x[key] for x in valid])
            stats[name][side] = item
        opt, jvm, old = (stats[name][s] for s in ('optimized', 'jvm', 'baseline'))
        if 'wall_seconds' in opt and 'wall_seconds' in jvm:
            stats[name]['jvm_over_optimized'] = jvm['wall_seconds']['median'] / opt['wall_seconds']['median']
        if 'wall_seconds' in opt and 'wall_seconds' in old:
            stats[name]['baseline_over_optimized'] = old['wall_seconds']['median'] / opt['wall_seconds']['median']
    return stats


def run(work, baseline, optimized):
    work = work.resolve()
    if work.exists() and any(work.iterdir()):
        raise RuntimeError('work directory must be empty')
    work.mkdir(parents=True, exist_ok=True)
    binaries = {'baseline': baseline.resolve(strict=True), 'optimized': optimized.resolve(strict=True)}
    specs = b.prepare(work)
    initial_identity = identities(binaries, specs)
    data = {'schema': 'ruscodium.performance.optimization.v1', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'seed': SEED, 'timeout_seconds': TIMEOUT, 'counts': COUNTS,
            'policy': 'Six JVM reference preflights; every scheduled attempt is retained. Full output inventories include all files and are compared outside the timer. A baseline 500 attempt is a capped pilot, with no baseline speed ratio.',
            'baseline_source_commit': '15b1db4c48ef0fbf7a86aefa6750f6ebcd5a5e88',
            'baseline_build_command': 'cargo build --offline --release --manifest-path /tmp/ruscodium-m14-clean/ruscodium/Cargo.toml',
            'optimized_build_command': 'cargo build --offline --release',
            'environment': b.environment(work), 'identities_before': initial_identity,
            'workloads': specs, 'preflight_schedule': [{'workload': name, 'side': 'jvm', 'trial': 1, 'kind': 'preflight'} for name in NAMES],
            'schedule': schedule(), 'preflights': [], 'samples': [], 'statistics': {}}
    report = work / 'optimization.json'
    save(report, data)  # The complete schedule and identities precede every invocation.
    references = {}
    for item in data['preflight_schedule']:
        result = invoke_attempt(item, specs, binaries, work, None)
        if 'exit_code' in result and success(result) and result['inventory'] and result['inventory']['file_count']:
            references[item['workload']] = result['inventory']
            result['matches_reference'] = True
        data['preflights'].append(result)
        save(report, data)
        print('preflight', item['workload'], result.get('wall_seconds'), result['matches_reference'], flush=True)
    for item in data['schedule']:
        result = invoke_attempt(item, specs, binaries, work, references.get(item['workload']))
        data['samples'].append(result)
        save(report, data)
        print('sample', item['workload'], item['side'], item['trial'], result.get('wall_seconds'), result['matches_reference'], flush=True)
    data['identities_after'] = identities(binaries, specs)
    data['identities_match'] = data['identities_after'] == initial_identity
    data['statistics'] = summarize(data) if data['identities_match'] else {}
    data['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(report, data)
    failures = [x for x in data['preflights'] if not x['matches_reference']]
    failures += [x for x in data['samples'] if not x['matches_reference'] and not (x['kind'] == 'censored-pilot' and x.get('timeout'))]
    if failures or not data['identities_match']:
        raise RuntimeError(f'{len(failures)} invalid invocations or identities changed; see {report}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--optimized', type=Path, required=True)
    args = parser.parse_args()
    run(args.work, args.baseline, args.optimized)
