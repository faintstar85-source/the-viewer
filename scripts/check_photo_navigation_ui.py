"""Run with QT_QPA_PLATFORM=offscreen on Linux; uses temporary settings and generated photos."""
import sys,tempfile,time,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pdf_page_dragger as v
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt,QSettings
from PySide6.QtWidgets import QApplication
from PIL import Image
app=QApplication([]);app.setStyle('Fusion')
with tempfile.TemporaryDirectory() as folder:
    root=Path(folder);QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(QSettings.Format.IniFormat,QSettings.Scope.UserScope,str(root/'settings'))
    photos=root/'인천세관';photos.mkdir()
    for name,color in [('1.JPG','red'),('2.png','green'),('10.JPEG','blue')]:
        Image.new('RGB',(800,600),color).save(photos/name)
    for p in [photos/'3.zip',photos/'4.cbz',photos/'5.pdf',photos/'6.txt',root/'인천세관.zip']:
        p.write_bytes(b'invalid - must not be opened by photo navigation')
    (photos/'7').mkdir()
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in photos.iterdir() if p.is_file()}
    window=v.Window(startup_pdf_count=1);window.show();errors=[]
    window.show_import_errors=lambda msgs:errors.extend(msgs)
    def wait(condition,label,seconds=20):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            app.processEvents();QTest.qWait(20)
            modal=QApplication.activeModalWidget()
            if modal is not None:raise AssertionError(f'unexpected modal during {label}: {modal.windowTitle()}')
            if errors:raise AssertionError(errors)
            if condition():return
        raise AssertionError(f'timeout {label}')
    def ready(name):
        e=window.preview_dialog
        return e is not None and not e.closed and Path(window.navigation_origin()).name==name and not window.pending_import and not window.imports and e.view.item is not None
    def arrow(direction):
        e=window.preview_dialog
        assert e.end_overlay.isHidden()
        QTest.mouseClick(e.nav_next if direction>0 else e.nav_previous,Qt.MouseButton.LeftButton)
    try:
        window.add_files([str(photos/'2.png')]);wait(lambda:ready('2.png'),'open photo')
        arrow(1);wait(lambda:ready('10.JPEG'),'next photo')
        uid=window.preview_dialog.page.uid
        arrow(1);wait(lambda:window.navigation_request is None and window.preview_dialog.navigation_notice.isVisible(),'last notice')
        assert window.preview_dialog.page.uid==uid
        notice=window.preview_dialog.navigation_notice
        assert notice.text()=='더 이상 읽을 파일이 없습니다.'
        wait(notice.isHidden,'notice auto hide',4)
        arrow(-1);wait(lambda:ready('2.png'),'previous photo')
        arrow(-1);wait(lambda:ready('1.JPG'),'first photo')
        uid=window.preview_dialog.page.uid
        arrow(-1);wait(lambda:window.navigation_request is None and window.preview_dialog.navigation_notice.isVisible(),'first notice')
        assert window.preview_dialog.page.uid==uid
        # Explicitly populated cached neighbors follow the same route.
        window.request_neighbor_names();wait(lambda:window.neighbor_ready,'cached neighbors')
        arrow(1);wait(lambda:ready('2.png'),'cached next arrow')
        # Left/right shortcuts must use the same page-navigation path.
        window.preview_dialog.view.setFocus()
        QTest.keyClick(window.preview_dialog.view,Qt.Key.Key_Right)
        wait(lambda:ready('10.JPEG'),'keyboard right')
        # A folder of pictures stays in its loaded sequence and shows no panel.
        only=root/'only';only.mkdir();Image.new('RGB',(200,100),'yellow').save(only/'only.jpg')
        (only/'bad.zip').write_bytes(b'bad')
        window.replace_inputs([str(only/'only.jpg')]);wait(lambda:ready('only.jpg'),'single photo folder')
        arrow(1);wait(lambda:window.navigation_request is None and window.preview_dialog.navigation_notice.isVisible(),'only photo notice')
        assert ready('only.jpg')
        assert hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in photos.iterdir() if p.is_file()}
        print(json.dumps({'actual_arrow_clicks':True,'cached_arrow_click':True,'keyboard_right':True,
          'first_last_and_single_photo_keep_current':True,'modal_errors':errors,'original_files_unchanged':True},ensure_ascii=False))
    finally:
        window.close();app.processEvents()
