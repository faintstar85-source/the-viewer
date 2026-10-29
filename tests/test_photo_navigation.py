"""Photo boundaries must never turn into folder/archive imports."""
import ast
import base64
import os
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

SOURCE=Path(__file__).resolve().parents[1]/'pdf_page_dragger.py'
tree=ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
namespace={'Path':Path,'os':os,'re':re,'base64':base64}
constants={'IMAGE_EXTENSIONS','ARCHIVE_EXTENSIONS','TEXT_EXTENSIONS','IMAGE_SOURCE_PREFIX'}
functions={'natural_path_key','neighboring_inputs','is_image_source','image_source_info'}
body=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name in functions) or
      (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in constants for t in n.targets))]
exec(compile(ast.Module(body=body,type_ignores=[]),str(SOURCE),'exec'),namespace)
namespace['INPUT_EXTENSIONS']=namespace['IMAGE_EXTENSIONS']|namespace['TEXT_EXTENSIONS']|{'.pdf','.zip','.cbz'}
namespace['QApplication']=SimpleNamespace(activeModalWidget=lambda:None)
for clsname,names in {
    'Window':{'navigation_origin','navigation_context','navigation_context_key','can_browse_photo_files','navigate_sibling','got_sibling'},
    'PreviewDialog':{'request_navigation'},
}.items():
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==clsname)
    for method in cls.body:
        if isinstance(method,ast.FunctionDef) and method.name in names:
            exec(compile(ast.Module(body=[method],type_ignores=[]),str(SOURCE),'exec'),namespace)


def bind(obj,*names):
    for name in names:setattr(obj,name,namespace[name].__get__(obj))
    return obj


class PhotoNavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.folder=self.root/'인천세관';self.folder.mkdir()
        for name in ('1.JPG','2.png','10.JPEG','3.zip','4.cbz','5.pdf','6.txt'):
            (self.folder/name).write_bytes(b'not read during directory navigation')
        (self.folder/'7').mkdir();(self.folder/'7'/'8.jpg').touch()
        (self.root/'인천세관.zip').touch()

    def owner(self,name='2.png'):
        photo=SimpleNamespace(input_path=str(self.folder/name),path='unused',uid='photo')
        owner=SimpleNamespace(pages=[photo],preview_dialog=SimpleNamespace(closed=False,page=photo),
            browse_path=None,browse_containers=False,browse_books=None,pending_import=None,
            dual_mode=False,book_mode=False,imports=[],import_cancelling=False,
            closing=False,clear_pending=False,navigation_request=None,navigation_token=0,
            neighbor_ready=False,neighbor_error='',neighbor_key=None,neighbor_paths={},
            show_navigation_notice=Mock(),replace_inputs=Mock(),update_action_states=Mock(),
            navigation_backend=SimpleNamespace(request=Mock()))
        return bind(owner,'navigation_origin','navigation_context','navigation_context_key',
                    'can_browse_photo_files','navigate_sibling','got_sibling')

    def test_mixed_folder_uses_only_photos_in_natural_order(self):
        for containers in (False,True):
            for name,previous,next_ in [('1.JPG','','2.png'),('2.png','1.JPG','10.JPEG'),('10.JPEG','2.png','')]:
                actual=namespace['neighboring_inputs'](str(self.folder/name),containers)
                self.assertEqual({k:Path(v).name if v else '' for k,v in actual.items()},
                                 {'previous':previous,'next':next_})

    def test_one_photo_does_not_escape_to_sibling_folder_or_zip(self):
        only=self.root/'single';only.mkdir();photo=only/'only.jpg';photo.touch()
        (only/'archive.zip').touch();(only/'document.pdf').touch()
        for containers in (False,True):
            self.assertEqual(namespace['neighboring_inputs'](str(photo),containers),{'previous':'','next':''})

    def test_stale_book_context_does_not_redirect_a_photo(self):
        result=namespace['neighboring_inputs'](str(self.folder/'2.png'),True,
                    {'root':str(self.root),'paths':[str(self.root/'인천세관.zip')]})
        self.assertEqual(Path(result['next']).name,'10.JPEG')

    def test_archive_library_still_uses_its_own_order(self):
        paths=[self.folder/'3.zip',self.folder/'4.cbz']
        result=namespace['neighboring_inputs'](str(paths[0]),True,{'root':str(self.root),'paths':list(map(str,paths))})
        self.assertEqual(result,{'previous':'','next':str(paths[1])})

    def test_missing_photo_is_not_silently_replaced(self):
        with self.assertRaises(ValueError):namespace['neighboring_inputs'](str(self.folder/'missing.jpg'))

    def test_origin_is_photo_itself(self):
        owner=self.owner()
        self.assertEqual(owner.navigation_context(),(str(self.folder/'2.png'),False,None))
        self.assertTrue(owner.can_browse_photo_files())
        owner.dual_mode=True;self.assertFalse(owner.can_browse_photo_files())
        owner.dual_mode=False;owner.pages.append(owner.pages[0]);self.assertFalse(owner.can_browse_photo_files())

    def test_uncached_navigation_requests_photo_and_boundary_keeps_it_open(self):
        owner=self.owner();owner.navigate_sibling(1)
        args=owner.navigation_backend.request.call_args
        self.assertEqual(args.args,('sibling',str(self.folder/'2.png')))
        self.assertFalse(args.kwargs['payload']['include_containers'])
        owner.got_sibling(owner.navigation_token,'','')
        owner.replace_inputs.assert_not_called()
        owner.show_navigation_notice.assert_called_once_with('더 이상 읽을 파일이 없습니다.')

    def test_cached_boundary_and_valid_photo(self):
        owner=self.owner();owner.neighbor_ready=True;owner.neighbor_key=owner.navigation_context_key()
        owner.navigate_sibling(-1)
        owner.replace_inputs.assert_not_called();owner.show_navigation_notice.assert_called_once()
        owner.neighbor_paths={'next':str(self.folder/'10.JPEG')};owner.navigate_sibling(1)
        owner.replace_inputs.assert_called_once_with([str(self.folder/'10.JPEG')],navigation_mode=False,navigation_books=None)

    def test_stale_worker_result_cannot_replace_newly_opened_photo(self):
        owner=self.owner();owner.navigate_sibling(1);token=owner.navigation_token
        owner.preview_dialog.page.input_path=str(self.folder/'1.JPG')
        owner.got_sibling(token,str(self.folder/'10.JPEG'),'')
        owner.replace_inputs.assert_not_called()

    def test_arrows_route_single_photo_but_scrubbing_stays_inside(self):
        owner=self.owner();owner.navigate_sibling=Mock();owner.page_number_session=None
        editor=SimpleNamespace(owner=owner,closed=False,dual_secondary=False,mode='pan',
            navigation_pages=lambda:owner.pages,page=owner.pages[0])
        for index,direction in [(-1,-1),(1,1)]:
            namespace['request_navigation'](editor,index)
            owner.navigate_sibling.assert_called_with(direction)
        owner.navigate_sibling.reset_mock()
        namespace['request_navigation'](editor,1,scrub=True)
        owner.navigate_sibling.assert_not_called()


if __name__=='__main__':unittest.main()
