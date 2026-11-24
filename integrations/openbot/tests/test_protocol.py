import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('protocol', ROOT / 'protocol.py')
protocol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(protocol)


class ProtocolTest(unittest.TestCase):
    def test_only_coordinator_delegates(self):
        self.assertTrue(protocol.can_delegate('aiox-master', 'dev'))
        self.assertFalse(protocol.can_delegate('dev', 'qa'))
        self.assertFalse(protocol.can_delegate('aiox-master', 'unknown'))

    def test_result_must_match_current_attempt(self):
        task = {'task_id': 't1', 'attempt': 2, 'role': 'dev', 'status': 'running'}
        result = {'task_id': 't1', 'attempt': 2, 'role': 'dev', 'status': 'completed', 'evidence': ['tests passed']}
        self.assertEqual(protocol.accept_result(task, result), 'review')
        for key, value in [('task_id', 'other'), ('attempt', 1), ('role', 'qa')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                protocol.accept_result(task, dict(result, **{key: value}))

    def test_cancelled_and_duplicate_returns_do_not_advance(self):
        result = {'task_id': 't1', 'attempt': 1, 'role': 'dev', 'status': 'completed', 'evidence': ['disk']}
        for status in ['cancelled', 'completed', 'review']:
            task = {'task_id': 't1', 'attempt': 1, 'role': 'dev', 'status': status}
            with self.subTest(status=status), self.assertRaises(ValueError):
                protocol.accept_result(task, result)

    def test_completion_requires_evidence_and_qa(self):
        with self.assertRaises(ValueError):
            protocol.accept_result({'task_id': 't', 'attempt': 1, 'role': 'dev', 'status': 'running'},
                                   {'task_id': 't', 'attempt': 1, 'role': 'dev', 'status': 'completed', 'evidence': []})
        self.assertFalse(protocol.can_close('review', 'FAIL', True))
        self.assertFalse(protocol.can_close('review', 'PASS', False))
        self.assertFalse(protocol.can_close('running', 'PASS', True))
        self.assertTrue(protocol.can_close('review', 'PASS', True))

    def test_manifest_is_portable_and_sources_exist(self):
        import json
        manifest = json.loads((ROOT / 'manifest.json').read_text())
        self.assertEqual(len(manifest['roles']), 12)
        self.assertEqual(len(set(r['id'] for r in manifest['roles'])), 12)
        for role in manifest['roles']:
            self.assertTrue((ROOT / role['instructions']).is_file())
            self.assertTrue((ROOT.parents[1] / role['source']).is_file())
            if role['id'] != 'aiox-master':
                self.assertEqual(role['reports_to'], 'aiox-master')
        self.assertNotIn('agent-', json.dumps(manifest))


if __name__ == '__main__':
    unittest.main()
