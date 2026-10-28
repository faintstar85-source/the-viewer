"""Check PDF Type3 byte boundaries and PDFium-compatible width normalization."""
import ast
import base64
import ctypes
import math
from pathlib import Path
import unittest
import sys
import zlib

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_repository import validate_backend_copies

SOURCE=Path(__file__).resolve().parents[1]/'pdf_page_dragger.py'
tree=ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_VIEWER_PDF_EDIT_SOURCE' for t in n.targets))
backend=ast.parse(ast.literal_eval(assignment.value))
names={'_font_code_size','_font_width_table'}
namespace={'ctypes':ctypes,'math':math}
exec(compile(ast.Module(body=[n for n in backend.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'viewer_pdf_edit','exec'),namespace)


class PdfDict(dict):
    def get_object(self):return self


class Indirect:
    def __init__(self,value):self.value=value
    def get_object(self):return self.value


class TestType3FontMetrics(unittest.TestCase):
    def font(self,**changes):
        result=PdfDict({'/Subtype':'/Type3','/FirstChar':65,'/LastChar':66,
                        '/Widths':Indirect([651,713]),'/FontMatrix':Indirect([.001,0,0,.001,0,0])})
        result.update(changes);return result
    def test_type3_uses_single_byte_codes_and_indirect_widths(self):
        step,widths,default=namespace['_font_width_table'](self.font())
        self.assertEqual((step,widths,default),(1,{65:651.,66:713.},0.))
    def test_nonstandard_font_matrix_is_applied_before_pdfium_rounding(self):
        f=self.font(**{'/FontMatrix':[.00125,.0002,0,.002,0,0]})
        self.assertEqual(namespace['_font_width_table'](f)[1],{65:814.,66:891.})
    def test_invalid_type3_metrics_are_refused(self):
        for changes in [{'/FontMatrix':[1,0]}, {'/FontMatrix':[float('nan'),0,0,1,0,0]},
                        {'/Widths':[650]}, {'/Widths':[650,float('inf')]},
                        {'/LastChar':256}, {'/LastChar':66.5}, {'/FirstChar':65.5}, {'/FirstChar':None}]:
            with self.subTest(changes=changes):
                with self.assertRaises((ValueError,TypeError)):namespace['_font_width_table'](self.font(**changes))
    def test_other_font_code_boundaries_are_preserved(self):
        self.assertEqual(namespace['_font_code_size'](PdfDict({'/Subtype':'/TrueType'})),1)
        self.assertEqual(namespace['_font_code_size'](PdfDict({'/Subtype':'/Type0','/Encoding':'/Identity-H'})),2)
        with self.assertRaises(ValueError):namespace['_font_code_size'](PdfDict({'/Subtype':'/Type0','/Encoding':'/Identity-V'}))
    def test_simple_font_indirect_width_array_still_works(self):
        f=PdfDict({'/Subtype':'/TrueType','/FirstChar':65,'/Widths':Indirect([651,713])})
        self.assertEqual(namespace['_font_width_table'](f),(1,{65:651.,66:713.},None))
    def test_stale_worker_backend_is_detected_before_packaging(self):
        fixed='def _font_code_size(font):\n return 1\ndef _font_width_table(font):\n return 1,{},0.\n'
        stale=fixed.replace('return 1,{},0.',"raise ValueError('Type3 unsupported')")
        def application(inner):
            capsule='_VIEWER_PDF_ENGINE_SOURCE = ""\n_VIEWER_PDF_EDIT_SOURCE = '+repr(inner)+'\n'
            encoded=base64.b85encode(zlib.compress(capsule.encode())).decode()
            return '_VIEWER_PDF_ENGINE_SOURCE = ""\n_VIEWER_PDF_EDIT_SOURCE = '+repr(fixed)+'\ndef _viewer_fast_pdf_worker():\n return base64.b85decode('+repr(encoded)+')\n'
        validate_backend_copies(application(fixed))
        with self.assertRaises(ValueError):validate_backend_copies(application(stale))


if __name__=='__main__':unittest.main()
