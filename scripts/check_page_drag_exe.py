"""Check packaged page-transfer/Windows virtual-file payloads, not physical mouse dragging.

The application self-test exercises Qt MIME and receiver-owned PDF snapshots.
Passing does not establish real Explorer drag/drop behavior on a user's desktop.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ('passed', 'cross_window_owned_copy', 'page_order_and_duplicates',
            'source_preserved', 'native_virtual_file_payloads', 'cancel_no_output')


def check_executable(exe: Path) -> dict:
    exe = Path(exe).resolve()
    if not exe.is_file():
        raise RuntimeError('The checked Windows executable is unavailable: ' + str(exe))
    env = os.environ.copy()
    isolated_runner = env.get('GITHUB_ACTIONS') == 'true'
    # Never inherit the mouse-synthesis opt-in on an arbitrary user's desktop.
    env.pop('THEVIEWER_ISOLATED_DRAG_TEST', None)
    if isolated_runner:
        env['THEVIEWER_ISOLATED_DRAG_TEST'] = '1'
    try:
        result = subprocess.run([str(exe), '--page-drag-self-test'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180, env=env)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('Packaged page-drag self-test exceeded 180 seconds; stdout=' +
                           repr((exc.stdout or b'')[-4000:]) + '; stderr=' +
                           repr((exc.stderr or b'')[-4000:])) from exc
    stdout = result.stdout.decode('utf-8-sig', errors='replace')
    stderr = result.stderr.decode('utf-8-sig', errors='replace')
    diagnostics = f'exit={result.returncode}; stdout={stdout[-4000:]!r}; stderr={stderr[-4000:]!r}'
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    try:
        report = json.loads(lines[-1]) if lines else None
    except json.JSONDecodeError as exc:
        raise RuntimeError('Packaged page-drag self-test did not end with JSON: ' + diagnostics) from exc
    if not isinstance(report, dict):
        raise RuntimeError('Packaged page-drag self-test has no object report: ' + diagnostics)
    required = REQUIRED + (('native_qt_drop',) if isolated_runner else ())
    missing = [key for key in required if report.get(key) is not True]
    if result.returncode != 0 or missing:
        raise RuntimeError(f'Packaged page-drag self-test failed ({missing}): ' + diagnostics)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', help='Optional Windows executable or test wrapper')
    args = parser.parse_args()
    if args.exe:
        exe = Path(args.exe)
    else:
        build = json.loads((ROOT / 'build/windows-run/Build_Result.json').read_text(encoding='utf-8-sig'))
        if build.get('status') != 'passed':
            raise RuntimeError('The Windows build did not pass')
        exe = Path(build['exe'])
    report = check_executable(exe)
    print('Packaged page-transfer and native virtual-file payload checks passed. '
          'This is not a physical mouse/Explorer drag-and-drop test.')
    print(json.dumps(report, ensure_ascii=True))


if __name__ == '__main__':
    main()
