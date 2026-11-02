#!/usr/bin/env python3
"""Checks for the M14 schedule, output gate and incomplete-result policy."""
import tempfile
import unittest
from pathlib import Path

import benchmark as b
import optimization as o


class OptimizationChecks(unittest.TestCase):
    def test_fixed_complete_balanced_schedule(self):
        schedule = o.schedule()
        self.assertEqual(schedule, o.schedule())
        for name in o.NAMES:
            for side in o.SIDES:
                items = [x for x in schedule if x['workload'] == name and x['side'] == side]
                self.assertEqual(len(items), o.COUNTS[name][side])
                if side != 'baseline':
                    self.assertEqual(sum(x['position'] == 1 for x in items), 4)
            for n in range(1, 9):
                pair = [i for i, x in enumerate(schedule) if x['workload'] == name and x['side'] != 'baseline' and x['trial'] == n]
                self.assertEqual(pair[1] - pair[0], 1)
        pilot = [x for x in schedule if x['kind'] == 'censored-pilot']
        self.assertEqual([(x['workload'], x['side']) for x in pilot], [('structs-500', 'baseline')])

    def test_complete_manifest_gate_rejects_changes_and_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'common').mkdir()
            (root / 'common' / 'file.h').write_bytes(b'expected')
            reference = b.manifest(root)
            ok = {'exit_code': 0, 'timeout': False, 'logging_error': False}
            self.assertTrue(o.check_result(ok, b.manifest(root), reference))
            (root / 'common' / 'file.h').write_bytes(b'different')
            self.assertFalse(o.check_result(ok, b.manifest(root), reference))
            (root / 'common' / 'file.h').unlink()
            self.assertFalse(o.check_result(ok, b.manifest(root), reference))
            self.assertFalse(o.check_result({**ok, 'logging_error': True}, reference, reference))
            self.assertFalse(o.check_result({**ok, 'timeout': True}, reference, reference))
            self.assertFalse(o.check_result({**ok, 'exit_code': 1}, reference, reference))
            self.assertFalse(o.check_result(ok, reference, None))

    def test_incomplete_samples_have_no_statistics_or_ratios(self):
        samples = []
        for side in ('jvm', 'optimized'):
            for _ in range(8):
                samples.append({'workload': 'structs-500', 'side': side, 'matches_reference': True, 'wall_seconds': 1, 'cpu_seconds': 1, 'peak_rss_kib': 1})
        samples.append({'workload': 'structs-500', 'side': 'baseline', 'matches_reference': True, 'wall_seconds': 2, 'cpu_seconds': 2, 'peak_rss_kib': 2})
        data = o.summarize({'samples': samples})
        self.assertNotIn('baseline_over_optimized', data['structs-500'])
        self.assertIn('jvm_over_optimized', data['structs-500'])
        samples[0]['matches_reference'] = False
        data = o.summarize({'samples': samples})
        self.assertNotIn('wall_seconds', data['structs-500']['jvm'])
        self.assertNotIn('jvm_over_optimized', data['structs-500'])


if __name__ == '__main__':
    unittest.main()
