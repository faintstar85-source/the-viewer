#!/usr/bin/env python3
"""Stress one real Qt window with 10/20 synthetic PDFs, without changing the app.

Run in a fresh process for each implementation/count. The supervisor samples this
process and its children; this file only drives the UI and records checkpoints.
No screenshots or user documents are uploaded by this test.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import time
import traceback
import weakref

LAB = Path(__file__).resolve().parent
REPO = LAB.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(LAB))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(part)
    return value.hexdigest()


def run(args):
    import bridge
    import launch
    import pdf_page_dragger as viewer
    import PySide6
    from PySide6.QtCore import QProcess, QTimer
    from PySide6.QtGui import QImage
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication, QMessageBox

    manifest = json.loads(args.manifest.read_text(encoding="utf8"))
    files = [str(Path(name).resolve()) for name in manifest["files"]]
    count, pages_per_file = int(manifest["count"]), int(manifest["pages_per_file"])
    if count not in (10, 20) or len(files) != count or len(set(files)) != count:
        raise ValueError("Manifest must contain exactly 10 or 20 distinct PDF paths")
    if pages_per_file < 2:
        raise ValueError("Need at least two pages per PDF for navigation")
    expected_pages = count * pages_per_file
    before = {path: digest(path) for path in files}
    for path, expected in manifest.get("fixture_hashes", {}).items():
        resolved = str(Path(path).resolve())
        if resolved in before and before[resolved] != expected:
            raise AssertionError(f"Fixture hash mismatch: {resolved}")
    bridge.verify_baseline(viewer)
    if args.implementation == "rust":
        bridge.install(viewer, args.rust)
    # Same experiment-only settings and startup behavior for both implementations.
    viewer.Window.check_startup_update = lambda self: None
    viewer.Window.check_for_updates = lambda self, *a, **k: None
    viewer.tv_update_mutex_open = lambda: None
    viewer.tv_update_mutex_close = lambda mutex: None

    app = QApplication.instance() or QApplication([])
    app.setStyle("Fusion")
    started = time.monotonic()
    result = {
        "schema": 1, "implementation": args.implementation,
        "platform": platform.platform(), "qt_platform": os.environ.get("QT_QPA_PLATFORM"),
        "pyside_version": PySide6.__version__, "baseline_commit": bridge.BASELINE_COMMIT,
        "baseline_source_sha256": digest(REPO / "pdf_page_dragger.py"),
        "stress_script_sha256": digest(__file__),
        "rust_binary_sha256": digest(args.rust) if args.implementation == "rust" else None,
        "file_count": count, "pages_per_file": pages_per_file,
        "expected_loaded_pages": expected_pages, "requested_cycles": args.cycles,
        "minimum_case_seconds": args.min_seconds, "completed_cycles": 0,
        "preview_count": 0, "dual_view_cycles": 0, "checkpoints": [],
        "frames": [], "worker_errors": [], "worker_crashes": [],
        "import_errors": [], "modal_messages": [], "python_exceptions": [],
        "errors": [], "timeout_count": 0, "passed": False, "input_sha256_before": before,
        "method": "One real Qt Window; fixed cycles; all PDFs remain loaded while first/middle/last pages of every PDF are rendered; dual view; clear and wait for release before reopen",
        "not_tested": ["native Windows desktop input", "out-of-memory injection", "forced native crash", "printing", "Office/HWP conversion", "user-supplied files", "full-day soak"],
    }
    window = None
    shutdown = False
    hooked = weakref.WeakSet()
    release_count = 0
    heartbeat_intervals = []
    last_beat = time.monotonic()
    original_hook = sys.excepthook
    original_warning, original_critical = QMessageBox.warning, QMessageBox.critical
    original_ask = viewer.ask_save_changes

    def exception_hook(kind, value, tb):
        result["python_exceptions"].append("".join(traceback.format_exception(kind, value, tb)))

    def modal(parent, title, message, *unused, **kwargs):
        result["modal_messages"].append({"title": str(title), "message": str(message)})
        return QMessageBox.StandardButton.Ok

    def beat():
        nonlocal last_beat
        now = time.monotonic()
        heartbeat_intervals.append((now - last_beat) * 1000)
        last_beat = now

    def error_response(error, context):
        if error and not shutdown:
            result["worker_errors"].append({"context": context, "error": str(error)})

    def process_failure(owner_ref, code, status):
        owner = owner_ref()
        if shutdown or owner is None or getattr(owner, "closing", False):
            return
        if code != 0 or status == QProcess.ExitStatus.CrashExit:
            result["worker_crashes"].append({"exit_code": int(code), "exit_status": str(status)})

    def process_error(owner_ref, error):
        owner = owner_ref()
        if shutdown or owner is None or getattr(owner, "closing", False):
            return
        result["worker_errors"].append({"context": "QProcess", "error": str(error)})

    def hook_backends():
        if window is None:
            return
        for backend in window.findChildren(viewer.PdfBackend):
            if backend in hooked:
                continue
            hooked.add(backend)
            owner_ref = weakref.ref(backend)
            backend.proc.finished.connect(lambda code, status, ref=owner_ref: process_failure(ref, code, status))
            backend.proc.errorOccurred.connect(lambda error, ref=owner_ref: process_error(ref, error))
            backend.preview.connect(lambda token, pix, error: error_response(error, "preview"))
            backend.thumbnail.connect(lambda path, number, pix, error: error_response(error, "thumbnail"))
            backend.metadata.connect(lambda token, path, number, error: error_response(error, "inspect"))

    def verify_health(label):
        keys = ("worker_errors", "worker_crashes", "import_errors", "modal_messages", "python_exceptions")
        if any(result[key] for key in keys):
            raise AssertionError(f"Failure during {label}: " + json.dumps({key: result[key][-2:] for key in keys if result[key]}, ensure_ascii=False))
        if window is not None and window.thumb_errors:
            raise AssertionError(f"Thumbnail errors during {label}: {window.thumb_errors}")
        active = QApplication.activeModalWidget()
        if active is not None:
            raise AssertionError(f"Unexpected modal during {label}: {active.windowTitle()}")

    def wait(predicate, label, timeout=60):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            hook_backends()
            app.processEvents()
            verify_health(label)
            if predicate():
                return
            QTest.qWait(10)
        raise TimeoutError(f"Timed out: {label}")

    def idle(seconds, label):
        until = time.monotonic() + max(0, seconds)
        while time.monotonic() < until:
            hook_backends()
            app.processEvents()
            verify_health(label)
            QTest.qWait(10)

    def ready(editor, uid=None):
        return (editor is not None and not editor.closed and editor.preview_ready
                and editor.view.item is not None and not editor.reading_base_pix.isNull()
                and (uid is None or editor.page.uid == uid))

    def checkpoint(event, cycle, **extra):
        renderer = window.reading_renderer
        row = {
            "event": event, "cycle": cycle, "elapsed_s": time.monotonic() - started,
            "implementation": args.implementation, "file_count": count,
            "loaded_pages": len(window.pages), "preview_count": result["preview_count"],
            "cache_pages": len(renderer.cache),
            "cache_bytes": sum(entry["bytes"] for entry in renderer.cache.values()),
            "thumbnail_count": len(window.thumbs),
            "thumbnail_bytes": sum(p.width() * p.height() * 4 for p in window.thumbs.values()),
            "prefetch_count": len(renderer.prefetch), **extra,
        }
        result["checkpoints"].append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)

    def record_frame(editor, cycle, file_index, page_number, pane="main"):
        image = editor.reading_base_pix.toImage().convertToFormat(QImage.Format.Format_RGB888)
        width, height, stride = image.width(), image.height(), image.bytesPerLine()
        raw = bytes(image.constBits())
        tight = b"".join(raw[y * stride:y * stride + width * 3] for y in range(height))
        result["frames"].append({"cycle": cycle, "file_index": file_index,
                                 "page_number": page_number, "pane": pane,
                                 "width": width, "height": height,
                                 "sha256": hashlib.sha256(tight).hexdigest()})
        result["preview_count"] += 1

    def released():
        nonlocal release_count
        release_count += 1

    sys.excepthook = exception_hook
    QMessageBox.warning, QMessageBox.critical = modal, modal
    viewer.ask_save_changes = lambda *a, **k: QMessageBox.StandardButton.No
    timer = QTimer()
    timer.setInterval(100)
    timer.timeout.connect(beat)
    try:
        with tempfile.TemporaryDirectory(prefix="viewer_stress_settings_") as folder:
            launch.isolate_settings(viewer, folder)
            window = viewer.Window(startup_pdf_count=count)
            window.resize(1280, 850)
            window.settings.setValue("updates/auto", False)
            window.comparison.set_alignment(False)
            window.show_import_errors = lambda errors: result["import_errors"].extend(map(str, errors))
            window.backend.released.connect(released)
            settings_file = Path(window.settings.fileName()).resolve()
            assert settings_file.is_relative_to(Path(folder).resolve()), settings_file
            result["isolated_settings"] = True
            window.show()
            timer.start()
            hook_backends()
            checkpoint("started", 0)
            for cycle in range(1, args.cycles + 1):
                opened_at = time.monotonic()
                assert window.add_files(files), "UI rejected the PDF batch"
                wait(lambda: len(window.pages) == expected_pages and not window.pending_import
                     and not window.imports and not window.import_cancelling,
                     f"cycle {cycle}: all PDFs loaded", timeout=120)
                loaded = Counter(str(Path(page.path).resolve()) for page in window.pages)
                assert loaded == Counter({path: pages_per_file for path in files}), loaded
                first = window.pages[0]
                window.open_preview(first)
                wait(lambda: ready(window.preview_dialog, first.uid), f"cycle {cycle}: initial preview")
                idle(.5, "initial layout settle")
                assert not window.has_unsaved_changes(), "Read-only import unexpectedly marked as an edit"
                if args.implementation == "rust":
                    assert Path(window.backend.proc.program()).resolve() == args.rust.resolve()
                checkpoint("opened", cycle, open_elapsed_s=time.monotonic() - opened_at,
                           loaded_files=len(loaded))

                for file_index, path in enumerate(files):
                    pages = {page.number: page for page in window.pages if str(Path(page.path).resolve()) == path}
                    for number in sorted({0, pages_per_file // 2, pages_per_file - 1}):
                        page = pages[number]
                        window.open_preview(page)
                        wait(lambda uid=page.uid: ready(window.preview_dialog, uid),
                             f"cycle {cycle}: PDF {file_index + 1}, page {number + 1}")
                        window.ensure_page_visible(page.uid)
                        window.prioritize_thumbnails()
                        wait(lambda key=(page.path, page.number): key in window.thumbs,
                             f"cycle {cycle}: visible thumbnail {file_index + 1}/{number + 1}")
                        record_frame(window.preview_dialog, cycle, file_index, number)

                window.open_dual_mode("review")
                wait(lambda: window.dual_mode and ready(window.preview_dialog) and ready(window.dual_preview),
                     f"cycle {cycle}: dual view")
                assert window.dual_preview.dual_secondary
                for pane, editor in (("dual_left", window.preview_dialog), ("dual_right", window.dual_preview)):
                    record_frame(editor, cycle, files.index(str(Path(editor.page.path).resolve())), editor.page.number, pane)
                # Do not let the test retain a closed secondary editor between cycles.
                editor = None
                result["dual_view_cycles"] += 1
                window.close_dual_mode(animate=False)
                wait(lambda: not window.dual_mode, f"cycle {cycle}: close dual view")
                idle(1.0, "after page traversal")
                # Fixed operation count. Faster cases idle with the event loop alive
                # instead of running extra cycles and changing the workload.
                target = started + cycle * args.min_seconds / args.cycles
                idle(max(0, target - time.monotonic()), "equal observation interval")
                result["completed_cycles"] = cycle
                checkpoint("cycle_complete", cycle)

                previous_release = release_count
                window.clear()
                wait(lambda: not window.pages and not window.clear_pending
                     and release_count > previous_release and window.backend.active is None
                     and not window.backend.jobs and not window.reading_renderer.prefetch,
                     f"cycle {cycle}: clear and PDF release", timeout=60)
                idle(2.0, "post-release observation")
                assert not window.reading_renderer.cache and not window.thumbs
                checkpoint("cleared", cycle, release_count=release_count)
            result["source_files_unchanged"] = all(digest(path) == before[path] for path in files)
            assert result["source_files_unchanged"], "A source PDF changed during read-only stress"
            result["passed"] = True
            checkpoint("complete", args.cycles, passed=True)
            shutdown = True
            timer.stop()
            window.close()
            app.processEvents()
            window = None
    except Exception as error:
        result["timeout_count"] += int(isinstance(error, TimeoutError))
        result["errors"].append(traceback.format_exc())
        print(json.dumps({"event": "failed", "implementation": args.implementation,
                          "file_count": count, "cycle": result["completed_cycles"],
                          "elapsed_s": time.monotonic() - started,
                          "exception_type": type(error).__name__, "error": str(error)},
                         ensure_ascii=False), flush=True)
    finally:
        shutdown = True
        timer.stop()
        if window is not None:
            try:
                window.close()
                app.processEvents()
            except Exception:
                result["errors"].append("shutdown: " + traceback.format_exc())
                result["passed"] = False
        result["elapsed_s"] = time.monotonic() - started
        result["heartbeat_samples"] = len(heartbeat_intervals)
        result["maximum_heartbeat_interval_ms"] = max(heartbeat_intervals, default=None)
        result["source_files_unchanged"] = all(Path(path).is_file() and digest(path) == before[path] for path in files)
        if any(result[key] for key in ("errors", "worker_errors", "worker_crashes", "import_errors", "modal_messages", "python_exceptions")):
            result["passed"] = False
        for counter, key in (("worker_error_count", "worker_errors"), ("worker_crash_count", "worker_crashes"),
                             ("modal_count", "modal_messages"), ("python_exception_count", "python_exceptions")):
            result[counter] = len(result[key])
        sys.excepthook = original_hook
        QMessageBox.warning, QMessageBox.critical = original_warning, original_critical
        viewer.ask_save_changes = original_ask
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
        print(json.dumps({"event": "result", "implementation": args.implementation,
                          "file_count": count, "passed": result["passed"],
                          "completed_cycles": result["completed_cycles"], "elapsed_s": result["elapsed_s"],
                          "result_file": str(args.out.resolve())}, ensure_ascii=False), flush=True)
    return 0 if result["passed"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation", choices=("python", "rust"), required=True)
    parser.add_argument("--rust", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cycles", type=int, default=10)
    parser.add_argument("--min-seconds", type=float, default=120)
    args = parser.parse_args()
    if args.cycles < 1 or args.min_seconds < 0:
        parser.error("cycles must be positive and min-seconds nonnegative")
    try:
        return run(args)
    except Exception as error:
        # Dependency, baseline, or manifest failures happen before the Qt case's
        # result exists. Still leave a machine-readable failure for the supervisor.
        result = {"schema": 1, "implementation": args.implementation,
                  "passed": False, "completed_cycles": 0,
                  "requested_cycles": args.cycles, "initialization_failed": True,
                  "errors": [traceback.format_exc()],
                  "exception_type": type(error).__name__}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
        print(json.dumps({"event": "failed", "implementation": args.implementation,
                          "cycle": 0, "elapsed_s": 0, "exception_type": type(error).__name__,
                          "error": str(error), "result_file": str(args.out.resolve())},
                         ensure_ascii=False), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
