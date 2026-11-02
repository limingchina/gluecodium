#!/usr/bin/env python3
"""Project independently built C++ jobs onto explicitly enumerated model facts."""
import json
from pathlib import PurePath
import sys


COMMON = 'attributes comment external path'.split()
TYPE = COMMON + ['childTypes']
CONTAINER = TYPE + 'classes constants enumerations exceptions functions interfaces lambdas properties structs typeAliases'.split()
SCHEMA = {
    'LimeModel': 'auxiliaryElements fileNameMap referenceMap topElements'.split(),
    'LimePath': 'disambiguator head tail'.split(),
    'LimeAttributes': ['attributes'],
    'LimeComment': 'isExcluded path placeholders'.split(),
    'LimeBasicType': TYPE + ['typeId'],
    'LimeClass': CONTAINER + 'isOpen parents'.split(),
    'LimeInterface': CONTAINER + 'isNarrow isOpen parents'.split(),
    'LimeStruct': CONTAINER + 'constructorComment fieldConstructors fields'.split(),
    'LimeEnumeration': TYPE + ['enumerators'],
    'LimeException': TYPE + ['errorType'],
    'LimeTypeAlias': TYPE + ['typeRef'],
    'LimeLambda': TYPE + 'parameters returnType'.split(),
    'LimeList': TYPE + ['elementType'],
    'LimeSet': TYPE + ['elementType'],
    'LimeMap': TYPE + 'keyType valueType'.split(),
    'LimeField': COMMON + 'defaultValue typeRef'.split(),
    'LimeConstant': COMMON + 'typeRef value'.split(),
    'LimeEnumerator': COMMON + ['explicitValue'],
    'LimeParameter': COMMON + ['typeRef'],
    'LimeLambdaParameter': COMMON + 'isNamedParameter typeRef'.split(),
    'LimeFunction': COMMON + 'isConstructor isStatic parameters returnType thrownType'.split(),
    'LimeProperty': COMMON + 'additionalDescriptionComment getter isStatic setter typeRef valueComment'.split(),
    'LimeReturnType': 'attributes comment typeRef'.split(),
    'LimeThrownType': 'comment typeRef'.split(),
    'LimeFieldConstructor': COMMON + 'fieldRefs structRef'.split(),
    'LimeLazyFieldRef': 'attributes element'.split(),
    'LimeValue$Literal': 'attributes typeRef value'.split(),
    'LimeValue$Null': 'attributes typeRef'.split(),
    'LimeBasicTypeRef': 'attributes element elementFullName isNullable type'.split(),
    'LimeLazyTypeRef': 'attributes element elementFullName isNullable type'.split(),
    'LimeAmbiguousTypeRef': 'attributes element isNullable type'.split(),
    'LimeDirectTypeRef': 'attributes element isNullable type'.split(),
}
MEMBERS = 'classes constants enumerations exceptions functions interfaces lambdas properties structs typeAliases fields fieldConstructors enumerators parameters'.split()
REFS = {'LimeBasicTypeRef', 'LimeLazyTypeRef', 'LimeAmbiguousTypeRef', 'LimeDirectTypeRef'}
OVERLAYS = {
    'LimeBasicType': {'name', 'fullName', 'actualType'},
    'LimeClass': {'name', 'fullName', 'actualType'},
    'LimeInterface': {'name', 'fullName', 'actualType'},
    'LimeStruct': {'name', 'fullName', 'actualType', 'uninitializedFields'},
    'LimeEnumeration': {'name', 'fullName', 'actualType', 'uniqueEnumerators'},
    'LimeException': {'name', 'fullName', 'actualType'},
    'LimeTypeAlias': {'name', 'fullName', 'actualType'},
    'LimeLambda': {'name', 'fullName', 'actualType'},
    'LimeList': {'name', 'fullName', 'actualType'},
    'LimeSet': {'name', 'fullName', 'actualType'},
    'LimeMap': {'name', 'fullName', 'actualType'},
    'LimeField': {'name', 'fullName'},
    'LimeConstant': {'name', 'fullName'},
    'LimeEnumerator': {'name', 'fullName'},
    'LimeParameter': {'name', 'fullName'},
    'LimeLambdaParameter': {'name', 'fullName'},
    'LimeFunction': {'name', 'fullName', 'exception'},
    'LimeProperty': {'name', 'fullName'},
    'LimeFieldConstructor': {'name', 'fullName', 'fields', 'struct'},
    'LimeReturnType': {'isVoid'},
    'LimeComment': {'isEmpty'},
}


def normalize_sections(raw):
    """Join adjacent ordinary same-tag fragments without merging placeholders."""
    sections = []
    for tag, fragment in raw:
        if sections and sections[-1][0] == tag and tag != 'Placeholder':
            sections[-1][1] += fragment
        else:
            sections.append([tag, fragment])
    return sections


class Projection:
    def __init__(self, job):
        self.job = job
        self.nodes = {n['id']: n for n in job['snapshot']['nodes']}
        if len(self.nodes) != len(job['snapshot']['nodes']):
            raise ValueError('duplicate node identity')
        self.overlays = job.get('property_overlays', {})
        self.comments = job.get('raw_comments', {})
        for node in self.nodes.values():
            kind = self.kind(node)
            if kind not in SCHEMA or set(node['properties']) != set(SCHEMA[kind]):
                raise ValueError(f'unhandled node/fields: {kind}: {sorted(node["properties"])}')
        for ident, values in self.overlays.items():
            kind = self.kind(self.nodes[ident])
            if set(values) - OVERLAYS.get(kind, set()):
                raise ValueError(f'unhandled getter properties: {kind}: {sorted(values)}')
        self.reference_map = self.props(job['snapshot']['root'])['referenceMap']

    @staticmethod
    def kind(node):
        return node['class'].rsplit('.', 1)[-1]

    def node(self, ref):
        if not isinstance(ref, dict) or set(ref) != {'$ref'}:
            raise ValueError(f'expected reference: {ref!r}')
        return self.nodes[ref['$ref']]

    def props(self, ref):
        return self.node(ref)['properties']

    def path(self, ref):
        p = self.props(ref)
        return {'head': p['head'], 'tail': p['tail'], 'disambiguator': p['disambiguator']}

    def named(self, ref):
        node = self.node(ref)
        p = node['properties']
        path = self.path(p['path'])
        result = {'kind': self.kind(node), 'path': path}
        if self.kind(node) == 'LimeBasicType':
            # Builtin wrappers often have empty paths and fresh allocations.
            result['typeId'] = p['typeId']
        return result

    def declared(self, ref):
        """Named type and field links must share the canonical model object."""
        node = self.node(ref)
        if self.kind(node) != 'LimeBasicType':
            path = self.path(node['properties']['path'])
            key = self.path_key(path)
            if self.reference_map.get(key) != ref:
                raise ValueError(f'noncanonical declaration target: {key}')
        return self.named(ref)

    @staticmethod
    def path_key(path):
        key = '.'.join(path['head'] + path['tail'])
        return key + (':' + path['disambiguator'] if path['disambiguator'] else '')

    def attrs(self, ref):
        return self.props(ref)['attributes']

    def comment(self, ref):
        p = self.props(ref)
        if p['placeholders']:
            raise ValueError('comment placeholders are outside this projection')
        ident = ref['$ref']
        if ident in self.comments:
            # Consecutive fragments with the same tag concatenate in order;
            # the JVM lexer may split words/punctuation while the native loader
            # retains a single contiguous fragment. Preserve tag transitions.
            raw = self.comments[ident]
            if any(tag == 'Placeholder' for tag, _ in raw):
                raise ValueError('comment placeholders are outside this projection')
            sections = normalize_sections(raw)
            empty = all(not fragment for _, fragment in raw)
        else:
            sections = None
            empty = self.overlays.get(ident, {}).get('isEmpty')
            if empty is None:
                raise ValueError(f'comment emptiness unavailable: {ident}')
        return {'empty': empty, 'excluded': p['isExcluded'], 'path': self.path(p['path']),
                'placeholders': p['placeholders'], 'sections': sections if sections else []}

    def target(self, ref, trail=()):
        node = self.node(ref)
        kind = self.kind(node)
        p = node['properties']
        if kind in REFS:
            return self.typeref(ref, trail)
        if kind in ('LimeList', 'LimeSet'):
            return {'kind': kind, 'attributes': self.attrs(p['attributes']),
                    'comment': self.comment(p['comment']), 'external': p['external'],
                    'path': self.path(p['path']), 'argument': self.typeref(p['elementType'], trail),
                    'childTypes': [self.typeref(x, trail) for x in p['childTypes']]}
        if kind == 'LimeMap':
            return {'kind': kind, 'attributes': self.attrs(p['attributes']),
                    'comment': self.comment(p['comment']), 'external': p['external'],
                    'path': self.path(p['path']), 'key': self.typeref(p['keyType'], trail),
                    'value': self.typeref(p['valueType'], trail),
                    'childTypes': [self.typeref(x, trail) for x in p['childTypes']]}
        return self.declared(ref)

    def typeref(self, ref, trail=()):
        node = self.node(ref)
        kind = self.kind(node)
        if kind not in REFS:
            raise ValueError(f'expected type ref, got {kind}')
        p = node['properties']
        target = p['element']
        # element and type are separate backend facts; compare both. Getter-created
        # equivalent objects are represented structurally instead of by allocation ID.
        direct = self.target(target, trail)
        resolved = self.target(p['type'], trail)
        actual = target
        while self.kind(self.node(actual)) == 'LimeTypeAlias':
            if actual['$ref'] in trail:
                raise ValueError('cyclic alias')
            trail = (*trail, actual['$ref'])
            actual = self.props(self.props(actual)['typeRef'])['type']
        return {'nullable': p['isNullable'], 'attributes': self.attrs(p['attributes']),
                'element': direct, 'type': resolved, 'actual': self.target(actual, trail)}

    def value(self, ref):
        if ref is None:
            return None
        node = self.node(ref)
        p = node['properties']
        kind = self.kind(node)
        if kind not in ('LimeValue$Null', 'LimeValue$Literal'):
            raise ValueError(f'unhandled value: {kind}')
        return {'kind': kind, 'attributes': self.attrs(p['attributes']),
                'type': self.typeref(p['typeRef']), 'value': p.get('value')}

    def return_type(self, ref):
        p = self.props(ref)
        return {'attributes': self.attrs(p['attributes']), 'comment': self.comment(p['comment']),
                'type': self.typeref(p['typeRef'])}

    def declaration(self, ref):
        node = self.node(ref)
        kind, p = self.kind(node), node['properties']
        path = self.path(p['path'])
        key = self.path_key(path)
        if key in self.reference_map and self.reference_map[key] != ref:
            raise ValueError(f'noncanonical owned declaration: {key}')
        result = {'kind': kind, 'path': path, 'attributes': self.attrs(p['attributes']),
                  'comment': self.comment(p['comment']), 'external': p['external']}
        for key in MEMBERS:
            if key in p:
                result[key] = [self.declaration(x) for x in p[key]]
        for key in ('isStatic', 'isConstructor', 'isNamedParameter', 'isOpen', 'isNarrow'):
            if key in p:
                result[key] = p[key]
        if 'parents' in p:
            result['parents'] = [self.typeref(x) for x in p['parents']]
        if 'typeRef' in p:
            result['typeRef'] = self.typeref(p['typeRef'])
        if 'errorType' in p:
            result['errorType'] = self.typeref(p['errorType'])
        if 'childTypes' in p:
            result['childTypes'] = [self.typeref(x) for x in p['childTypes']]
        if 'returnType' in p:
            result['returnType'] = self.return_type(p['returnType'])
        if 'thrownType' in p:
            thrown = p['thrownType']
            if thrown is None:
                result['thrownType'] = None
                exception = None
            else:
                if self.kind(self.node(thrown)) != 'LimeThrownType':
                    raise ValueError('expected LimeThrownType')
                tp = self.props(thrown)
                result['thrownType'] = {'typeRef': self.typeref(tp['typeRef']),
                                        'comment': self.comment(tp['comment'])}
                actual = result['thrownType']['typeRef']['actual']
                exception = actual if actual['kind'] == 'LimeException' else None
            overlay = self.overlays.get(ref['$ref'], {})
            if 'exception' in overlay:
                observed = None if overlay['exception'] is None else self.declared(overlay['exception'])
                if observed != exception:
                    raise ValueError(f'inconsistent exception getter: {ref["$ref"]}')
            result['exception'] = exception
        for key in ('getter', 'setter'):
            if key in p:
                result[key] = None if p[key] is None else self.declaration(p[key])
        for key in ('additionalDescriptionComment', 'valueComment', 'constructorComment'):
            if key in p:
                result[key] = self.comment(p[key])
        for key in ('defaultValue', 'explicitValue'):
            if key in p:
                result[key] = self.value(p[key])
        if kind == 'LimeConstant':
            result['value'] = self.value(p['value'])
        if 'fieldRefs' in p:
            result['fieldRefs'] = [{'attributes': self.attrs(self.props(x)['attributes']),
                                    'element': self.declared(self.props(x)['element'])}
                                   for x in p['fieldRefs']]
            result['structRef'] = self.typeref(p['structRef'])
        return result

    def project(self):
        # Getter-created views may be separately allocated. Check their semantic
        # targets rather than comparing identities or silently discarding them.
        for ident, overlay in self.overlays.items():
            if 'actualType' not in overlay:
                continue
            ref = {'$ref': ident}
            node = self.node(ref)
            if self.kind(node) == 'LimeTypeAlias':
                expected = self.typeref(node['properties']['typeRef'])['actual']
            else:
                expected = self.target(ref)
            if self.target(overlay['actualType']) != expected:
                raise ValueError(f'inconsistent actualType getter: {ident}')
        root = self.props(self.job['snapshot']['root'])
        refs = {key: self.named(ref) for key, ref in sorted(root['referenceMap'].items())}
        builtins = {}
        for key, ref in sorted(root['referenceMap'].items()):
            node = self.node(ref)
            if self.kind(node) == 'LimeBasicType':
                p = node['properties']
                builtins[key] = {'identity': self.named(ref), 'typeId': p['typeId'],
                                 'attributes': self.attrs(p['attributes']),
                                 'comment': self.comment(p['comment']), 'external': p['external'],
                                 'childTypes': [self.typeref(x) for x in p['childTypes']]}
        source_paths = set(root['fileNameMap'].values())
        if len({PurePath(path).name for path in source_paths}) != len(source_paths):
            raise ValueError('source basenames collide; cannot normalize ownership')
        return {'main': [self.declaration(x) for x in root['topElements']],
                'auxiliary': [self.declaration(x) for x in root['auxiliaryElements']],
                'referenceMap': refs, 'builtins': builtins,
                'fileNameMap': {key: PurePath(path).name for key, path in sorted(root['fileNameMap'].items())}}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: project.py JOB')
    with open(sys.argv[1], encoding='utf-8') as source:
        print(json.dumps(Projection(json.load(source)).project(), indent=2, sort_keys=True))
