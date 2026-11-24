"""Distribution boundary regressions using only the standard library."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location('exporter', ROOT / 'integrations/openbot/261124-110000-exportar-pacote-openbot.py')
exporter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(exporter)


class DistributionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='openbot-export-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def test_exact_allowlist_and_hashes_exclude_unlisted_private_files(self):
        source = self.base / 'source'
        for name in exporter.ALLOWLIST:
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, path)
        for name in ('.claude/settings.json', 'private-note.txt',
                     'integrations/openbot/exercise/report.txt'):
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('synthetic unlisted sentinel')
        output = self.base / 'bundle'
        exporter.export(source, output)
        actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
        self.assertEqual(actual, set(exporter.ALLOWLIST) | {exporter.HASH_NAME})
        hashes = json.loads((output / exporter.HASH_NAME).read_text())['sha256']
        for name, digest in hashes.items():
            self.assertEqual(hashlib.sha256((output / name).read_bytes()).hexdigest(), digest)
        self.assertFalse(any(p.is_symlink() for p in output.rglob('*')))

    def test_existing_destination_is_preserved(self):
        output = self.base / 'existing'
        output.mkdir()
        sentinel = output / 'keep.txt'
        sentinel.write_text('preserve')
        with self.assertRaises(ValueError):
            exporter.export(ROOT, output)
        self.assertEqual(sentinel.read_text(), 'preserve')

    def test_missing_input_leaves_no_destination(self):
        source = self.base / 'empty-source'
        source.mkdir()
        output = self.base / 'missing-bundle'
        with self.assertRaises(ValueError):
            exporter.export(source, output)
        self.assertFalse(output.exists())

    def test_symlinked_input_refused_before_writes(self):
        source = self.base / 'source'
        source.mkdir()
        (source / '.aiox-core').symlink_to(ROOT / '.aiox-core', target_is_directory=True)
        output = self.base / 'symlink-bundle'
        with self.assertRaises(ValueError):
            exporter.export(source, output)
        self.assertFalse(output.exists())

    def test_destination_inside_source_refused(self):
        with self.assertRaises(ValueError):
            exporter.export(ROOT, ROOT / 'never-created-export')


if __name__ == '__main__':
    unittest.main(verbosity=2)
