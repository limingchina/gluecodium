import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('surface', Path(__file__).parents[1] / 'template_surface.py')
surface = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(surface)


class SurfaceTest(unittest.TestCase):
    def test_references_comments_helpers_and_partials(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'x.mustache').write_text('''{{!! comment {{ignored}}
!}}
{{name}} {{#items}}{{value}}{{/items}}
{{#set local=thing flag=true}}{{local.x}}{{/set}}
{{#if obj.field logic="or"}}{{resolveName "mode" other}}{{/if}}
{{>cpp/Foo}} {{prefixPartial "cpp/Bar" "  "}} {{joinPartial things part ", "}}
{{#eval "mapping.key" this}}{{@index}}{{/eval}}
''')
            result = surface.scan(root)
        paths = result['property_candidates']
        self.assertEqual([(x['path'], x['line']) for x in paths], [
            ('name', 3), ('items', 3), ('value', 3), ('thing', 4), ('local.x', 4),
            ('obj.field', 5), ('other', 5), ('things', 6), ('part', 6), ('this', 7), ('@index', 7)])
        self.assertEqual(next(x for x in paths if x['path'] == 'local.x')['classification'], 'possible_local')
        self.assertEqual(next(x for x in paths if x['path'] == 'this')['classification'], 'context')
        self.assertEqual([(x['name'], x['category']) for x in result['helpers']], [
            ('set', 'builtin'), ('if', 'builtin'), ('resolveName', 'registered'),
            ('prefixPartial', 'registered'), ('joinPartial', 'registered'), ('eval', 'builtin')])
        self.assertEqual([x['dynamic'] for x in result['partials']], [False, False, True])
        self.assertEqual(result['selectors'][-1]['arguments'], ['"mapping.key"', 'this'])
        self.assertEqual(result['template_count'], 1)

    def test_deterministic_hash_and_target_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'cpp').mkdir()
            (root / 'cpp' / 'b.mustache').write_text('{{name}}')
            first = surface.scan(root)
            self.assertEqual(first, surface.scan(root))
            self.assertEqual(first['targets'], {'cpp': 1})
            (root / 'cpp' / 'b.mustache').write_text('{{other}}')
            self.assertNotEqual(first['corpus_sha256'], surface.scan(root)['corpus_sha256'])


if __name__ == '__main__':
    unittest.main()
