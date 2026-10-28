"""Font matching regressions; no GUI dependency is needed for static CI."""
import ast
from pathlib import Path
import re
import unittest

SOURCE=Path(__file__).resolve().parents[1]/'pdf_page_dragger.py'
NAMES={'font_family_key','installed_font_family','prioritized_font_families'}
tree=ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
namespace={'re':re}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in NAMES],type_ignores=[]),str(SOURCE),'exec'),namespace)


class TestDocumentFontChoices(unittest.TestCase):
    families=('Arial','Batang','Malgun Gothic','Noto Sans KR','Times New Roman')
    def test_pdf_subset_names_and_korean_aliases_match_installed_family(self):
        for name,expected in [('ABCDEF+MalgunGothicBold','Malgun Gothic'),('맑은고딕','Malgun Gothic'),
                              ('Arial-BoldMT','Arial'),('TimesNewRomanPSMT','Times New Roman'),
                              ('NotoSansKR-Regular','Noto Sans KR')]:
            with self.subTest(name=name):self.assertEqual(namespace['installed_font_family'](name,self.families),expected)
    def test_document_font_precedes_malgun_and_all_fonts_remain_available(self):
        result=namespace['prioritized_font_families'](('ABCDEF+Batang','Batang'),self.families)
        self.assertEqual(result[:2],('Batang','Malgun Gothic'))
        self.assertCountEqual(result,self.families)
    def test_missing_original_font_is_not_mislabeled_as_installed(self):
        self.assertEqual(namespace['installed_font_family']('UnknownEmbeddedFont',self.families),'')
        result=namespace['prioritized_font_families'](('UnknownEmbeddedFont',),self.families)
        self.assertEqual(result[0],'Malgun Gothic');self.assertCountEqual(result,self.families)


if __name__=='__main__':unittest.main()
