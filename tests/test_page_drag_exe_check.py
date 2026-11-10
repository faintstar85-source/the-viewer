"""Fail-closed validation of the packaged page-transfer self-test report."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import check_page_drag_exe as checker


class TestPackagedPageDragReport(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(checker.os.environ, {'GITHUB_ACTIONS': 'false'})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.exe = Path(self.temp.name) / 'viewer.exe'
        self.exe.touch()
        self.report = dict.fromkeys(checker.REQUIRED, True)

    def run_report(self, report, code=0, prefix=b''):
        result = subprocess.CompletedProcess([], code, prefix + json.dumps(report).encode() + b'\n', b'diagnostic')
        with patch.object(checker.subprocess, 'run', return_value=result) as run:
            actual = checker.check_executable(self.exe)
            self.assertEqual(run.call_args.kwargs['timeout'], 180)
            self.assertEqual(run.call_args.args[0], [str(self.exe.resolve()), '--page-drag-self-test'])
            return actual

    def test_accepts_last_json_after_startup_output(self):
        self.assertEqual(self.run_report(self.report, prefix=b'Qt startup\n'), self.report)

    def test_every_required_check_must_be_true(self):
        for key in checker.REQUIRED:
            for value in (False, None, 1, 'true'):
                with self.subTest(key=key, value=value), self.assertRaises(RuntimeError):
                    self.run_report({**self.report, key: value})

    def test_nonzero_exit_is_failure_even_with_passed_report(self):
        with self.assertRaises(RuntimeError):
            self.run_report(self.report, code=1)

    def test_missing_executable(self):
        with self.assertRaises(RuntimeError):
            checker.check_executable(self.exe.parent / 'missing.exe')

    def test_non_object_report(self):
        with self.assertRaises(RuntimeError):
            self.run_report([])

    def test_malformed_and_empty_output(self):
        for stdout in (b'', b'not json', b'{"passed":true}\ntrailing junk'):
            with self.subTest(stdout=stdout):
                result = subprocess.CompletedProcess([], 0, stdout, b'')
                with patch.object(checker.subprocess, 'run', return_value=result), self.assertRaises(RuntimeError):
                    checker.check_executable(self.exe)

    def test_timeout_reports_partial_output(self):
        error = subprocess.TimeoutExpired('viewer.exe', 180, output=b'partial', stderr=b'hung')
        with patch.object(checker.subprocess, 'run', side_effect=error):
            with self.assertRaisesRegex(RuntimeError, 'partial.*hung'):
                checker.check_executable(self.exe)

    def test_ci_requires_native_qt_drop_and_sets_isolated_opt_in(self):
        with patch.dict(checker.os.environ, {'GITHUB_ACTIONS': 'true'}):
            with self.assertRaisesRegex(RuntimeError, 'native_qt_drop'):
                self.run_report(self.report)
            report = {**self.report, 'native_qt_drop': True}
            result = subprocess.CompletedProcess([], 0, json.dumps(report).encode(), b'')
            with patch.object(checker.subprocess, 'run', return_value=result) as run:
                checker.check_executable(self.exe)
                self.assertEqual(run.call_args.kwargs['env']['THEVIEWER_ISOLATED_DRAG_TEST'], '1')

    def test_local_run_strips_inherited_mouse_opt_in(self):
        with patch.dict(checker.os.environ, {'THEVIEWER_ISOLATED_DRAG_TEST': '1'}):
            result = subprocess.CompletedProcess([], 0, json.dumps(self.report).encode(), b'')
            with patch.object(checker.subprocess, 'run', return_value=result) as run:
                checker.check_executable(self.exe)
                self.assertNotIn('THEVIEWER_ISOLATED_DRAG_TEST', run.call_args.kwargs['env'])


if __name__ == '__main__':
    unittest.main()
