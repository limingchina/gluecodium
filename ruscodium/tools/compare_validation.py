#!/usr/bin/env python3
"""Compare validation outcomes with an installed JVM Gluecodium.

Build ruscodium first and install the JVM distribution. Pass --java-home when
needed. --smoke also runs each checked-in smoke input with its auxiliary files.
This compares acceptance, not diagnostics, generated output, or crash behavior.
"""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[2]
CASES = {
    'basic': (True, ['package sample\nstruct Point { x: Int }\ninterface Service { fun fetch(point: Point): String }\n']),
    'multifile': (True, ['package sample\ninterface Service { fun f(x: other.Item) }\n', 'package other\nstruct Item { x: Int }\n']),
    'unresolved': (False, ['package sample\nstruct Point { x: Missing }\n']),
    'alias_cycle': (False, ['package sample\ntypealias A = B\ntypealias B = A\n']),
    'inherit_cycle': (False, ['package sample\ninterface A: B {}\ninterface B: A {}\n']),
    'ambiguous_enclosing': (False, ['package sample\nstruct Item { x: Int }\ninterface Outer {\nstruct Item { y: Int }\nfun f(x: Item)\n}\n']),
    'ambiguous_import': (False, ['package sample\nimport other.Item\nstruct Item { x: Int }\ninterface Service { fun f(x: Item) }\n', 'package other\nstruct Item { x: Int }\n']),
    'null_nonnullable': (False, ['package sample\nstruct A { x: Int = null }\n']),
}
KNOWN_SMOKE = {
    'comments': 'JVM rejects this group when its auxiliary comment source is supplied.',
    'defaults_const': 'Rust duplicate-member validation rejects this fixture; JVM accepts it.',
    'name_clash_overloads': 'Rust duplicate-member validation rejects this fixture; JVM accepts it.',
    'skip': 'Rust does not yet apply JVM filtering before validation.',
}


def invoke(binary, inputs, auxiliary, env, jvm, temp):
    command = [str(binary)]
    for path in inputs:
        command += ['-input', str(path)]
    for path in auxiliary:
        command += ['-auxinput', str(path)]
    command += ['-validate']
    if jvm:
        command += ['-generators', 'cpp']
    try:
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=45, errors='replace')
        output = (result.stdout + '\n' + result.stderr).replace(str(temp), '<temp>').replace(str(REPO), '<repo>')
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        relevant = [line for line in lines if any(term in line.lower() for term in ('error', 'exception', 'severe:', 'ambiguous', 'not found', 'duplicate', 'cycle'))]
        return {'returncode': result.returncode, 'accepted': result.returncode == 0,
                'crash': 'StackOverflowError' in output, 'diagnostics': (relevant or lines)[:4]}
    except subprocess.TimeoutExpired:
        return {'returncode': None, 'accepted': False, 'crash': False, 'timeout': True, 'diagnostics': ['Timed out after 45 seconds']}


def compare(name, inputs, auxiliary, expected, known, rust, jvm, env, temp):
    a = invoke(rust, inputs, auxiliary, env, False, temp)
    b = invoke(jvm, inputs, auxiliary, env, True, temp)
    difference = a['accepted'] != b['accepted']
    expected_difference = bool(known and difference and a['accepted'] == known[0] and b['accepted'] == known[1])
    failed = a.get('timeout', False) or b.get('timeout', False) or (difference and not expected_difference)
    if expected is not None and (a['accepted'] != expected or b['accepted'] != expected):
        failed = True
    return {'name': name, 'rust': a, 'jvm': b, 'expected_acceptance': expected,
            'expected_difference': known[2] if expected_difference else None, 'unexpected': bool(failed)}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--rust', type=Path, default=REPO / 'ruscodium/target/debug/ruscodium')
    parser.add_argument('--jvm', type=Path, default=REPO / 'gluecodium/build/install/gluecodium/bin/gluecodium')
    parser.add_argument('--java-home', type=Path, help='JDK home for the JVM launcher')
    parser.add_argument('--report', type=Path, help='write structured JSON to this path')
    parser.add_argument('--smoke', action='store_true', help='also compare checked-in smoke groups')
    args = parser.parse_args()
    for binary in (args.rust, args.jvm):
        if not binary.is_file() or not os.access(binary, os.X_OK):
            parser.error(f'executable not found: {binary}')
    with tempfile.TemporaryDirectory(prefix='ruscodium-validation-') as folder:
        temp = Path(folder)
        env = os.environ.copy()
        if args.java_home:
            env['JAVA_HOME'] = str(args.java_home.resolve())
        env['JAVA_OPTS'] = env.get('JAVA_OPTS', '') + ' ' + shlex.quote('-Duser.home=' + str(temp))
        results = []
        for name, (expected, sources) in CASES.items():
            directory = temp / name
            directory.mkdir()
            for index, source in enumerate(sources):
                (directory / f'{index}.lime').write_text(source, encoding='utf-8')
            results.append(compare(name, [directory], [], expected, None, args.rust.resolve(), args.jvm.resolve(), env, temp))
        results.append(compare('calculator', [REPO / 'examples/calculator/lime'], [], True, None, args.rust.resolve(), args.jvm.resolve(), env, temp))
        if args.smoke:
            smoke = REPO / 'gluecodium/src/test/resources/smoke'
            for group in sorted(smoke.iterdir()):
                inputs = group / 'input'
                if not inputs.is_dir() or not any(inputs.rglob('*.lime')):
                    continue
                aux = group / 'auxiliary'
                known = ((True, False) if group.name == 'comments' else (False, True)) + (KNOWN_SMOKE[group.name],) if group.name in KNOWN_SMOKE else None
                results.append(compare('smoke/' + group.name, [inputs], [aux] if aux.is_dir() else [], None, known, args.rust.resolve(), args.jvm.resolve(), env, temp))
        report = {'schema': 1, 'scope': 'validation acceptance only', 'cases': results,
                  'unexpected_count': sum(item['unexpected'] for item in results)}
        data = json.dumps(report, indent=2) + '\n'
        if args.report:
            args.report.write_text(data, encoding='utf-8')
        else:
            print(data, end='')
        return 1 if report['unexpected_count'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
