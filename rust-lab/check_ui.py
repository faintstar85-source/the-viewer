#!/usr/bin/env python3
"""Exercise the unchanged Qt UI using the experimental Rust worker.

This verifies only the listed actions. It is not a Windows desktop, file-dialog,
printing, document-conversion, difference-analysis, or full feature-parity test.
Run after performance measurements, never concurrently with the benchmark.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import runpy
import subprocess
import sys
import tempfile
import time
import traceback

LAB = Path(__file__).resolve().parent
REPO = LAB.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(LAB))
if os.name != "nt":
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fixture(path):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(str(path), pagesize=(612, 792), invariant=1)
    for page in range(3):
        c.setFillColorRGB(.12, .20, .32)
        c.setFont("Helvetica-Bold", 23)
        c.drawString(45, 735, f"THE VIEWER / PAGE {page + 1}")
        c.setFont("Helvetica", 12)
        c.drawString(45, 705, "NEEDLE: Rust reader UI verification")
        c.drawString(45, 682, "Original UI, PDFium, and compatibility editing")
        for row in range(11):
            y = 600 - row * 35
            c.line(45, y, 567, y)
            if row < 10:
                c.drawString(54, y - 23, f"Row {row + 1:02d} / sample page {page + 1}")
                c.drawRightString(550, y - 23, f"{(page+1)*100+row}.00")
        for x in (45, 425, 567):
            c.line(x, 250, x, 600)
        c.showPage()
    c.save()


def picture_signature(pixmap):
    from PySide6.QtGui import QImage
    image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGB888)
    width, height, stride = image.width(), image.height(), image.bytesPerLine()
    data = bytes(image.constBits())
    tight = b"".join(data[y * stride:y * stride + width * 3] for y in range(height))
    return {"width": width, "height": height, "sha256": hashlib.sha256(tight).hexdigest()}


def photo_child(rust):
    import bridge
    import launch
    import pdf_page_dragger as viewer
    bridge.install(viewer, rust)
    with tempfile.TemporaryDirectory(prefix="viewer_rust_photo_settings_") as folder:
        launch.isolate_settings(viewer, folder)
        runpy.run_path(str(REPO / "scripts/check_photo_navigation_ui.py"), run_name="__main__")


def run_ui(rust, output):
    import bridge
    import pdf_page_dragger as viewer
    import PySide6
    from PySide6.QtCore import QSettings, Qt
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication, QMessageBox
    from PySide6.QtGui import QFont, QFontDatabase

    output.mkdir(parents=True, exist_ok=True)
    result = {
        "baseline_commit": bridge.BASELINE_COMMIT,
        "baseline_sha256": bridge.BASELINE_SHA256,
        "rust_sha256": digest(rust),
        "platform": platform.platform(),
        "qt_platform": os.environ.get("QT_QPA_PLATFORM", "default"),
        "pyside_version": PySide6.__version__,
        "scope": "Qt UI and QProcess integration; hybrid, not a complete Rust application",
        "checks": {}, "screenshots": [], "errors": [],
        "not_tested": ["Windows desktop execution", "native file dialogs", "printing",
                       "Office/HWP conversion", "difference analysis", "all editing tools",
                       "drag and drop from Windows Explorer"],
    }
    app = QApplication.instance() or QApplication([])
    app.setStyle("Fusion")
    # Optional local QA font for Linux hosts without Korean system fonts.
    # The application launcher itself retains the original platform font choice.
    test_font = os.environ.get("VIEWER_TEST_FONT")
    if test_font:
        font_id = QFontDatabase.addApplicationFont(test_font)
        families = QFontDatabase.applicationFontFamilies(font_id)
        if not families:
            raise RuntimeError("QA font could not be loaded")
        app.setFont(QFont(families[0], 10))
        result["qa_font"] = {"family": families[0], "sha256": digest(test_font)}
    bridge.install(viewer, rust)
    viewer.APP_NAME = "The Viewer (정) · Rust 처리 시험본"
    window = None
    extra_backend = None
    original_warning = QMessageBox.warning
    original_critical = QMessageBox.critical
    original_ask = viewer.ask_save_changes
    modal_messages = []

    def reject_modal(parent, title, message, *unused, **kwargs):
        modal_messages.append({"title": str(title), "message": str(message)})
        return QMessageBox.StandardButton.Ok

    # Prevent a failed automated check from waiting indefinitely in a modal.
    # Every captured warning is a failure; none is interpreted as a success.
    QMessageBox.warning = reject_modal
    QMessageBox.critical = reject_modal
    # Only generated, disposable fixture edits are discarded on test shutdown.
    viewer.ask_save_changes = lambda *args, **kwargs: QMessageBox.StandardButton.No
    try:
        with tempfile.TemporaryDirectory(prefix="viewer_rust_ui_") as folder:
            root = Path(folder)
            settings_root = root / "settings"
            import launch
            launch.isolate_settings(viewer, settings_root)
            source = root / "한글 경로 검사 자료.pdf"
            fixture(source)
            before_hash = digest(source)
            imports = []
            window = viewer.Window(startup_pdf_count=1)
            window.resize(1280, 850)
            window.show_import_errors = lambda errors: imports.extend(map(str, errors))
            window.settings.setValue("updates/auto", False)
            window.comparison.set_alignment(False)
            window.show()

            def wait(predicate, label, timeout=40):
                deadline = time.monotonic() + timeout
                while time.monotonic() < deadline:
                    app.processEvents()
                    if modal_messages or imports:
                        raise AssertionError({"stage": label, "modals": modal_messages, "imports": imports})
                    modal = QApplication.activeModalWidget()
                    if modal is not None:
                        raise AssertionError(f"Unexpected modal at {label}: {modal.windowTitle()}")
                    if predicate():
                        return
                    QTest.qWait(10)
                raise AssertionError(f"Timed out: {label}")

            def ready(editor):
                return editor is not None and not editor.closed and editor.preview_ready and editor.view.item is not None

            def shot(name):
                app.processEvents()
                path = output / name
                if not window.grab().save(str(path)):
                    raise AssertionError(f"Could not save screenshot {path}")
                result["screenshots"].append(str(path.resolve()))

            settings_file = Path(window.settings.fileName()).resolve()
            assert settings_file.is_relative_to(settings_root.resolve()), settings_file
            result["checks"]["isolated_ini_settings"] = True
            metadata = []
            window.backend.metadata.connect(lambda token, path, count, error: metadata.append((count, error)))
            window.add_files([str(source)])
            wait(lambda: len(window.pages) == 3 and not window.pending_import and not window.imports and ready(window.preview_dialog), "PDF open and first preview")
            assert metadata and metadata[0] == (3, ""), metadata
            assert Path(window.backend.proc.program()).resolve() == rust.resolve()
            result["checks"]["rust_qprocess_metadata_three_pages"] = True
            result["checks"]["first_pdf_preview"] = picture_signature(window.preview_dialog.reading_base_pix)
            wait(lambda: bool(window.thumbs) and not window.thumb_errors, "visible thumbnail")
            result["checks"]["visible_thumbnail"] = {"count": len(window.thumbs), "errors": dict(window.thumb_errors)}
            shot("rust_ui_single.png")

            editor = window.preview_dialog
            QTest.mouseClick(editor.nav_next, Qt.MouseButton.LeftButton)
            wait(lambda: ready(window.preview_dialog) and window.preview_dialog.page.number == 1, "actual next-page button")
            result["checks"]["next_page_button"] = True

            # Exercise the real search panel and its connected button signal.
            panel = window.pdf_search
            panel.show_panel()
            panel.input.setText("NEEDLE")
            QTest.mouseClick(panel.find_button, Qt.MouseButton.LeftButton)
            wait(lambda: panel.cursor == 3 and not panel.pending and len(panel.results) == 3, "search panel")
            assert panel.errors == [], panel.errors
            assert all(hit["match"] == "NEEDLE" for hit in panel.results)
            result["checks"]["search_panel_fallback"] = {"hits": len(panel.results), "pages": panel.cursor}
            shot("rust_ui_search.png")
            panel.close_panel()

            # Use the application's own dual-view operation. Analysis is excluded.
            window.open_dual_mode("review")
            wait(lambda: window.dual_mode and ready(window.preview_dialog) and ready(window.dual_preview), "dual PDF view")
            result["checks"]["dual_pdf_view"] = {
                "left": picture_signature(window.preview_dialog.reading_base_pix),
                "right": picture_signature(window.dual_preview.reading_base_pix),
                "right_read_only": bool(window.dual_preview.dual_secondary),
            }
            assert window.dual_preview.dual_secondary
            shot("rust_ui_dual.png")
            window.close_dual_mode(animate=False)

            # Request a thumbnail explicitly through PdfBackend, independently
            # of the UI's preview-derived thumbnail cache.
            extra_backend = viewer.PdfBackend(window, lazy=True)
            thumbnails = []
            extra_backend.thumbnail.connect(lambda path, page, pix, error: thumbnails.append((path, page, picture_signature(pix) if not pix.isNull() else None, error)))
            extra_backend.request("render", str(source), 2, payload={"thumb_side": 370})
            wait(lambda: len(thumbnails) == 1, "PdfBackend thumbnail request")
            assert thumbnails[0][1] == 2 and thumbnails[0][2] and not thumbnails[0][3], thumbnails
            result["checks"]["pdfbackend_thumbnail_signal"] = thumbnails[0][2]
            extra_backend.stop()

            # Use existing editor APIs and callback path to create a real
            # disposable edit, then verify re-rendering and original preservation.
            editor = window.preview_dialog
            editor.set_mode("edit")
            wait(lambda: bool(editor.info) and not editor.loading_info and not editor.busy, "edit info fallback")
            result["checks"]["editor_info_fallback"] = {"width": editor.info["width"], "height": editor.info["height"]}
            original_page_path = editor.page.path
            old_picture = picture_signature(editor.reading_base_pix)
            editor.submit_edit({"kind": "cover", "rect": [50, 160, 170, 195], "color": "#e64b4b"})
            wait(lambda: not editor.busy and editor.page.path != original_page_path and ready(editor), "edit callback and revised preview")
            edited_path = Path(editor.page.path)
            assert edited_path.is_file() and digest(source) == before_hash
            new_picture = picture_signature(editor.reading_base_pix)
            assert new_picture["sha256"] != old_picture["sha256"], "Edit did not change the displayed pixels"
            import pypdfium2
            edited = pypdfium2.PdfDocument(str(edited_path))
            try:
                assert len(edited) == 1
                page = edited[0]
                try:
                    text = page.get_textpage()
                    try:
                        assert "NEEDLE" in text.get_text_range()
                    finally:
                        text.close()
                finally:
                    page.close()
            finally:
                edited.close()
            result["checks"]["real_cover_edit_fallback"] = {"saved_pdf_reopens": True, "original_unchanged": True, "preview_changed": True}
            shot("rust_ui_edited.png")
            assert digest(source) == before_hash
            result["checks"]["original_pdf_preserved"] = True
            window.close()
            app.processEvents()
            window = None

        # The existing photograph smoke test owns its QApplication, so run it
        # in a fresh process after installing the bridge in that process.
        photo = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--rust", str(rust), "--photo-child"],
                               cwd=REPO, capture_output=True, text=True, timeout=120)
        (output / "photo_ui_stdout.txt").write_text(photo.stdout, encoding="utf8")
        (output / "photo_ui_stderr.txt").write_text(photo.stderr, encoding="utf8")
        if photo.returncode:
            raise AssertionError(f"Original photo UI smoke test failed ({photo.returncode}): {photo.stderr[-3000:]}")
        lines = [line for line in photo.stdout.splitlines() if line.startswith("{")]
        assert lines, "Photo smoke test did not emit its verification record"
        result["checks"]["existing_photo_navigation_smoke"] = json.loads(lines[-1])
        result["passed"] = True
    except Exception:
        result["passed"] = False
        result["errors"].append(traceback.format_exc())
    finally:
        if extra_backend is not None:
            extra_backend.stop()
        if window is not None:
            window.close()
            app.processEvents()
        result["modal_messages"] = modal_messages
        QMessageBox.warning = original_warning
        QMessageBox.critical = original_critical
        viewer.ask_save_changes = original_ask
        (output / "ui_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rust", type=Path, default=LAB / "target/release" / ("viewer-rust-worker.exe" if os.name == "nt" else "viewer-rust-worker"))
    parser.add_argument("--out", type=Path, default=LAB / "results/ui")
    parser.add_argument("--photo-child", action="store_true")
    args = parser.parse_args()
    if args.photo_child:
        photo_child(args.rust.resolve())
        return 0
    return run_ui(args.rust.resolve(), args.out.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
