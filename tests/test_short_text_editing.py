import ast
import math
from pathlib import Path
import struct
import unittest

SOURCE=Path(__file__).resolve().parents[1]/'pdf_page_dragger.py'
tree=ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_VIEWER_PDF_ENGINE_SOURCE' for t in n.targets))
engine=ast.parse(ast.literal_eval(node.value));namespace={'math':math}
functions=[n for n in engine.body if isinstance(n,ast.FunctionDef) and n.name in {'_font_program_weight','_font_name_is_bold'}]
functions.extend(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='nearest_text_hit')
exec(compile(ast.Module(body=functions,type_ignores=[]),'short text helpers','exec'),namespace)


class TestShortTextEditing(unittest.TestCase):
    def program(self,weight):
        data=bytearray(36);data[:4]=b'\x00\x01\x00\x00';struct.pack_into('>H',data,4,1)
        data[12:16]=b'OS/2';struct.pack_into('>II',data,20,28,8);struct.pack_into('>H',data,32,weight)
        return bytes(data)
    def test_actual_embedded_weight_is_available_without_stem_estimation(self):
        for weight in (400,600,700):self.assertEqual(namespace['_font_program_weight'](self.program(weight)),weight)
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
