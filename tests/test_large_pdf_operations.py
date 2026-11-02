"""Regression checks for large-document copies and page-order operations."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
AVAILABLE = all(importlib.util.find_spec(name) for name in
                ('PySide6', 'pypdf', 'pypdfium2', 'PIL'))
if AVAILABLE:
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject
    import pdf_page_dragger as viewer
    import viewer_pdf_engine as engine


@unittest.skipUnless(AVAILABLE, 'PDF and Qt runtime dependencies are unavailable')
class LargePdfOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.app.setQuitOnLastWindowClosed(False)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.pdf'
        writer = PdfWriter()
        for i in range(20):
            page = writer.add_blank_page(width=500+i, height=700)
            if i == 0:
                page[NameObject('/Rotate')] = NumberObject(90)
                annotation = DictionaryObject({NameObject('/Type'): NameObject('/Annot'),
                    NameObject('/Subtype'): NameObject('/Text'),
                    NameObject('/Rect'): ArrayObject([NumberObject(1), NumberObject(1),
                                                     NumberObject(10), NumberObject(10)])})
                page[NameObject('/Annots')] = ArrayObject([writer._add_object(annotation)])
        with self.source.open('wb') as stream:
            writer.write(stream)

    def test_one_snapshot_is_reused_and_invalidated_on_source_change(self):
        with engine.open(self.source) as source, engine.open() as result:
            with patch.object(source, 'tobytes', wraps=source.tobytes) as serialize:
                for number in (4, 1, 4, 0, 2):
                    result.insert_pdf(source, from_page=number, to_page=number)
                self.assertEqual(serialize.call_count, 1)
                self.assertEqual([int(p.mediabox.width) for p in result._writer.pages],
                                 [504, 501, 504, 500, 502])
                source.new_page(width=777, height=700)
                result.insert_pdf(source, from_page=20, to_page=20)
                self.assertEqual(serialize.call_count, 2)
                self.assertEqual(int(result._writer.pages[-1].mediabox.width), 777)

    def test_rotation_and_annotations_do_not_change_later_copies(self):
        with engine.open(self.source) as source, engine.open() as result:
            result.insert_pdf(source, from_page=0, to_page=0, rotate=180, annots=False)
            result.insert_pdf(source, from_page=0, to_page=0)
            first, second = result._writer.pages
            self.assertEqual(first.rotation, 180)
            self.assertNotIn('/Annots', first)
            self.assertEqual(second.rotation, 90)
            self.assertIn('/Annots', second)
            self.assertEqual(source._writer.pages[0].rotation, 90)
            self.assertIn('/Annots', source._writer.pages[0])

    def test_self_insertion_snapshots_original_order(self):
        with engine.open() as doc:
            doc.new_page(width=100, height=200)
            doc.new_page(width=200, height=200)
            doc.insert_pdf(doc, from_page=0, to_page=1, start_at=1)
            self.assertEqual([int(p.mediabox.width) for p in doc._writer.pages],
                             [100, 100, 200, 200])

    def test_export_in_child_keeps_ui_responsive_and_order(self):
        pages = [viewer.PageRef(str(self.source), i) for i in (4, 1, 4, 0)]
        ticks = []
        timer = QTimer()
        timer.setInterval(10)
        timer.timeout.connect(lambda: ticks.append(1))
        timer.start()
        try:
            [output] = viewer.export_pages(pages, self.root, 'combined')
        finally:
            timer.stop()
        self.assertGreater(len(ticks), 3)
        self.assertEqual([int(p.mediabox.width) for p in PdfReader(output).pages],
                         [504, 501, 504, 500])
        self.assertEqual(list(self.root.glob('.TheViewer-copy-*')), [])

    def test_separate_exports_keep_order_and_existing_files_are_safe(self):
        pages = [viewer.PageRef(str(self.source), i) for i in (7, 2, 7)]
        files = viewer.export_pages(pages, self.root, 'separate', separate=True)
        self.assertEqual([p.name for p in files],
                         ['separate_001.pdf', 'separate_002.pdf', 'separate_003.pdf'])
        self.assertEqual([int(PdfReader(p).pages[0].mediabox.width) for p in files],
                         [507, 502, 507])
        original = files[0].read_bytes()
        with self.assertRaises(FileExistsError):
            viewer.export_pages(pages, self.root, 'separate', separate=True)
        self.assertEqual(files[0].read_bytes(), original)

    def test_large_document_selected_copy_and_move_undo(self):
        source = self.root / 'large.pdf'
        writer = PdfWriter()
        for i in range(1722):
            writer.add_blank_page(width=500+(i % 100), height=700)
        with source.open('wb') as stream:
            writer.write(stream)
        pages = [viewer.PageRef(str(source), i) for i in range(1722)]
        original = [p.uid for p in pages]
        selected = [pages[i] for i in (2, 365, 999, 1721)]
        owner = SimpleNamespace(pages=pages, history=[], future=[], original_path=str(source),
                                preview_dialog=None, refresh=Mock())
        owner.snapshot = lambda: viewer.Window.snapshot(owner)
        viewer.Window.reorder(owner, [p.uid for p in selected], 20)
        remaining = [p for p in pages if p not in selected]
        self.assertEqual([p.uid for p in owner.pages],
                         [p.uid for p in remaining[:20]+selected+remaining[20:]])
        viewer.Window.undo(owner)
        self.assertEqual([p.uid for p in owner.pages], original)
        viewer.Window.redo(owner)
        self.assertEqual([p.uid for p in owner.pages[20:24]], [p.uid for p in selected])
        [output] = viewer.export_pages(selected, self.root, 'large-selection')
        self.assertEqual([int(p.mediabox.width) for p in PdfReader(output).pages],
                         [502, 565, 599, 521])

    def test_worker_failure_and_cancel_leave_no_final_or_staged_copy(self):
        pages = [viewer.PageRef(str(self.root / 'missing.pdf'), 0)]
        with self.assertRaises(RuntimeError):
            viewer.export_pages(pages, self.root, 'failed')
        self.assertFalse((self.root / 'failed.pdf').exists())
        self.assertEqual(list(self.root.glob('.TheViewer-copy-*')), [])
        dialog = viewer.PdfExportDialog(None, [viewer.PageRef(str(self.source), 0)],
                                        [self.root / 'cancelled.pdf'], 'cancelled', False)
        stage = dialog.stage
        dialog.reject()
        self.app.processEvents()
        self.assertTrue(dialog.cancelled)
        self.assertFalse(stage.exists())
        self.assertFalse((self.root / 'cancelled.pdf').exists())


if __name__ == '__main__':
    unittest.main()
