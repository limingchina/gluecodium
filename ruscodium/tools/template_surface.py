#!/usr/bin/env python3
"""Inventory lexical references in the checked-in Trimou templates."""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

REGISTERED = set('prefix prefixPartial joinPartial instanceOf notInstanceOf capitalize escape switch case default setJoin resolveName ifPredicate unlessPredicate sort filter'.split())
BUILTINS = set('eval isEq isNotEq include join numExpr set if unless each with'.split())
HELPERS = REGISTERED | BUILTINS
TAG = re.compile(r'{{!!.*?!}}|{{!!.*?}}|{{{.*?}}}|{{.*?}}', re.S)
TOKEN = re.compile(r'''(?:[^\s="']+=)?(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[^\s]+)''')
NUMBER = re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$')


def is_literal(value):
    return (not value or value[0] in "\"'" or value in ('true', 'false', 'null')
            or bool(NUMBER.fullmatch(value)))


def scan(root):
    files = sorted(root.rglob('*.mustache'))
    counts = collections.Counter()
    paths, helpers, partials, selectors = [], [], [], []
    file_hashes = []
    for file in files:
        name = file.relative_to(root).as_posix()
        target = name.split('/')[0] if '/' in name else '(root)'
        raw = file.read_bytes()
        text = raw.decode('utf-8')
        file_hashes.append({'file': name, 'sha256': hashlib.sha256(raw).hexdigest()})
        counts[target] += 1
        # File-wide binding names are conservative: scopes and shadowing require an engine.
        bindings = set()
        for candidate in TAG.finditer(text):
            body = candidate.group()[2:-2].strip()
            if body.startswith('#set '):
                bindings.update(t.split('=', 1)[0] for t in TOKEN.findall(body[5:]) if '=' in t)
        for match in TAG.finditer(text):
            tag = match.group()
            if tag.startswith('{{!'):
                continue
            line = text.count('\n', 0, match.start()) + 1
            location = {'file': name, 'line': line}
            body = tag[3:-3].strip() if tag.startswith('{{{') else tag[2:-2].strip()
            if not body or body[0] in '/!=':
                continue
            sigil = body[0] if body[0] in '#^>&+' else ''
            if sigil:
                body = body[1:].strip()
            parts = TOKEN.findall(body)
            if not parts:
                continue
            head, args = parts[0], parts[1:]
            if sigil == '+':
                partials.append({**location, 'kind': 'inline_definition', 'selector': head, 'dynamic': False})
                args_to_scan = args
            elif sigil == '>':
                partials.append({**location, 'kind': 'partial', 'selector': head, 'dynamic': not is_literal(head) and head.startswith('(')})
                args_to_scan = args
            elif head in HELPERS:
                helpers.append({**location, 'name': head, 'category': 'registered' if head in REGISTERED else 'builtin', 'section': sigil in '#^' and bool(sigil), 'arguments': args})
                args_to_scan = args
                if head in ('prefixPartial', 'joinPartial', 'include'):
                    index = 1 if head == 'joinPartial' else 0
                    if len(args) > index:
                        value = args[index]
                        partials.append({**location, 'kind': head, 'selector': value, 'dynamic': not value.startswith(('"', "'"))})
                if head in ('resolveName', 'ifPredicate', 'unlessPredicate', 'filter', 'sort', 'eval', 'instanceOf', 'notInstanceOf'):
                    selectors.append({**location, 'helper': head, 'arguments': args})
            else:
                args_to_scan = parts
            for token in args_to_scan:
                assignment = None
                if '=' in token:
                    assignment, token = token.split('=', 1)
                if not is_literal(token):
                    classification = ('context' if token == 'this' or token.startswith(('this.', '@', '../', './')) else 'possible_local' if token.split('.')[0] in bindings else 'candidate_property')
                    paths.append({**location, 'path': token, 'classification': classification, 'role': 'assignment_value' if assignment else ('section_or_value' if token == head and head not in HELPERS else 'argument'), **({'assignment': assignment} if assignment else {})})
    digest = hashlib.sha256(''.join(f"{x['file']}\0{x['sha256']}\n" for x in file_hashes).encode()).hexdigest()
    return {'schema': 1, 'template_count': len(files), 'targets': dict(sorted(counts.items())), 'corpus_sha256': digest, 'files': file_hashes, 'property_candidates': paths, 'helpers': helpers, 'partials': partials, 'selectors': selectors}


def main():
    default = Path(__file__).resolve().parents[2] / 'gluecodium/src/main/resources/templates'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=default, help='template root (default: repository production templates)')
    parser.add_argument('--summary', action='store_true', help='omit per-occurrence evidence')
    parser.add_argument('--output', type=Path, help='write JSON to this file instead of stdout')
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f'template root does not exist: {args.root}')
    result = scan(args.root)
    if args.summary:
        result = {**{k: result[k] for k in ('schema', 'template_count', 'targets', 'corpus_sha256')}, 'occurrence_counts': {k: len(result[k]) for k in ('property_candidates', 'helpers', 'partials', 'selectors')}, 'helper_counts': dict(sorted(collections.Counter(x['name'] for x in result['helpers']).items()))}
    output = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(output, encoding='utf-8')
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
