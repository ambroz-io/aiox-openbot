"""Contract regression tests; does not assert live OpenBot enforcement.

Uses the already available jsonschema validator; installs no dependencies.
"""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class DelegationContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / 'schemas/delegation.json').read_text())
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema)

    def setUp(self):
        self.task = dict(task_id='fix-contract', attempt=1, role='dev',
                         project='example-project', scope='Repair delegation contract',
                         inputs=['Confirmed review findings'],
                         allowed_files=['integrations/openbot/schemas/delegation.json'],
                         acceptance=['Contract regression tests pass'],
                         authorization='User authorized integration changes')

    def test_valid_contract_for_every_specialist(self):
        manifest = json.loads((ROOT / 'manifest.json').read_text())
        for role in manifest['roles']:
            if role['id'] != 'aiox-master':
                with self.subTest(role=role['id']):
                    self.validator.validate(dict(self.task, role=role['id']))

    def test_all_contract_fields_are_required(self):
        for field in self.task:
            task = copy.deepcopy(self.task)
            del task[field]
            with self.subTest(field=field):
                self.assertFalse(self.validator.is_valid(task))

    def test_text_fields_require_non_whitespace_content(self):
        for field in ['task_id', 'project', 'scope', 'authorization']:
            for value in ['', ' ', '\t\n', None, 42]:
                with self.subTest(field=field, value=value):
                    self.assertFalse(self.validator.is_valid(dict(self.task, **{field: value})))

    def test_lists_require_nonempty_text_items(self):
        for field in ['inputs', 'allowed_files', 'acceptance']:
            for value in [[], '', None, [''], [' \t\n'], [42], ['valid', ' ']]:
                with self.subTest(field=field, value=value):
                    self.assertFalse(self.validator.is_valid(dict(self.task, **{field: value})))

    def test_attempt_and_recipient_constraints(self):
        for value in [0, -1, 1.5, '1', True]:
            with self.subTest(attempt=value):
                self.assertFalse(self.validator.is_valid(dict(self.task, attempt=value)))
        for role in ['aiox-master', 'unknown', '']:
            with self.subTest(role=role):
                self.assertFalse(self.validator.is_valid(dict(self.task, role=role)))

    def test_coordinator_bundle_matches_and_has_no_self_reporting(self):
        source = (ROOT / 'agents/aiox-master.md').read_text()
        bundled = (ROOT / 'skills/aiox-openbot-team/references/roles/aiox-master.md').read_text()
        self.assertEqual(source, bundled)
        self.assertIn('Reporta a: usuário.', source)
        self.assertIn('Antes de delegar, registre tarefa', source)
        self.assertIn('reporte ao usuário', source)
        self.assertIn('peça esclarecimentos ao usuário', source)
        self.assertNotIn('Não delegue a outro especialista', source)
        self.assertNotIn('retorne bloqueio a Orion', source)

    def test_specialists_still_cannot_delegate(self):
        for path in (ROOT / 'agents').glob('*.md'):
            if path.stem != 'aiox-master':
                with self.subTest(role=path.stem):
                    self.assertIn('Não delegue a outro especialista', path.read_text())
