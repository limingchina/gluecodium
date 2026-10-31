import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('compare_validation', Path(__file__).parents[1] / 'compare_validation.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class ComparisonTest(unittest.TestCase):
    def test_known_divergence_is_directional_and_timeout_is_failure(self):
        accepted = {'accepted': True}
        rejected = {'accepted': False}
        known = (False, True, 'known stricter validation')
        with patch.object(module, 'invoke', side_effect=[rejected, accepted]):
            result = module.compare('case', [], [], None, known, '', '', {}, Path('/tmp'))
        self.assertFalse(result['unexpected'])
        self.assertEqual(result['expected_difference'], known[2])
        with patch.object(module, 'invoke', side_effect=[accepted, rejected]):
            result = module.compare('case', [], [], None, known, '', '', {}, Path('/tmp'))
        self.assertTrue(result['unexpected'])
        with patch.object(module, 'invoke', side_effect=[{'accepted': False, 'timeout': True}, rejected]):
            result = module.compare('case', [], [], False, None, '', '', {}, Path('/tmp'))
        self.assertTrue(result['unexpected'])

    def test_stack_overflow_is_reported_as_crash(self):
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / 'fake'
            executable.write_text('#!/bin/sh\necho java.lang.StackOverflowError >&2\nexit 1\n')
            executable.chmod(0o755)
            result = module.invoke(executable, [], [], {}, True, Path(directory))
        self.assertFalse(result['accepted'])
        self.assertTrue(result['crash'])
        self.assertEqual(result['returncode'], 1)


if __name__ == '__main__':
    unittest.main()
