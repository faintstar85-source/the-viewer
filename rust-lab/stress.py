#!/usr/bin/env python3
"""Supervise real Qt UI stress cases for the unchanged and Rust-hybrid readers.

One application window holds 10 or 20 PDFs, not 10/20 separate applications.
Only generated fixtures are used. Each implementation receives identical files.
"""
from __future__ import annotations

import argparse
from collections import deque
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import threading
import time

import psutil

LAB = Path(__file__).resolve().parent
REPO = LAB.parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.partial')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
    temporary.replace(path)


def fixtures(folder):
    import numpy as np
    from PIL import Image, ImageDraw
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    folder.mkdir(parents=True, exist_ok=True)
    records = []
    for number in range(20):
        path = folder / f'{number + 1:02d}_한글_검사_{"scan" if number % 2 else "text"}.pdf'
        c = canvas.Canvas(str(path), pagesize=(612, 792), invariant=1, pageCompression=1)
        scan = None
        if number % 2:
            rng = np.random.default_rng(1900 + number)
            pixels = rng.integers(215, 256, (2000, 1500), dtype=np.uint8)
            scan = Image.fromarray(pixels).convert('RGB')
            draw = ImageDraw.Draw(scan)
            for row in range(35):
                y = 70 + row * 52
                draw.text((55, y), f'SCANNED REPORT {number + 1:02d} / ROW {row:02d} / 0123456789', fill=(20, 35, 55), font_size=27)
                draw.line((50, y + 39, 1450, y + 39), fill=(60, 75, 100), width=2)
            scan = ImageReader(scan)
        for page in range(10):
            if scan is not None:
                c.drawImage(scan, 0, 0, width=612, height=792)
            else:
                c.setFont('Helvetica-Bold', 22)
                c.drawString(40, 745, f'TEXT / TABLE DOCUMENT {number + 1:02d}')
                c.setFont('Helvetica', 10)
                for row in range(35):
                    y = 705 - row * 18
                    c.drawString(45, y, f'Record {number + 1:02d}-{page + 1:02d}-{row + 1:02d} / sample data / {row * 137}.25')
                    c.line(40, y - 5, 572, y - 5)
                for x in (40, 230, 400, 572):
                    c.line(x, 70, x, 725)
            c.setFillColorRGB(1, 1, 1)
            c.rect(350, 5, 255, 24, fill=1, stroke=0)
            c.setFillColorRGB(0, 0, 0)
            c.setFont('Helvetica', 12)
            c.drawString(355, 12, f'DOCUMENT {number + 1:02d} / PAGE {page + 1:02d}')
            c.showPage()
        c.save()
        records.append({'path': str(path.resolve()), 'sha256': digest(path), 'bytes': path.stat().st_size,
                        'pages': 10, 'kind': 'scan' if number % 2 else 'text_table'})
    return records


def host_process(proc):
    # Containers may expose host /proc while Popen returns a namespace PID.
    if sys.platform == 'linux':
        lines = Path('/proc/self/status').read_text().splitlines()
        parent = int(next(line.split()[1] for line in lines if line.startswith('Pid:')))
        if parent != os.getpid():
            for child in psutil.Process(parent).children():
                try:
                    ids = next(line.split()[1:] for line in Path(f'/proc/{child.pid}/status').read_text().splitlines()
                               if line.startswith('NSpid:'))
                    if int(ids[-1]) == proc.pid and child.ppid() == parent:
                        return child
                except (OSError, StopIteration, psutil.NoSuchProcess):
                    continue
            raise RuntimeError('Cannot identify GUI PID in the host namespace')
    return psutil.Process(proc.pid)


def median(values):
    return statistics.median(values) if values else None


def run_case(implementation, count, rust, manifest, output, cycles, seconds):
    name = f'{implementation}_{count}'
    case_path = output / name
    case_path.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, str(LAB / 'stress_ui_case.py'), '--implementation', implementation,
               '--rust', str(rust), '--manifest', str(manifest), '--out', str(case_path / 'ui.json'),
               '--cycles', str(cycles), '--min-seconds', str(seconds)]
    env = dict(os.environ, QT_QPA_PLATFORM='offscreen', PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    start = time.monotonic()
    proc = subprocess.Popen(command, cwd=REPO, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding='utf8', errors='replace', bufsize=1)
    root = host_process(proc)
    records, events, warnings = [], [], []
    tracked = {}
    stdout, stderr = deque(maxlen=4000), deque(maxlen=4000)
    stop = threading.Event()

    def read_stdout():
        for line in proc.stdout:
            stdout.append(line)
            try:
                record = json.loads(line)
            except (ValueError, TypeError):
                continue
            if isinstance(record, dict) and 'event' in record:
                record['supervisor_elapsed_s'] = time.monotonic() - start
                events.append(record)
                if record['event'] in ('cycle_complete', 'complete', 'failed'):
                    print(json.dumps({'case': name, **record}, ensure_ascii=False), flush=True)

    def read_stderr():
        for line in proc.stderr:
            stderr.append(line)

    def sample():
        while not stop.is_set():
            try:
                members = [root, *root.children(recursive=True)]
                rss, private, handles = 0, 0, 0
                has_private, has_handles = True, True
                live = 0
                for member in members:
                    try:
                        stamp = member.create_time()
                        tracked[(member.pid, stamp)] = member
                        info = member.memory_info()
                        rss += info.rss
                        if hasattr(info, 'private'):
                            private += info.private
                        else:
                            has_private = False
                        if hasattr(member, 'num_handles'):
                            handles += member.num_handles()
                        else:
                            has_handles = False
                        live += 1
                    except psutil.NoSuchProcess:
                        continue
                records.append({'elapsed_s': time.monotonic() - start, 'rss_bytes': rss,
                                'private_bytes': private if has_private else None,
                                'handles': handles if has_handles else None, 'processes': live})
            except psutil.NoSuchProcess:
                break
            except (psutil.AccessDenied, OSError) as exc:
                warnings.append(str(exc))
            stop.wait(.1)

    readers = [threading.Thread(target=read_stdout, daemon=True), threading.Thread(target=read_stderr, daemon=True),
               threading.Thread(target=sample, daemon=True)]
    for reader in readers:
        reader.start()
    timed_out = False
    try:
        proc.wait(timeout=max(180, seconds * 3 + 60))
    except subprocess.TimeoutExpired:
        timed_out = True
        # A timed-out test is a failure. Cleanup cannot turn it into a pass.
        for child in reversed(root.children(recursive=True)):
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        proc.kill()
        proc.wait(timeout=15)
    stop.set()
    for reader in readers:
        reader.join(timeout=5)
    # Permit normal child exits, then record stragglers BEFORE cleanup.
    tracked_children = [p for (pid, _), p in tracked.items() if pid != root.pid]
    _, alive = psutil.wait_procs(tracked_children, timeout=3)
    remaining = []
    for child in alive:
        try:
            if child.is_running() and child.status() != psutil.STATUS_ZOMBIE:
                remaining.append({'pid': child.pid, 'created': child.create_time(), 'name': child.name()})
                child.kill()
        except psutil.NoSuchProcess:
            pass
    psutil.wait_procs(alive, timeout=3)
    for stream in (proc.stdout, proc.stderr):
        stream.close()
    (case_path / 'stdout.txt').write_text(''.join(stdout), encoding='utf8')
    (case_path / 'stderr.txt').write_text(''.join(stderr), encoding='utf8')
    ui_path = case_path / 'ui.json'
    ui = json.loads(ui_path.read_text('utf8')) if ui_path.exists() else {'passed': False, 'errors': ['No child result file']}
    phases = []
    for event in events:
        t = event['supervisor_elapsed_s']
        nearby = [r for r in records if t - 1.0 <= r['elapsed_s'] <= t]
        phases.append({**event, 'memory': {key: median([r[key] for r in nearby if r[key] is not None])
                        for key in ('rss_bytes', 'private_bytes', 'handles', 'processes')}, 'samples': len(nearby)})
    peak = {key: max((r[key] for r in records if r[key] is not None), default=None)
            for key in ('rss_bytes', 'private_bytes', 'handles', 'processes')}
    result = {'implementation': implementation, 'file_count': count, 'exit_code': proc.returncode,
              'timed_out': timed_out, 'elapsed_s': time.monotonic() - start, 'ui': ui,
              'memory_peak': peak, 'memory_samples': records, 'phase_memory': phases,
              'measurement_warnings': list(dict.fromkeys(warnings)), 'remaining_processes_before_cleanup': remaining,
              'passed': proc.returncode == 0 and ui.get('passed') is True and not timed_out and not remaining}
    save(case_path / 'result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rust', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--cycles', type=int, default=10)
    parser.add_argument('--min-seconds', type=float, default=120)
    parser.add_argument('--counts', type=int, nargs='+', default=[10, 20])
    args = parser.parse_args()
    if args.cycles < 1 or args.min_seconds < 0 or any(c not in (10, 20) for c in args.counts):
        parser.error('Use positive cycles, non-negative duration, and counts 10 or 20')
    output, rust = args.out.resolve(), args.rust.resolve()
    if not rust.is_file():
        parser.error('Compiled Rust worker is missing')
    output.mkdir(parents=True, exist_ok=True)
    inputs = fixtures(output / 'fixtures')
    manifests = {}
    for count in args.counts:
        path = output / f'manifest_{count}.json'
        save(path, {'count': count, 'pages_per_file': 10, 'files': [r['path'] for r in inputs[:count]],
                    'fixture_hashes': {r['path']: r['sha256'] for r in inputs[:count]}})
        manifests[count] = path
    result = {'schema': 1, 'scope': 'One Qt window holding 10/20 PDFs; no separate application instances',
              'platform': platform.platform(), 'python': sys.version, 'cpu_count': os.cpu_count(),
              'versions': {name: importlib.metadata.version(name) for name in
                           ('PySide6', 'pypdfium2', 'pypdf', 'Pillow', 'numpy', 'reportlab', 'psutil')},
              'baseline_sha256': digest(REPO / 'pdf_page_dragger.py'), 'rust_sha256': digest(rust),
              'test_script_sha256': digest(__file__), 'ui_script_sha256': digest(LAB / 'stress_ui_case.py'),
              'cycles_per_case': args.cycles, 'minimum_seconds_per_case': args.min_seconds, 'inputs': inputs,
              'method': {'qt_platform': 'offscreen', 'sampling_ms': 100,
                         'rss': 'Sum of GUI and descendant resident memory; shared pages may be counted twice',
                         'private': 'Windows sum of private committed bytes, when psutil provides this field',
                         'phase_memory': 'Median of samples in the second preceding each child phase event',
                         'limitations': ['Synthetic PDFs only', 'No forced native crash or low-memory injection',
                                         'No proof of leak absence or general crash-rate superiority',
                                         'No user desktop/printing/Office/HWP testing']}, 'cases': []}
    save(output / 'stress-results.json', result)
    for index, count in enumerate(args.counts):
        order = ('python', 'rust') if index % 2 == 0 else ('rust', 'python')
        for implementation in order:
            print(f'START {implementation}: {count} PDF files, {args.cycles} cycles, minimum {args.min_seconds}s', flush=True)
            result['cases'].append(run_case(implementation, count, rust, manifests[count], output,
                                            args.cycles, args.min_seconds))
            save(output / 'stress-results.json', result)
    result['inputs_unchanged'] = all(digest(row['path']) == row['sha256'] for row in inputs)
    result['implementation_unchanged'] = (
        digest(REPO / 'pdf_page_dragger.py') == result['baseline_sha256']
        and digest(rust) == result['rust_sha256']
        and digest(__file__) == result['test_script_sha256']
        and digest(LAB / 'stress_ui_case.py') == result['ui_script_sha256'])
    result['frame_parity'] = []
    for count in args.counts:
        pair = {case['implementation']: case['ui'].get('frames', []) for case in result['cases']
                if case['file_count'] == count}
        expected = args.cycles * (count * 3 + 2)
        result['frame_parity'].append({'file_count': count, 'expected_frames_per_implementation': expected,
            'actual_frames': {key: len(value) for key, value in pair.items()},
            'passed': len(pair.get('python', [])) == expected and pair.get('python') == pair.get('rust')})
    result['passed'] = (all(case['passed'] for case in result['cases']) and result['inputs_unchanged']
                        and result['implementation_unchanged'] and all(row['passed'] for row in result['frame_parity']))
    save(output / 'stress-results.json', result)
    print(json.dumps({'passed': result['passed'], 'cases': len(result['cases']),
                      'inputs_unchanged': result['inputs_unchanged'], 'report': str(output / 'stress-results.json')}), flush=True)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
