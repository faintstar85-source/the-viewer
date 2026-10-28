"""The Viewer packaging checks extracted from the user's integrated manager 5.0.1.
No GUI, auto-installer, upload action or library mutation runs on import.
Sample checks are inherited, not a claim that this tool was tested on Windows.
"""
from __future__ import annotations
import ast
import hashlib
import json
import os
import re
import sys
from pathlib import Path

COLLECT_RULES = {
    "ttkbootstrap": [("--collect-all", "ttkbootstrap")],
    "tkinterdnd2": [("--collect-all", "tkinterdnd2")],
    "rapidfuzz": [("--collect-all", "rapidfuzz")],
    "xlwings": [("--collect-all", "xlwings")],
    "selenium": [("--collect-submodules", "selenium")],
    "cv2": [("--collect-all", "cv2")],
    "mediapipe": [("--collect-all", "mediapipe")],
    "easyocr": [("--collect-all", "easyocr")],
    "torch": [("--collect-submodules", "torch")],
    "pypdfium2": [("--collect-all", "pypdfium2"), ("--collect-all", "pypdfium2_raw")],
    "reportlab": [("--collect-all", "reportlab")],
    "openpyxl": [("--collect-submodules", "openpyxl")],
    # hwpx.data is a data-only namespace. Import collection alone does not
    # include its Skeleton.hwpx; the viewer also reads distribution metadata.
    "hwpx": [
        ("--collect-data", "hwpx"),
        ("--copy-metadata", "python-hwpx"),
        ("--hidden-import", "hwpx.data"),
    ],
}


def hwpx_build_requirement(imports: list[str]) -> dict | None:
    """Check the build interpreter and fingerprint the template it can open."""
    if "hwpx" not in imports:
        return None
    try:
        from importlib.metadata import version
        from hwpx import HwpxDocument
        from hwpx.templates import blank_document_bytes
        with HwpxDocument.new():
            pass
        template = blank_document_bytes()
        return {
            "version": version("python-hwpx"),
            "template_sha256": hashlib.sha256(template).hexdigest(),
            "template_bytes": len(template),
        }
    except Exception as exc:
        raise RuntimeError(
            "한글 변환 빌드 환경 검사 실패: 빌드에 사용하는 Python에서 "
            "python-hwpx 모듈·버전 정보·Skeleton.hwpx를 열 수 있어야 합니다.\n"
            f"실행 Python: {sys.executable}\n실제 오류: {type(exc).__name__}: {exc}"
        ) from exc


def validate_hwpx_bundle(artifact: Path, mode: str, requirement: dict | None) -> dict | None:
    """Verify delivered bytes, including inside a onefile CArchive."""
    if requirement is None:
        return None
    from email.parser import BytesParser
    artifact = Path(artifact)
    try:
        if mode == "onedir":
            internal = artifact / "_internal"
            template_name = "hwpx/data/Skeleton.hwpx"
            template = (internal / template_name).read_bytes()
            candidates = sorted(internal.glob("python_hwpx-*.dist-info/METADATA"))
            candidates += sorted(internal.glob("python-hwpx-*.dist-info/METADATA"))
            if len(candidates) != 1:
                raise ValueError("python-hwpx 버전 정보 파일은 정확히 하나 있어야 합니다.")
            metadata = candidates[0].read_bytes()
        elif mode == "onefile":
            from PyInstaller.archive.readers import CArchiveReader
            archive = CArchiveReader(str(artifact))
            names = {name.replace("\\", "/"): name for name in archive.toc}
            template_name = "hwpx/data/Skeleton.hwpx"
            if template_name not in names:
                raise FileNotFoundError("EXE 내부에 hwpx/data/Skeleton.hwpx가 없습니다.")
            template = archive.extract(names[template_name])
            candidates = [name for name in names if name.endswith(".dist-info/METADATA")
                          and name.startswith(("python_hwpx-", "python-hwpx-"))]
            if len(candidates) != 1:
                raise ValueError("EXE 내부 python-hwpx 버전 정보 파일은 정확히 하나 있어야 합니다.")
            metadata = archive.extract(names[candidates[0]])
        else:
            raise ValueError(f"확인할 수 없는 패키징 방식: {mode}")
        if not isinstance(template, bytes) or hashlib.sha256(template).hexdigest() != requirement["template_sha256"]:
            raise ValueError("배포된 Skeleton.hwpx가 빌드 환경의 정상 템플릿과 다릅니다.")
        if not isinstance(metadata, bytes):
            raise ValueError("python-hwpx 버전 정보 파일을 읽을 수 없습니다.")
        info = BytesParser().parsebytes(metadata)
        if re.sub(r"[-_.]+", "-", info.get("Name", "").lower()) != "python-hwpx":
            raise ValueError("배포 정보의 패키지 이름이 python-hwpx와 다릅니다.")
        if info.get("Version") != requirement["version"]:
            raise ValueError("배포된 python-hwpx 버전 정보가 빌드 환경과 다릅니다.")
        return {"status": "verified", "mode": mode, "template": template_name, **requirement}
    except Exception as exc:
        raise RuntimeError(
            "한글 변환 배포 검사 실패: Skeleton.hwpx 또는 python-hwpx 배포 정보가 "
            "누락되거나 손상되었습니다. 이 결과는 완료 처리하지 않습니다.\n"
            f"검사 대상: {artifact}\n실제 오류: {type(exc).__name__}: {exc}"
        ) from exc


VIEWER_RUNTIME_HOOK_SOURCE = r'''"""Restore inherited worker pipes only when Windows GUI mode leaves stdio unset."""
import io
import os
import sys

if sys.platform == 'win32':
    _flags = {'--pdf-worker', '--image-worker', '--input-worker',
              '--hangul-worker', '--image-export-worker', '--vector-worker', '--document-worker', '--print-worker', '--print-job-worker', '--pkpk-viewer-check'}
    _worker = bool(_flags.intersection(sys.argv[1:]))
    for _name, _constant, _read in (('stdin', 'STD_INPUT_HANDLE', True), ('stdout', 'STD_OUTPUT_HANDLE', False), ('stderr', 'STD_ERROR_HANDLE', False)):
        if getattr(sys, _name, None) is not None:
            continue
        _stream = None
        if _worker:
            import _winapi
            import msvcrt
            _duplicate = None
            _fd = None
            try:
                _handle = _winapi.GetStdHandle(getattr(_winapi, _constant))
                if _handle in (None, 0, -1, (1 << 64)-1, (1 << 32)-1):
                    raise OSError('상속된 파이프 핸들이 없습니다.')
                _process = _winapi.GetCurrentProcess()
                _duplicate = _winapi.DuplicateHandle(_process, _handle, _process, 0, False,
                                                    _winapi.DUPLICATE_SAME_ACCESS)
                _fd = msvcrt.open_osfhandle(_duplicate, os.O_BINARY | (os.O_RDONLY if _read else os.O_WRONLY))
                _duplicate = None  # CRT fd now owns this duplicate, not the parent's original.
                _raw = os.fdopen(_fd, 'rb' if _read else 'wb', buffering=0)
                _fd = None
                _stream = io.TextIOWrapper(_raw, encoding='utf-8', errors='replace', write_through=True)
            except Exception as _error:
                if _fd is not None:
                    os.close(_fd)
                if _duplicate is not None:
                    _winapi.CloseHandle(_duplicate)
                if _name != 'stderr':
                    raise RuntimeError('The Viewer 작업 프로세스의 '+_name+' 파이프를 열 수 없습니다.') from _error
        if _stream is None:
            _stream = open(os.devnull, 'r' if _read else 'w', encoding='utf-8')
        setattr(sys, _name, _stream)
'''


VIEWER_CHECK_SOURCE = r'''"""Offline packaging checks; operates only on generated temporary samples."""
import base64
import importlib.util
import io
import json
import os
from pathlib import Path
import ssl
import subprocess
import sys
import tempfile
import time
import traceback
import zipfile

CHECK_SCHEMA = 1


def run_checks(namespace, report_path, nonce):
    from importlib.metadata import version
    report = {
        'schema': CHECK_SCHEMA, 'nonce': nonce, 'ok': False, 'completed': False, 'active_check': None,
        'viewer_version': namespace.get('APP_VERSION'),
        'python': sys.version.split()[0], 'platform': sys.platform,
        'frozen': bool(getattr(sys, 'frozen', False)), 'checks': [], 'versions': {},
        'required_check_count': 14 + int('printing_package_selftest' in namespace) + int('vector_package_selftest' in namespace) + 2*int('document_package_selftest' in namespace) + int('bundled_engines_package_selftest' in namespace) + int('text_package_selftest' in namespace) + int('compare_page_pair' in namespace) + int('editing_ui_package_selftest' in namespace) + int('type3_edit_package_selftest' in namespace) + int('short_text_edit_package_selftest' in namespace),
        'scope': 'generated local samples; no DeepL API request or user settings access',
    }

    def save_report():
        target = Path(report_path)
        temp = target.with_name(target.name + '.tmp')
        temp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        os.replace(temp, target)

    save_report()

    def check(name, action):
        started = time.monotonic()
        report['active_check'] = name
        save_report()
        try:
            details = action()
            report['checks'].append({'name': name, 'status': 'passed', 'details': details,
                                     'seconds': round(time.monotonic() - started, 3)})
        except Exception as exc:
            report['checks'].append({'name': name, 'status': 'failed',
                                     'error': f'{type(exc).__name__}: {exc}',
                                     'traceback': traceback.format_exc()})
        # Keep partial diagnostics even if a later native DLL crashes the process.
        report['active_check'] = None
        save_report()

    def versions():
        names = ['PySide6', 'shiboken6', 'PySide6_Essentials', 'PySide6_Addons',
                 'pypdfium2', 'reportlab', 'pypdf', 'Pillow', 'deepl', 'python-hwpx',
                 'certifi', 'lxml', 'requests', 'cryptography']
        if 'document_package_selftest' in namespace:names.extend(['psd-tools','ezdxf','psutil'])
        if 'compare_page_pair' in namespace:names.extend(['opencv-python-headless','numpy'])
        if sys.platform == 'win32':
            names.append('pywin32')
        for name in names:
            report['versions'][name] = version(name)
        if report['versions']['python-hwpx'] != '6.6.0':
            raise ValueError('현재 The Viewer에는 python-hwpx==6.6.0이 필요합니다.')
        pdfium_minimum=(5,14,0) if any(name in namespace for name in
            ('_viewer_pdf_read_module','_viewer_fast_pdf_worker')) else (5,3,0)
        for name, minimum in [('pypdfium2', pdfium_minimum), ('pypdf', (6,)), ('reportlab', (4,))]:
            actual = tuple(int(n) for n in report['versions'][name].split('.') if n.isdigit())
            if actual < minimum:
                raise ValueError(f'{name} 버전이 부족합니다: {report["versions"][name]}')
        return report['versions'].copy()

    check('모듈 버전 및 배포 정보', versions)
    with tempfile.TemporaryDirectory(prefix='pkpk_viewer_check_') as temp:
        work = Path(temp)
        ctx = {}

        def qt_start():
            from PySide6.QtWidgets import QApplication
            from PySide6.QtGui import QImageReader
            ctx['app'] = QApplication.instance() or QApplication(['pkpk-viewer-check'])
            if sys.platform == 'win32' and ctx['app'].platformName().lower() != 'windows':
                raise RuntimeError('Windows 플랫폼 플러그인이 사용되지 않았습니다.')
            if namespace['application_icon']().isNull():
                raise ValueError('내장 아이콘을 읽지 못했습니다.')
            return {'platform_plugin': ctx['app'].platformName(),
                    'image_formats': sorted(bytes(v).decode('ascii') for v in QImageReader.supportedImageFormats())}

        check('Qt 플랫폼·이미지 플러그인·내장 아이콘', qt_start)
        if 'editing_ui_package_selftest' in namespace:
            check('문서 글꼴 우선순위·편집 버튼·한글/번역 버튼 표시',namespace['editing_ui_package_selftest'])
        if 'short_text_edit_package_selftest' in namespace:
            check('짧은 숫자 선택·입력·원본 굵기',namespace['short_text_edit_package_selftest'])

        def images():
            from PIL import Image
            image = Image.new('RGB', (32, 24), (51, 102, 153))
            for fmt, suffix in [('PNG', '.png'), ('JPEG', '.jpg'), ('WEBP', '.webp'),
                                ('TIFF', '.tiff'), ('BMP', '.bmp')]:
                path = work/('sample'+suffix)
                image.save(path, format=fmt)
                with Image.open(path) as loaded:
                    loaded.load()
                    if loaded.size != (32, 24):
                        raise ValueError(f'{fmt} 읽기 결과 크기가 다릅니다.')
            image.save(work/'multi.tiff', save_all=True, append_images=[image])
            oriented = image.getexif()
            oriented[274] = 6
            image.save(work/'rotated.jpg', exif=oriented)
            with zipfile.ZipFile(work/'book.cbz', 'w') as archive:
                for name in ('10.png', '2.png', '1.png'):
                    archive.writestr(name, (work/'sample.png').read_bytes())
            return ['PNG', 'JPEG', 'WebP', 'TIFF', 'BMP', 'TIFF 2쪽', 'EXIF 방향', 'CBZ']

        check('Pillow 이미지 코덱·샘플 생성', images)

        def decode(engine):
            if 'app' not in ctx:
                raise RuntimeError('Qt 초기화 검사에 먼저 성공해야 합니다.')
            reader = namespace['DirectImageReader']()
            try:
                results = []
                for suffix in ('.png', '.jpg', '.webp', '.tiff', '.bmp'):
                    src = namespace['image_source_path'](work/('sample'+suffix))
                    frame = reader.read(src, 0, (64, 64), engine)
                    if frame[4] != engine or frame[1:3] != (32, 24):
                        raise ValueError(f'{suffix}: {engine} 실패 또는 다른 엔진으로 대체됨: {frame[4:]}')
                    results.append(suffix)
                rotated = reader.read(namespace['image_source_path'](work/'rotated.jpg'), 0, (64, 64), engine)
                if rotated[1:3] != (24, 32) or rotated[4] != engine:
                    raise ValueError('EXIF 회전 또는 지정 엔진 사용 검사 실패')
                return results + ['EXIF 방향 유지']
            finally:
                reader.close()

        for engine, label in [('qt', 'Qt'), ('pillow', 'Pillow')]:
            check(label+' 뷰어 실제 이미지 읽기', lambda engine=engine: decode(engine))

        def pdf_sample():
            import pypdfium2 as pdfium
            from reportlab.pdfgen import canvas
            from pypdf import PdfReader, PdfWriter
            pdf = work/'sample.pdf'
            drawing = canvas.Canvas(str(pdf), pagesize=(595,842))
            drawing.drawString(72,742,'The Viewer packaging check')
            drawing.drawString(72,720,'Editable paragraph and image sample.')
            drawing.drawImage(str(work/'sample.png'),72,644,width=64,height=48)
            drawing.save()
            reader = PdfReader(str(pdf))
            writer = PdfWriter()
            writer.add_page(reader.pages[0])
            with (work/'copy.pdf').open('wb') as output:
                writer.write(output)
            with pdfium.PdfDocument(str(work/'copy.pdf')) as copy:
                if len(copy) != 1:
                    raise ValueError('PDF 저장 후 쪽수 재확인 실패')
                page=copy[0]
                try:
                    textpage=page.get_textpage()
                    try:
                        if 'packaging check' not in textpage.get_text_range():
                            raise ValueError('PDF 텍스트 재확인 실패')
                    finally:textpage.close()
                    bitmap=page.render(scale=1)
                    try:
                        if bitmap.width <= 0 or bitmap.height <= 0:
                            raise ValueError('PDFium 렌더링 실패')
                    finally:bitmap.close()
                finally:page.close()
            namespace['inspect_edit_page'](str(pdf), 0, tables=True, images=True)
            return 'ReportLab 생성·pypdf 저장·PDFium 텍스트/렌더링·편집 정보 읽기'

        check('PDFium·pypdf·ReportLab 및 편집 모듈', pdf_sample)
        if 'type3_edit_package_selftest' in namespace:
            check('Type3 글자 이동·삭제·교체·원본 배치 보존',namespace['type3_edit_package_selftest'])

        def catalog():
            entries = []
            result = namespace['discover_input_pages'](str(work/'book.cbz'), entries.append)
            paths = [item['path'] for batch in entries for item in batch.get('items', [batch]) if 'path' in item]
            members = [namespace['image_source_info'](path)['member'] for path in paths]
            if result['errors'] or members != ['1.png', '2.png', '10.png']:
                raise ValueError(f'CBZ 자연 정렬 실패: {members}, {result}')
            reader = namespace['DirectImageReader']()
            try:
                frame = reader.read(paths[0], 0, (64, 64), 'auto')
                if frame[1:3] != (32, 24):
                    raise ValueError('압축파일 안 이미지 읽기 실패')
                frame = reader.read(namespace['image_source_path'](work/'multi.tiff'), 1, (64, 64), 'pillow')
                if frame[1:3] != (32, 24):
                    raise ValueError('TIFF 두 번째 쪽 읽기 실패')
            finally:
                reader.close()
            return members

        check('ZIP/CBZ·숫자 순서·다중 TIFF', catalog)

        def worker(flag, payload=None, extra=()):
            exe, args = namespace['worker_launch'](flag)
            data = b'' if payload is None else (json.dumps(payload)+'\n').encode('utf-8')
            done = subprocess.run([exe, *args, *map(str, extra)], input=data,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work,
                                  timeout=90, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            if done.returncode:
                raise RuntimeError(f'{flag} 종료 코드 {done.returncode}: '+done.stderr.decode('utf-8', 'replace')[-1800:])
            if not done.stdout:
                raise RuntimeError(f'{flag} 출력 응답이 없습니다. 표준 입출력 또는 작업 프로세스를 확인하세요. ' + done.stderr.decode('utf-8', 'replace')[-1800:])
            return done.stdout

        def json_lines(raw):
            return [json.loads(line) for line in raw.splitlines() if line.startswith(b'{')]

        def pdf_worker():
            fast = '_viewer_fast_pdf_worker' in namespace
            raw = worker('--pdf-worker', {'id': 1, 'op': 'render' if fast else 'thumbnail', 'path': str(work/'sample.pdf'),
                                         'page': 0, 'payload': {'thumb_side': 128}})
            data = json_lines(raw)[-1]
            if not data.get('ok') or not base64.b64decode(data.get('png', '')).startswith(b'\x89PNG'):
                raise ValueError(str(data))
            if not fast and '_viewer_pdf_read_module' not in namespace:
                return '별도 PDF 프로세스에서 썸네일 수신'
            def read_raw(path,reader):
                response=worker('--pdf-worker',{'id':2,'op':'preview','path':str(path),
                    'page':0,'max_side':1000,'payload':{'raw_frame':True}})
                line,separator,pixels=response.partition(b'\n')
                header=json.loads(line)
                if not header.get('ok') or (not fast and header.get('reader')!=reader):
                    raise ValueError('PDF 읽기 경로 검사 실패: '+str(header))
                width,height,stride=header['width'],header['height'],header['stride']
                if stride!=width*3 or len(pixels)!=stride*height or len(pixels)!=header['nbytes']:
                    raise ValueError('PDF RGB 프레임 크기 검사 실패')
                import viewer_pdf_engine
                with viewer_pdf_engine.open(path) as doc:
                    page=doc[0];scale=1000/max(1,page.rect.width,page.rect.height)
                    pix=page.get_pixmap(matrix=viewer_pdf_engine.Matrix(scale,scale),alpha=False)
                    if (width,height)!=(pix.width,pix.height) or pixels!=pix.samples:
                        raise ValueError('PDF 빠른 읽기/양식 호환 경로의 픽셀이 원본 엔진과 다릅니다.')
                return reader
            direct=read_raw(work/'sample.pdf','direct')
            from reportlab.pdfgen import canvas
            form=work/'read-form.pdf';drawing=canvas.Canvas(str(form),pagesize=(595,842))
            drawing.drawString(72,742,'FORM READING CHECK')
            drawing.acroForm.textfield(name='test',value='VISIBLE FORM',x=72,y=640,width=230,height=30)
            drawing.showPage();drawing.save()
            compatible=read_raw(form,'compat')
            if fast:
                search = json_lines(worker('--pdf-worker', {'id':3,'op':'search',
                    'path':str(work/'sample.pdf'),'page':0,'payload':{'query':'packaging'}}))[-1]
                if not search.get('ok') or not search.get('search',{}).get('hits'):
                    raise ValueError('빠른 PDF 작업 프로세스의 검색 응답 검사 실패: '+str(search))
                edit = json_lines(worker('--pdf-worker', {'id':4,'op':'editinfo',
                    'path':str(work/'sample.pdf'),'page':0,'payload':{'tables':True,'images':True}}))[-1]
                if not edit.get('ok') or not isinstance(edit.get('info'),dict):
                    raise ValueError('PDF 편집 호환 코드 검사 실패: '+str(edit))
            return {'png':True,'rgb_readers':[direct,compatible],'pixel_match':True,
                    'fast_search_and_editinfo_checked':fast}

        check('실행파일 PDF 작업 프로세스·파이프 통신', pdf_worker)

        def image_worker():
            raw = worker('--image-worker', {'id': 2, 'op': 'preview',
                'path': namespace['image_source_path'](work/'sample.png'), 'page': 0, 'max_side': 128})
            line, separator, pixels = raw.partition(b'\n')
            data = json.loads(line)
            if not data.get('ok') or data.get('nbytes', 0) != len(pixels) or len(pixels) == 0:
                raise ValueError(str(data))
            return {'width': data['width'], 'height': data['height'], 'engine': data['engine']}

        check('실행파일 그림 작업 프로세스·픽셀 통신', image_worker)

        def input_worker():
            rows = json_lines(worker('--input-worker', {'id': 3, 'path': str(work/'book.cbz')}))
            result = rows[-1]['done']
            if result['errors'] or result['count'] != 3:
                raise ValueError(str(result))
            return '별도 목록 프로세스에서 CBZ 3쪽 확인'

        check('실행파일 ZIP 목록 작업 프로세스', input_worker)

        def image_export():
            target = work/'image-export.pdf'
            rows = json_lines(worker('--image-export-worker', {'inputs': [str(work/'sample.png')], 'stage': str(target)}))
            if not rows[-1].get('ready') or not target.is_file():
                raise ValueError(str(rows[-1]))
            import pypdfium2 as pdfium
            with pdfium.PdfDocument(str(target)) as doc:
                if len(doc) != 1:
                    raise ValueError('그림 → PDF 결과 쪽수 오류')
            return '그림 → PDF 작업 프로세스 및 결과 재열기'

        check('실행파일 JPG to PDF 작업 프로세스', image_export)

        def hangul_worker():
            job = work/'hangul-job.json'
            target = work/'converted.hwpx'
            job.write_text(json.dumps({'pages': [[str(work/'sample.pdf'), 0]], 'output': str(target),
                'mode': 'unified', 'dpi': 144, 'font': '함초롬바탕', 'options': {'write_report': False}}), encoding='utf-8')
            rows = json_lines(worker('--hangul-worker', extra=[job]))
            if not rows or 'result' not in rows[-1]:
                raise ValueError(str(rows[-1:] if rows else '결과 없음'))
            from hwpx import HwpxDocument
            with HwpxDocument.open(target) as doc:
                if not doc.validate().ok:
                    raise ValueError('HWPX 구조 검사 실패')
            return '실제 PDF → HWPX 작업 프로세스·저장·재열기'

        check('실행파일 한글 변환 작업 프로세스', hangul_worker)

        def translation():
            import certifi
            import requests
            pem = Path(certifi.where())
            ssl.create_default_context(cafile=str(pem))
            original = requests.sessions.Session.request
            def offline(*args, **kwargs):
                raise RuntimeError('패키징 검사는 네트워크 요청을 허용하지 않습니다.')
            requests.sessions.Session.request = offline
            try:
                client = namespace['deepl_client']('00000000-0000-0000-0000-000000000000:fx')
                if not callable(getattr(client, 'translate_document', None)):
                    raise ValueError('DeepL 문서 번역 인터페이스가 없습니다.')
                close = getattr(client, 'close', None)
                if close:
                    close()
            finally:
                requests.sessions.Session.request = original
            return 'SDK 초기화·TLS 인증서 확인 (API 요청 없음)'

        check('DeepL SDK·인증서 오프라인 검사', translation)
        if 'text_package_selftest' in namespace:
            check('UTF-8·CP949 텍스트 읽기·편집·왕복 저장', namespace['text_package_selftest'])
        if 'compare_page_pair' in namespace:
            def comparison_sample():
                from PIL import Image, ImageDraw
                from reportlab.pdfgen import canvas
                cv2, np = namespace['comparison_dependencies']()
                first = work/'comparison_original.png'
                second = work/'comparison_changed.png'
                center = (168/320, 128/240)
                with Image.new('RGB', (320,240), 'white') as image:
                    draw = ImageDraw.Draw(image)
                    for row in range(4):
                        for col in range(5):
                            x, y = 16+col*59, 18+row*54
                            draw.rectangle((x,y,x+30,y+28), outline=(35,60,95), width=3)
                            draw.ellipse((x+5,y+4,x+18,y+17), fill=(25+col*20,80+row*25,150))
                    draw.rectangle((158,118,178,138), fill=(220,25,35))
                    image.save(first)
                    draw.rectangle((158,118,178,138), fill=(255,255,255))
                    image.save(second)
                ref = lambda path: {'path':namespace['image_source_path'](path),'number':0}
                a, b = ref(first), ref(second)
                same = namespace['compare_page_pair'](a,a,'image',True)
                if same['total'] or same['status'] != 'no_candidates':
                    raise ValueError('동일 그림을 차이로 판정했습니다: '+str(same))
                rows = json_lines(worker('--compare-worker', {'a':a,'b':b,'mode':'image','auto_align':True}))
                different = rows[-1].get('result',{}) if rows else {}
                hit = any(box['a'][0] <= center[0] <= box['a'][2] and box['a'][1] <= center[1] <= box['a'][3]
                          for box in different.get('candidates',[]))
                if different.get('status') != 'candidates' or not hit:
                    raise ValueError('별도 비교 프로세스가 알려진 변경 위치를 찾지 못했습니다: '+str(different))
                before, after = work/'comparison_before.pdf', work/'comparison_after.pdf'
                for path, text in ((before,'DOCUMENT COLOR ALPHA'),(after,'DOCUMENT COLOR BETA')):
                    drawing=canvas.Canvas(str(path),pagesize=(320,240))
                    drawing.setFont('Helvetica',15)
                    drawing.drawString(35,160,text)
                    drawing.save()
                pdf = namespace['compare_page_pair']({'path':str(before),'number':0},
                    {'path':str(after),'number':0},'document',True)
                if not any(item.get('kind') == 'text' and 'ALPHA' in item.get('before','') and 'BETA' in item.get('after','')
                           for item in pdf['candidates']):
                    raise ValueError('PDF 문자 변경 후보를 찾지 못했습니다: '+str(pdf))
                return {'opencv':cv2.__version__,'numpy':np.__version__,'identical_candidates':same['total'],
                    'changed_image_candidates':different['total'],'known_location_found':hit,
                    'pdf_text_change_found':True,'separate_compare_worker':True}
            check('OpenCV 비교·동일 그림·변경 위치·PDF 문자·작업 프로세스', comparison_sample)
        if 'printing_package_selftest' in namespace:
            check('인쇄 모듈·미리보기·부수·양면 배치', namespace['printing_package_selftest'])
        if 'vector_package_selftest' in namespace:
            check('제외한 DWG·AI·EPS 형식 차단과 폴더 탐색 제외', namespace['vector_package_selftest'])

        if 'document_package_selftest' in namespace:
            check('PSD·DXF PDF 변환·GIF 플러그인',namespace['document_package_selftest'])
            def document_worker():
                from PIL import Image
                from psd_tools import PSDImage
                source=work/'sample.psd'
                with Image.new('RGB',(64,48),(25,140,80)) as picture:PSDImage.frompil(picture).save(source)
                rows=json_lines(worker('--document-worker',{'path':str(source),'directory':str(work/'document_worker')}))
                result=rows[-1].get('result',{}) if rows else {}
                if result.get('error') or result.get('count')!=1:raise ValueError('문서 변환 작업 실패: '+str(rows))
                return '실행파일 PSD PDF 변환·작업 파이프 확인'
            check('실행파일 문서 변환 작업 파이프',document_worker)

        if 'bundled_engines_package_selftest' in namespace:
            if sys.platform=='win32' and getattr(sys,'frozen',False):
                def office_bundle():
                    details=namespace['bundled_engines_package_selftest']()
                    if details.get('not_applicable'):
                        if details.get('excluded_engines_absent') is not True:
                            raise ValueError('제외 엔진 부재 검사에 실패했습니다.')
                        report['office_bundle_included']=False
                    else:report['office_bundle_included']=True
                    return details
                check('Office 동봉 상태·변환 결과·제외 엔진 부재',office_bundle)
                if report['checks'][-1].get('details',{}).get('not_applicable'):
                    report['checks'][-1]['status']='not_applicable'
            else:
                report['checks'].append({'name':'Office 동봉 상태·변환 결과·제외 엔진 부재','status':'not_applicable',
                    'details':'Windows EXE 빌드 후 수행하는 검사입니다. 현재 단계에서는 실행하지 않았습니다.'})

        if sys.platform == 'win32':
            def windows():
                import pythoncom
                import pywintypes
                import win32crypt
                import win32gui
                import win32com.client
                from win32com.shell import shell, shellcon
                from win32com.propsys import propsys, pscon
                payload = b'pkpk16-generated-test-value'
                encoded = win32crypt.CryptProtectData(payload, 'pkpk16 test', None, None, None, 1)
                if win32crypt.CryptUnprotectData(encoded, None, None, None, 1)[1] != payload:
                    raise ValueError('Windows DPAPI 암복호화 검사 실패')
                pythoncom.CoInitialize()
                try:
                    propsys.PROPVARIANTType('pkpk16 test', pythoncom.VT_LPWSTR)
                    if not propsys.IID_IPropertyStore or not pscon.PKEY_AppUserModel_ID:
                        raise ValueError('Windows Shell 속성 인터페이스를 확인할 수 없습니다.')
                finally:
                    pythoncom.CoUninitialize()
                return 'DPAPI 테스트 값 왕복·COM/Shell DLL 로드 (사용자 키 접근 없음)'
            check('Windows pywin32·키 저장·Shell', windows)
        else:
            report['checks'].append({'name': 'Windows pywin32·키 저장·Shell',
                                     'status': 'not_applicable', 'details': 'Windows 빌드 시 수행'})

    report['ok'] = bool(report['checks']) and not any(row['status'] == 'failed' for row in report['checks'])
    report['completed'] = True
    report['active_check'] = None
    save_report()
    return 0 if report['ok'] else 1


def source_main():
    source, report_path, nonce = sys.argv[1:4]
    try:
        spec = importlib.util.spec_from_file_location('_pkpk_viewer_target', source)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return run_checks(vars(module), report_path, nonce)
    except Exception as exc:
        Path(report_path).write_text(json.dumps({'schema': CHECK_SCHEMA, 'nonce': nonce, 'ok': False,
            'checks': [{'name': '뷰어 소스 불러오기', 'status': 'failed',
                        'error': f'{type(exc).__name__}: {exc}', 'traceback': traceback.format_exc()}]},
            ensure_ascii=False, indent=2), encoding='utf-8')
        return 1


if __name__ == '__main__':
    raise SystemExit(source_main())
'''


VIEWER_METADATA = (
    'PySide6', 'PySide6_Essentials', 'PySide6_Addons', 'shiboken6',
    'pypdfium2', 'reportlab', 'pypdf', 'Pillow', 'deepl', 'python-hwpx', 'certifi', 'lxml', 'requests', 'psd-tools', 'ezdxf', 'psutil',
    'opencv-python-headless', 'numpy',
)


VIEWER_CHECK_MODULE = '_pkpk_viewer_checks'


VIEWER_CHECK_FLAG = '--pkpk-viewer-check'


def detect_viewer_profile(main: Path) -> dict | None:
    tree = ast.parse(Path(main).read_text(encoding='utf-8-sig'))
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    constants[target.id] = node.value.value
    if constants.get('APP_NAME') != 'The Viewer (정)' or constants.get('APP_USER_MODEL_ID') != 'KRS.PDFMagnet':
        return None
    return {'name': 'The Viewer (정)', 'version': str(constants.get('APP_VERSION', 'unknown')),
            'checks_schema': 1}


def viewer_collection_options() -> list[tuple[str, str]]:
    """Collect only the implemented PDFium/Qt Widgets/Pillow profile."""
    options = [('--hidden-import', VIEWER_CHECK_MODULE),
               ('--hidden-import','viewer_pdf_engine'),('--hidden-import','viewer_pdf_edit'),
               ('--hidden-import','pypdf'),('--collect-data','certifi'),
               ('--collect-data','psd_tools'),('--collect-data','ezdxf'),
               ('--hidden-import','psutil'),('--hidden-import','PySide6.QtSvg'),
               ('--collect-all','cv2'),('--hidden-import','numpy')]
    options.extend(COLLECT_RULES['pypdfium2'])
    options.extend(COLLECT_RULES['reportlab'])
    options.extend(COLLECT_RULES['hwpx'])
    options.extend(('--copy-metadata', name) for name in VIEWER_METADATA)
    for module in ('PIL.JpegImagePlugin', 'PIL.PngImagePlugin', 'PIL.WebPImagePlugin',
                   'PIL.TiffImagePlugin', 'PIL.BmpImagePlugin', 'PIL.GifImagePlugin', 'PIL.PsdImagePlugin', 'PIL.ImageWin'):
        options.append(('--hidden-import', module))
    if os.name == 'nt':
        options.append(('--copy-metadata', 'pywin32'))
        options.extend(('--hidden-import', name) for name in (
            'win32crypt', 'win32gui', 'pythoncom', 'pywintypes', 'win32com.client', 'win32job','win32process','win32api',
            'win32com.shell.shell', 'win32com.shell.shellcon',
            'win32com.propsys.propsys', 'win32com.propsys.pscon'))
    return list(dict.fromkeys(options))


def prepare_viewer_check(staged_main: Path) -> Path:
    """Inject a private, offline CLI check only into the temporary build copy."""
    source = staged_main.read_text(encoding='utf-8-sig')
    tree = ast.parse(source)
    names = {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    required = {'DirectImageReader', 'image_source_path', 'image_source_info', 'discover_input_pages',
                'inspect_edit_page', 'worker_launch', 'deepl_client', 'application_icon'}
    if not required.issubset(names):
        raise RuntimeError('뷰어 검사 인터페이스가 변경되었습니다. 누락: '+', '.join(sorted(required-names)))
    entry = [node for node in tree.body if isinstance(node, ast.If)
             and isinstance(node.test, ast.Compare)
             and ast.dump(node.test, include_attributes=False) == ast.dump(
                 ast.parse("__name__ == '__main__'", mode='eval').body, include_attributes=False)]
    if len(entry) != 1:
        raise RuntimeError('뷰어의 마지막 실행 진입점을 안전하게 찾을 수 없습니다.')
    helper = staged_main.parent/(VIEWER_CHECK_MODULE+'.py')
    if helper.exists():
        raise RuntimeError('뷰어 검사 보조 파일 이름이 기존 프로젝트와 충돌합니다: '+str(helper))
    injection = (
        "\n# pkpk16: offline checks in the temporary build copy only.\n"
        "if __name__ == '__main__' and len(sys.argv) == 4 and sys.argv[1] == '--pkpk-viewer-check':\n"
        "    from _pkpk_viewer_checks import run_checks as _pkpk_run_checks\n"
        "    raise SystemExit(_pkpk_run_checks(globals(), sys.argv[2], sys.argv[3]))\n\n"
    )
    lines = source.splitlines(keepends=True)
    lines.insert(entry[0].lineno-1, injection)
    result = ''.join(lines)
    compile(result, str(staged_main), 'exec')
    helper.write_text(VIEWER_CHECK_SOURCE, encoding='utf-8')
    staged_main.write_text(result, encoding='utf-8')
    return helper


def verify_viewer_report(path: Path, nonce: str, frozen: bool, returncode: int,
                         expected_versions: dict | None = None) -> dict:
    path = Path(path)
    try:
        result = json.loads(path.read_text(encoding='utf-8-sig'))
        if not isinstance(result, dict):
            raise ValueError('JSON 객체가 아닙니다.')
    except (OSError, ValueError) as exc:
        raise RuntimeError('뷰어 기능 검사 보고서가 없거나 읽을 수 없습니다.\n'
                           + f'실행 종료 코드: {returncode} / {type(exc).__name__}: {exc}'
                           + '\n로그: ' + str(path.with_suffix('.log')) + '\n보고서: ' + str(path)) from exc
    reasons = []
    checks = result.get('checks')
    if not isinstance(checks, list):
        checks = []
        reasons.append('검사 목록 형식이 올바르지 않습니다.')
    failures = [str(row.get('name', '?')) + ': ' + str(row.get('error', row.get('status', '?')))
                for row in checks if isinstance(row, dict) and row.get('status') not in ('passed', 'not_applicable')]
    if any(not isinstance(row, dict) for row in checks): reasons.append('검사 항목 형식 오류')
    if returncode != 0:
        code = f'{returncode} (0x{returncode & 0xffffffff:08X})'
        reasons.append('실행파일 종료 코드: ' + code)
    if result.get('schema') != 1: reasons.append('검사 보고서 형식 버전 불일치')
    if result.get('nonce') != nonce: reasons.append('이번 실행과 보고서 식별값이 다릅니다. 오래된 보고서를 사용할 수 없습니다.')
    if result.get('frozen') is not frozen: reasons.append('소스 검사 / EXE 검사 구분이 다릅니다.')
    required = result.get('required_check_count')
    if required not in range(14, 25) or len(checks) != required:
        reasons.append(f'검사 수 미완료: 기록 {len(checks)}개 / 예정 {required}개')
    if result.get('active_check'): reasons.append('마지막 진행 항목: ' + str(result['active_check']))
    if result.get('completed') is False: reasons.append('전체 검사 완료 기록이 없습니다.')
    if result.get('ok') is not True and not failures: reasons.append('보고서가 성공 상태가 아닙니다.')
    if expected_versions is not None and result.get('versions') != expected_versions:
        actual = result.get('versions') or {}
        if not isinstance(actual, dict): actual = {}
        changes = [f'{name}: 빌드={expected_versions.get(name, "없음")}, EXE={actual.get(name, "없음")}'
                   for name in sorted(set(actual) | set(expected_versions)) if actual.get(name) != expected_versions.get(name)]
        reasons.append('빌드 환경과 EXE의 모듈 버전 불일치: ' + '; '.join(changes))
    if failures or reasons:
        raise RuntimeError('뷰어 기능 검사 실패 · 완료 처리하지 않습니다.\n'
                           + '\n'.join(failures + reasons)
                           + '\n로그: ' + str(path.with_suffix('.log')) + '\n보고서: ' + str(path))
    return result


def viewer_probe_environment(frozen: bool, executable: Path) -> dict[str, str]:
    env = os.environ.copy()
    for name in ('PYTHONPATH', 'PYTHONHOME', 'QT_PLUGIN_PATH', 'QT_QPA_PLATFORM_PLUGIN_PATH',
                 'QML2_IMPORT_PATH', 'QML_IMPORT_PATH', 'VIPS_PATH', 'GI_TYPELIB_PATH'):
        env.pop(name, None)
    env.update(PYTHONUTF8='1', PYTHONUNBUFFERED='1', PYTHONIOENCODING='utf-8')
    if os.name == 'nt':
        env['QT_QPA_PLATFORM'] = 'windows'
        if frozen:
            windows = Path(env.get('SystemRoot', r'C:\Windows'))
            env['PATH'] = os.pathsep.join(map(str, [executable.parent, windows/'System32', windows]))
    elif not env.get('DISPLAY') and not env.get('WAYLAND_DISPLAY'):
        env['QT_QPA_PLATFORM'] = 'offscreen'
    return env
