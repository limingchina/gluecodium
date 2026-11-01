#!/usr/bin/env python3
"""Adversarial checks that the comparison detects semantic changes."""
import copy
import json
from pathlib import Path
import unittest

from project import Projection, normalize_sections

JOB = Path(__file__).resolve().parents[2] / 'tests/cpp-generation-goldens/default/job.json'


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.job = json.loads(JOB.read_text(encoding='utf-8'))
        self.expected = copy.deepcopy(Projection(self.job).project())
        self.nodes = {n['id']: n for n in self.job['snapshot']['nodes']}
        self.root = self.nodes[self.job['snapshot']['root']['$ref']]['properties']

    def test_identity_is_not_allocation_order(self):
        altered = copy.deepcopy(self.job)
        altered['snapshot']['nodes'].reverse()
        self.assertEqual(self.expected, Projection(altered).project())

    def test_root_order(self):
        self.root['topElements'].reverse()
        self.assertNotEqual(self.expected, Projection(self.job).project())

    def test_reference_map_membership(self):
        del self.root['referenceMap']['oracle.basic.Data.count']
        self.assertNotEqual(self.expected, Projection(self.job).project())

    def test_file_ownership(self):
        self.root['fileNameMap']['oracle.basic.Data'] = '/elsewhere/other.lime'
        self.assertNotEqual(self.expected, Projection(self.job).project())

    def test_ambiguous_source_basenames_fail_closed(self):
        self.root['fileNameMap']['oracle.basic.Data'] = '/elsewhere/default.lime'
        with self.assertRaisesRegex(ValueError, 'basenames collide'):
            Projection(self.job).project()

    def test_builtin_type_identity(self):
        field = self.nodes[self.root['referenceMap']['oracle.basic.Data.count']['$ref']]['properties']
        ref = self.nodes[field['typeRef']['$ref']]['properties']
        self.nodes[ref['element']['$ref']]['properties']['typeId']['name'] = 'UINT32'
        self.assertNotEqual(self.expected, Projection(self.job).project())

    def test_distinct_same_path_type_target_is_rejected(self):
        original = self.nodes[self.root['referenceMap']['oracle.basic.Shade']['$ref']]
        clone = copy.deepcopy(original)
        clone['id'] = 'forged-clone'
        self.job['snapshot']['nodes'].append(clone)
        callback = self.nodes[self.root['referenceMap']['oracle.basic.Callback']['$ref']]['properties']
        parameter = self.nodes[callback['parameters'][0]['$ref']]['properties']
        typeref = self.nodes[parameter['typeRef']['$ref']]['properties']
        typeref['element'] = {'$ref': clone['id']}
        typeref['type'] = {'$ref': clone['id']}
        with self.assertRaisesRegex(ValueError, 'noncanonical declaration target'):
            Projection(self.job).project()

    def test_constructor_link_attributes(self):
        constructor = self.nodes[self.root['referenceMap']['oracle.basic.Data.:0']['$ref']]['properties']
        ref = self.nodes[constructor['fieldRefs'][0]['$ref']]['properties']
        self.nodes[ref['attributes']['$ref']]['properties']['attributes'] = {'CPP': {'NAME': 'changed'}}
        self.assertNotEqual(self.expected, Projection(self.job).project())

    def test_direct_nullable_edge(self):
        field = self.nodes[self.root['referenceMap']['oracle.basic.Data.maybe']['$ref']]['properties']
        self.nodes[field['typeRef']['$ref']]['properties']['isNullable'] = False
        self.assertNotEqual(self.expected, Projection(self.job).project())

    def test_constructor_field_link(self):
        constructor = self.nodes[self.root['referenceMap']['oracle.basic.Data.:0']['$ref']]['properties']
        constructor['fieldRefs'] = []
        self.assertNotEqual(self.expected, Projection(self.job).project())

    def test_unknown_relevant_property_fails_closed(self):
        self.nodes[self.root['topElements'][0]['$ref']]['properties']['surprise'] = True
        with self.assertRaisesRegex(ValueError, 'unhandled node/fields'):
            Projection(self.job)

    def test_adjacent_comment_fragments_preserve_text_and_tags(self):
        ident = self.nodes[self.root['topElements'][0]['$ref']]['properties']['comment']['$ref']
        self.job['raw_comments'] = {ident: [['', 'hello'], ['', ' world'], ['Cpp', 'cpp']]}
        expected = Projection(self.job).project()
        self.job['raw_comments'][ident] = [['', 'hello world'], ['Cpp', 'cpp']]
        self.assertEqual(expected, Projection(self.job).project())
        self.job['raw_comments'][ident] = [['Cpp', 'hello world'], ['', 'cpp']]
        self.assertNotEqual(expected, Projection(self.job).project())

    def test_adjacent_placeholders_never_coalesce(self):
        sections = [['Placeholder', 'first'], ['Placeholder', 'second']]
        self.assertEqual(sections, normalize_sections(sections))

    def test_empty_tag_transition_is_retained(self):
        sections = [['', 'one'], ['Cpp', ''], ['', 'two']]
        self.assertEqual(sections, normalize_sections(sections))


if __name__ == '__main__':
    unittest.main()
