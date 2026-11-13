"""Focused regression checks; no live T3 mutations."""
import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    'picker', Path(__file__).resolve().parents[2] / 'scripts/t3-picker.py')
picker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(picker)


class PickerTests(unittest.TestCase):
    def test_duplicate_titles_keep_distinct_targets(self):
        with patch.object(picker.subprocess, 'run', return_value=
                          subprocess.CompletedProcess([], 0, '2. Same title\n')):
            self.assertEqual(picker.pick('Threads', [('Same title', 'a'),
                                                    ('Same title', 'b')]), 'b')

    def test_cancel_does_not_send(self):
        with patch.object(picker.subprocess, 'run', return_value=
                          subprocess.CompletedProcess([], 130, '')) as run:
            picker.compose(Path('/unused'), 'a', 'send')
            self.assertEqual(run.call_count, 1)

    def test_declined_confirmation_does_not_send(self):
        with patch.object(picker.subprocess, 'run', side_effect=[
            subprocess.CompletedProcess([], 0, 'draft'),
            subprocess.CompletedProcess([], 1),
        ]) as run:
            picker.compose(Path('/unused'), 'a', 'send')
            self.assertEqual(run.call_count, 2)

    def test_literal_multiline_message_uses_stdin(self):
        message = 'literal $(text)\nsecond line'
        with patch.object(picker.subprocess, 'run', side_effect=[
            subprocess.CompletedProcess([], 0, message),
            subprocess.CompletedProcess([], 0),
            subprocess.CompletedProcess([], 0),
        ]) as run:
            picker.compose(Path('/path with spaces'), 'b', 'send')
            self.assertEqual(run.call_args.args[0], ['t3', 'thread', 'send',
                '--base-dir', '/path with spaces', 'b', '-'])
            self.assertEqual(run.call_args.kwargs['input'], message)


if __name__ == '__main__':
    unittest.main()
