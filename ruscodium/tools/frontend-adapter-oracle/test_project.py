#!/usr/bin/env python3
"""Adversarial checks that the comparison detects semantic changes."""
import copy
import json
from pathlib import Path
import unittest

from project import Projection

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

    def test_builtin_type_identity(self):
        field = self.nodes[self.root['referenceMap']['oracle.basic.Data.count']['$ref']]['properties']
        ref = self.nodes[field['typeRef']['$ref']]['properties']
        self.nodes[ref['element']['$ref']]['properties']['typeId']['name'] = 'UINT32'
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


if __name__ == '__main__':
    unittest.main()
