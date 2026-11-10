"""Page drag regression tests: owned snapshots, validation and real drop handlers."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import struct
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
    from PySide6.QtCore import QMimeData, QPointF, Qt, QUrl
    from PySide6.QtWidgets import QApplication
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject
    import pdf_page_dragger as viewer


@unittest.skipUnless(AVAILABLE, 'PDF and Qt runtime dependencies are unavailable')
class PageDragTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.app.setQuitOnLastWindowClosed(False)

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / 'source.pdf'
        writer = PdfWriter()
        for i in range(4):
            page = writer.add_blank_page(width=500+i, height=700)
            if i == 0:
                page[NameObject('/Rotate')] = NumberObject(90)
                annotation = DictionaryObject({NameObject('/Type'): NameObject('/Annot'),
                    NameObject('/Subtype'): NameObject('/Text'),
                    NameObject('/Rect'): ArrayObject([NumberObject(n) for n in (1, 1, 10, 10)])})
                page[NameObject('/Annots')] = ArrayObject([writer._add_object(annotation)])
        with self.source.open('wb') as stream:
            writer.write(stream)
        self.pages = [viewer.PageRef(str(self.source), i) for i in (2, 0, 2)]
        self.mime = viewer.PageDragData(self.pages, 'a'*32)
        self.addCleanup(self.mime.deleteLater)
        self.payload = viewer.read_page_transfer(self.mime)
        self.patch_temp = patch.object(viewer, 'TEMP_ROOT', self.root / 'runtime')
        self.patch_temp.start()
        self.addCleanup(self.patch_temp.stop)

    def encoded(self, data):
        mime = QMimeData()
        mime.setData(viewer.PAGE_TRANSFER_MIME, json.dumps(data).encode())
        return mime

    def owner(self):
        owner = SimpleNamespace(session='b'*32, clear_pending=False, closing=False,
            page_batch_job=None, pending_import=None, imports=[], pages=[],
            focus_after_file_drop=Mock(), card_size=160, by_id={},
            history=[], future=[], canvas=SimpleNamespace(selected=set(), anchor=None),
            refresh=Mock())
        def insert(pages, at):
            owner.pages[at:at] = pages
        owner.insert_page_refs = Mock(side_effect=insert)
        owner.receive_page_transfer = lambda mime, slot=None: viewer.Window.receive_page_transfer(owner, mime, slot)
        return owner

    def event(self, mime):
        return SimpleNamespace(mimeData=lambda: mime, buttons=lambda: Qt.MouseButton.LeftButton,
            position=lambda: QPointF(20, 20), accept=Mock(), ignore=Mock(), setDropAction=Mock())

    def test_cross_session_owned_copy_order_duplicates_rotation_annotations_and_source_hash(self):
        digest = hashlib.sha256(self.source.read_bytes()).digest()
        owner = self.owner()
        existing = viewer.PageRef(str(self.source), 3)
        owner.pages = [existing]
        self.assertTrue(owner.receive_page_transfer(self.mime, 0))
        self.assertIs(owner.pages[-1], existing)
        copied = owner.pages[:3]
        self.assertEqual([p.number for p in copied], [0, 1, 2])
        self.assertEqual(len({p.uid for p in copied}), 3)
        self.assertEqual(len({p.path for p in copied}), 1)
        target = Path(copied[0].path)
        self.assertNotEqual(target, self.source)
        self.assertIn(owner.session, target.parts)
        reader = PdfReader(target)
        self.assertEqual([int(p.mediabox.width) for p in reader.pages], [502, 500, 502])
        self.assertEqual(reader.pages[1].rotation, 90)
        self.assertEqual(len(reader.pages[1]['/Annots']), 1)
        self.assertEqual(hashlib.sha256(self.source.read_bytes()).digest(), digest)
        self.source.unlink()
        self.assertEqual(len(PdfReader(target).pages), 3)

    def test_duplicate_token_is_inserted_only_once_even_after_source_deletion(self):
        owner = self.owner()
        self.assertTrue(owner.receive_page_transfer(self.mime))
        self.source.unlink()
        self.assertTrue(owner.receive_page_transfer(self.mime))
        self.assertEqual(owner.insert_page_refs.call_count, 1)
        self.assertEqual(len(owner.pages), 3)

    def test_metadata_construction_and_same_session_reorder_do_not_export(self):
        with patch.object(viewer, 'export_pages', side_effect=AssertionError('eager export')):
            mime = viewer.PageDragData(self.pages, 'a'*32)
            self.addCleanup(mime.deleteLater)
            self.assertFalse(mime.paths)
            self.assertFalse(mime.directory.exists())
            self.assertFalse(mime.hasUrls())
            owner = self.owner()
            owner.session = 'a'*32
            owner.pages = self.pages
            owner.by_id = {p.uid:p for p in self.pages}
            owner.reorder = Mock()
            canvas = viewer.PageCanvas(owner)
            self.addCleanup(canvas.deleteLater)
            canvas.timer.stop()
            canvas.slot = 1
            canvas.layout_pages = Mock()
            event = self.event(mime)
            canvas.dropEvent(event)
            owner.reorder.assert_called_once_with([p.uid for p in self.pages], 1)
            owner.insert_page_refs.assert_not_called()
            event.accept.assert_called_once()

    def test_foreign_canvas_drop_uses_visible_insertion_slot(self):
        owner = self.owner()
        owner.receive_page_transfer = Mock(return_value=True)
        canvas = viewer.PageCanvas(owner)
        self.addCleanup(canvas.deleteLater)
        canvas.timer.stop()
        canvas.layout_pages = Mock()
        canvas.slot = 2
        event = self.event(self.mime)
        canvas.dropEvent(event)
        owner.receive_page_transfer.assert_called_once_with(self.mime, 2)
        event.accept.assert_called_once()
        self.assertIsNone(canvas.slot)
        self.assertIsNone(canvas.pointer)

    def test_rejected_canvas_drop_is_not_accepted(self):
        owner = self.owner()
        owner.receive_page_transfer = Mock(return_value=False)
        canvas = viewer.PageCanvas(owner)
        self.addCleanup(canvas.deleteLater)
        canvas.timer.stop()
        canvas.layout_pages = Mock()
        canvas.slot = 0
        event = self.event(self.mime)
        canvas.dropEvent(event)
        event.ignore.assert_called_once()
        event.accept.assert_not_called()

    def test_preview_foreign_pages_insert_but_ordinary_files_replace(self):
        owner = self.owner()
        owner.accepts_open_drop = Mock(return_value=True)
        owner.after_selection = Mock(return_value=7)
        owner.receive_page_transfer = Mock(return_value=True)
        owner.replace_inputs = Mock(return_value=True)
        owner.canvas = SimpleNamespace(pdf_paths=Mock(return_value=[str(self.source)]))
        event = self.event(self.mime)
        viewer.Window.dropEvent(owner, event)
        owner.receive_page_transfer.assert_called_once_with(self.mime, 7)
        owner.replace_inputs.assert_not_called()
        file_mime = QMimeData()
        file_mime.setUrls([QUrl.fromLocalFile(str(self.source))])
        viewer.Window.dropEvent(owner, self.event(file_mime))
        owner.replace_inputs.assert_called_once_with([str(self.source)])

    def test_invalid_metadata_and_oversized_payload_are_rejected(self):
        self.assertIsNone(viewer.read_page_transfer(QMimeData()))
        changes = [lambda d:d.update(schema=2), lambda d:d.update(session='bad'),
            lambda d:d.update(token='X'*32), lambda d:d.update(pages=[]),
            lambda d:d.update(pages=[None]),
            lambda d:d['pages'][0].update(path='relative.pdf'),
            lambda d:d['pages'][0].update(path='/tmp/not-pdf.txt'),
            lambda d:d['pages'][0].update(number=-1),
            lambda d:d['pages'][0].update(number=True),
            lambda d:d['pages'][0].update(count=-1),
            lambda d:d['pages'][0].update(signature=[1,2]),
            lambda d:d['pages'][0].update(signature=[1,2,False])]
        for change in changes:
            data = copy.deepcopy(self.payload)
            change(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                viewer.read_page_transfer(self.encoded(data))
        for raw in (b'not json', b' '*(8*1024*1024+1)):
            mime = QMimeData()
            mime.setData(viewer.PAGE_TRANSFER_MIME, raw)
            with self.assertRaises(ValueError):viewer.read_page_transfer(mime)
        data = dict(self.payload, pages=[{}]*100001)
        with self.assertRaises(ValueError):viewer.read_page_transfer(self.encoded(data))

    def test_malformed_internal_json_is_ignored(self):
        canvas = viewer.PageCanvas(self.owner())
        self.addCleanup(canvas.deleteLater)
        canvas.timer.stop()
        for raw in (b'[]', b'null', b'1', b'"string"', b'invalid'):
            mime = QMimeData()
            mime.setData(viewer.MIME, raw)
            self.assertFalse(canvas.is_internal(mime))

    def test_changed_source_is_rejected_before_export(self):
        with self.source.open('ab') as stream:stream.write(b'\n%changed')
        with patch.object(viewer, 'export_pages') as export:
            with self.assertRaises(ValueError):
                viewer.snapshot_page_transfer(self.payload, self.root/'copy')
            export.assert_not_called()

    def test_incorrect_document_count_fails_without_publishing(self):
        data = copy.deepcopy(self.payload)
        data['pages'][0]['count'] = 100
        with self.assertRaises(ValueError):
            viewer.snapshot_page_transfer(data, self.root/'bad-count')
        self.assertEqual(list((self.root/'bad-count').glob('*.pdf')), [])

    def test_out_of_range_page_fails_without_insertion(self):
        data = copy.deepcopy(self.payload)
        data['pages'][0]['number'] = 999
        owner = self.owner()
        with patch.object(viewer.QMessageBox, 'warning'):
            self.assertFalse(owner.receive_page_transfer(self.encoded(data)))
        owner.insert_page_refs.assert_not_called()
        self.assertEqual(owner.pages, [])

    def test_export_postcheck_failure_removes_completed_snapshot(self):
        target = self.root/'copy.pdf'
        target.write_bytes(self.source.read_bytes())
        with patch.object(viewer, 'export_pages', return_value=[target]), \
             patch.object(viewer, 'verify_page_transfer', side_effect=[None, ValueError('changed')]):
            with self.assertRaises(ValueError):viewer.snapshot_page_transfer(self.payload, self.root)
        self.assertFalse(target.exists())

    def test_snapshot_count_mismatch_removes_completed_snapshot(self):
        target = self.root/'copy.pdf'
        target.write_bytes(self.source.read_bytes())
        with patch.object(viewer, 'export_pages', return_value=[target]):
            with self.assertRaises(ValueError):viewer.snapshot_page_transfer(self.payload, self.root)
        self.assertFalse(target.exists())

    def test_failure_or_cancel_preserves_receiver_and_retry_token(self):
        for error in (RuntimeError('worker failure'), viewer.ExportCancelled()):
            owner = self.owner()
            owner.pages = [self.pages[0]]
            with patch.object(viewer, 'snapshot_page_transfer', side_effect=error), \
                 patch.object(viewer.QMessageBox, 'warning'):
                self.assertFalse(owner.receive_page_transfer(self.mime))
            self.assertEqual(owner.pages, [self.pages[0]])
            owner.insert_page_refs.assert_not_called()
            self.assertFalse(owner.receiving_page_drop)
            self.assertFalse(owner.received_page_drops)
            self.assertEqual(list((self.root/'runtime').rglob('*.pdf')), [])

    def test_insertion_failure_rolls_back_pages_and_leaves_token_retryable(self):
        owner = self.owner()
        original = self.pages[0]
        owner.pages = [original]
        owner.history = ['previous undo']
        owner.future = ['previous redo']
        owner.canvas.selected = {original.uid}
        owner.canvas.anchor = original.uid
        def failing_insert(pages, at):
            owner.pages[at:at] = pages
            owner.history.append('new undo')
            owner.future.clear()
            owner.canvas.selected = {p.uid for p in pages}
            owner.canvas.anchor = pages[-1].uid
            raise RuntimeError('refresh failed after insertion')
        owner.insert_page_refs = Mock(side_effect=failing_insert)
        with patch.object(viewer.QMessageBox, 'warning'):
            self.assertFalse(owner.receive_page_transfer(self.mime, 0))
        self.assertEqual(owner.pages, [original])
        self.assertEqual(owner.history, ['previous undo'])
        self.assertEqual(owner.future, ['previous redo'])
        self.assertEqual(owner.canvas.selected, {original.uid})
        self.assertEqual(owner.canvas.anchor, original.uid)
        owner.refresh.assert_called_once()
        self.assertFalse(owner.received_page_drops)
        self.assertEqual(list((self.root/'runtime').rglob('*.pdf')), [])

    def test_precancelled_outgoing_drag_creates_no_files(self):
        mime = viewer.PageDragData(self.pages, 'a'*32, cancelled=lambda:True)
        self.addCleanup(mime.deleteLater)
        with patch.object(viewer, 'export_pages') as export:
            with self.assertRaises(viewer.ExportCancelled):mime.ensure_files()
            export.assert_not_called()
        self.assertFalse(mime.directory.exists())
        self.assertEqual(mime.paths, [])

    def test_outgoing_render_failure_or_cancel_removes_every_partial_file(self):
        for cancel in (False, True):
            mime = viewer.PageDragData(self.pages, 'a'*32)
            self.addCleanup(mime.deleteLater)
            def dialog_factory(parent, pages, targets, stem, separate):
                targets[0].write_bytes(b'partial PDF')
                return SimpleNamespace(ended=True, cancelled=cancel,
                    error='' if cancel else 'worker failure', result_paths=[],
                    setWindowModality=Mock(), show=Mock(), hide=Mock(), deleteLater=Mock())
            with patch.object(viewer, 'PdfExportDialog', side_effect=dialog_factory):
                with self.assertRaises(viewer.ExportCancelled if cancel else RuntimeError):
                    mime.ensure_files()
            self.assertFalse(mime.directory.exists())
            self.assertEqual(mime.paths, [])
            self.assertFalse(mime.rendering)
            self.assertTrue(mime.error)

    def test_outgoing_success_is_rendered_only_once(self):
        mime = viewer.PageDragData(self.pages, 'a'*32)
        self.addCleanup(mime.deleteLater)
        def dialog_factory(parent, pages, targets, stem, separate):
            targets[0].write_bytes(self.source.read_bytes())
            return SimpleNamespace(ended=True, cancelled=False, error='',
                result_paths=targets, setWindowModality=Mock(), show=Mock(),
                hide=Mock(), deleteLater=Mock())
        with patch.object(viewer, 'PdfExportDialog', side_effect=dialog_factory) as render:
            first = mime.ensure_files()
            second = mime.ensure_files()
        self.assertIs(first, second)
        self.assertEqual(render.call_count, 1)
        self.assertTrue(first[0].is_file())
        self.assertFalse(mime.rendering)

    def test_outgoing_source_change_during_render_removes_result(self):
        mime = viewer.PageDragData(self.pages, 'a'*32)
        self.addCleanup(mime.deleteLater)
        def dialog_factory(parent, pages, targets, stem, separate):
            targets[0].write_bytes(self.source.read_bytes())
            with self.source.open('ab') as stream:
                stream.write(b'\n% changed during render')
            return SimpleNamespace(ended=True, cancelled=False, error='',
                result_paths=targets, setWindowModality=Mock(), show=Mock(),
                hide=Mock(), deleteLater=Mock())
        with patch.object(viewer, 'PdfExportDialog', side_effect=dialog_factory):
            with self.assertRaises(ValueError):mime.ensure_files()
        self.assertFalse(mime.directory.exists())
        self.assertEqual(mime.paths, [])

    def test_windows_descriptors_have_exact_layout_unicode_and_terminator(self):
        names = ['한글_사본.pdf', 'copy_002.pdf']
        data = viewer.virtual_file_descriptors(names)
        self.assertEqual(struct.unpack_from('<I', data)[0], 2)
        self.assertEqual(len(data), 4+592*2)
        for i, name in enumerate(names):
            base = 4+592*i
            self.assertEqual(struct.unpack_from('<I', data, base)[0], 0x80004004)
            self.assertEqual(struct.unpack_from('<I', data, base+36)[0], 0x80)
            self.assertEqual(data[base+72:base+592].decode('utf-16-le').rstrip('\0'), name)
        for name in ('a'*260, '../bad.pdf'):
            with self.assertRaises(ValueError):viewer.virtual_file_descriptors([name])


if __name__ == '__main__':
    unittest.main()
