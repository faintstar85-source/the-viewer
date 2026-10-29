import ast
import ctypes
import math
from pathlib import Path
import struct
import unittest
from types import SimpleNamespace

SOURCE=Path(__file__).resolve().parents[1]/'pdf_page_dragger.py'
tree=ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_VIEWER_PDF_ENGINE_SOURCE' for t in n.targets))
engine=ast.parse(ast.literal_eval(node.value));namespace={'math':math}
functions=[n for n in engine.body if isinstance(n,ast.FunctionDef) and n.name in {'_font_program_weight','_font_name_is_bold','_font_source_is_bold'}]
functions.extend(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='nearest_text_hit')
exec(compile(ast.Module(body=functions,type_ignores=[]),'short text helpers','exec'),namespace)


class TestShortTextEditing(unittest.TestCase):
    def program(self,weight):
        data=bytearray(36);data[:4]=b'\x00\x01\x00\x00';struct.pack_into('>H',data,4,1)
        data[12:16]=b'OS/2';struct.pack_into('>II',data,20,28,8);struct.pack_into('>H',data,32,weight)
        return bytes(data)
    def test_actual_embedded_weight_is_available_without_stem_estimation(self):
        for weight in (400,600,700):self.assertEqual(namespace['_font_program_weight'](self.program(weight)),weight)
    def test_font_data_length_uses_size_t_on_32_and_64_bit_windows(self):
        # Windows unsigned long remains 32-bit while Win64 size_t is 64-bit.
        for size_type in (ctypes.c_uint32,ctypes.c_uint64):
            for weight in (400,700):
                with self.subTest(size=ctypes.sizeof(size_type),weight=weight):
                    data=self.program(weight);calls=[]
                    def font_data(font,buffer,capacity,out):
                        self.assertIs(type(out._obj),size_type)
                        out._obj.value=len(data);calls.append(capacity)
                        if buffer is not None:
                            for i,b in enumerate(data):buffer[i]=b
                        return 1
                    namespace['ctypes']=SimpleNamespace(c_ulong=ctypes.c_uint32,c_size_t=size_type,
                                                       byref=ctypes.byref,c_ubyte=ctypes.c_ubyte)
                    namespace['pdfium']=SimpleNamespace(raw=SimpleNamespace(FPDFFont_GetIsEmbedded=lambda _:1,
                                                                            FPDFFont_GetFontData=font_data))
                    self.assertEqual(namespace['_font_source_is_bold'](1,'Unknown'),weight>=700)
                    self.assertEqual(calls,[0,len(data)])
    def test_invalid_or_unidentified_program_does_not_invent_weight(self):
        for data in (b'',b'ttcf'+b'\0'*30,self.program(0),self.program(400)[:33]):
            self.assertIsNone(namespace['_font_program_weight'](data))
    def test_subset_prefix_and_regular_or_semibold_names_do_not_force_bold(self):
        for name in ('BOLDAB+Arial','ABCDEF+MalgunGothic','Arial-Regular','Arial-SemiBold','Unknown'):
            self.assertFalse(namespace['_font_name_is_bold'](name),name)
        for name in ('ABCDEF+Arial-BoldMT','MalgunGothicBold','Arial-BoldItalicMT'):
            self.assertTrue(namespace['_font_name_is_bold'](name),name)
    def test_small_digit_hit_prefers_the_nearest_text(self):
        a={'text':'7','rect':[10,10,14,18]};b={'text':'12','rect':[22,10,32,18]}
        self.assertIs(namespace['nearest_text_hit']([a,b],[16,14],6),a)
        self.assertIs(namespace['nearest_text_hit']([a,b],[21,14],6),b)
    def test_hit_does_not_reach_faraway_or_hidden_object_text(self):
        a={'text':'7','rect':[10,10,14,18]}
        self.assertIsNone(namespace['nearest_text_hit']([a],[40,40],6))
        self.assertIsNone(namespace['nearest_text_hit']([{**a,'object_id':'managed'}],[12,14],6))


if __name__=='__main__':unittest.main()
