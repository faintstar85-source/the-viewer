"""Native drag protocol contract with mocked COM; not a Windows ABI smoke test."""
import ast
from pathlib import Path
import re
import struct
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

SOURCE = Path(__file__).resolve().parents[1] / 'pdf_page_dragger.py'
tree = ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
namespace = {'Path': Path, 're': re, 'struct': struct}
exec(compile(ast.Module(body=[node for node in tree.body
    if isinstance(node, ast.FunctionDef) and node.name == 'create_windows_drag_objects'],
    type_ignores=[]), str(SOURCE), 'exec'), namespace)
create_objects = namespace['create_windows_drag_objects']


class COMException(Exception):
    def __init__(self, desc='', scode=0):
        super().__init__(desc)
        self.scode = scode


class Medium:
    def set(self, kind, value):
        self.tymed = kind
        self.input_type = type(value)
        self.data = bytes(value) if kind == 1 else value


class NativeAdapterTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.paths = [Path(directory.name) / f'{i}.pdf' for i in range(2)]
        for i, path in enumerate(self.paths):
            path.write_bytes(b'%PDF-1.7\n' + str(i).encode())
        self.formats = {}
        def register(name):
            return self.formats.setdefault(name, 0xC000 + len(self.formats))
        self.register = register
        self.pc = types.SimpleNamespace(TYMED_HGLOBAL=1, TYMED_ISTREAM=4,
            DVASPECT_CONTENT=1, IID_IDataObject='data', IID_IDropSource='drop',
            IID_IEnumFORMATETC='enum', STGMEDIUM=Medium, DATADIR_GET=1, DATADIR_SET=2,
            ReleaseStgMedium=Mock(side_effect=AssertionError('gateway owns release')))
        names = ['DV_E_DVASPECT', 'DV_E_LINDEX', 'DV_E_TYMED', 'DV_E_FORMATETC',
            'E_FAIL', 'E_UNEXPECTED', 'E_ABORT', 'E_NOTIMPL', 'E_INVALIDARG',
            'OLE_E_ADVISENOTSUPPORTED']
        self.errors = types.SimpleNamespace(**{n: -i-1 for i, n in enumerate(names)})
        modules = {'pythoncom': self.pc,
            'win32clipboard': types.SimpleNamespace(RegisterClipboardFormat=register),
            'win32con': types.SimpleNamespace(MK_RBUTTON=2, MK_LBUTTON=1),
            'winerror': self.errors,
            'win32com': types.ModuleType('win32com'),
            'win32com.server': types.ModuleType('win32com.server'),
            'win32com.server.exception': types.SimpleNamespace(COMException=COMException),
            'win32com.server.util': types.SimpleNamespace(NewEnum=lambda seq, iid: iter(seq),
                                                         wrap=lambda obj, iid: obj),
            'win32com.shell': types.SimpleNamespace(shell=types.SimpleNamespace(
                SHCreateStreamOnFileEx=lambda path, mode, attr, create: Path(path).open('rb')))}
        patcher = patch.dict(sys.modules, modules)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.mime = types.SimpleNamespace(native_cancelled=False,
            formats=lambda: ['application/x-test', 'text/uri-list'],
            data=lambda name: b'{"session":"sample"}',
            descriptor_bytes=lambda: struct.pack('<I', 2) + bytes(592*2),
            ensure_files=Mock(return_value=self.paths))
        self.cancel = False
        self.data, self.source = create_objects(self.mime, lambda: self.cancel)

    def fmt(self, name, index=-1, tymed=1):
        return (self.register(name), None, 1, index, tymed)

    def test_capability_queries_enumeration_and_static_reads_never_export(self):
        formats = list(self.data.EnumFormatEtc(1))
        for fmt in formats:
            self.data.QueryGetData(fmt)
        self.data.QueryGetData(self.fmt('FileContents', -1, 5))
        self.assertEqual([f[3] for f in formats if f[0] == self.formats['FileContents']], [0, 1])
        self.assertNotIn('text/uri-list', self.formats)
        raw = self.data.GetData(self.fmt('application/x-test'))
        self.assertEqual(raw.data, b'{"session":"sample"}')
        self.assertIs(raw.input_type, memoryview)
        self.assertEqual(len(self.data.GetData(self.fmt('FileGroupDescriptorW')).data), 1188)
        self.assertEqual(self.data.GetData(self.fmt('Preferred DropEffect')).data, struct.pack('<I', 1))
        self.mime.ensure_files.assert_not_called()

    def test_indexed_contents_keep_order_export_once_and_use_fresh_streams(self):
        for index in (1, 0, 1):
            raw = self.data.GetData(self.fmt('FileContents', index))
            self.assertEqual(raw.data, self.paths[index].read_bytes())
            self.assertIs(raw.input_type, memoryview)
        self.mime.ensure_files.assert_called_once()
        first = self.data.GetData(self.fmt('FileContents', 0, 4)).data
        second = self.data.GetData(self.fmt('FileContents', 0, 4)).data
        try:
            self.assertIsNot(first, second)
            first.read(2)
            self.assertEqual(second.read(), self.paths[0].read_bytes())
        finally:
            first.close()
            second.close()
        with self.assertRaises(COMException):self.data.GetData(self.fmt('FileContents', -1))

    def test_private_shell_feedback_is_copied_and_roundtrips_both_release_modes(self):
        for release in (False, True):
            with self.subTest(release=release):
                fmt = self.fmt(f'DragImageBits-{release}', index=3)
                original = bytearray(b'private\x00shell\xffpayload')
                medium = types.SimpleNamespace(tymed=1, data=original)
                self.assertIsNone(self.data.SetData(fmt, medium, release))
                original[:] = bytes(len(original))
                self.data.QueryGetData(fmt)
                result = self.data.GetData(fmt)
                self.assertEqual(result.data, b'private\x00shell\xffpayload')
                self.assertIs(result.input_type, memoryview)
                self.assertIn(fmt, list(self.data.EnumFormatEtc(1)))
        self.pc.ReleaseStgMedium.assert_not_called()
        self.mime.ensure_files.assert_not_called()

    def test_optional_bad_feedback_never_raises_or_releases_medium(self):
        class BrokenMedium:
            tymed = 1
            @property
            def data(self):raise ValueError('unsupported helper payload')
        for release in (False, True):
            for fmt, medium in ((self.fmt('UnknownHelper'), BrokenMedium()),
                    (None, object()),
                    (self.fmt('StreamHelper'), types.SimpleNamespace(tymed=4, data=object()))):
                self.assertIsNone(self.data.SetData(fmt, medium, release))
        self.pc.ReleaseStgMedium.assert_not_called()
        self.assertFalse(self.mime._native_drag_errors)
        self.mime.ensure_files.assert_not_called()

    def test_setdata_cannot_overwrite_static_metadata_or_file_contents(self):
        for release in (False, True):
            for name in ('application/x-test', 'FileGroupDescriptorW', 'Preferred DropEffect'):
                fmt = self.fmt(name)
                original = self.data.GetData(fmt).data
                self.data.SetData(fmt, types.SimpleNamespace(tymed=1, data=b'overwrite'), release)
                self.assertEqual(self.data.GetData(fmt).data, original)
            fmt = self.fmt('FileContents', 0)
            self.data.SetData(fmt, types.SimpleNamespace(tymed=1, data=b'overwrite'), release)
            self.assertNotIn((fmt[0], fmt[2], fmt[3]), self.data.feedback)
        self.mime.ensure_files.assert_not_called()

    def test_effect_feedback_is_recorded_without_changing_copy_preference(self):
        for name in ('Performed DropEffect', 'Logical Performed DropEffect', 'Paste Succeeded'):
            fmt = self.fmt(name)
            self.data.SetData(fmt, types.SimpleNamespace(tymed=1, data=struct.pack('<I', 2)), True)
            self.assertEqual(self.data.effects[fmt[0]], 2)
            self.assertEqual(self.data.GetData(fmt).data, struct.pack('<I', 2))
        self.assertEqual(self.data.GetData(self.fmt('Preferred DropEffect')).data, struct.pack('<I', 1))

    def test_escape_right_click_and_external_cancel_prevent_export(self):
        for escape, keys, cancelled in ((True, 1, False), (False, 3, False), (False, 1, True)):
            self.mime.native_cancelled = False
            self.cancel = cancelled
            self.assertEqual(self.source.QueryContinueDrag(escape, keys), 0x40101)
            self.assertTrue(self.mime.native_cancelled)
            with self.assertRaises(COMException) as error:
                self.data.GetData(self.fmt('FileContents', 0))
            self.assertEqual(error.exception.scode, self.errors.E_ABORT)
        self.mime.ensure_files.assert_not_called()

    def test_button_release_and_default_feedback(self):
        self.assertEqual(self.source.QueryContinueDrag(False, 1), 0)
        self.assertEqual(self.source.QueryContinueDrag(False, 0), 0x40100)
        self.assertEqual(self.source.GiveFeedback(1), 0x40102)
        self.assertFalse(self.mime.native_cancelled)

    def test_incomplete_exports_fail_atomically_and_are_not_retried(self):
        self.mime.ensure_files.return_value = self.paths[:1]
        for index in (0, 1):
            with self.assertRaises(COMException):self.data.GetData(self.fmt('FileContents', index))
        self.mime.ensure_files.assert_called_once()
        self.assertIsNone(self.data.paths)
        self.assertEqual(len(self.mime._native_drag_errors), 1)

    def test_cancel_during_export_publishes_no_contents(self):
        def export():
            self.cancel = True
            return self.paths
        self.mime.ensure_files.side_effect = export
        with self.assertRaises(COMException) as error:
            self.data.GetData(self.fmt('FileContents', 0))
        self.assertEqual(error.exception.scode, self.errors.E_ABORT)
        self.assertIsNone(self.data.paths)
        self.assertFalse(self.data.preparing)


if __name__ == '__main__':
    unittest.main()
