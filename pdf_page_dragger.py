"""The Viewer (정) 3.6.1 — 한글 모듈 진단 · 폴더 속 ZIP 책 탐색 · 화살표 옆 고정 안내.
설치 (Windows): python -m pip install -U PySide6 "pymupdf>=1.26.6" "pypdf>=5" pywin32 deepl Pillow
그림 추가 설치만: python -m pip install -U Pillow
libvips 추가 설치(선택): python -m pip install "pyvips[binary]"
자동 보기: JPG·WebP·BMP는 Qt 우선, PNG·TIFF는 libvips 우선. 불가하면 다른 엔진/Pillow로 읽습니다.
정 → 기본 → 그림 읽기 엔진: 자동 / Qt 우선 / libvips 우선 / Pillow 호환.
화면 전송은 PNG 재압축 없이 픽셀로 전달합니다. 원본 화질·파일은 변경하지 않습니다.
사진 처리기는 파일을 바꿔도 재사용합니다. 준비된 썸네일을 먼저 표시한 뒤 화면 크기에 맞게 원본을 읽습니다.
그림 확대: 배율·화면 배율에 맞춰 원본을 다시 읽습니다. 긴 변 16,384px·전체 2,500만 픽셀 이내.
6,000×4,000 사진은 원본 크기까지 표시. 제한을 넘는 그림은 비율 유지 축소, 원본보다 큰 확대는 보간합니다.
그림은 원본에서 직접 표시합니다. ZIP/CBZ도 전체 압축 해제나 보기용 PDF를 만들지 않습니다.
하단 진행률은 목록 확인 기준입니다. 그림 디코딩은 보이는 쪽부터 진행하고 메모리 캐시를 제한합니다.
원본 그림/압축파일은 보기를 마칠 때까지 이동·삭제하지 마세요. 편집/저장할 때 필요한 쪽만 PDF로 변환합니다.
정 → 기본의 붉은 [JPG to PDF]: 현재 그림 또는 파일/폴더를 PDF로 변환 (%·취소 지원).
목록 확인 중에는 전체 수를 계산합니다. [+]는 읽기를 중단한 뒤 저장 확인과 전체 비우기를 수행합니다.
편집용 임시 PDF는 사용하는 동안 유지, 미사용 파일은 취소·비우기·정상 종료 때 정리합니다.
외부 붙여넣기/드래그용 사본은 전달을 위해 유지합니다. 정 → 기본에서 임시 폴더를 열 수 있습니다.
PDF/JPG/JPEG/PNG/WebP/TIF/TIFF/BMP, 폴더(하위 폴더 포함), ZIP/CBZ를 드롭하세요.
숫자순 정렬 · TIFF 각 쪽 분리 · EXIF 방향/비율 유지 · 원본/압축파일은 변경하지 않습니다.
폴더 안 PDF는 첫 장 카드 하나로 표시(겹친 종이 + 전체 쪽수). 더블클릭하면 그 PDF 전체를 엽니다.
PDF 파일을 직접 열면 모든 쪽을 표시합니다. 폴더 PDF 카드의 저장·복사·변환에는 뒷장도 포함됩니다.
폴더 PDF 카드의 글/그림 편집은 더블클릭으로 전체 PDF를 연 뒤 수행하세요.
붉은 PDF 블록 뒤 파랑·초록 사진 카드 아이콘을 내장했습니다. 별도 아이콘 파일 없이 적용합니다.
기본은 왼쪽 크게 보기 + 오른쪽 썸네일. 파일을 넣기 전에는 썸네일 비활성, 1쪽부터 함께 표시.
맨 오른쪽 테두리의 <<: 썸네일 접기 / +: 펼치기. 선택·편집 상태와 분할 비율은 유지합니다.
크게 보기에 드롭: 새로 열기(미저장 수정 확인). 썸네일에 드롭: 지정한 위치에 추가 / 순서 변경.
쉼표(,) / 마침표(.), 또는 [ / ]: 같은 폴더의 이전 / 다음 파일. 일반 PDF·그림으로 시작하면 PDF·그림만 이동.
폴더·ZIP/CBZ를 직접 열어 시작한 경우에만 같은 단계의 폴더·압축파일도 이동 대상으로 포함합니다. 끝에서 멈춤.
다음 쪽: → / Space / PgDown / 휠 아래. 이전 쪽: ← / Backspace / PgUp / 휠 위.
크게 보기의 확대: ↑, 축소: ↓. 정 → 단축키에서 키와 휠 위/아래를 변경·저장합니다.
휠 단축키는 크게 보기에 적용됩니다. 썸네일 영역에서는 기존처럼 목록을 스크롤합니다.
ZIP·폴더의 마지막 페이지: 반투명 이전/다음 항목 버튼과 현재 단축키 표시. 클릭 또는 파일 이동 키로 이동.
첫 페이지에서 이전 쪽으로 더 이동하려 해도 같은 안내가 표시됩니다. 다른 페이지로 이동하면 사라집니다.
안내창은 오른쪽 화살표 바로 왼쪽 위에 고정되며 이전/다음 ZIP·폴더의 실제 이름을 표시합니다.
ZIP·CBZ가 있는 폴더: 이름순 첫 압축파일 한 권만 열고 [, ] / , . 키로 폴더 안의 책을 이동합니다.
하위 폴더의 압축파일도 폴더 안 책 목록에 포함합니다. 다른 책은 선택하기 전까지 내용을 읽지 않습니다.
탐색기에서 파일을 드롭하면 뷰어가 키 입력을 받습니다. 첫 ZIP도 별도 클릭 없이 페이지 이동.
문자 입력과 편집 개체의 방향키 정밀 이동을 우선합니다. Esc·Enter·Tab은 고정 동작입니다.
PDF 테두리: 붉은색. 그림 테두리: 파랑~초록. 선택한 테두리는 더 굵고 밝게 표시.
경계 드래그: 보기 비율 조절. Esc: 편집/탐색 취소. OCR은 이 버전에 포함되지 않습니다.
한글 변환 추가 설치: py -m pip install "python-hwpx==6.6.0"
정 → 한글 변환 → 모듈 확인: 실제 실행 Python·모듈 버전과 불러오기 오류 확인.
한글 모듈 오류창: 현재 실행 환경의 설치 명령 / 진단 정보를 복사합니다.
번–한글–정: 한글 통합 변환 (본문 글상자 없음, 문단/표/머리말/쪽 테두리)
정 → 한글 변환: 양식·쪽 나눔 보존, 문서 전체 서식, 분석 기준, 쪽별 검사표
복잡한 흐름도·그림 글자는 부분 그림으로 남습니다. 스캔에는 먼저 OCR이 필요합니다.
실행: py pdf_page_dragger.py
Ctrl/Shift: 선택 | Ctrl+A: 전체 | Ctrl+Z/Y: 되돌리기/다시 실행 | Delete: 작업목록에서 제외
확대창 우클릭: 글/그림 편집 · 문자추가 · 흰색 덮기 | Ctrl+V: 캡처/그림/문자 붙여넣기
진한 빨간 테두리 선택 후 Del: 삭제 | 양쪽 화살표: 한 장 이동, 잡고 위/아래: 연속 탐색
약 2cm 안에서는 한 장씩, 더 당기면 가속(주황→붉은 테두리). 제자리 유지: 계속 이동, 우클릭/Esc: 취소.
확대창 하단: 현재 쪽 / 전체 장수. 목록 하단: 전체 장수. 모니터가 보고한 DPI로 약 2cm를 계산합니다.
방향키 이동: 0.5mm, Ctrl 0.1mm, Shift 5mm | 가로 페이지 점선은 화면 가이드(저장 제외)
그림: 드래그 이동, 모서리 크기(Shift 자유 비율), 더블클릭 위치·크기·교체, Del 삭제
그림 선택 후 Ctrl+C 복사 / Ctrl+X 잘라내기 / Ctrl+V 붙여넣기 (우클릭 메뉴 지원)
그림 편집 대상은 비트맵 이미지입니다. 스캔의 내부 사물·벡터 도형은 개별 분리하지 않습니다.
Ctrl+S: 처음 연 파일 이름-정(번호).pdf로 전체 저장 | Ctrl+O: 옵션 | Ctrl+Shift+O: 파일 추가
[+] / Ctrl+N: 전체 비우기 (미저장 수정이 있으면 저장·비우기·취소 선택)
Ctrl+T / 번: 확인 후 현재 전체 페이지를 한국어로 번역 → 원본이름-(번역).pdf
정 → 번역: DeepL API 키·저장 위치·연결 확인. PDF 번역은 DeepL API 사용량을 소비합니다.
Ctrl 누르기: 저장(S)/번역(T)/한글(H)/옵션(O) 표시 | 목록 휠: 빠르게, Ctrl+휠: 정밀 이동
정 → 기본 → 바탕화면 아이콘 만들기: 'The Viewer (정)' 실행 바로가기 생성
시작 화면의 [ + ]: PDF·그림·폴더·ZIP/CBZ 드롭 또는 더블클릭으로 열기.
정 옵션 맨 아래: 버전 / 도네이션. 도네이션을 누르면 내장된 후원 QR을 표시합니다.
정 → 소식: 블로그 / GitHub 코드·업데이트·오류 제보. GitHub 저장소 주소를 등록해 사용합니다.
썸네일 Ctrl+C/V: 페이지 복사/붙여넣기 | 우클릭: 빈 페이지
원본 PDF는 변경하지 않습니다. 바깥 드롭 후 이름 변경은 Windows 탐색기/바탕화면용입니다.
참고: https://pymupdf.readthedocs.io/en/latest/recipes-multiprocessing.html
      https://doc.qt.io/qtforpython-6/PySide6/QtGui/QDrag.html
"""
import sys
import os
import json
import math
import uuid
import base64
import hashlib
import tempfile
import html
import time
import io
import re
from pathlib import Path
from dataclasses import dataclass, field
from collections import OrderedDict
from contextlib import contextmanager

APP_NAME = 'The Viewer (정)'
APP_VERSION = '3.6.1'
BLOG_URL = 'https://blog.naver.com/faintstar'
# GitHub 도우미가 업로드용 사본에 실제 저장소 주소를 넣는다.
PROJECT_GITHUB_URL = 'https://github.com/faintstar85-source/the-viewer'
# 기존 작업 표시줄 연결, 기본 앱 등록 및 사용자 설정과의 호환성을 유지한다.
APP_USER_MODEL_ID = 'KRS.PDFMagnet'

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.bmp'}
ARCHIVE_EXTENSIONS = {'.zip', '.cbz'}
INPUT_EXTENSIONS = IMAGE_EXTENSIONS | ARCHIVE_EXTENSIONS | {'.pdf'}
IMAGE_SOURCE_PREFIX='krsimg:'
# 긴 사진을 무조건 5,000px로 줄이지 않되, 한 화면의 최대 RGB 메모리 양은 유지한다.
IMAGE_PREVIEW_MAX_SIDE=16384
IMAGE_PREVIEW_MAX_PIXELS=25_000_000
IMAGE_FRAME_MAX_BYTES=IMAGE_PREVIEW_MAX_PIXELS*3+IMAGE_PREVIEW_MAX_SIDE*3


def is_image_source(path):
    return str(path).startswith(IMAGE_SOURCE_PREFIX)


def image_source_path(path,member=None,index=None,info=None):
    if info is None:
        path=Path(path).resolve();stat=path.stat()
        value={'file':str(path),'stamp':[stat.st_size,stat.st_mtime_ns]}
    else:value=dict(info)
    if member is not None:value.update(member=member,index=index)
    return IMAGE_SOURCE_PREFIX+base64.urlsafe_b64encode(json.dumps(value,ensure_ascii=True).encode()).decode()


def image_source_info(path):
    if not is_image_source(path):raise ValueError('그림 원본 정보가 없습니다.')
    return json.loads(base64.urlsafe_b64decode(path[len(IMAGE_SOURCE_PREFIX):]))


def validate_image_source(path):
    value=image_source_info(path);source=Path(value['file']);stat=source.stat()
    if [stat.st_size,stat.st_mtime_ns]!=value['stamp']:
        raise ValueError('원본 파일이 변경되었습니다. 파일을 다시 열어주세요.')
    return value,source


def pillow_reader():
    try:
        from PIL import Image,ImageOps
        return Image,ImageOps
    except ImportError:
        raise ValueError('그림 읽기 모듈을 설치하세요.\npython -m pip install -U Pillow') from None


@contextmanager
def open_image_stream(path,archives=None):
    """Read a validated original or a ZIP member without extracting to disk."""
    import zipfile
    value,source=validate_image_source(path)
    archive=None;own_archive=False;stream=None
    try:
        if 'member' in value:
            cache_key=(str(source),*value['stamp'])
            archive=archives.get(cache_key) if archives is not None else None
            if archive is None:
                archive=zipfile.ZipFile(source)
                if archives is not None:
                    archives[cache_key]=archive
                    while len(archives)>2:archives.popitem(last=False)[1].close()
                else:own_archive=True
            elif archives is not None:archives.move_to_end(cache_key)
            member=archive.infolist()[value['index']]
            if member.filename!=value['member']:raise ValueError('압축파일의 그림 목록이 변경되었습니다.')
            if member.flag_bits&1:raise ValueError('암호가 설정된 그림은 먼저 압축을 풀어주세요.')
            if member.file_size>256*1024*1024:raise ValueError('그림 한 파일이 256MB를 초과합니다.')
            stream=archive.open(member)
        else:stream=source.open('rb')
        yield stream
    finally:
        if stream is not None:stream.close()
        if archive is not None and own_archive:archive.close()


@contextmanager
def open_image_source(path,number=0,archives=None):
    import warnings
    Image,_=pillow_reader()
    with open_image_stream(path,archives) as stream, warnings.catch_warnings():
        warnings.simplefilter('error',Image.DecompressionBombWarning)
        with Image.open(stream) as picture:
            picture.seek(int(number))
            yield picture,stream


def image_page_size(picture):
    dpi=picture.info.get('dpi',(96,96))
    try:dpi=float(dpi[0] if isinstance(dpi,(tuple,list)) else dpi)
    except (TypeError,ValueError,IndexError):dpi=96
    if not math.isfinite(dpi) or not 20<=dpi<=2400:dpi=96
    width,height=picture.size
    # TIFF decoder updates orientation while loading; get geometry afterwards for TIFF.
    if picture.getexif().get(274,1) in (5,6,7,8):width,height=height,width
    w,h=width*72/dpi,height*72/dpi
    scale=min(max(1,1/min(w,h)),14400/max(w,h))
    return w*scale,h*scale


def image_page_document(path,number=0):
    """Convert one requested frame only, for editing/export. Caller closes the PDF."""
    import pymupdf
    _,ImageOps=pillow_reader()
    doc=pymupdf.open()
    try:
        with open_image_source(path,number) as (picture,stream):
            orientation=picture.getexif().get(274,1)
            picture.load()
            width,height=image_page_size(picture)
            page=doc.new_page(width=width,height=height)
            if picture.format=='JPEG' and orientation==1:
                stream.seek(0);page.insert_image(page.rect,stream=stream.read())
            else:
                with ImageOps.exif_transpose(picture) as normalized:
                    mode='RGBA' if 'A' in normalized.getbands() or 'transparency' in normalized.info else 'RGB'
                    with normalized.convert(mode) as bitmap:
                        data=io.BytesIO();bitmap.save(data,format='PNG')
                    page.insert_image(page.rect,stream=data.getvalue())
        return doc
    except Exception:
        doc.close();raise


def render_image_source(path,number,bounds,archives=None):
    Image,ImageOps=pillow_reader()
    with open_image_source(path,number,archives) as (picture,_stream):
        # thumbnail uses JPEG decoder reduction before resizing; never decode into a PDF.
        rotated=picture.getexif().get(274,1) in (5,6,7,8)
        if picture.format=='TIFF':picture.load();rotated=picture.getexif().get(274,1) in (5,6,7,8)
        picture.thumbnail(tuple(reversed(bounds)) if rotated else bounds,Image.Resampling.LANCZOS,reducing_gap=2.0)
        with ImageOps.exif_transpose(picture) as normalized:
            with normalized.convert('RGBA') as rgba:
                with Image.new('RGB',rgba.size,'white') as canvas:
                    canvas.paste(rgba,mask=rgba.getchannel('A'))
                    data=io.BytesIO();canvas.save(data,format='PNG',compress_level=1)
                    return data.getvalue()


class DirectImageReader:
    """Native decoders, bounded ZIP-member/frame caches, no intermediate image/PDF."""
    MEMBER_LIMIT=32*1024*1024
    FRAME_LIMIT=48*1024*1024

    def __init__(self):
        from PySide6.QtCore import QCoreApplication
        self.app=QCoreApplication.instance() or QCoreApplication([])
        self.archives=OrderedDict();self.members=OrderedDict();self.frames=OrderedDict()
        self.member_bytes=0;self.frame_bytes=0;self.vips=None;self.vips_checked=False;self.vips_error=''

    def close(self):
        for archive in self.archives.values():archive.close()
        self.archives.clear();self.members.clear();self.frames.clear()
        self.member_bytes=self.frame_bytes=0

    def source(self,path,validated=None):
        value,source=validated if validated is not None else validate_image_source(path)
        if 'member' not in value:return str(source),None
        data=self.members.pop(path,None)
        if data is not None:self.members[path]=data;return None,data
        # Decompress this member once. Native decoders may seek many times;
        # a QBuffer / vips buffer avoids repeatedly inflating a ZipExtFile.
        with open_image_stream(path,self.archives) as stream:data=stream.read(256*1024*1024+1)
        if len(data)>256*1024*1024:raise ValueError('그림 한 파일이 256MB를 초과합니다.')
        if len(data)<=self.MEMBER_LIMIT:
            self.members[path]=data;self.member_bytes+=len(data)
            while self.member_bytes>self.MEMBER_LIMIT:self.member_bytes-=len(self.members.popitem(last=False)[1])
        return None,data

    def image_format(self,filename,data,number):
        # Header/frame validation retains the existing Pillow pixel-limit policy.
        import warnings
        Image,_=pillow_reader()
        with warnings.catch_warnings():
            warnings.simplefilter('error',Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data) if data is not None else filename) as picture:
                picture.seek(number)
                if picture.width<=0 or picture.height<=0:raise ValueError('그림 크기를 읽지 못했습니다.')
                # Pillow PNG.getexif() can force a full pixel decode. Keep header
                # inspection lazy; Qt's fallback scans late eXIf chunks without decoding.
                if picture.format=='PNG':
                    raw=picture.info.get('exif')
                    if raw:
                        exif=Image.Exif();exif.load(raw);orientation=exif.get(274,1)
                    else:orientation=None
                else:orientation=picture.getexif().get(274,1)
                # Pillow TIFF는 load 전 size에도 회전을 반영할 수 있어 원시 태그 크기를 쓴다.
                size=(int(picture.tag_v2.get(256,picture.width)),int(picture.tag_v2.get(257,picture.height))) if picture.format=='TIFF' else picture.size
                return picture.format,orientation,size

    def png_orientation(self,filename,data):
        import struct
        Image,_=pillow_reader()
        with io.BytesIO(data) if data is not None else open(filename,'rb') as stream:
            if stream.read(8)!=b'\x89PNG\r\n\x1a\n':return 1
            while True:
                header=stream.read(8)
                if len(header)!=8:return 1
                size,kind=struct.unpack('>I4s',header)
                if kind==b'IEND':return 1
                if kind==b'eXIf':
                    if size>16*1024*1024:raise ValueError('PNG EXIF 메타데이터가 너무 큽니다.')
                    exif=Image.Exif();exif.load(stream.read(size));return exif.get(274,1)
                stream.seek(size+4,1)

    def load_vips(self):
        if not self.vips_checked:
            self.vips_checked=True
            os.environ.setdefault('VIPS_CONCURRENCY',str(min(4,os.cpu_count() or 1)))
            try:
                import pyvips
                pyvips.cache_set_max(0)
                self.vips=pyvips
            except Exception as exc:self.vips_error=str(exc)
        if self.vips is None:
            raise ValueError('libvips 사용 불가 · python -m pip install "pyvips[binary]"')
        return self.vips

    def read_vips(self,filename,data,number,bounds,fmt,orientation=1):
        vips=self.load_vips();options=f'page={number},n=1' if fmt=='TIFF' else ''
        manual=fmt=='PNG'
        if manual and orientation is None:orientation=self.png_orientation(filename,data)
        target=tuple(reversed(bounds)) if manual and orientation in (5,6,7,8) else bounds
        kwargs=dict(height=target[1],size='down',no_rotate=manual,fail_on='error',output_profile='srgb')
        if data is not None:
            picture=vips.Image.thumbnail_buffer(data,target[0],option_string=options,**kwargs)
        else:
            picture=vips.Image.thumbnail(filename+(f'[{options}]' if options else ''),target[0],**kwargs)
        if manual:
            if orientation==2:picture=picture.flip('horizontal')
            elif orientation==3:picture=picture.rot('d180')
            elif orientation==4:picture=picture.flip('vertical')
            elif orientation==5:picture=picture.rot('d90').flip('horizontal')
            elif orientation==6:picture=picture.rot('d90')
            elif orientation==7:picture=picture.rot('d90').flip('vertical')
            elif orientation==8:picture=picture.rot('d270')
        if picture.interpretation!='srgb':picture=picture.colourspace('srgb')
        if picture.hasalpha():picture=picture.flatten(background=[255,255,255])
        if picture.format!='uchar':picture=picture.cast('uchar')
        if picture.bands!=3:raise ValueError('libvips RGB 변환 실패')
        return bytes(picture.write_to_memory()),picture.width,picture.height,picture.width*3

    def read_qt(self,filename,data,number,bounds,fmt,orientation=1):
        from PySide6.QtCore import QBuffer,QByteArray,QIODevice,QSize,Qt
        from PySide6.QtGui import QImageReader,QImage,QPainter,QColorSpace,QTransform
        reader=QImageReader();buffer=None
        try:
            if fmt=='PNG' and orientation is None:orientation=self.png_orientation(filename,data)
            if data is not None:
                buffer=QBuffer();buffer.setData(QByteArray(data));buffer.open(QIODevice.OpenModeFlag.ReadOnly)
                reader.setDevice(buffer)
            else:reader.setFileName(filename)
            reader.setAutoTransform(True);reader.setQuality(100)
            if number and not reader.jumpToImage(number):raise ValueError('Qt에서 해당 TIFF 쪽을 읽지 못했습니다.')
            size=reader.size()
            if not size.isValid():raise ValueError(reader.errorString())
            native_transform=reader.transformation().value
            manual=orientation if native_transform==0 else 1
            rotated=bool(native_transform & 4) or manual in (5,6,7,8)
            target=QSize(*(tuple(reversed(bounds)) if rotated else bounds))
            if size.width()>target.width() or size.height()>target.height():
                reader.setScaledSize(size.scaled(target,Qt.AspectRatioMode.KeepAspectRatio))
            picture=reader.read()
            if picture.isNull():raise ValueError(reader.errorString())
            # Qt's PNG/WebP plugins may not expose EXIF orientation. Apply it only
            # when the handler did not advertise a transform, avoiding double rotation.
            if manual in (2,3,4):picture=picture.mirrored(manual in (2,3),manual in (3,4))
            elif manual==5:picture=picture.transformed(QTransform(0,1,1,0,0,0))
            elif manual==6:picture=picture.transformed(QTransform().rotate(90))
            elif manual==7:picture=picture.transformed(QTransform(0,-1,-1,0,0,0))
            elif manual==8:picture=picture.transformed(QTransform().rotate(270))
            if picture.width()>bounds[0] or picture.height()>bounds[1]:
                picture=picture.scaled(QSize(*bounds),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
            if picture.colorSpace().isValid():picture=picture.convertedToColorSpace(QColorSpace(QColorSpace.NamedColorSpace.SRgb))
            if picture.hasAlphaChannel():
                canvas=QImage(picture.size(),QImage.Format.Format_RGB888);canvas.fill(Qt.GlobalColor.white)
                painter=QPainter(canvas);painter.drawImage(0,0,picture);painter.end();picture=canvas
            else:picture=picture.convertToFormat(QImage.Format.Format_RGB888)
            return bytes(picture.constBits()),picture.width(),picture.height(),picture.bytesPerLine()
        finally:
            # Detach the native reader BEFORE releasing its Python-owned QBuffer.
            reader.setDevice(None)
            if buffer is not None:buffer.close()

    def read_pillow(self,filename,data,number,bounds,fmt,orientation=1):
        Image,ImageOps=pillow_reader()
        with Image.open(io.BytesIO(data) if data is not None else filename) as picture:
            picture.seek(number)
            if picture.format=='TIFF':picture.load()
            rotated=picture.getexif().get(274,1) in (5,6,7,8)
            picture.thumbnail(tuple(reversed(bounds)) if rotated else bounds,Image.Resampling.LANCZOS,reducing_gap=2.0)
            with ImageOps.exif_transpose(picture) as normalized, normalized.convert('RGBA') as rgba:
                with Image.new('RGB',rgba.size,'white') as canvas:
                    canvas.paste(rgba,mask=rgba.getchannel('A'))
                    return canvas.tobytes(),canvas.width,canvas.height,canvas.width*3

    def read(self,path,number,bounds,mode='auto'):
        if number<0:raise ValueError('그림 쪽 번호가 올바르지 않습니다.')
        bounds=tuple(max(1,min(IMAGE_PREVIEW_MAX_SIDE,int(v))) for v in bounds)
        validated=validate_image_source(path)  # Revalidate even a decoded-cache hit.
        key=(path,number,bounds,mode);frame=self.frames.pop(key,None)
        if frame is not None:self.frames[key]=frame;return frame
        filename,data=self.source(path,validated)
        fmt,orientation,original_size=self.image_format(filename,data,number)
        if fmt=='PNG' and orientation is None:orientation=self.png_orientation(filename,data)
        width,height=reversed(original_size) if orientation in (5,6,7,8) else original_size
        scale=min(1.0,bounds[0]/width,bounds[1]/height,
                  math.sqrt(IMAGE_PREVIEW_MAX_PIXELS/(width*height)))
        target=(max(1,min(bounds[0],math.floor(width*scale))),
                max(1,min(bounds[1],math.floor(height*scale))))
        first=mode if mode in ('qt','vips','pillow') else ('vips' if fmt in ('PNG','TIFF') else 'qt')
        engines=[first]+([e for e in ('qt','vips','pillow') if e!=first] if first!='pillow' else [])
        errors=[]
        for engine in engines:
            try:
                raw,width,height,stride=getattr(self,'read_'+engine)(filename,data,number,target,fmt,orientation)
                if (not 0<width<=bounds[0] or not 0<height<=bounds[1] or
                        width*height>IMAGE_PREVIEW_MAX_PIXELS or len(raw)!=stride*height):
                    raise ValueError('그림 디코더의 출력 크기가 올바르지 않습니다.')
                frame=(raw,width,height,stride,engine,' / '.join(errors))
                if len(raw)<=self.FRAME_LIMIT:
                    self.frames[key]=frame;self.frame_bytes+=len(raw)
                    while self.frame_bytes>self.FRAME_LIMIT:self.frame_bytes-=len(self.frames.popitem(last=False)[1][0])
                return frame
            except Exception as exc:errors.append(f'{engine}: {exc}')
        raise ValueError('그림을 읽지 못했습니다.\n'+'\n'.join(errors))


def image_worker():
    reader=DirectImageReader()
    for line in sys.stdin.buffer:
        request={};raw=b''
        try:
            request=json.loads(line)
            if request['op']=='release':
                reader.close();result={}
            else:
                side=request.get('max_side',1800) if request['op']=='preview' else request.get('payload',{}).get('thumb_side',370)
                side=max(64,min(IMAGE_PREVIEW_MAX_SIDE,side))
                bounds=(side,side) if request['op']=='preview' else (round(side*280/370),side)
                raw,width,height,stride,engine,note=reader.read(request['path'],request['page'],bounds,
                    request.get('payload',{}).get('engine','auto'))
                result=dict(width=width,height=height,stride=stride,engine=engine,note=note)
            response={'id':request['id'],'ok':True,**result}
        except Exception as exc:raw=b'';response={'id':request.get('id'),'ok':False,'error':str(exc)}
        response['nbytes']=len(raw)
        sys.stdout.buffer.write((json.dumps(response,ensure_ascii=True)+'\n').encode('ascii'))
        sys.stdout.buffer.write(raw);sys.stdout.buffer.flush()
    reader.close()


if __name__=='__main__' and '--image-worker' in sys.argv:
    image_worker();raise SystemExit(0)


def natural_path_key(value):
    # Tag tokens so names beginning with a digit and a letter remain comparable.
    return tuple(tuple((1,int(t)) if t.isdecimal() else (0,t.casefold())
                       for t in re.split(r'(\d+)',part))
                 for part in str(value).replace('\\','/').split('/'))


def supported_input(path):
    return Path(path).suffix.lower() in INPUT_EXTENSIONS or Path(path).is_dir()


def input_origin(path):
    p=Path(path)
    return str(p/(p.name+'.pdf')) if p.is_dir() else str(p)


def neighboring_inputs(path,include_containers=False,book_library=None):
    """이름·파일 속성만 읽는다. 책 폴더 탐색은 해당 폴더에서 찾은 ZIP/CBZ로 제한한다."""
    current=Path(path).resolve();entries=[];found=False
    current_key=os.path.normcase(str(current))
    if book_library:
        root=Path(book_library['root']).resolve()
        for value in book_library.get('paths',[]):
            candidate=Path(value)
            if candidate.suffix.lower() not in ARCHIVE_EXTENSIONS or root not in candidate.parents:continue
            if candidate.is_symlink() or not candidate.is_file():continue
            entries.append(str(candidate))
            if os.path.normcase(str(candidate))==current_key:found=True
        entries=sorted(set(entries),key=lambda p:(natural_path_key(Path(p).relative_to(root)),p))
    else:
        allowed=INPUT_EXTENSIONS if include_containers else IMAGE_EXTENSIONS|{'.pdf'}
        with os.scandir(current.parent) as items:
            for item in items:
                try:
                    if os.path.normcase(item.path)==current_key:
                        entries.append(str(current));found=True;continue
                    if ((Path(item.name).suffix.lower() in allowed and item.is_file(follow_symlinks=False)) or
                            (include_containers and item.is_dir(follow_symlinks=False))):
                        entries.append(str(Path(item.path)))
                except OSError:continue
        entries.sort(key=lambda p:(natural_path_key(Path(p).name),p))
    if not found:raise ValueError('현재 항목을 같은 폴더에서 찾지 못했습니다. 파일을 다시 열어주세요.')
    index=next((i for i,p in enumerate(entries) if os.path.normcase(p)==os.path.normcase(str(current))),None)
    if index is None:raise ValueError('현재 항목을 같은 폴더에서 찾지 못했습니다. 파일을 다시 열어주세요.')
    return {'previous':entries[index-1] if index>0 else '',
            'next':entries[index+1] if index+1<len(entries) else ''}


def next_sibling_input(path,direction,include_containers=False,book_library=None):
    return neighboring_inputs(path,include_containers,book_library)['previous' if direction<0 else 'next']


def import_input_pages(path, directory, emit, progress=None):
    """Stream immutable page PDFs and their thumbnails from a separate process."""
    import zipfile
    import shutil
    import warnings
    import pymupdf
    root=Path(path);directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    errors=[];page_count=0;completed=0;total=0;members_by_path={};last_scan=0
    progress=progress or (lambda data:None)

    def report(name='',frame=0,frames=0):
        fraction=frame/frames if frames else 0
        progress({'phase':'convert','done':completed,'total':total,'fraction':fraction,
                  'name':str(name),'frame':frame,'frames':frames,'pages':page_count,'errors':len(errors)})

    def publish(data):
        nonlocal page_count
        page_count+=data['count'];emit(data)

    def scan(found,force=False):
        nonlocal last_scan
        now=time.monotonic()
        if force or now-last_scan>=.1:
            progress({'phase':'scan','found':found,'name':str(root)});last_scan=now

    def image_pages(source, label):
        try:
            from PIL import Image, ImageOps
        except ImportError:
            raise ValueError('그림 읽기 모듈이 필요합니다. 실행에 사용하는 Python의 CMD에서\n'
                             'python -m pip install -U Pillow') from None
        with warnings.catch_warnings():
            warnings.simplefilter('error',Image.DecompressionBombWarning)
            with Image.open(source) as picture:
                frames=getattr(picture,'n_frames',1) if picture.format=='TIFF' else 1
                for index in range(frames):
                    target=None;published=False
                    try:
                        report(label,index,frames)
                        picture.seek(index)
                        dpi=picture.info.get('dpi',(96,96))
                        try: dpi=float(dpi[0] if isinstance(dpi,(tuple,list)) else dpi)
                        except (TypeError,ValueError,IndexError): dpi=96
                        if not math.isfinite(dpi) or not 20<=dpi<=2400:dpi=96
                        orientation=picture.getexif().get(274,1)
                        # Load before exif_transpose: TIFF's decoder may already apply orientation.
                        picture.load()
                        normalized=ImageOps.exif_transpose(picture)
                        try:
                            width,height=normalized.size
                            page_w,page_h=width*72/dpi,height*72/dpi
                            scale=min(max(1,1/min(page_w,page_h)),14400/max(page_w,page_h))
                            page_w,page_h=page_w*scale,page_h*scale
                            target=directory/(uuid.uuid4().hex+'.pdf')
                            with pymupdf.open() as doc:
                                page=doc.new_page(width=page_w,height=page_h)
                                if picture.format=='JPEG' and orientation==1:
                                    # Keep the original JPEG stream; no second lossy compression.
                                    page.insert_image(page.rect,filename=str(source))
                                else:
                                    mode='RGBA' if 'A' in normalized.getbands() or 'transparency' in normalized.info else 'RGB'
                                    with normalized.convert(mode) as bitmap:
                                        stream=io.BytesIO();bitmap.save(stream,format='PNG')
                                    page.insert_image(page.rect,stream=stream.getvalue())
                                doc.save(str(target),deflate=True)
                                zoom=min(280/page_w,370/page_h)
                                pix=page.get_pixmap(matrix=pymupdf.Matrix(zoom,zoom),alpha=False)
                                thumb=base64.b64encode(pix.tobytes('png')).decode('ascii')
                            publish({'path':str(target),'count':1,'source_path':str(label),
                                     'source_number':index,'thumbnail':thumb})
                            published=True
                        finally:normalized.close()
                    except Exception as exc:
                        errors.append(f'{label} · {index+1}쪽: {exc}')
                    finally:
                        if target is not None and not published:target.unlink(missing_ok=True)
                        report(label,index+1,frames)

    def read_file(source, label=None):
        nonlocal completed
        label=label or str(source)
        suffix=source.suffix.lower()
        archive_input=suffix in ARCHIVE_EXTENSIONS
        start_count=completed
        report(label)
        try:
            if suffix=='.pdf':
                with pymupdf.open(source) as doc:
                    if not doc.is_pdf or doc.needs_pass:raise ValueError('암호가 없는 PDF를 선택하세요.')
                    if doc.page_count:publish({'path':str(source),'count':doc.page_count})
            elif suffix in IMAGE_EXTENSIONS:image_pages(source,label)
            elif suffix in ARCHIVE_EXTENSIONS:
                with zipfile.ZipFile(source) as archive:
                    members=members_by_path[source]
                    for member in members:
                        staged=directory/(uuid.uuid4().hex+Path(member.filename).suffix.lower())
                        member_label=str(source)+'/'+member.filename.replace('\\','/')
                        report(member_label)
                        try:
                            if member.flag_bits&1:raise ValueError('암호가 설정된 그림은 먼저 압축을 풀어주세요.')
                            if member.file_size>256*1024*1024:raise ValueError('그림 한 파일이 256MB를 초과합니다.')
                            # Generated path only: never extract archive member paths into the filesystem.
                            with archive.open(member) as incoming,staged.open('xb') as output:
                                shutil.copyfileobj(incoming,output,1024*1024)
                            image_pages(staged,member_label)
                        except Exception as exc:errors.append(f'{member_label}: {exc}')
                        finally:
                            staged.unlink(missing_ok=True);completed+=1;report(member_label)
        except Exception as exc:errors.append(f'{label}: {exc}')
        finally:
            if archive_input:completed=start_count+len(members_by_path.get(source,()))
            else:completed+=1
            report(label)

    scan(0,True)
    entries=[]
    if root.is_dir():
        def walk_error(exc):errors.append(str(exc))
        for base,dirs,files in os.walk(root,followlinks=False,onerror=walk_error):
            dirs[:]=[d for d in dirs if not d.startswith('.') and d!='__MACOSX'
                     and not Path(base,d).is_symlink()]
            entries.extend(Path(base,f) for f in files if not f.startswith('.')
                           and Path(f).suffix.lower() in INPUT_EXTENSIONS)
            scan(len(entries))
        entries.sort(key=lambda p:(natural_path_key(p.relative_to(root)),str(p)))
    elif root.is_file():entries=[root]
    else:errors.append(f'파일 또는 폴더를 찾을 수 없습니다: {root}')
    ready=[]
    for source in entries:
        if source.suffix.lower() in ARCHIVE_EXTENSIONS:
            try:
                with zipfile.ZipFile(source) as archive:
                    members=sorted((i for i in archive.infolist() if not i.is_dir()
                        and Path(i.filename).suffix.lower() in IMAGE_EXTENSIONS
                        and not any(p.startswith('.') or p=='__MACOSX' for p in i.filename.replace('\\','/').split('/'))),
                        key=lambda i:(natural_path_key(i.filename),i.filename))
                if not members:raise ValueError('압축파일에 지원하는 그림이 없습니다.')
                members_by_path[source]=members;total+=len(members);ready.append(source)
            except Exception as exc:errors.append(f'{source}: {exc}')
        else:total+=1;ready.append(source)
        scan(total)
    report(root)
    for source in ready:read_file(source)
    if not page_count and not errors:errors.append('읽을 수 있는 PDF 또는 그림이 없습니다.')
    return {'count':page_count,'errors':errors,'done':completed,'total':total}


def discover_input_pages(path,emit,progress=None,images_only=False):
    """Catalog originals only. Decode pixels later in the visible-page image worker."""
    import zipfile
    root=Path(path);progress=progress or (lambda _data:None);folder_input=root.is_dir()
    extensions=IMAGE_EXTENSIONS|ARCHIVE_EXTENSIONS if images_only else INPUT_EXTENSIONS
    errors=[];records=[];pending=[];page_count=0;last_report=0;last_publish=0
    def report(data,force=False):
        nonlocal last_report
        now=time.monotonic()
        if force or now-last_report>=.08:progress(data);last_report=now
    report({'phase':'scan','found':0,'name':str(root)},True)
    entries=[]
    if folder_input:
        for base,dirs,files in os.walk(root,followlinks=False,onerror=lambda exc:errors.append(str(exc))):
            dirs[:]=[d for d in dirs if not d.startswith('.') and d!='__MACOSX' and not Path(base,d).is_symlink()]
            entries.extend(Path(base,f) for f in files if not f.startswith('.') and Path(f).suffix.lower() in extensions)
            report({'phase':'scan','found':len(entries),'name':str(root)})
        entries.sort(key=lambda p:(natural_path_key(p.relative_to(root)),str(p)))
    elif root.is_file() and root.suffix.lower() in extensions:entries=[root]
    else:errors.append(f'파일 또는 폴더를 찾을 수 없습니다: {root}')
    book_library=None;book_path=''
    if folder_input and not images_only:
        books=[source for source in entries if source.suffix.lower() in ARCHIVE_EXTENSIONS and not source.is_symlink()]
        if books:
            book_library={'root':str(root.resolve()),'paths':[str(source.resolve()) for source in books]}
            book_path=book_library['paths'][0]
            emit({'items':[],'book_library':book_library,'book_path':book_path})
            # 각 압축파일은 한 권이다. 첫 책 외에는 ZIP 헤더나 그림을 읽지 않는다.
            entries=[Path(book_path)];folder_input=False
    for source in entries:
        try:
            if source.suffix.lower() in ARCHIVE_EXTENSIONS:
                with zipfile.ZipFile(source) as archive:
                    members=sorted(((i,m) for i,m in enumerate(archive.infolist()) if not m.is_dir()
                        and Path(m.filename).suffix.lower() in IMAGE_EXTENSIONS
                        and not any(p.startswith('.') or p=='__MACOSX' for p in m.filename.replace('\\','/').split('/'))),
                        key=lambda pair:(natural_path_key(pair[1].filename),pair[1].filename,pair[0]))
                    if not members:errors.append(f'{source}: 압축파일에 지원하는 그림이 없습니다.')
                    for index,member in members:
                        records.append((source,member,index))
            else:records.append((source,None,None))
        except Exception as exc:errors.append(f'{source}: {exc}')
        report({'phase':'scan','found':len(records),'name':str(root)})
    total=len(records);archives=OrderedDict();source_info={}
    try:
        report({'phase':'catalog','total':total,'done':0,'name':str(root)},True)
        for done,(source,member,index) in enumerate(records,1):
            label=str(source)+('/'+member.filename.replace('\\','/') if member else '')
            try:
                suffix=Path(member.filename if member else source).suffix.lower()
                if member and (member.flag_bits&1 or member.file_size>256*1024*1024):
                    raise ValueError('암호가 있거나 256MB를 초과하는 그림은 읽을 수 없습니다.')
                if suffix=='.pdf':
                    import pymupdf
                    with pymupdf.open(source) as doc:
                        if not doc.is_pdf or doc.needs_pass:raise ValueError('암호가 없는 PDF를 선택하세요.')
                        if not len(doc):raise ValueError('페이지가 없는 PDF입니다.')
                        item={'path':str(source),'count':1 if folder_input else len(doc)}
                        if folder_input:item['document_pages']=len(doc)
                else:
                    if source not in source_info:
                        resolved=source.resolve();stat=resolved.stat()
                        source_info[source]={'file':str(resolved),'stamp':[stat.st_size,stat.st_mtime_ns]}
                    locator=image_source_path(source,member.filename if member else None,index,source_info[source])
                    count=1
                    if suffix in ('.tif','.tiff'):
                        with open_image_source(locator,0,archives) as (picture,_):count=getattr(picture,'n_frames',1)
                    item={'path':locator,'count':count,'source_path':label,'image':True}
                page_count+=item['count'];pending.append(item)
                now=time.monotonic()
                if page_count==item['count'] or len(pending)>=64 or now-last_publish>=.05:
                    emit({'items':pending,'book_path':book_path});pending=[];last_publish=now
            except Exception as exc:errors.append(f'{label}: {exc}')
            report({'phase':'catalog','total':total,'done':done,'name':label,'pages':page_count,'errors':len(errors)},done==total)
        if pending:emit({'items':pending,'book_path':book_path})
    finally:
        for archive in archives.values():archive.close()
    if not page_count and not errors:errors.append('읽을 수 있는 PDF 또는 그림이 없습니다.')
    return {'count':page_count,'errors':errors,'done':total,'total':total}


def input_worker():
    def send(data):
        sys.stdout.buffer.write((json.dumps(data,ensure_ascii=True)+'\n').encode('ascii'));sys.stdout.buffer.flush()
    for line in sys.stdin.buffer:
        job={}
        try:
            job=json.loads(line)
            emit=lambda data:send({'id':job['id'],'item':data})
            progress=lambda data:send({'id':job['id'],'progress':data})
            if job.get('mode')=='convert':result=import_input_pages(job['path'],job['directory'],emit,progress)
            else:result=discover_input_pages(job['path'],emit,progress)
            send({'id':job['id'],'done':result})
        except Exception as exc:send({'id':job.get('id'),'done':{'count':0,'errors':[str(exc)]}})


if __name__=='__main__' and '--input-worker' in sys.argv:
    input_worker();raise SystemExit(0)


def editable_copy(path, number):
    """페이지별 불변 작업 사본. 화면 좌표와 PDF 편집 좌표를 일치시킨다."""
    import pymupdf
    if is_image_source(path):return image_page_document(path,number)
    result = pymupdf.open()
    try:
        with pymupdf.open(path) as source:
            result.insert_pdf(source, from_page=number, to_page=number)
        result[0].remove_rotation()
        return result
    except Exception:
        result.close()
        raise


def image_pdf_reader(doc):
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ValueError('그림 편집 모듈이 필요합니다. CMD에서 py -m pip install -U pypdf 를 실행하세요.') from None
    return PdfReader(io.BytesIO(doc.tobytes()))


def pdf_image_occurrences(doc, reader=None):
    """XObject/인라인 그림의 개별 그리기 명령을 찾는다. 공유 xref와 배치 ID를 구분."""
    import pymupdf
    from pypdf.generic import ContentStream
    reader = reader or image_pdf_reader(doc)
    page = doc[0]
    result = []

    def walk(stream, resources, matrix, path, clip, complex_clip=False, ancestors=()):
        if len(path) > 24:
            raise ValueError('그림의 중첩 구조가 너무 깊어 편집할 수 없습니다.')
        stack = []
        path_rect = None; other_path = False
        axis_aligned = lambda m: (abs(m.b)<1e-5 and abs(m.c)<1e-5) or (abs(m.a)<1e-5 and abs(m.d)<1e-5)
        for index, (args, op) in enumerate(ContentStream(stream, reader).operations):
            if op == b'q':
                stack.append((pymupdf.Matrix(matrix), pymupdf.Rect(clip), complex_clip))
            elif op == b'Q' and stack:
                matrix, clip, complex_clip = stack.pop()
            elif op == b'cm':
                matrix = pymupdf.Matrix(*map(float, args)) * matrix
            elif op == b're':
                x,y,w,h = map(float,args)
                area = pymupdf.Rect(x,y,x+w,y+h).normalize() * matrix * page.transformation_matrix
                if path_rect is not None: other_path = True
                if not axis_aligned(matrix * page.transformation_matrix): other_path = True
                path_rect = area
            elif op in (b'm', b'l', b'c', b'v', b'y'):
                other_path = True
            elif op in (b'W', b'W*'):
                if path_rect is not None and not other_path:
                    clip = clip & path_rect
                else:
                    complex_clip = True
            elif op in (b'n', b'S', b's', b'f', b'F', b'f*', b'B', b'B*', b'b', b'b*'):
                path_rect = None; other_path = False
            elif op == b'Tr' and int(args[0])>=4:
                complex_clip = True
            elif op in (b'Do', b'INLINE IMAGE'):
                obj = None
                if op == b'Do':
                    obj = resources.get('/XObject', {}).get_object().get(args[0]) if '/XObject' in resources else None
                    if obj is None: continue
                    obj = obj.get_object()
                    if obj.get('/Subtype') == '/Form':
                        identity = (getattr(obj.indirect_reference, 'idnum', None) if hasattr(obj,'indirect_reference') else id(obj))
                        if identity in ancestors: continue
                        fm = pymupdf.Matrix(*map(float, obj.get('/Matrix', [1,0,0,1,0,0]))) * matrix
                        fc = clip
                        if '/BBox' in obj:
                            fc = clip & (pymupdf.Rect(list(map(float,obj['/BBox']))) * fm * page.transformation_matrix)
                        walk(obj, obj.get('/Resources', resources).get_object(), fm, path+[index], fc,
                             complex_clip or not axis_aligned(fm * page.transformation_matrix), ancestors+(identity,))
                        continue
                    if obj.get('/Subtype') != '/Image': continue
                    width, height = int(obj.get('/Width',0)), int(obj.get('/Height',0))
                else:
                    settings = args['settings']
                    width = int(settings.get('/W', settings.get('/Width',0)))
                    height = int(settings.get('/H', settings.get('/Height',0)))
                transform = pymupdf.Matrix(1,0,0,-1,0,1) * matrix * page.transformation_matrix
                box = pymupdf.Rect(0,0,1,1) * transform
                if box.is_empty or (box & clip).is_empty: continue
                result.append({'id':path+[index], 'rect':list(box), 'width':width, 'height':height,
                               'transform':list(transform), 'clip':list(clip), 'complex_clip':complex_clip})

    root = reader.pages[0]
    walk(root.get_contents(), root['/Resources'].get_object(), pymupdf.Matrix(1,0,0,1,0,0), [], page.rect)
    return result


def change_pdf_image(doc, operation):
    """선택한 Do 명령과 그 Form 경로만 복제. 다른 배치·레이어·투명도·원본 해상도를 보존."""
    import pymupdf
    from pypdf import PdfWriter
    from pypdf.generic import ContentStream, DecodedStreamObject, DictionaryObject, NameObject, FloatObject
    reader = image_pdf_reader(doc)
    images = pdf_image_occurrences(doc, reader)
    chosen = next((im for im in images if im['id'] == operation['image_id']), None)
    if chosen is None or max(abs(a-b) for a,b in zip(chosen['rect'],operation['rect'])) > 0.1:
        raise ValueError('그림이 변경되었습니다. 다시 선택하세요.')
    kind = operation['kind']
    source = pymupdf.Rect(chosen['rect'])
    target = pymupdf.Rect(operation.get('target', chosen['rect']))
    delta = pymupdf.Matrix(1,0,0,1,0,0)
    if kind == 'image_transform':
        if target.width < 2 or target.height < 2 or not doc[0].rect.contains(target):
            raise ValueError('그림은 페이지 안에 놓아주세요. 최소 크기는 2pt입니다.')
        if chosen['complex_clip'] or not (pymupdf.Rect(chosen['clip']) + (-0.1,-0.1,0.1,0.1)).contains(target):
            raise ValueError('이 그림에는 잘라내기 경계가 있습니다. 경계 안으로 이동하거나 새 그림 넣기를 사용하세요.')
        sx, sy = target.width/source.width, target.height/source.height
        delta = pymupdf.Matrix(sx,0,0,sy,target.x0-source.x0*sx,target.y0-source.y0*sy)
    writer = PdfWriter(); writer.clone_document_from_reader(reader)
    root = writer.pages[0]
    replacement = None
    if kind == 'image_replace':
        with pymupdf.open() as image_doc:
            image_page = image_doc.new_page()
            image_page.insert_image(pymupdf.Rect(0,0,100,100), filename=operation['filename'], keep_proportion=False)
            image_reader = image_pdf_reader(image_doc)
            objects = image_reader.pages[0]['/Resources']['/XObject']
            replacement = next(iter(objects.values())).clone(writer)

    def modify(container, stream, resources, depth, matrix, text_mode=0):
        content = ContentStream(stream, writer)
        operations = list(content.operations)
        chosen_index = chosen['id'][depth]
        inherited_text_mode=text_mode
        stack = []
        for args,op in operations[:chosen_index]:
            if op == b'q': stack.append((pymupdf.Matrix(matrix),text_mode))
            elif op == b'Q' and stack: matrix,text_mode = stack.pop()
            elif op == b'cm': matrix = pymupdf.Matrix(*map(float,args)) * matrix
            elif op == b'Tr':text_mode=int(args[0])
        # 리소스 사전도 복제하여 같은 Form의 다른 배치에 영향을 주지 않는다.
        local_resources = DictionaryObject(dict(resources.get_object()))
        objects = DictionaryObject(dict(local_resources.get('/XObject', DictionaryObject()).get_object()))
        local_resources[NameObject('/XObject')] = objects
        container[NameObject('/Resources')] = local_resources
        args,op = operations[chosen_index]
        name = NameObject('/PM'+uuid.uuid4().hex)
        if depth+1 < len(chosen['id']):
            original = objects[args[0]].get_object()
            form = DecodedStreamObject()
            for key,value in original.items():
                if key not in ('/Length','/Filter','/DecodeParms'): form[key] = value
            form.set_data(original.get_data())
            objects[name] = writer._add_object(form)
            operations[chosen_index] = ([name],b'Do')
            fm = pymupdf.Matrix(*map(float,form.get('/Matrix',[1,0,0,1,0,0]))) * matrix
            modify(form, form, form.get('/Resources',local_resources), depth+1, fm,text_mode)
        elif kind == 'image_delete':
            operations[chosen_index:chosen_index+1] = []
        elif kind == 'image_replace':
            objects[name] = replacement
            operations[chosen_index] = ([name],b'Do')
        elif kind == 'image_transform':
            world = matrix * doc[0].transformation_matrix
            if abs(world.a*world.d-world.b*world.c) < 1e-9:
                raise ValueError('변환할 수 없는 그림 좌표입니다.')
            local_delta = world * delta * ~world
            operations[chosen_index:chosen_index+1] = [([],b'q'),
                ([FloatObject(float(v)) for v in local_delta],b'cm'), (args,op), ([],b'Q')]
        if kind == 'image_isolate':
            # Keep the selected occurrence and its graphics/clipping state,
            # including nested Forms. Other page artwork must not be copied.
            isolated=[];text_mode=inherited_text_mode;text_stack=[]
            for index,(values,operator) in enumerate(operations):
                if operator==b'q':text_stack.append(text_mode)
                elif operator==b'Q' and text_stack:text_mode=text_stack.pop()
                if operator in (b'Do',b'INLINE IMAGE') and index!=chosen_index:continue
                if operator==b'sh':continue
                if operator in (b'S',b's',b'f',b'F',b'f*',b'B',b'B*',b'b',b'b*'):
                    values,operator=[],b'n'
                if operator==b'Tr':
                    text_mode=int(values[0]);values=[FloatObject(7 if text_mode>=4 else 3)]
                isolated.append((values,operator))
                if operator==b'BT':isolated.append(([FloatObject(7 if text_mode>=4 else 3)],b'Tr'))
            operations=isolated
        content.operations = operations
        if depth == 0:
            container[NameObject('/Contents')] = writer._add_object(content)
        else:
            container.set_data(content.get_data())

    modify(root, root.get_contents(), root['/Resources'], 0, pymupdf.Matrix(1,0,0,1,0,0))
    buffer = io.BytesIO(); writer.write(buffer)
    # 새 객체를 다시 열어 검증하고, 작업 사본을 압축한다.
    with pymupdf.open(stream=buffer.getvalue(), filetype='pdf') as result:
        return result.tobytes(garbage=4,deflate=True)


def copy_pdf_image_png(path,number,selected):
    """Transparent raster of one occurrence, with displayed transform/mask/clip.

    Render at least 216 dpi where possible, bounded to 4096 px on each side.
    Never rasterize neighbouring text or pictures into the clipboard image.
    """
    import pymupdf
    with editable_copy(path,number) as doc:
        area=pymupdf.Rect(selected['rect']) & doc[0].rect
        if area.is_empty:raise ValueError('복사할 그림 영역이 없습니다.')
        data=change_pdf_image(doc,{'kind':'image_isolate','rect':selected['rect'],'image_id':selected['id']})
        scale=min(max(3,selected.get('width',0)/area.width,selected.get('height',0)/area.height),
                  4096/max(area.width,area.height))
        with pymupdf.open(stream=data,filetype='pdf') as isolated:
            pix=isolated[0].get_pixmap(matrix=pymupdf.Matrix(scale,scale),clip=area,alpha=True,annots=False)
            return pix.tobytes('png'),[area.width,area.height]


def inspect_edit_page(path, number, tables=False, images=False):
    import pymupdf
    pymupdf.TOOLS.set_small_glyph_heights(True)
    with editable_copy(path, number) as doc:
        page = doc[0]
        spans = []
        for block in page.get_text('dict', flags=pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES)['blocks']:
            for line in block.get('lines', []):
                dx, dy = line.get('dir', (1, 0))
                angle = math.degrees(math.atan2(-dy, dx)) % 360
                rotation = int(round(angle / 90) * 90) % 360
                if abs((angle - rotation + 180) % 360 - 180) > 1:
                    continue  # 임의 각도 글자는 영역 도구로 보정한다.
                for span in line.get('spans', []):
                    if span['text'].strip():
                        spans.append({'rect': list(span['bbox']), 'text': span['text'],
                                      'size': span['size'], 'color': '#%06x' % span['color'],
                                      'bold': bool(span['flags'] & 16), 'rotate': rotation})
        cells = []
        if tables:
            seen = set()
            for table in page.find_tables().tables:
                for box in table.cells:
                    if box is None or tuple(box) in seen:
                        continue
                    seen.add(tuple(box))
                    r = pymupdf.Rect(box)
                    inner = r + (1, 1, -1, -1)
                    contained = [s for s in spans if inner.contains(pymupdf.Rect(s['rect']))]
                    sample = contained[0] if contained else {}
                    text_rect = [min(s['rect'][0] for s in contained), min(s['rect'][1] for s in contained),
                                 r.x1-2, r.y1-2] if contained else list(r + (2, 2, -2, -2))
                    cells.append({'rect': list(r), 'text': page.get_textbox(inner).strip(),
                                  'size': sample.get('size', 11), 'color': sample.get('color', '#111111'),
                                  'bold': sample.get('bold', False), 'rotate': sample.get('rotate', 0),
                                  'text_rect': text_rect})
        pictures = pdf_image_occurrences(doc, image_pdf_reader(doc)) if images else []
        return {'width': page.rect.width, 'height': page.rect.height, 'spans': spans, 'cells': cells,
                'tables': tables, 'images':pictures, 'images_ready':images}


def insert_editor_text(page, rect, operation):
    """실제 PDF 텍스트를 기록. 넘치는 내용은 50%까지만 줄이고 나머지는 오류로 알린다."""
    import pymupdf
    text = operation.get('text', '')
    if not text:
        return
    size = max(4, min(144, float(operation.get('size', 11))))
    family = operation.get('font', 'sans-serif')
    if family not in ('sans-serif', 'serif', 'monospace'):
        family = 'sans-serif'
    color = operation.get('color', '#111111')
    if len(color) != 7 or color[0] != '#' or any(c not in '0123456789abcdefABCDEF' for c in color[1:]):
        raise ValueError('올바른 글자 색상을 선택하세요.')
    align = operation.get('align', 'left')
    if align not in ('left', 'center', 'right'):
        align = 'left'
    css = ('body {margin:0; padding:0;} p {margin:0; padding:0; line-height:1.05; '
           f'font-family:{family}; font-size:{size}pt; color:{color}; text-align:{align}; '
           f'font-weight:{"bold" if operation.get("bold") else "normal"};' + '}')
    # HTML은 텍스트 이스케이프 후에만 사용. CJK는 MuPDF 내장 대체 글꼴 사용.
    content = '<p>' + html.escape(text).replace('\n', '<br>') + '</p>'
    spare, scale = page.insert_htmlbox(rect, content, css=css, scale_low=0.5,
                                       rotate=operation.get('rotate', 0))
    if spare < 0:
        raise ValueError('내용이 선택 영역에 들어가지 않습니다. 글자 크기를 줄이거나 영역을 넓혀주세요.')


def move_pdf_text(page, source_path, number, rect, dx, dy, expected_text):
    """선택한 텍스트만 벡터 PDF로 옮긴다. 폰트/자간은 재입력하지 않는다."""
    import pymupdf
    destination = rect + (dx, dy, dx, dy)
    if not page.rect.contains(destination):
        raise ValueError('글자 박스가 페이지 밖으로 나갈 수 없습니다.')
    with editable_copy(source_path, number) as fragment:
        piece = fragment[0]
        # Redaction의 glyph 판정 범위는 font ascender/descender까지 포함한다.
        pymupdf.TOOLS.set_small_glyph_heights(False)
        try:
            spans = [s for b in piece.get_text('dict', flags=pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES)['blocks']
                     for line in b.get('lines', []) for s in line['spans'] if s['text'] == expected_text]
        finally:
            pymupdf.TOOLS.set_small_glyph_heights(True)
        if not spans:
            raise ValueError('이동할 글자를 다시 선택하세요.')
        match = min(spans, key=lambda s: sum(abs(s['bbox'][i]-rect[i]) for i in range(4)))
        keep = (pymupdf.Rect(match['bbox']) + (-0.2,-0.2,0.2,0.2)) & piece.rect
        for annot in list(piece.annots() or []):
            piece.delete_annot(annot)
        for widget in list(piece.widgets() or []):
            piece.delete_widget(widget)
        piece.add_redact_annot(piece.rect, fill=False, cross_out=False)
        piece.apply_redactions(images=1, graphics=2, text=1)
        full = piece.rect
        # 선택 영역 밖의 글자도 실제로 제거하여 숨겨진 중복 텍스트를 남기지 않는다.
        for box in [(0,0,full.width,keep.y0), (0,keep.y1,full.width,full.height),
                    (0,keep.y0,keep.x0,keep.y1), (keep.x1,keep.y0,full.width,keep.y1)]:
            area = pymupdf.Rect(box)
            if not area.is_empty:
                piece.add_redact_annot(area, fill=False, cross_out=False)
        piece.apply_redactions(images=0, graphics=0, text=0)
        compact = lambda value: ''.join(value.split())
        if compact(piece.get_text()) != compact(expected_text):
            raise ValueError('겹치거나 분리할 수 없는 글자 영역입니다. 글자 수정 도구를 사용하세요.')
        # 이웃 글자가 선택 영역과 겹치면 원본 글자가 함께 지워지는 것을 막는다.
        for block in page.get_text('dict', flags=pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES)['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    box = pymupdf.Rect(span['bbox'])
                    if span['text'].strip() and (box & rect).get_area() > 0.05:
                        if max(abs(box[i]-rect[i]) for i in range(4)) > 0.1:
                            raise ValueError('다른 글자와 겹친 영역은 개별 이동할 수 없습니다.')
        page.add_redact_annot(rect, fill=False, cross_out=False)
        page.apply_redactions(images=0, graphics=0, text=0)
        # 글리프의 실제 획이 작은 글자 경계 밖으로 나오는 경우까지 보존한다.
        clip = (keep + (-2,-2,2,2)) & piece.rect
        target = clip + (dx,dy,dx,dy)
        page.show_pdf_page(target, fragment, 0, clip=clip, keep_proportion=False, overlay=True)


def check_text_delete(page, rect, expected_text):
    """선택한 글자 경계가 다른 글자에 걸치면 실제 삭제 전에 중단한다."""
    import pymupdf
    matched=False
    for block in page.get_text('dict',flags=pymupdf.TEXTFLAGS_DICT & ~pymupdf.TEXT_PRESERVE_IMAGES)['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if not span['text'].strip():continue
                box=pymupdf.Rect(span['bbox'])
                if (box & rect).get_area()<=0:continue
                if span['text']==expected_text and max(abs(box[i]-rect[i]) for i in range(4))<0.1 and not matched:
                    matched=True
                else:
                    raise ValueError('다른 글자와 겹친 영역입니다. 흰색 덮기로 필요한 범위를 지정하세요.')
    if not matched:raise ValueError('삭제할 글자가 변경되었습니다. 다시 선택하세요.')


def apply_page_edit(path, number, operation, output):
    """수정은 새 PDF에만 기록한다. 오류 시 원본과 이전 작업 사본은 그대로 유지."""
    import pymupdf
    pymupdf.TOOLS.set_small_glyph_heights(True)
    with editable_copy(path, number) as doc:
        page = doc[0]
        kind = operation['kind']
        image_data = None
        rect = pymupdf.Rect(operation['rect']) & page.rect
        minimum = 0.1 if kind == 'text_delete' else (0.5 if kind == 'cover' else 2)
        if kind != 'line' and (rect.is_empty or rect.width < minimum or rect.height < minimum):
            raise ValueError('조금 더 넓은 영역을 선택하세요.')
        if kind in ('replace', 'cell', 'move','text_delete'):
            # 기존의 미적용 redaction 주석까지 적용하지 않도록 보호한다.
            if any(a.type[0] == pymupdf.PDF_ANNOT_REDACT for a in (page.annots() or [])):
                raise ValueError('미적용 삭제 주석이 있는 페이지입니다. 글자 넣기 / 흰색 덮기를 사용하세요.')
            if kind != 'move':
                if kind=='text_delete':check_text_delete(page,rect,operation['text'])
                erase = rect + (1, 1, -1, -1) if kind == 'cell' else rect
                page.add_redact_annot(erase, fill=False, cross_out=False)
                page.apply_redactions(images=0, graphics=0, text=0)
        if kind == 'cover' or operation.get('white'):
            page.draw_rect(rect, color=None, fill=(1, 1, 1), fill_opacity=1, overlay=True)
        if kind in ('image_transform', 'image_replace', 'image_delete'):
            image_data = change_pdf_image(doc, operation)
        elif kind == 'image_add':
            page.insert_image(rect, filename=operation['filename'], keep_proportion=True, overlay=True)
        elif kind == 'move':
            move_pdf_text(page, path, number, rect, operation['dx'], operation['dy'], operation['text'])
        elif kind == 'text_delete':
            pass
        elif kind in ('replace', 'cell', 'text'):
            target = rect + (2, 2, -2, -2) if kind == 'cell' else rect
            if kind == 'cell' and operation.get('text_rect'):
                target = pymupdf.Rect(operation['text_rect']) & target
            insert_editor_text(page, target, operation)
        elif kind == 'line':
            a, b = pymupdf.Point(operation['start']), pymupdf.Point(operation['end'])
            if not (page.rect.contains(a) and page.rect.contains(b)):
                raise ValueError('선은 페이지 안에 그려주세요.')
            color = tuple(int(operation.get('color', '#111111')[i:i+2], 16)/255 for i in (1, 3, 5))
            page.draw_line(a, b, color=color, width=operation.get('width', 1), overlay=True)
        elif kind == 'table':
            values = operation['values']
            rows, cols = len(values), len(values[0])
            if not 1 <= rows <= 30 or not 1 <= cols <= 15 or any(len(r) != cols for r in values):
                raise ValueError('표 크기가 올바르지 않습니다.')
            cw, ch = rect.width / cols, rect.height / rows
            if cw < 12 or ch < 12:
                raise ValueError('표 영역이 너무 작습니다. 영역을 넓히거나 행·열 수를 줄이세요.')
            for r in range(rows):
                for c in range(cols):
                    cell = pymupdf.Rect(rect.x0+c*cw+3, rect.y0+r*ch+3,
                                     rect.x0+(c+1)*cw-3, rect.y0+(r+1)*ch-3)
                    insert_editor_text(page, cell, {**operation, 'text': values[r][c]})
            shape = page.new_shape()
            for r in range(rows+1):
                shape.draw_line((rect.x0, rect.y0+r*ch), (rect.x1, rect.y0+r*ch))
            for c in range(cols+1):
                shape.draw_line((rect.x0+c*cw, rect.y0), (rect.x0+c*cw, rect.y1))
            shape.finish(color=(0.12, 0.12, 0.12), width=0.7)
            shape.commit()
        elif kind != 'cover':
            raise ValueError('지원하지 않는 편집 도구입니다.')
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        data = image_data if image_data is not None else doc.tobytes(garbage=4, deflate=True)
        try:
            with output.open('xb') as stream:
                stream.write(data)
        except FileExistsError:
            raise
        except Exception:
            output.unlink(missing_ok=True)
            raise
    return str(output)


def pdf_worker():
    """Qt와 분리된 단일 PDF 프로세스. PyMuPDF를 여러 스레드에서 호출하지 않는다."""
    import pymupdf
    pymupdf.TOOLS.mupdf_display_errors(False)
    pymupdf.TOOLS.mupdf_display_warnings(False)
    documents = OrderedDict()
    for line in sys.stdin.buffer:
        request = {}
        try:
            request = json.loads(line)
            if request['op']=='release':
                for cached in documents.values():cached.close()
                documents.clear()
                sys.stdout.buffer.write((json.dumps({'id':request['id'],'ok':True})+'\n').encode('ascii'))
                sys.stdout.buffer.flush()
                continue
            path = request['path']
            if request['op'] in ('sibling','neighbors'):
                payload=request.get('payload',{})
                neighbors=neighboring_inputs(path,payload.get('include_containers',False),payload.get('book_library'))
                result=({'path':neighbors['previous' if payload['direction']<0 else 'next']}
                        if request['op']=='sibling' else {'neighbors':neighbors})
                sys.stdout.buffer.write((json.dumps({'id':request['id'],'ok':True,**result},ensure_ascii=True)+'\n').encode('ascii'))
                sys.stdout.buffer.flush();continue
            if is_image_source(path):
                payload=request.get('payload',{})
                if request['op']=='editinfo':
                    result={'info':inspect_edit_page(path,request['page'],payload.get('tables',False),payload.get('images',False))}
                elif request['op']=='edit':
                    result={'path':apply_page_edit(path,request['page'],payload['operation'],payload['output'])}
                else:raise ValueError('그림 미리보기는 그림 엔진에서 처리해야 합니다.')
                sys.stdout.buffer.write((json.dumps({'id':request['id'],'ok':True,**result},ensure_ascii=True)+'\n').encode('ascii'))
                sys.stdout.buffer.flush();continue
            if path not in documents:
                doc = pymupdf.open(path)
                if not doc.is_pdf or doc.needs_pass:
                    doc.close()
                    raise ValueError('암호가 없는 PDF 파일을 선택하세요.')
                documents[path] = doc
            documents.move_to_end(path)
            while len(documents) > 4:
                documents.popitem(last=False)[1].close()
            doc = documents[path]
            if request['op'] == 'editinfo':
                payload = request.get('payload', {})
                result = {'info': inspect_edit_page(path, request['page'], payload.get('tables', False), payload.get('images', False))}
            elif request['op'] == 'edit':
                payload = request['payload']
                result = {'path': apply_page_edit(path, request['page'], payload['operation'], payload['output'])}
            elif request['op'] == 'inspect':
                result = {'count': len(doc)}
            else:
                page = doc[request['page']]
                rect = page.rect
                if request['op'] == 'preview':
                    limit = max(1000, min(5000, request.get('max_side', 1800)))
                    scale = limit / max(1, rect.width, rect.height)
                else:
                    limit = request.get('payload', {}).get('thumb_side', 370)
                    scale = min(limit*280/370 / max(1, rect.width), limit / max(1, rect.height))
                pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), colorspace=pymupdf.csRGB, alpha=False)
                result = {'png': base64.b64encode(pix.tobytes('png')).decode('ascii')}
            response = {'id': request['id'], 'ok': True, **result}
        except Exception as exc:
            response = {'id': request.get('id'), 'ok': False, 'error': str(exc)}
        sys.stdout.buffer.write((json.dumps(response, ensure_ascii=True) + '\n').encode('ascii'))
        sys.stdout.buffer.flush()
    for doc in documents.values():
        doc.close()


if __name__ == '__main__' and '--pdf-worker' in sys.argv:
    pdf_worker()
    raise SystemExit(0)

def hangul_python_executable():
    if getattr(sys,'frozen',False):return ''
    executable=Path(sys.executable)
    if executable.name.lower()=='pythonw.exe' and executable.with_name('python.exe').is_file():
        executable=executable.with_name('python.exe')
    return str(executable)


def hangul_install_command():
    executable=hangul_python_executable()
    return f'"{executable}" -m pip install "python-hwpx==6.6.0"' if executable else ''


def hangul_environment_report(installed_version='',module_path=''):
    return (f'{APP_NAME} v{APP_VERSION}\n'
            f'실행 방식: {"EXE" if getattr(sys,"frozen",False) else "Python"}\n'
            f'실행 파일: {sys.executable}\n'
            f'Python 버전: {sys.version.split()[0]}\n'
            f'프로그램 파일: {Path(__file__).resolve()}\n'
            f'python-hwpx 버전: {installed_version or "확인되지 않음"}\n'
            f'hwpx 모듈 위치: {module_path or "확인되지 않음"}')


class HangulDependencyError(ValueError):
    def __init__(self,message,*,cause=None,installed_version='',module_path=''):
        import traceback
        self.message=message;self.install_command=hangul_install_command()
        self.details=message+'\n\n'+hangul_environment_report(installed_version,module_path)
        if cause is not None:
            self.details+='\n\n실제 오류:\n'+''.join(traceback.format_exception(type(cause),cause,cause.__traceback__)).strip()
        if self.install_command:self.details+='\n\n현재 실행 환경의 설치 명령:\n'+self.install_command
        else:self.details+='\n\nEXE 배포본에는 hwpx 모듈과 python-hwpx 배포 정보가 함께 포함되어야 합니다.'
        super().__init__(self.details)


def hangul_dependencies():
    """Check the active interpreter, preserving the real import/metadata failure."""
    import importlib
    import importlib.util
    from importlib.metadata import version, PackageNotFoundError
    # Refresh finders after a module is installed while the program is running.
    importlib.invalidate_caches();ver='';metadata_error=None;module_path=''
    try:ver=version('python-hwpx')
    except PackageNotFoundError as exc:metadata_error=exc
    try:
        spec=importlib.util.find_spec('hwpx')
        if spec is not None:module_path=spec.origin or ''
    except (ImportError,ValueError,AttributeError):pass
    try:
        import hwpx
        from hwpx import HwpxDocument
        module_path=getattr(hwpx,'__file__','') or module_path
    except ModuleNotFoundError as exc:
        message=('현재 뷰어의 실행 환경에서 hwpx 모듈을 찾지 못했습니다.' if exc.name=='hwpx' else
                 f'한글 모듈을 불러오던 중 필요한 모듈을 찾지 못했습니다: {exc.name or "확인되지 않음"}')
        raise HangulDependencyError(message,cause=exc,installed_version=ver,module_path=module_path) from exc
    except Exception as exc:
        raise HangulDependencyError('한글 모듈을 불러오는 과정에서 오류가 발생했습니다.',cause=exc,
                                    installed_version=ver,module_path=module_path) from exc
    if metadata_error is not None:
        raise HangulDependencyError('hwpx 모듈은 불러왔지만 설치 버전 정보를 확인하지 못했습니다.',
                                    cause=metadata_error,module_path=module_path) from metadata_error
    if ver!='6.6.0':
        raise HangulDependencyError(f'한글 변환에는 python-hwpx 6.6.0이 필요합니다. 현재 버전: {ver}',
                                    installed_version=ver,module_path=module_path)
    return HwpxDocument,ver


# Conversion controls are shared by the worker and the settings panel. Each
# numeric control participates in layout analysis or native paragraph formatting.
HANGUL_DEFAULTS = {'unified':dict(join=78,gap_weight=65,indent_weight=55,font_weight=80,
    space_gap=18,keep_pages=True,soft_breaks=False,keep_headers=True,cross_page=False,join_words=True,
    body_size=11,table_size=11,header_size=10,body_ratio=100,letter_spacing=0,line_spacing=160,
    paragraph_gap=6,keep_page_borders=True,keep_title_frames=True,keep_margins=True,
    fit_spacing=True,write_report=True)}


def hangul_options(mode='unified',values=None):
    if mode not in ('unified','visual','editable'):raise ValueError('한글 변환 방식을 확인하세요.')
    result=dict(HANGUL_DEFAULTS['unified'])
    for key,value in (values or {}).items():
        if key not in result:continue
        if isinstance(result[key],bool):result[key]=value if isinstance(value,bool) else str(value).lower() in ('1','true')
        else:
            lo,hi={'space_gap':(5,45),'body_size':(8,24),'table_size':(8,24),'header_size':(8,16),
                'body_ratio':(80,120),'letter_spacing':(-10,20),'line_spacing':(100,220),
                'paragraph_gap':(0,20)}.get(key,(0,100))
            result[key]=max(lo,min(hi,int(value)))
    if result['keep_pages']:result['cross_page']=False
    return result


def hangul_rect_union(rects):
    rects = list(rects)
    return (min(r[0] for r in rects), min(r[1] for r in rects),
            max(r[2] for r in rects), max(r[3] for r in rects)) if rects else (0,0,0,0)


def hangul_inside(rect, area):
    x, y = (rect[0]+rect[2])/2, (rect[1]+rect[3])/2
    return area[0]-.5 <= x <= area[2]+.5 and area[1]-.5 <= y <= area[3]+.5


def hangul_extract_lines(page, options, clip=None):
    """Char fragments -> baselines -> runs -> physical lines, without rewriting.

    Old Hangul Type3 PDFs frequently split a single baseline into word-sized PDF
    lines. Group the actual characters first; PDF block/line IDs are not prose.
    Wide gutters remain separate so columns and table cells are not concatenated.
    """
    import statistics
    import unicodedata
    chars, rotated = [], []
    for block in page.get_text('rawdict',clip=clip)['blocks']:
        if block['type'] != 0:
            continue
        for line in block['lines']:
            if abs(line['dir'][0]-1) > .02 or abs(line['dir'][1]) > .02:
                rotated.append(tuple(line['bbox']))
                continue
            for span in line['spans']:
                style = {k: span[k] for k in ('size','font','flags','color')}
                for char in span['chars']:
                    s = ''.join(c for c in char['c'] if (ord(c) >= 32 or c == '\t')
                                and c not in '\ufffe\uffff')
                    if s:
                        chars.append(dict(text=s, bbox=tuple(char['bbox']),
                                          y=char['origin'][1], **style))
    rows = []
    for char in sorted(chars, key=lambda c: (round(c['y'],1), c['bbox'][0])):
        row = next((r for r in reversed(rows[-5:])
                    if abs(r['y']-char['y']) <= max(1, min(r['size'],char['size'])*.16)), None)
        if row is None:
            rows.append(dict(y=char['y'], size=char['size'], chars=[char]))
        else:
            row['chars'].append(char)
    lines = []
    for row in rows:
        ordered = sorted(row['chars'], key=lambda c: c['bbox'][0])
        groups, group, prev = [], [], None
        for char in ordered:
            # Coincident invisible/visible text layers must not double the text.
            if prev and char['text'] == prev['text'] and max(abs(a-b) for a,b in zip(char['bbox'],prev['bbox'])) < .3:
                continue
            if prev and char['bbox'][0]-prev['bbox'][2] > max(24, 2.6*char['size']):
                groups.append(group);group=[]
            group.append(char);prev=char
        if group:groups.append(group)
        for group in groups:
            runs=[];prev=None
            for char in group:
                text=char['text']
                if prev and not prev['text'].isspace() and not text.isspace():
                    if char['bbox'][0]-prev['bbox'][2] > max(.7, char['size']*options['space_gap']/100):
                        text=' '+text
                key=(round(char['size'],2), char['font'], char['flags'], char['color'])
                if runs and runs[-1]['key']==key:
                    runs[-1]['text']+=text
                    runs[-1]['bbox']=hangul_rect_union([runs[-1]['bbox'],char['bbox']])
                else:
                    runs.append(dict(key=key,text=text,bbox=char['bbox'],size=char['size'],
                                     bold=bool(char['flags']&16),italic=bool(char['flags']&2),color=char['color']))
                prev=char
            if not runs:continue
            runs[0]['text']=runs[0]['text'].lstrip();runs[-1]['text']=runs[-1]['text'].rstrip()
            text=''.join(r['text'] for r in runs)
            if not text.strip():continue
            for run in runs:
                ems=sum(1 if unicodedata.east_asian_width(c) in 'WF' else
                        .5 if c.isspace() else .28 if c in '.,:;!ilI\'|' else
                        .72 if c.isupper() else .5 for c in run['text'])
                run['ratio']=max(65,min(135,round(100*(run['bbox'][2]-run['bbox'][0])/max(1,ems*run['size']))))
                run.pop('key',None)
            lines.append(dict(text=text,runs=runs,bbox=hangul_rect_union(c['bbox'] for c in group),
                              y=row['y'],size=statistics.median(c['size'] for c in group),
                              fonts=tuple(sorted(set(c['font'] for c in group))),
                              bold=any(r['bold'] for r in runs)))
    return sorted(lines,key=lambda line:(line['bbox'][1],line['bbox'][0])), rotated


def hangul_regions(page, lines, rotated, dpi, options):
    """Detect ruled tables and bounded diagrams; never rasterize a whole page."""
    import pymupdf
    paths=page.get_drawings()
    simple=[p for p in paths if len(p['items'])<=8 and
            not any(i[0]=='c' for i in p['items']) and
            max(p['rect'].width,p['rect'].height)>25]
    tables=[]
    try:
        found=page.find_tables(paths=simple,strategy='lines_strict').tables if simple else []
    except (ValueError,RuntimeError):
        found=[]
    images=[tuple(i['bbox']) for i in page.get_image_info()]
    def crop(rect):
        r=(pymupdf.Rect(rect)+(-1,-1,1,1)) & page.rect
        scale=min(dpi/72,4000/max(1,r.width,r.height))
        return page.get_pixmap(matrix=pymupdf.Matrix(scale,scale),clip=r,
                              colorspace=pymupdf.csRGB,alpha=False).tobytes('png')
    for t in found:
        if t.row_count<2 or t.col_count<2 or t.row_count*t.col_count>2000:
            continue
        cells=[]
        for row in t.rows:
            cellrow=[]
            for rect in row.cells:
                if rect is None:cellrow.append(None);continue
                # Re-extract per cell BEFORE baseline merging. Adjacent columns
                # can have a smaller gap than ordinary word spacing in a PDF.
                cell_lines,_=hangul_extract_lines(page,options,clip=pymupdf.Rect(rect))
                pics=[r for r in images if hangul_inside(r,rect)]
                # Text and pictures can coexist in a cell; only crop each bounded
                # image region, rather than flattening the cell's native text.
                picrect=hangul_rect_union(pics) if pics else None
                cellrow.append(dict(bbox=tuple(rect),lines=cell_lines,
                                    image=crop(picrect) if picrect else None,image_bbox=picrect))
            cells.append(cellrow)
        if sum(bool(c and c['lines']) for row in cells for c in row)<2:
            continue
        tables.append(dict(kind='table',bbox=tuple(t.bbox),rows=t.row_count,cols=t.col_count,cells=cells))
    # Paths of Type3 glyphs are typically tiny. Only sizable contours with few
    # segments seed a diagram. A frame around the cover alone is not a diagram.
    regions=[]
    for path in paths:
        r=path['rect']
        if len(path['items'])>30 or max(r.width,r.height)<25:continue
        if r.get_area()>page.rect.get_area()*.72 or r.height>page.rect.height*.8:continue
        if any(hangul_inside(r,t['bbox']) for t in tables):continue
        if r.y1<page.rect.height*.13 or r.y0>page.rect.height*.94:continue
        regions.append(dict(bbox=tuple(r),large=int(r.width>35 and r.height>20)))
    clusters=[]
    for region in regions:
        box=pymupdf.Rect(region['bbox'])+(-5,-5,5,5)
        matches=[c for c in clusters if box.intersects(pymupdf.Rect(c['bbox']))]
        if matches:
            region={'bbox':hangul_rect_union([region['bbox']]+[c['bbox'] for c in matches]),
                    'large':region['large']+sum(c['large'] for c in matches)}
            clusters=[c for c in clusters if c not in matches]
        clusters.append(region)
    figures=[]
    for cluster in clusters:
        rect=cluster['bbox'];r=pymupdf.Rect(rect)
        contained=[l for l in lines if hangul_inside(l['bbox'],rect)]
        if cluster['large']>=3 and r.width>60 and r.height>60 and len(contained)>=3:
            # Some text protrudes beyond connector bounds; include only text
            # intersecting the diagram, never its caption or neighboring prose.
            rect=hangul_rect_union([rect]+[l['bbox'] for l in contained])
            if pymupdf.Rect(rect).get_area()<page.rect.get_area()*.72:
                figures.append(dict(kind='figure',bbox=rect,image=crop(rect),text_lines=len(contained)))
    candidates=images+rotated
    for rect in candidates:
        if any(hangul_inside(rect,t['bbox']) for t in tables+figures):continue
        r=pymupdf.Rect(rect)
        if r.get_area()>page.rect.get_area()*.72:
            # A scanned page with an OCR layer is rebuilt from its OCR text.
            # A scan without text is rejected by the caller, not silently pasted.
            continue
        overlaps=[f for f in figures if (pymupdf.Rect(f['bbox'])+(-2,-2,2,2)).intersects(r)]
        if overlaps:
            rect=hangul_rect_union([rect]+[f['bbox'] for f in overlaps])
            figures=[f for f in figures if f not in overlaps]
        figures.append(dict(kind='figure',bbox=rect,image=crop(rect),text_lines=0))
    return tables,figures


def hangul_line_kind(line, body_size):
    text=line['text'].strip()
    if re.match(r'^[<〈《\[]\s*(그림|표|Figure|Table)\s*\d',text,re.I):return 'caption'
    if re.match(r'^(?:\d+(?:\.\d+)*[.)]?\s+|[가-힣A-Z][.)]\s+)',text):
        return 'heading' if len(text)<65 and line['size']>=body_size*1.025 else 'list'
    if re.match(r'^(?:\([가-힣A-Za-z0-9]+\)|[○●ㅇ•․▪■※]|[-–]\s)',text):return 'list'
    if re.match(r'^[가-힣 ]{2,15}\s*[:：]',text):return 'label'
    if line['size']>body_size*1.13 or (line['bold'] and len(text)<55):return 'heading'
    return 'body'


def hangul_order_lines(lines, left, right):
    """Conservative column boundary: only split on a repeated, empty gutter."""
    if len(lines)<8:return sorted(lines,key=lambda l:(l['bbox'][1],l['bbox'][0]))
    width=right-left
    for fraction in (.5,.42,.58):
        x=left+width*fraction
        a=[l for l in lines if l['bbox'][2]<x-5]
        b=[l for l in lines if l['bbox'][0]>x+5]
        spanning=[l for l in lines if l not in a and l not in b]
        if len(a)>=4 and len(b)>=4 and not spanning:
            return sorted(a,key=lambda l:l['bbox'][1])+sorted(b,key=lambda l:l['bbox'][1])
    return sorted(lines,key=lambda l:(l['bbox'][1],l['bbox'][0]))


def hangul_paragraphs(lines, options, body_size, bounds):
    """Physical lines -> coherent native paragraphs using adjustable evidence.

    List/heading starts and column jumps are hard boundaries. Sentence-ending
    punctuation is evidence, not an automatic paragraph break: one paragraph
    can contain several sentences, just as an editable word processor expects.
    """
    paragraphs=[]
    left,right=bounds
    for line in hangul_order_lines(lines,left,right):
        kind=hangul_line_kind(line,body_size)
        merge=False
        if paragraphs:
            para=paragraphs[-1];prev=para['lines'][-1]
            size=max(1,(prev['size']+line['size'])/2)
            delta=line['y']-prev['y']
            dy=delta/size
            dx=abs(line['bbox'][0]-prev['bbox'][0])/size
            overlap=min(line['bbox'][2],prev['bbox'][2])-max(line['bbox'][0],prev['bbox'][0])
            if kind=='body' and para['kind'] in ('body','list') and .55<dy<2.85 and overlap>size:
                gap_score=max(0,1-abs(dy-1.55)/1.3)
                # A hanging indent after a bullet is expected, not a new block.
                indent_score=max(0,1-dx/4) if para['kind']=='list' else max(0,1-dx/2.2)
                font_score=max(0,1-abs(prev['size']-line['size'])/size*5)
                if prev.get('fonts')!=line.get('fonts'):font_score*=.55
                weights=[options[k] for k in ('gap_weight','indent_weight','font_weight')]
                score=sum(v*w for v,w in zip((gap_score,indent_score,font_score),weights))/max(1,sum(weights))
                end=prev['text'].rstrip()
                if re.search(r'[.!?。][”’"\')]*$',end) and prev['bbox'][2]<right-size*2:score-=.22
                if prev['bbox'][2]<right-size*5:score-=.20
                merge=score >= .96-options['join']*.005
                if (para['kind']=='list' and len(para['lines'])==1 and
                    re.match(r'^[○●ㅇ■]',prev['text']) and prev['bbox'][2]<right-size*6):
                    merge=False  # Short bullet section label, then a new paragraph.
        if merge:
            paragraphs[-1]['lines'].append(line)
            paragraphs[-1]['bbox']=hangul_rect_union([paragraphs[-1]['bbox'],line['bbox']])
        else:
            paragraphs.append(dict(kind=kind,lines=[line],bbox=line['bbox']))
    return paragraphs


def hangul_join_separator(before, after, vocabulary=None, join_words=True):
    """Recover physical line wrapping only; no language-model paraphrasing."""
    if not before or not after or before[-1].isspace() or after[0].isspace():return ''
    if after[0] in ',.;:!?)]}〉》”’' or before[-1] in '([{〈《“‘':return ''
    if re.search(r'[.!?。][”’"\')]*$',before):return ' '
    if not join_words:return ' '
    left=re.search(r'([가-힣]+)$',before);right=re.match(r'([가-힣]+)',after)
    if left and right:
        a,b=left[1],right[1];word=a+b;vocabulary=vocabulary or set()
        if word in vocabulary:return ''
        # Reuse words already found elsewhere in this document, including a
        # different particle ending. This never substitutes or invents letters.
        stem=re.sub(r'(으로서|으로써|에게|에서|으로|에는|에도|까지|부터|은|는|이|가|을|를|의|에|와|과|로)$','',word)
        if len(stem)>=3 and any(v.startswith(stem) for v in vocabulary):return ''
        if len(a)==1 and a not in '이그저각본및등내외전후위수중한첫두세네더큰':return ''
        if len(b)==1 and b in '다며고면':return ''
    # A short particle beginning the next line is strong evidence of a word
    # split. Other cases remain a space, because PDF geometry is not morphology.
    if re.match(r'^(?:으로서|으로써|으로|에서|에게|까지|부터|이라는|이라고|이라|이나|에는|에도|하여|하며|도록|적인|적으로|의|을|를|은|는|에|로)(?:\s|[,.])',after):return ''
    return ' '


def hangul_analyze(pages, options, dpi, progress=None):
    import pymupdf
    import statistics
    from collections import Counter
    models=[]
    for index,(path,number) in enumerate(pages):
        if progress:progress(index,len(pages),f'{index+1} / {len(pages)}쪽 · 글자와 표 분석')
        with editable_copy(path,int(number)) as work:
            page=work[0];page.remove_rotation()
            w,h=page.rect.width,page.rect.height
            if max(w,h)>4000:raise ValueError('너무 큰 용지입니다. 일반 용지 크기로 먼저 조정하세요.')
            lines,rotated=hangul_extract_lines(page,options)
            if not lines and page.get_image_info():
                raise ValueError(f'{index+1}쪽은 추출 가능한 글자가 없는 스캔입니다. OCR로 글자를 인식한 PDF를 먼저 만드세요. 페이지 전체를 그림으로 대신 저장하지 않습니다.')
            tables,figures=hangul_regions(page,lines,rotated,dpi,options)
            decorations=[]
            for drawing in page.get_drawings():
                if drawing['type']!='s' or len(drawing['items'])>4:continue
                if any(hangul_inside(drawing['rect'],r['bbox']) for r in tables+figures):continue
                for item in drawing['items']:
                    if item[0]!='l':continue
                    a,b=item[1:3]
                    if max(abs(a.x-b.x),abs(a.y-b.y))<25:continue
                    if abs(a.x-b.x)>.5 and abs(a.y-b.y)>.5:continue
                    decorations.append(dict(a=tuple(a),b=tuple(b),width=drawing.get('width',.5),
                                            color=drawing.get('color') or (0,0,0)))
            body_size=statistics.median(l['size'] for l in lines) if lines else 11
            models.append(dict(path=str(path),number=int(number),index=index,width=w,height=h,
                lines=lines,tables=tables,figures=figures,body_size=body_size,
                cover=bool(len(lines)<12 and body_size>14),rotated=len(rotated),decorations=decorations))
    key=lambda s:re.sub(r'\s+','',s)
    header_occurrences={(key(l['text']),m['path'],m['number']) for m in models for l in m['lines']
                        if l['bbox'][1]<m['height']*.13}
    counts=Counter(text for text,path,number in header_occurrences)
    unique_pages=len({(m['path'],m['number']) for m in models})
    for m in models:
        w,h=m['width'],m['height']
        m['headers']=[];m['footers']=[]
        native=[]
        for line in m['lines']:
            if any(hangul_inside(line['bbox'],r['bbox']) for r in m['tables']+m['figures']):continue
            if not m['cover'] and line['bbox'][1]<h*.13 and counts[key(line['text'])]>=max(2,unique_pages//3):
                m['headers'].append(line)
            elif line['bbox'][1]>h*.92 and re.fullmatch(r'\s*[-–]?\s*\d+\s*[-–]?\s*',line['text']):
                m['footers'].append(line)
            else:native.append(line)
        all_rects=[l['bbox'] for l in native]+[r['bbox'] for r in m['tables']+m['figures']]
        bounds=hangul_rect_union(all_rects) if all_rects else (50,50,w-50,h-50)
        m['bounds']=bounds
        # Native paragraphs cannot span an intervening picture or table.
        regions=sorted(m['tables']+m['figures'],key=lambda r:r['bbox'][1])
        pending=list(native);blocks=[]
        for region in regions:
            before=[l for l in pending if l['bbox'][1]<region['bbox'][1]]
            pending=[l for l in pending if l not in before]
            blocks.extend(hangul_paragraphs(before,options,m['body_size'],(bounds[0],bounds[2])))
            blocks.append(region)
        blocks.extend(hangul_paragraphs(pending,options,m['body_size'],(bounds[0],bounds[2])))
        m['blocks']=blocks
    return models


def hangul_normalize_document(doc,roles,options,font,stats):
    """Final document-wide pass AFTER joining: discard source span typography.

    All body/list paragraphs share one character style. Headings use a small,
    deterministic hierarchy; table text, captions and running text each have an
    explicit style. Coalesce fragment runs, retaining section/object controls.
    """
    HP='{http://www.hancom.co.kr/hwpml/2011/paragraph}'
    header=doc.parts.headers[0];styles={};formats={};normalized=[]
    for paragraph,kind,cover,cell in roles:
        text=paragraph.text or ''
        if not text.strip():continue
        # Short numbered section titles sometimes use the same PDF font size
        # as body text. Classify them after joining so their style is consistent.
        if (not cell and not cover and len(text)<90 and '\n' not in text and
                re.match(r'^\d+(?:\.\d+)*\.?\s+\S',text) and
                not re.search(r'[.!?。]$',text)):
            kind='heading'
        size=options['table_size'] if cell else options['body_size']
        bold=False;align='LEFT';level=0;before=0;after=options['paragraph_gap']
        left=first=0
        if kind=='heading':
            match=re.match(r'^(\d+(?:\.\d+)*)\.?\s',text)
            level=min(3,match[1].count('.')+1) if match else 0
            size=options['body_size']+(4 if level==0 else max(1,4-level))
            bold=True;before=10;after=6;align='CENTER' if level==0 else 'LEFT'
        elif kind=='title':
            size=options['body_size']+7;bold=True;align='CENTER';before=0;after=0
        elif kind=='subheading':
            size=options['body_size']+1;bold=True;before=0;after=6
        elif cover:
            size=options['body_size']+5;align='CENTER';before=0;after=0
        elif kind=='caption':
            bold=True;align='CENTER';before=5;after=5
        elif kind in ('running','footer','header_cell'):
            size=options['header_size'];after=0
            align='CENTER' if kind in ('footer','header_cell') else 'LEFT'
        elif kind=='list':
            level=1 if re.match(r'^\([가-힣A-Za-z]\)',text) else 0
            left=3.5+(3.5*level);first=-3.5
        if cell and kind not in ('title','header_cell'):
            before=0;after=2;left=first=0
            if kind=='table_list':
                # Hancom's negative indent moves FOLLOWING lines; adding a
                # left margin as well would apply the inset twice. Preserve
                # the source marker/space, like Ctrl+Shift+Tab at the first
                # text character, rather than adding a tab control.
                match=re.match(r'^([○●ㅇ•․·▪■※\-–]\s*|\([가-힣A-Za-z0-9]+\)\s*|\d+(?:\.\d+)*[.)]?\s+|[가-힣A-Z][.)]\s+)',text)
                if match:
                    from hwpx.form_fit.measure import estimate_text_width,TextStyle
                    prefix=match[0].rstrip()+' '
                    text=prefix+text[match.end():]
                    measure=TextStyle(ratio=options['body_ratio'],spacing=options['letter_spacing'])
                    first=-round(estimate_text_width(prefix,size,measure)*25.4/7200,3)
        line=100 if kind in ('running','footer','header_cell') else options['line_spacing']
        ck=(size,bold,kind=='subheading')
        if ck not in styles:
            styles[ck]=doc.styles.ensure_run(font=font,size=size,bold=bold,italic=False,underline=kind=='subheading',
                strike=False,color='#000000',ratio=options['body_ratio'],letter_spacing=options['letter_spacing'])
        pk=(align,line,left,first,before,after,kind=='heading')
        if pk not in formats:
            # Use the public human-unit API here, avoiding doubled margin units.
            result=doc.styles.apply_paragraph_format(paragraphs=[paragraph],alignment=align,
                line_spacing_percent=line,indent_left_mm=left,indent_right_mm=0,
                first_line_indent_mm=first,spacing_before_pt=before,spacing_after_pt=after,
                keep_with_next=kind=='heading',keep_lines=False,page_break_before=False)
            formats[pk]=paragraph.para_pr_id_ref
        else:paragraph.para_pr_id_ref=formats[pk]
        # Only text-only runs are removed. The anchor's secPr, colPr and object
        # runs survive, and the reconstructed paragraph is one editable text run.
        for run in list(paragraph.element.findall(HP+'run')):
            if all(c.tag==HP+'t' for c in run):paragraph.element.remove(run)
            else:
                for node in list(run.findall(HP+'t')):run.remove(node)
        paragraph.add_run(text,char_pr_id_ref=styles[ck],expand_special_characters=True)
        paragraph.char_pr_id_ref=styles[ck]
        for cache in list(paragraph.element.findall(HP+'linesegarray')):paragraph.element.remove(cache)
        paragraph._pdf_format=dict(size=size,align=align,line=line,left=left,first=first,before=before,after=after,keep=kind=='heading',style=styles[ck],kind=kind)
        paragraph.section.mark_dirty();normalized.append((kind,cell,cover,styles[ck],formats[pk]))
    stats['normalized_paragraphs']=len(normalized)
    stats['body_character_styles']=len({cs for kind,cell,cover,cs,ps in normalized if kind in ('body','list','label') and not cell and not cover})
    stats['normalization']={key:options[key] for key in ('body_size','table_size','body_ratio','letter_spacing','line_spacing','paragraph_gap')}


HP_HANGUL='{http://www.hancom.co.kr/hwpml/2011/paragraph}'


def hangul_detect_frames(model):
    """Closed axis-aligned frames from PDF rules; not arbitrary text boxes."""
    segments=model['decorations'];vertical=[];horizontal=[];frames=[]
    for line in segments:
        a,b=line['a'],line['b']
        if abs(a[0]-b[0])<.6:vertical.append((a[0],min(a[1],b[1]),max(a[1],b[1])))
        if abs(a[1]-b[1])<.6:horizontal.append((a[1],min(a[0],b[0]),max(a[0],b[0])))
    for i,a in enumerate(vertical):
        for b in vertical[i+1:]:
            if abs(a[1]-b[1])>.7 or abs(a[2]-b[2])>.7:continue
            x0,x1=sorted((a[0],b[0]));y0,y1=a[1:]
            if x1-x0<20 or y1-y0<10:continue
            edges=[y for y,l,r in horizontal if l<=x0+1 and r>=x1-1 and y0-.7<=y<=y1+.7]
            if not any(abs(y-y0)<.7 for y in edges) or not any(abs(y-y1)<.7 for y in edges):continue
            box=(x0,y0,x1,y1)
            if any(max(abs(x-y) for x,y in zip(box,f['bbox']))<1 for f in frames):continue
            frames.append({'bbox':box,'rows':sorted(set(round(v,2) for v in edges))})
    return sorted(frames,key=lambda f:(f['bbox'][2]-f['bbox'][0])*(f['bbox'][3]-f['bbox'][1]),reverse=True)


def hangul_prepare_template(model,options):
    """Promote real form elements, then regroup the remaining native body."""
    frames=hangul_detect_frames(model);w,h=model['width'],model['height']
    outer=next((f for f in frames if f['bbox'][2]-f['bbox'][0]>w*.6 and f['bbox'][3]-f['bbox'][1]>h*.6),None)
    small=[f for f in frames if f is not outer]
    header=next((f for f in small if f['bbox'][1]<h*.16 and f['bbox'][3]<h*.19
                 and f['bbox'][2]-f['bbox'][0]<w*.65 and
                 any(hangul_inside(l['bbox'],f['bbox']) for l in model['lines'])),None)
    if header:
        model['headers']=[l for l in model['lines'] if hangul_inside(l['bbox'],header['bbox'])]
    title_frames=[f for f in small if f is not header and f['bbox'][1]<h*.55
                  and any(hangul_inside(l['bbox'],f['bbox']) for l in model['lines'])]
    excluded={id(l) for l in model['headers']+model['footers']}
    for region in model['tables']+model['figures']:
        excluded.update(id(l) for l in model['lines'] if hangul_inside(l['bbox'],region['bbox']))
    regions=list(model['tables'])+list(model['figures'])
    for f in title_frames:
        lines=[l for l in model['lines'] if id(l) not in excluded and hangul_inside(l['bbox'],f['bbox'])]
        if not lines:continue
        if options['keep_title_frames']:
            regions.append(dict(kind='title_table',bbox=f['bbox'],lines=lines))
            excluded.update(id(l) for l in lines)
    native=[l for l in model['lines'] if id(l) not in excluded]
    rects=[l['bbox'] for l in native]+[r['bbox'] for r in regions]
    bounds=hangul_rect_union(rects) if rects else (50,100,w-50,h-50)
    blocks=[];pending=native
    for region in sorted(regions,key=lambda b:(b['bbox'][1],b['bbox'][0])):
        before=[l for l in pending if l['bbox'][1]<region['bbox'][1]]
        pending=[l for l in pending if l not in before]
        blocks.extend(hangul_paragraphs(before,options,model['body_size'],(bounds[0],bounds[2])))
        blocks.append(region)
    blocks.extend(hangul_paragraphs(pending,options,model['body_size'],(bounds[0],bounds[2])))
    model.update(blocks=blocks,bounds=bounds,page_frame=outer,header_frame=header,title_frames=title_frames)
    # A single underlined heading is a character style, not a floating rule.
    used=[f['bbox'] for f in frames]
    for block in blocks:
        if 'lines' not in block or block['kind']=='title_table':continue
        bb=block['bbox']
        block['underline']=any(abs(d['a'][1]-d['b'][1])<.6 and abs(d['a'][1]-bb[3])<2
            and abs(min(d['a'][0],d['b'][0])-bb[0])<2
            and abs(max(d['a'][0],d['b'][0])-bb[2])<3
            and not any(abs(d['a'][1]-f[1])<1 or abs(d['a'][1]-f[3])<1 for f in used)
            for d in model['decorations'])
    if options['keep_margins']:
        left=max(24,min(bounds[0],w*.23));right=max(24,min(w-bounds[2],w*.23))
        if header and options['keep_headers']:left=min(left,header['bbox'][0])
        if outer:
            left=max(left,outer['bbox'][0]+10);right=max(right,w-outer['bbox'][2]+10)
        top=max(24,min(bounds[1],h*.38))
    else:left=right=min(60,w*.1);top=52
    header_box=header['bbox'] if header else hangul_rect_union(l['bbox'] for l in model['headers'])
    if options['keep_headers'] and model['headers']:
        head_top=max(12,header_box[1]);top=max(top,header_box[3]+8)
        head_height=top-head_top
    else:head_top=top;head_height=0
    foot_size=options['header_size'] if options['keep_headers'] and model['footers'] else 0
    foot_bottom=(max(16,h-max(l['bbox'][3] for l in model['footers'])) if foot_size else 48)
    foot_height=(foot_size+6 if foot_size else 0)
    limit=h-foot_bottom-foot_height
    if outer:limit=min(limit,outer['bbox'][3]-10)
    model['layout']=dict(left=left,right=right,body_top=top,top=head_top,header=head_height,
                         bottom=h-limit-foot_height,footer=foot_height,body_bottom=limit,
                         width=w-left-right,capacity=limit-top)


def hangul_paragraph_measure(paragraph,width,options):
    """Estimated height only: no installed Hancom renderer is implied."""
    from hwpx.form_fit.measure import estimate_lines,TextStyle
    s=paragraph._pdf_format
    style=TextStyle(ratio=options['body_ratio'],spacing=options['letter_spacing'],
                    indent=round(s['first']*7200/25.4))
    available=max(20,width-s['left']*72/25.4)
    n=estimate_lines(paragraph.text,available*100,s['size'],style=style)
    return dict(lines=n,height=s['before']+s['after']+n*s['size']*s['line']/100)


def hangul_paragraph_spacer(doc,paragraph,points,alignment=None):
    s=paragraph._pdf_format;s['before']=max(0,points)
    doc.styles.apply_paragraph_format(paragraphs=[paragraph],alignment=alignment or s['align'],
        line_spacing_percent=s['line'],indent_left_mm=s['left'],indent_right_mm=0,
        first_line_indent_mm=s['first'],spacing_before_pt=s['before'],spacing_after_pt=s['after'],
        keep_with_next=s['keep'],keep_lines=False,page_break_before=False)


def hangul_picture_line(paragraph,width,height):
    HP=HP_HANGUL;root=paragraph.element
    for old in list(root.findall(HP+'linesegarray')):root.remove(old)
    array=root.makeelement(HP+'linesegarray',{})
    array.append(root.makeelement(HP+'lineseg',{k:str(v) for k,v in dict(textpos=0,vertpos=0,
        vertsize=round(height*100),textheight=round(height*100),baseline=round(height*100),spacing=0,
        horzpos=0,horzsize=round(width*100),flags=393216).items()}))
    root.append(array);paragraph.section.mark_dirty()


def hangul_body_text(section):
    """Ordered body text, including cells, excluding duplicated story mirrors."""
    HP=HP_HANGUL;parts=[]
    def walk(e):
        if e.tag in (HP+'secPr',HP+'ctrl'):return
        if e.tag==HP+'t':parts.append(''.join(e.itertext()));return
        for child in e:walk(child)
    for p in section.paragraphs:walk(p.element)
    return ''.join(parts)


def hangul_story_text(section,kind):
    HP=HP_HANGUL
    stories=section.properties.headers if kind=='header' else section.properties.footers
    return ''.join(''.join(t.itertext()) for story in stories for t in story.element.iter(HP+'t'))


def hangul_style_snapshot(doc):
    """Compare used text/paragraph properties across native serialization."""
    HP=HP_HANGUL;HH='{http://www.hancom.co.kr/hwpml/2011/head}'
    HC='{http://www.hancom.co.kr/hwpml/2011/core}';root=doc.parts.headers[0].element
    chars={e.get('id'):e for e in root.iter(HH+'charPr')}
    paras={e.get('id'):e for e in root.iter(HH+'paraPr')};out=[]
    def attrs(node):return tuple(sorted(node.attrib.items())) if node is not None else ()
    def walk(node):
        if node.tag in (HP+'secPr',HP+'ctrl'):return
        if node.tag==HP+'p':
            used=[]
            for run in node.findall(HP+'run'):
                text=''.join(''.join(t.itertext()) for t in run.findall(HP+'t'))
                if not text.strip():continue
                char=chars[run.get('charPrIDRef')]
                used.append((re.sub(r'\s+','',text),char.get('height'),char.get('textColor'),
                    tuple(attrs(char.find(HH+k)) for k in ('fontRef','ratio','spacing')),
                    tuple(char.find(HH+k) is not None for k in ('bold','italic')),
                    attrs(char.find(HH+'underline'))))
            if used:
                para=paras[node.get('paraPrIDRef')]
                spacing=next(para.iter(HH+'lineSpacing'),None)
                # HWP's percentage field has no separate XML unit token.
                line=(spacing.get('type'),spacing.get('value')) if spacing is not None else ()
                shape=(attrs(para.find(HH+'align')),
                    tuple(attrs(next(para.iter(HC+k),None)) for k in ('intent','left','right','prev','next')),
                    line,attrs(para.find(HH+'breakSetting')))
                out.append((tuple(used),shape))
        for child in node:walk(child)
    for section in doc.sections:
        for p in section.paragraphs:walk(p.element)
        for story in list(section.properties.headers)+list(section.properties.footers):walk(story.element)
    return out


def hangul_write_audit_report(result,path):
    """Evidence checklist, never an invented visual-fidelity percentage."""
    escape=html.escape;rows=[]
    for p in result['page_checks']:
        state='확인 필요' if p['warnings'] else '구조 통과'
        forms=f"머리말 {p['headers']} · 제목 틀 {p['title_frames']} · 쪽 테두리 {p['page_borders']}"
        rows.append('<tr>'+''.join('<td>'+escape(str(v))+'</td>' for v in
            [p['index'],f"{p['source']} / {p['source_page']}쪽",p['paragraphs'],
             '통과' if p['content_ok'] else '실패','통과' if p['style_ok'] else '실패',forms,
             f"{p['estimated_height_pt']:.1f} / {p['available_height_pt']:.1f} pt",state,
             ' / '.join(p['warnings']) or '실제 한컴 화면 확인 전'])+'</tr>')
    n=result['normalization'];summary=f"본문 {n['body_size']}pt · 장평 {n['body_ratio']}% · 자간 {n['letter_spacing']}% · 줄 간격 {n['line_spacing']}% · 문단 뒤 {n['paragraph_gap']}pt"
    document='''<!doctype html><html lang="ko"><meta charset="utf-8"><title>한글 변환 검사</title>
<style>body{font:15px/1.6 sans-serif;margin:32px;color:#182333;background:#f7f8fb}h1{font-size:26px}main{background:white;padding:28px;border-radius:16px}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border:1px solid #d6dce6;padding:9px;text-align:left}th{background:#eaf0fa}small{color:#556070}.note{border-left:4px solid #ad303c;padding:12px;background:#fff5f6}</style><main>'''
    document+=f'<h1>한글 통합 변환 · 검사 결과</h1><p>{escape(Path(result["output"]).name)}</p><p>{escape(summary)}</p>'
    document+=f'<p>원본 {result["pages"]}쪽 · 본문 글상자 0개 · 문서 구조 검사 통과 · 본문 문자/순서 검사 통과 · 서식 검사 통과</p>'
    review=sum(bool(p['warnings']) for p in result['page_checks'])
    document+=f'<p>원본 쪽별 문자·순서 {result["pages"]}/{result["pages"]} 통과 · 별도 검토 표시 {review}쪽 · 머리말 표 {result["header_tables"]}개 · 제목 틀 {result["title_tables"]}개 · 쪽 테두리 {result["page_borders"]}개</p>'
    document+='<p class="note">이 표는 저장된 문서 구조와 문자·서식을 검사한 결과입니다. 높이는 글꼴 파일을 사용하지 않은 추정치이며 실제 한컴의 쪽 수·겹침·글자 모양을 보증하지 않습니다. 완성도 100% 또는 시각적 일치율을 뜻하지 않습니다.</p>'
    if result.get('spacing_adjustment'):document+='<p>'+escape(result['spacing_adjustment'])+'</p>'
    document+='<table><thead><tr>'+''.join('<th>'+v+'</th>' for v in ['순서','원본','문단','문자·순서','본문 서식','복원 양식','예상 높이 / 공간','상태','확인 사항'])+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
    document+='<p>검사 범위: 본문·표의 문자 및 순서, 글상자 부재, 지정 글자/문단 서식, 머리말·꼬리말 저장, 쪽 테두리 저장. 부분 그림 안의 글자는 편집 가능한 본문에 포함되지 않습니다.</p>'
    document+='<p>출처: <a href="https://github.com/airmang/python-hwpx/releases/tag/v6.6.0">python-hwpx 6.6.0</a> · <a href="https://help.hancom.com/hoffice/multi/ko_kr/hwp/format/setting_paper/setting_paper(margins).htm">한컴 용지 여백 설명</a></p></main></html>'
    with open(path,'x',encoding='utf-8') as f:f.write(document)


def convert_pdf_to_hangul(pages,output,*,mode='unified',dpi=300,font='함초롬바탕',options=None,progress=None):
    """One native paragraph writer. Options preserve forms, never text boxes."""
    import warnings
    from collections import Counter
    HwpxDocument,writer_version=hangul_dependencies();options=hangul_options(mode,options)
    output=Path(output)
    if output.suffix.lower() not in ('.hwp','.hwpx'):raise ValueError('저장 형식은 .hwp 또는 .hwpx여야 합니다.')
    if not pages:raise ValueError('변환할 PDF 페이지가 없습니다.')
    if not 144<=int(dpi)<=600:raise ValueError('그림 해상도를 확인하세요.')
    models=hangul_analyze(pages,options,int(dpi),progress)
    for model in models:hangul_prepare_template(model,options)
    output.parent.mkdir(parents=True,exist_ok=True)
    stage=output.parent/('.'+output.stem+'-'+uuid.uuid4().hex+'.tmp'+output.suffix)
    doc=HwpxDocument.new();HP=HP_HANGUL;sections=[];roles=[];records=[];current=None;previous=None
    stats=dict(pages=len(models),paragraphs=0,joined_lines=0,cross_page_joins=0,tables=0,figures=0,
        image_table_cells=0,body_textboxes=0,writer=writer_version,mode='unified',dpi=int(dpi),warnings=[],
        options=options.copy(),omitted_header_lines=0,word_joins=0,header_tables=0,title_tables=0,page_borders=0)
    normalized=lambda text:re.sub(r'\s+','',text)
    vocabulary={word for m in models for l in m['lines'] for word in re.findall(r'[가-힣]{2,}',l['text'])}
    border=doc.styles.ensure_border_fill(border_color='#000000',border_width='0.12 mm')
    no_border=doc.styles.ensure_border_fill(active_borders=[])
    one=doc.styles.ensure_run(font=font,size=1,ratio=100,letter_spacing=0)
    def template_key(m):
        return (m['path'],round(m['width']),round(m['height']),m['cover'],bool(m['page_frame']),
                tuple(l['text'] for l in m['headers']) if options['keep_headers'] else ())
    def plain(lines,soft=False):
        out='';before=''
        for line in lines:
            sep=('\n' if soft else hangul_join_separator(before,line['text'],vocabulary,options['join_words'])) if before else ''
            if before and not sep and re.search(r'[가-힣]$',before) and re.match(r'[가-힣]',line['text']):stats['word_joins']+=1
            out+=sep+line['text'];before=line['text']
        return out
    def host(m):
        p=m.pop('anchor',None)
        if p is None:p=doc.add_paragraph(section=m['section'],include_run=False)
        p.char_pr_id_ref=one
        doc.styles.apply_paragraph_format(paragraphs=[p],line_spacing_percent=100,spacing_before_pt=0,spacing_after_pt=0)
        return p
    def write_text(p,text,kind,m,cell=False,cover=None):
        p.add_run(text,expand_special_characters=True)
        roles.append((p,kind,m['cover'] if cover is None else cover,cell));stats['paragraphs']+=1
        records.append(dict(paragraph=p,source=m['index'],kind=kind,cell=cell))
        return p
    try:
        for m in models:
            key=template_key(m)
            if current is None or options['keep_pages'] or key!=previous:
                current=doc.sections[0] if not sections else doc.add_section();sections.append(current)
                m['first_section_page']=True
            else:m['first_section_page']=False
            m['section']=current;previous=key;m['elements']=[]
            if not m['first_section_page']:continue
            lay=m['layout'];sec=current
            # add_section clones the preceding section, including all three
            # parity variants. Explicitly reset them even on borderless pages.
            for variant in ('BOTH','EVEN','ODD'):
                sec.properties.set_page_border_fill(page_type=variant,border_fill_id_ref=no_border,
                    text_border='PAPER',header_inside=False,footer_inside=False,fill_area='PAPER',
                    offset_left=0,offset_right=0,offset_top=0,offset_bottom=0)
            doc.page.set_size(width=round(m['width']*100),height=round(m['height']*100),
                              orientation='LANDSCAPE' if m['width']>m['height'] else 'PORTRAIT',section=sec)
            doc.page.set_margins(section=sec,**{k:round(lay[k]*100) for k in ('left','right','top','bottom','header','footer')},gutter=0)
            m['anchor']=sec.paragraphs[0]
            # Explicit empty stories stop a preceding section's form inheriting.
            header=doc.page.set_header(text='',section=sec);footer=doc.page.set_footer(text='',section=sec)
            for story in (header,footer):
                p=story.paragraphs[0];p.char_pr_id_ref=one
                doc.styles.apply_paragraph_format(paragraphs=[p],line_spacing_percent=100,spacing_before_pt=0,spacing_after_pt=0)
            if options['keep_headers'] and m['headers']:
                lines=m['headers'];p=header.paragraphs[0];frame=m['header_frame']
                if frame:
                    bb=frame['bbox'];ys=frame['rows'];count=max(1,len(ys)-1)
                    table=p.add_table(count,1,width=round((bb[2]-bb[0])*100),height=round((bb[3]-bb[1])*100),border_fill_id_ref=border)
                    # Header tables stay inline; no extra absolute offset is
                    # applied to their position within the header story.
                    table.set_treat_as_char(True);table.element.set('pageBreak','NONE')
                    table.element.set('textWrap','TOP_AND_BOTTOM')
                    pos=table.element.find(HP+'pos')
                    for k,v in dict(horzRelTo='COLUMN',vertRelTo='PARA',horzAlign='LEFT',vertAlign='TOP',
                        horzOffset=0,vertOffset=0,flowWithText=1,allowOverlap=0,affectLSpacing=1).items():pos.set(k,str(v))
                    doc.styles.apply_paragraph_format(paragraphs=[p],alignment='LEFT',
                        indent_left_mm=max(0,bb[0]-lay['left'])*25.4/72,indent_right_mm=0,
                        first_line_indent_mm=0,line_spacing_percent=100,spacing_before_pt=0,spacing_after_pt=0)
                    hangul_picture_line(p,bb[2]-bb[0],bb[3]-bb[1])
                    for ri in range(count):
                        cell=table.cell(ri,0);cell.set_size(height=round((ys[ri+1]-ys[ri])*100));cell.set_margins(left=180,right=180,top=150,bottom=150)
                        cell.element.find(HP+'subList').set('vertAlign','CENTER')
                        selected=[l for l in lines if ys[ri]<=sum(l['bbox'][1::2])/2<=ys[ri+1]]
                        pp=cell.paragraphs[0]
                        write_text(pp,plain(selected,True),'header_cell',m,cell=True,cover=False)
                    stats['header_tables']+=1;m['header_preserved']=1
                else:
                    for i,line in enumerate(lines):
                        pp=p if i==0 else header.add_paragraph()
                        write_text(pp,line['text'],'running',m,cover=False)
                    m['header_preserved']=1
            if options['keep_headers'] and m['footers']:
                if options['keep_pages']:
                    write_text(footer.paragraphs[0],plain(m['footers'],True),'footer',m,cover=False)
                else:
                    footer=doc.page.set_page_number(target='footer',align='CENTER',prefix='- ',suffix=' -',section=sec)
                    for p in footer.paragraphs:p.char_pr_id_ref=doc.styles.ensure_run(font=font,size=options['header_size'],ratio=100,letter_spacing=0)
            if options['keep_page_borders'] and m['page_frame']:
                bb=m['page_frame']['bbox']
                # HWP5/HWPX's stored token is counterintuitive: CONTENT/bit0=0
                # is the paper-edge UI basis in Hancom interoperability fixtures.
                # See edwardkim/rhwp, src/model/page.rs and
                # mydocs/working/archives/task_m100_1129_stage28.md.
                for variant in ('BOTH','EVEN','ODD'):
                    sec.properties.set_page_border_fill(page_type=variant,border_fill_id_ref=border,text_border='CONTENT',
                        header_inside=False,footer_inside=False,fill_area='PAPER',offset_left=round(bb[0]*100),
                        offset_right=round((m['width']-bb[2])*100),offset_top=round(bb[1]*100),offset_bottom=round((m['height']-bb[3])*100))
                stats['page_borders']+=1
        last=None
        for m in models:
            if progress:progress(m['index'],len(models),f'{m["index"]+1} / {len(models)}쪽 · 문단과 양식 구성')
            lay=m['layout'];sec=m['section']
            if not options['keep_headers']:stats['omitted_header_lines']+=len(m['headers'])+len(m['footers'])
            for bi,block in enumerate(m['blocks']):
                kind=block['kind'];bb=block['bbox']
                if kind not in ('table','figure','title_table'):
                    text=plain(block['lines'],options['soft_breaks'] or m['cover'])
                    cross=(bi==0 and last is not None and options['cross_page'] and not options['keep_pages'] and
                        last['model']['section'] is sec and m['number']==last['model']['number']+1 and
                        last['block']['kind'] in ('body','list') and kind=='body' and
                        not re.search(r'[.!?。][”’"\')]*$',last['text']) and
                        abs(last['block']['lines'][-1]['size']-block['lines'][0]['size'])<1 and
                        last['block']['bbox'][2]>last['model']['bounds'][2]-m['body_size']*3 and
                        abs(last['block']['lines'][-1]['bbox'][0]-block['lines'][0]['bbox'][0])<m['body_size']*2)
                    if cross:
                        p=last['paragraph'];p.add_run(hangul_join_separator(last['text'],text,vocabulary,options['join_words'])+text,expand_special_characters=True)
                        stats['cross_page_joins']+=1
                    else:
                        p=write_text(host(m),text,'subheading' if block.get('underline') else kind,m)
                        m['elements'].append(dict(kind='paragraph',paragraph=p,bbox=bb))
                    stats['joined_lines']+=max(0,len(block['lines'])-1)
                    last=dict(paragraph=p,model=m,block=block,text=block['lines'][-1]['text'])
                elif kind=='figure':
                    p=host(m);width=min(bb[2]-bb[0],lay['width']);height=(bb[3]-bb[1])*width/max(1,bb[2]-bb[0])
                    if height>lay['capacity']-30:width*=max(1,lay['capacity']-30)/height;height=max(1,lay['capacity']-30)
                    item=doc.media.add_image(block['image'],'png')
                    p.add_picture(str(item),width=round(width*100),height=round(height*100),treat_as_char=True)
                    doc.styles.apply_paragraph_format(paragraphs=[p],alignment='CENTER',line_spacing_percent=100,spacing_before_pt=0,spacing_after_pt=4)
                    hangul_picture_line(p,width,height);m['elements'].append(dict(kind='figure',paragraph=p,height=height+4,bbox=bb))
                    stats['figures']+=1;last=None
                else:
                    p=host(m);is_title=kind=='title_table';rows,cols=(1,1) if is_title else (block['rows'],block['cols'])
                    width=min(bb[2]-bb[0],lay['width']);table=p.add_table(rows,cols,width=round(width*100),height=round((bb[3]-bb[1])*100),border_fill_id_ref=border)
                    table.set_treat_as_char(True);table.element.set('pageBreak','NONE');table.element.set('repeatHeader','0')
                    doc.styles.apply_paragraph_format(paragraphs=[p],alignment='LEFT' if options['keep_margins'] else 'CENTER',
                        indent_left_mm=max(0,bb[0]-lay['left'])*25.4/72 if options['keep_margins'] else 0,
                        line_spacing_percent=100,spacing_before_pt=0,spacing_after_pt=4)
                    e=dict(kind='table',table=table,paragraph=p,width=width,bbox=bb,cells=[],row_heights=[0]*rows,title=is_title)
                    if is_title:
                        cell=table.cell(0,0);cell.set_margins(left=600,right=600,top=450,bottom=450)
                        cell.element.find(HP+'subList').set('vertAlign','CENTER')
                        pp=write_text(cell.paragraphs[0],plain(block['lines'],True),'title',m,cell=True,cover=True)
                        e['cells'].append(dict(cell=cell,row=0,rowspan=1,width=width-12,paragraphs=[pp],padding=9,image_height=0))
                        e['row_heights'][0]=bb[3]-bb[1];stats['title_tables']+=1
                    else:
                        # Keep table-wide and per-cell padding consistent:
                        # 2 mm left/right, 1 mm top/bottom.
                        pad_x=round(2*7200/25.4);pad_y=round(7200/25.4)
                        table.element.find(HP+'inMargin').attrib.update({k:str(v) for k,v in
                            dict(left=pad_x,right=pad_x,top=pad_y,bottom=pad_y).items()})
                        xs=sorted(set(round(c['bbox'][i],2) for row in block['cells'] for c in row if c for i in (0,2)))
                        ys=sorted(set(round(c['bbox'][i],2) for row in block['cells'] for c in row if c for i in (1,3)))
                        if len(xs)==cols+1:table.set_column_widths([b-a for a,b in zip(xs,xs[1:])])
                        for ri,row in enumerate(block['cells']):
                            for ci,source in enumerate(row):
                                if source is None:continue
                                sr=source['bbox'];cell=table.cell(ri,ci);endrow=ri;endcol=ci
                                if len(xs)==cols+1 and len(ys)==rows+1:
                                    endcol=min(range(len(xs)),key=lambda j:abs(xs[j]-sr[2]))-1;endrow=min(range(len(ys)),key=lambda j:abs(ys[j]-sr[3]))-1
                                    if endrow>ri or endcol>ci:table.merge_cells(ri,ci,max(ri,endrow),max(ci,endcol))
                                cell.set_margins(left=pad_x,right=pad_x,top=pad_y,bottom=pad_y);cell.element.find(HP+'subList').set('vertAlign','TOP')
                                cps=hangul_paragraphs(source['lines'],options,m['body_size'],(sr[0],sr[2]));pps=[]
                                for i,bp in enumerate(cps):
                                    pp=cell.paragraphs[0] if i==0 else cell.add_paragraph()
                                    write_text(pp,plain(bp['lines']),'table_list' if bp['kind']=='list' else 'table',m,cell=True,cover=False);pps.append(pp)
                                    stats['joined_lines']+=max(0,len(bp['lines'])-1)
                                ih=0
                                if source['image']:
                                    pp=cell.paragraphs[0] if not pps else cell.add_paragraph();pp.char_pr_id_ref=one
                                    ir=source['image_bbox'];iw=max(1,min(ir[2]-ir[0],(sr[2]-sr[0])*width/(bb[2]-bb[0])-2*pad_x/100));ih=(ir[3]-ir[1])*iw/max(1,ir[2]-ir[0])
                                    item=doc.media.add_image(source['image'],'png');pp.add_picture(str(item),width=round(iw*100),height=round(ih*100),treat_as_char=True)
                                    doc.styles.apply_paragraph_format(paragraphs=[pp],alignment='CENTER',line_spacing_percent=100,spacing_before_pt=0,spacing_after_pt=0)
                                    hangul_picture_line(pp,iw,ih);stats['image_table_cells']+=1
                                e['cells'].append(dict(cell=cell,row=ri,rowspan=endrow-ri+1,width=max(1,(sr[2]-sr[0])*width/(bb[2]-bb[0])-2*pad_x/100),paragraphs=pps,padding=2*pad_y/100,image_height=ih))
                                if endrow==ri:e['row_heights'][ri]=max(e['row_heights'][ri],sr[3]-sr[1])
                        stats['tables']+=1
                    m['elements'].append(e);last=None
            sec.mark_dirty()
        effective=options.copy()
        for attempt in range(9):
            if progress:progress(len(models),len(models),'문서 전체 서식 통일 · 쪽별 높이 추정')
            hangul_normalize_document(doc,roles,effective,font,stats)
            overflow=[]
            for m in models:
                lay=m['layout'];cursor=0
                for e in m['elements']:
                    if e['kind']=='paragraph':
                        p=e['paragraph']
                        if m['cover'] and options['keep_margins']:
                            hangul_paragraph_spacer(doc,p,max(0,e['bbox'][1]-lay['body_top']-cursor),alignment='CENTER')
                        height=hangul_paragraph_measure(p,lay['width'],effective)['height']
                    elif e['kind']=='figure':height=e['height']
                    else:
                        row_heights=list(e['row_heights'])
                        for c in e['cells']:
                            needed=sum(hangul_paragraph_measure(p,c['width'],effective)['height'] for p in c['paragraphs'])+c['padding']+c['image_height']
                            ri=c['row'];span=c['rowspan']
                            if span==1:row_heights[ri]=max(row_heights[ri],needed)
                            elif needed>sum(row_heights[ri:ri+span]):
                                delta=(needed-sum(row_heights[ri:ri+span]))/span
                                for r in range(ri,ri+span):row_heights[r]+=delta
                        for c in e['cells']:c['cell'].set_size(height=round(sum(row_heights[c['row']:c['row']+c['rowspan']])*100))
                        height=sum(row_heights)+4
                        e['table'].element.find(HP+'sz').set('height',str(round((height-4)*100)))
                        hangul_picture_line(e['paragraph'],e['width'],height-4)
                    cursor+=height
                m['estimated_height']=cursor
                if cursor>lay['capacity']+1:overflow.append(m['index'])
            if not overflow or not options['keep_pages'] or not options['fit_spacing'] or attempt==8:break
            # One shared spacing policy for the ENTIRE document; never shrink
            # isolated boxes or pages to different font sizes / character widths.
            old=(effective['paragraph_gap'],effective['line_spacing'])
            effective['paragraph_gap']=min(effective['paragraph_gap'],max(2,effective['paragraph_gap']-1))
            effective['line_spacing']=min(effective['line_spacing'],max(140,effective['line_spacing']-3))
            if old==(effective['paragraph_gap'],effective['line_spacing']):break
        if any(effective[k]!=options[k] for k in ('line_spacing','paragraph_gap')):
            stats['spacing_adjustment']=f"문서 전체 간격 조정: 줄 {options['line_spacing']}→{effective['line_spacing']}%, 문단 뒤 {options['paragraph_gap']}→{effective['paragraph_gap']}pt. 글자 크기·장평·자간은 유지했습니다."
        if progress:progress(len(models),len(models),'문자·순서·서식 검사 및 저장')
        if any(list(s.element.iter(HP+'drawText')) for s in doc.sections):raise ValueError('통합 변환에 글상자가 포함되었습니다.')
        before_body=[normalized(hangul_body_text(s)) for s in doc.sections]
        before_stories=[(normalized(hangul_story_text(s,'header')),normalized(hangul_story_text(s,'footer'))) for s in doc.sections]
        expected=['']*len(sections)
        for m in models:
            text=[]
            for b in m['blocks']:
                if 'lines' in b:text.extend(l['text'] for l in b['lines'])
                if b['kind']=='table':text.extend(l['text'] for row in b['cells'] for c in row if c for l in c['lines'])
            expected[sections.index(m['section'])]+=normalized(''.join(text))
        if expected!=before_body:raise ValueError('본문 구성 중 원본 문자 또는 순서가 달라졌습니다. 저장을 중단했습니다.')
        # All actual text-bearing paragraphs must use the normalized style.
        style_ok=all(len({r.char_pr_id_ref for r in p.runs if r.text})==1 for p,_,_,_ in roles if p.text.strip())
        if not style_ok:raise ValueError('한 문단에 서로 다른 조각 서식이 남았습니다.')
        doc.oxml._manifest=doc.package.manifest_tree();doc.oxml._manifest_dirty=True
        check=doc.validate()
        if not check.ok or check.warnings:raise ValueError('한글 문서 구조 검사 실패: '+str(check)[:1200])
        before_borders=[[s.properties.page_border_fill(v) for v in ('BOTH','EVEN','ODD')] for s in doc.sections]
        before_styles=hangul_style_snapshot(doc)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always');doc.save_to_path(stage)
            if any('Conversion' in w.category.__name__ for w in caught):raise ValueError('한글 저장 중 변환 손실이 감지되었습니다.')
        with HwpxDocument.open(stage) as saved:
            check=saved.validate()
            if not check.ok or check.warnings:raise ValueError('저장 후 구조 검사 실패: '+str(check)[:1200])
            if len(saved.sections)!=len(sections) or any(list(s.element.iter(HP+'drawText')) for s in saved.sections):raise ValueError('저장 후 문단/구역 구조가 달라졌습니다.')
            if before_body!=[normalized(hangul_body_text(s)) for s in saved.sections]:raise ValueError('저장 후 본문 문자 또는 순서가 달라졌습니다.')
            after_stories=[(normalized(hangul_story_text(s,'header')),normalized(hangul_story_text(s,'footer'))) for s in saved.sections]
            if before_stories!=after_stories:raise ValueError('저장 후 머리말 또는 꼬리말이 달라졌습니다.')
            if before_borders!=[[s.properties.page_border_fill(v) for v in ('BOTH','EVEN','ODD')] for s in saved.sections]:raise ValueError('저장 후 쪽 테두리 설정이 달라졌습니다.')
            if before_styles!=hangul_style_snapshot(saved):raise ValueError('저장 후 실제 사용된 글자 또는 문단 서식이 달라졌습니다.')
        for serial in range(100000):
            candidate=output if serial==0 else output.with_name(f'{output.stem}({serial}){output.suffix}')
            try:
                if sys.platform=='win32':os.rename(stage,candidate)
                else:os.link(stage,candidate)
            except FileExistsError:continue
            break
        else:raise FileExistsError('중복되지 않는 저장 이름을 만들 수 없습니다.')
        stats['output']=str(candidate);stats['sections']=len(sections);stats['page_checks']=[]
        for m in models:
            notes=[]
            if any(e['kind']=='figure' for e in m['elements']):notes.append('흐름도·그림 내부 글자는 부분 그림')
            image_cells=sum(bool(c['image']) for b in m['blocks'] if b['kind']=='table' for row in b['cells'] for c in row if c)
            if image_cells:notes.append(f'그림 글자로 된 표 셀 {image_cells}개는 그림 유지')
            if m['rotated']:notes.append('회전 글자 포함 영역은 별도 확인')
            if m['estimated_height']>m['layout']['capacity']+1 and options['keep_pages']:notes.append('추정 높이가 쪽 공간을 초과함')
            if not options['keep_pages']:notes.append('연속 편집: 출력 쪽 경계는 원본과 달라짐')
            stats['page_checks'].append(dict(index=m['index']+1,source=Path(m['path']).name,source_page=m['number']+1,
                paragraphs=sum(r['source']==m['index'] for r in records),content_ok=True,style_ok=True,
                headers=int(options['keep_headers'] and bool(m['headers'])),
                title_frames=sum(e.get('title',False) for e in m['elements']),page_borders=int(options['keep_page_borders'] and bool(m['page_frame'])),
                estimated_height_pt=round(m['estimated_height'],1),available_height_pt=round(m['layout']['capacity'],1),warnings=notes))
        stats['warnings'].append('검사 결과는 문자·문서 구조·지정 서식 기준입니다. 쪽 높이는 추정치이며 한컴 화면의 일치율은 확인되지 않았습니다.')
        if stats['figures']:stats['warnings'].append(f'흐름도·그림 {stats["figures"]}개는 해당 영역만 그림으로 유지했습니다.')
        if stats['image_table_cells']:stats['warnings'].append(f'그림 글자만 있는 표 셀 {stats["image_table_cells"]}개는 그림입니다.')
        if options['write_report']:
            report_path=candidate.with_suffix(candidate.suffix+'.검사.html')
            try:
                for serial in range(100000):
                    report_candidate=report_path if serial==0 else report_path.with_name(f'{report_path.stem}({serial}){report_path.suffix}')
                    try:hangul_write_audit_report(stats,report_candidate)
                    except FileExistsError:continue
                    stats['report']=str(report_candidate);break
                else:raise FileExistsError('검사표 이름의 중복을 해소하지 못했습니다.')
            except (OSError,ValueError) as exc:stats['warnings'].append('검사표 저장 실패: '+str(exc))
        return stats
    finally:doc.close();stage.unlink(missing_ok=True)


def hangul_worker(job_path):
    """One-shot child process: PyMuPDF never runs on a GUI worker thread."""
    def emit(payload):
        sys.stdout.buffer.write((json.dumps(payload, ensure_ascii=True)+'\n').encode('ascii'))
        sys.stdout.buffer.flush()
    try:
        job = json.loads(Path(job_path).read_text(encoding='utf-8'))
        result = convert_pdf_to_hangul(job['pages'], job['output'], mode=job['mode'],
            dpi=job['dpi'], font=job.get('font','함초롬바탕'), options=job.get('options'),
            progress=lambda n,total,message:emit({'progress':n,'total':total,'message':message}))
        emit({'result':result})
        return 0
    except Exception as exc:
        emit({'error':f'{type(exc).__name__}: {exc}'})
        return 1


if __name__ == '__main__' and '--hangul-worker' in sys.argv:
    raise SystemExit(hangul_worker(sys.argv[sys.argv.index('--hangul-worker')+1]))

def image_export_worker():
    import pymupdf
    def emit(data):
        sys.stdout.buffer.write((json.dumps(data,ensure_ascii=True)+'\n').encode('ascii'));sys.stdout.buffer.flush()
    try:
        job=json.loads(sys.stdin.buffer.readline());pages=list(job.get('pages',[]))
        for path in job.get('inputs',[]):
            def collect(data):
                for item in data.get('items',[data]):
                    if is_image_source(item['path']):pages.extend((item['path'],i) for i in range(item['count']))
            result=discover_input_pages(path,collect,lambda data:emit({'catalog':data}),images_only=True)
            if result['errors']:raise ValueError('\n'.join(result['errors'][:5]))
        if not pages:raise ValueError('변환할 그림이 없습니다.')
        opened=OrderedDict()
        try:
            with pymupdf.open() as out:
                for index,(path,number) in enumerate(pages):
                    emit({'done':index,'total':len(pages),'phase':'pages'})
                    if is_image_source(path):
                        with image_page_document(path,int(number)) as source:out.insert_pdf(source)
                    else:
                        if path not in opened:
                            source=pymupdf.open(path)
                            if not source.is_pdf or source.needs_pass:
                                source.close();raise ValueError('암호가 없는 PDF를 선택하세요.')
                            opened[path]=source
                            while len(opened)>4:opened.popitem(last=False)[1].close()
                        opened.move_to_end(path);out.insert_pdf(opened[path],from_page=int(number),to_page=int(number))
                emit({'done':len(pages),'total':len(pages),'phase':'write'})
                out.save(job['stage'],garbage=3,deflate=True)
        finally:
            for source in opened.values():source.close()
        emit({'ready':True,'count':len(pages)})
        return 0
    except Exception as exc:emit({'error':str(exc)});return 1


if __name__=='__main__' and '--image-export-worker' in sys.argv:
    raise SystemExit(image_export_worker())


from PySide6.QtCore import (
    Qt, QTimer, QPoint, QPointF, QRectF, QSize, QMimeData, QUrl,
    QProcess, QSettings, QFile, Signal, QObject, QEvent, QThread, QByteArray, QBuffer, QIODevice,
)
from PySide6.QtGui import (
    QColor, QPainter, QPen, QBrush, QConicalGradient, QLinearGradient,
    QDesktopServices, QPixmap, QDrag, QCursor, QFont, QIcon, QPainterPath, QKeySequence, QShortcut, QTransform, QImage, QImageReader,
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QAbstractScrollArea, QToolButton,
    QDialog, QVBoxLayout, QFormLayout, QSlider, QCheckBox, QComboBox,
    QPushButton, QDialogButtonBox, QFileDialog, QMessageBox, QInputDialog,
    QLineEdit, QToolTip, QLabel, QGraphicsView, QGraphicsScene, QMenu, QSizePolicy,
    QPlainTextEdit, QDoubleSpinBox, QSpinBox, QHBoxLayout, QTableWidget,
    QHeaderView, QColorDialog, QWidget, QTabWidget, QProgressBar, QScrollArea, QSplitter, QKeySequenceEdit, QTableWidgetItem,
)

MIME = 'application/x-krs-pdf-pages-v2'
CLIPBOARD_MIME = 'application/x-krs-pdf-clipboard-v1'
IMAGE_CLIPBOARD_MIME = 'application/x-krs-pdf-image-size-v1'
TEMP_ROOT = Path(tempfile.gettempdir()) / 'KRS_PDF_Page_Drag'
PT_PER_MM = 72 / 25.4


def prune_working_files(session_root, references=(), protected=(), scopes=None):
    """Only our working areas; never remove originals, delivery copies or other sessions."""
    session_root=Path(session_root).absolute()
    allowed=[session_root/name for name in ('imports','edits','blank','paste')]
    keep={os.path.normcase(os.path.abspath(p)) for p in references}
    protected=[Path(p).absolute() for p in protected]
    failures=[]
    for scope in (allowed if scopes is None else [Path(p).absolute() for p in scopes]):
        if not any(scope==base or base in scope.parents for base in allowed):continue
        if any(p.is_symlink() for p in [scope,*scope.parents] if p==session_root or session_root in p.parents):continue
        if not scope.is_dir():continue
        for root,dirs,files in os.walk(scope,topdown=False,followlinks=False):
            root=Path(root)
            for name in files:
                path=root/name
                if os.path.normcase(os.path.abspath(path)) in keep:continue
                if any(path==p or p in path.parents for p in protected):continue
                try:path.unlink(missing_ok=True)
                except OSError:failures.append(str(path))
            for name in dirs:
                path=root/name
                if path.is_symlink():continue
                try:path.rmdir()
                except OSError:pass
        try:scope.rmdir()
        except OSError:pass
    try:session_root.rmdir()
    except OSError:pass
    return failures


def worker_launch(flag='--pdf-worker'):
    executable = Path(sys.executable)
    if getattr(sys, 'frozen', False):
        return str(executable), [flag]
    if executable.name.lower() == 'pythonw.exe' and executable.with_name('python.exe').is_file():
        executable = executable.with_name('python.exe')
    return str(executable), ['-u', str(Path(__file__).resolve()), flag]


def windows_registration_values(command, icon_path):
    """현재 사용자에게 열기 후보를 등록. UserChoice / 기존 기본 앱은 변경하지 않는다."""
    classes = r'Software\Classes'
    progid = 'KRS.PDFMagnet.PDF'
    capabilities = r'Software\KRS\PDFMagnet\Capabilities'
    return [
        (classes+'\\'+progid, '', APP_NAME+' PDF'),
        (classes+'\\'+progid, 'FriendlyTypeName', APP_NAME),
        (classes+'\\'+progid, 'AppUserModelID', APP_USER_MODEL_ID),
        (classes+'\\'+progid+r'\DefaultIcon', '', '"'+icon_path+'",0'),
        (classes+'\\'+progid+r'\shell\open\command', '', command),
        (classes+r'\.pdf\OpenWithProgids', progid, ''),
        (capabilities, 'ApplicationName', APP_NAME),
        (capabilities, 'ApplicationIcon', '"'+icon_path+'",0'),
        (capabilities, 'ApplicationDescription', 'PDF · 그림 · 압축 그림 보기, 페이지 편집 및 분리 복사'),
        (capabilities+r'\FileAssociations', '.pdf', progid),
        (r'Software\RegisteredApplications', 'PDF Magnet', capabilities),
    ]


@dataclass
class PageRef:
    path: str
    number: int
    uid: str = field(default_factory=lambda: uuid.uuid4().hex)
    source_path: str = ''
    source_number: int = -1
    input_path: str = ''  # 연 파일/폴더/ZIP. 편집·복사 후에도 파일 탐색 기준을 보존한다.
    document_pages: int = 0  # 폴더의 PDF 대표 카드만 전체 쪽수. 일반 페이지는 0.

    @property
    def is_document_card(self):
        return self.document_pages > 0

    @property
    def state_key(self):
        return (self.path, self.number, self.document_pages)

    @property
    def label_path(self):
        return self.source_path or self.path

    @property
    def label_number(self):
        return self.source_number if self.source_number >= 0 else self.number


def total_page_count(pages):
    return sum(p.document_pages or 1 for p in pages)


def expanded_page_refs(pages):
    """출력할 때만 PDF 카드를 전체 쪽으로 펼친다. 화면/원본은 변경하지 않는다."""
    expanded=[];counts={}
    for page in pages:
        if not page.is_document_card:
            expanded.append(page);continue
        if page.path not in counts:
            import pymupdf
            with pymupdf.open(page.path) as doc:
                if not doc.is_pdf or doc.needs_pass:raise ValueError('암호가 없는 PDF를 선택하세요.')
                counts[page.path]=len(doc)
        if counts[page.path]!=page.document_pages:
            raise ValueError(f'원본 PDF의 쪽수가 바뀌었습니다. 폴더를 다시 열어주세요: {Path(page.label_path).name}')
        expanded.extend(PageRef(page.path,i,source_path=page.source_path,
                        source_number=i,input_path=page.input_path) for i in range(page.document_pages))
    return expanded


def page_is_picture(page):
    return is_image_source(page.path) or Path(page.label_path).suffix.lower() in IMAGE_EXTENSIONS


def page_border_brush(page, rect, selected=False, angle=0):
    picture=page_is_picture(page)
    if selected:
        gradient=QConicalGradient(rect.center(),angle)
        colors=('#238bff','#20b2df','#b5fff0','#27d99c','#238bff') if picture else (
                '#e91435','#ff294a','#ffc0c9','#ff425d','#e91435')
        for stop,color in zip((0,.32,.47,.58,1),colors):gradient.setColorAt(stop,QColor(color))
        return QBrush(gradient)
    if picture:
        gradient=QLinearGradient(rect.topLeft(),rect.bottomRight())
        gradient.setColorAt(0,QColor('#298eff'));gradient.setColorAt(1,QColor('#24c79c'))
        return QBrush(gradient)
    return QBrush(QColor('#dc3952'))


def clean_name(value):
    value = value.strip()
    if value.lower().endswith('.pdf'):
        value = value[:-4]
    if not value or any(c in value for c in '<>:"/\\|?*') or any(ord(c) < 32 for c in value):
        raise ValueError('파일 이름에서 \\ / : * ? " < > | 문자를 빼주세요.')
    value = value.rstrip(' .')
    if not value or value.split('.')[0].upper() in {
        'CON', 'PRN', 'AUX', 'NUL', *('COM'+str(i) for i in range(1,10)),
        *('LPT'+str(i) for i in range(1,10)),
    }:
        raise ValueError('Windows에서 사용할 수 없는 파일 이름입니다.')
    if len(value) > 140:
        raise ValueError('파일 이름은 140자 이내로 입력하세요.')
    return value


class ExportCancelled(Exception):
    pass


def export_pages(pages, directory, stem, separate=False):
    """화면 순서대로 복사. 이름 충돌을 먼저 점검하며 실패 시 이번 출력만 정리한다."""
    import pymupdf
    pages = expanded_page_refs(pages)
    if not pages:
        return []
    stem = clean_name(stem)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    groups = [[p] for p in pages] if separate else [pages]
    targets = [directory / (f'{stem}_{i+1:03d}.pdf' if separate else f'{stem}.pdf')
               for i in range(len(groups))]
    for target in targets:
        if target.exists():
            raise FileExistsError(f'이미 있는 파일입니다: {target.name}')
    opened, created = {}, []
    try:
        for group, target in zip(groups, targets):
            app=QApplication.instance()
            if any(is_image_source(p.path) for p in group) and app is not None and QThread.currentThread()==app.thread():
                dialog=ImageExportDialog(app.activeWindow(),target,group);dialog.exec()
                result,error,cancelled=dialog.result_path,dialog.error,dialog.cancelled;dialog.deleteLater()
                if cancelled:raise ExportCancelled()
                if not result:
                    if target.exists():raise FileExistsError(f'이미 있는 파일입니다: {target.name}')
                    raise RuntimeError(error or '그림 PDF 변환을 완료하지 못했습니다.')
                created.append(target);continue
            with pymupdf.open() as out:
                for page in group:
                    if is_image_source(page.path):
                        with image_page_document(page.path,page.number) as doc:out.insert_pdf(doc)
                        continue
                    if page.path not in opened:
                        doc = pymupdf.open(page.path)
                        if doc.needs_pass:
                            doc.close()
                            raise ValueError('암호가 설정된 PDF입니다.')
                        opened[page.path] = doc
                    out.insert_pdf(opened[page.path], from_page=page.number, to_page=page.number)
                # exclusive create: 기존 파일을 덮어쓰지 않는다.
                data = out.tobytes(garbage=3, deflate=True)
                with target.open('xb') as stream:
                    created.append(target)
                    stream.write(data)
        return targets
    except Exception:
        for target in created:
            target.unlink(missing_ok=True)
        raise
    finally:
        for doc in opened.values():
            doc.close()


def export_numbered_copy(pages, original_path, directory=None):
    """원본 이름 계열의 다음 번호. 동시 실행 중 충돌도 exclusive create로 재시도."""
    if not pages:
        raise ValueError('저장할 페이지가 없습니다.')
    original = Path(original_path)
    folder = Path(directory) if directory is not None else original.parent
    stem = re.sub(r'(?:-정\([0-9]+\))+$', '', original.stem) or original.stem
    pattern = re.compile(re.escape(stem)+r'-정\(([0-9]+)\)\.pdf$', re.IGNORECASE)
    number = 1
    if folder.is_dir():
        for child in folder.iterdir():
            match = pattern.fullmatch(child.name)
            if match:
                number = max(number,int(match[1])+1)
    while True:
        try:
            return export_pages(pages,folder,f'{stem}-정({number})',False)[0]
        except FileExistsError:
            if not folder.is_dir():raise
            number += 1


def deepl_client(api_key):
    try:
        import deepl
    except ImportError:
        raise RuntimeError('번역 모듈을 설치하세요.\nCMD: py -m pip install -U deepl') from None
    client_type=getattr(deepl,'DeepLClient',deepl.Translator)
    return client_type(api_key)


def protect_deepl_key(key):
    """Windows 현재 사용자 계정의 DPAPI로 보호. 평문 설정 파일을 만들지 않는다."""
    if sys.platform!='win32':
        raise RuntimeError('이 PC에 키 저장은 Windows에서 지원합니다. 현재 실행 중에는 키를 사용할 수 있습니다.')
    try:
        import win32crypt
    except ImportError:
        raise RuntimeError('키 저장 모듈을 설치하세요.\nCMD: py -m pip install -U pywin32') from None
    encrypted=win32crypt.CryptProtectData(key.encode('utf-8'),'PDF Magnet DeepL',None,None,None,1)
    return base64.b64encode(encrypted).decode('ascii')


def load_deepl_key(settings):
    encrypted=settings.value('deepl/key_dpapi','',type=str)
    if not encrypted or sys.platform!='win32':return ''
    try:
        import win32crypt
        return win32crypt.CryptUnprotectData(base64.b64decode(encrypted),None,None,None,1)[1].decode('utf-8')
    except Exception:
        return ''


def translation_stem(original):
    base=Path(original).stem
    base=re.sub(r'-\(번역\)(?:\([0-9]+\))?$','',base) or base
    return clean_name(base+'-(번역)')


def next_translation_path(directory, stem):
    folder=Path(directory);stem=clean_name(stem);number=0
    while True:
        candidate=folder/(stem+(f'({number})' if number else '')+'.pdf')
        if not candidate.exists():return candidate
        number+=1


def publish_translation(download, directory, stem):
    """완료된 다운로드를 새 파일로 복사. 경합 시 번호를 올리고 기존 파일은 보존."""
    import shutil
    folder=Path(directory);folder.mkdir(parents=True,exist_ok=True)
    while True:
        target=next_translation_path(folder,stem)
        try:
            stream=target.open('xb')
        except FileExistsError:
            continue
        try:
            with stream, Path(download).open('rb') as source:
                shutil.copyfileobj(source,stream,1024*1024)
            return target
        except Exception:
            try:target.unlink(missing_ok=True)
            except OSError:pass
            raise


class DeepLWorker(QThread):
    """네트워크 전용 작업. PDF 처리는 이 스레드에서 실행하지 않는다."""
    stage=Signal(str)
    result=Signal(object)
    failed=Signal(object)

    def __init__(self, api_key, job=None, parent=None):
        super().__init__(parent)
        self.api_key=api_key
        self.job=dict(job) if job is not None else None

    def run(self):
        try:
            client=deepl_client(self.api_key)
            if self.job is None:
                usage=client.get_usage()
                chars=usage.character
                self.result.emit({'kind':'usage','valid':chars.valid,
                                  'count':chars.count if chars.valid else None,
                                  'limit':chars.limit if chars.valid else None})
                return
            job=self.job
            handle=job.get('handle')
            if handle is None:
                self.stage.emit('DeepL로 PDF 전송 중…')
                with Path(job['input']).open('rb') as source:
                    handle=client.translate_document_upload(source,target_lang='KO',output_format='pdf')
                job['handle']=handle
            self.stage.emit('DeepL 번역 상태 확인 중…')
            deadline=time.monotonic()+1800
            previous=''
            while True:
                status=client.translate_document_get_status(handle)
                if not status.ok:
                    job['terminal_error']=True
                    raise RuntimeError(status.error_message or 'DeepL에서 문서 번역에 실패했습니다.')
                if status.done:
                    job['billed_characters']=status.billed_characters
                    break
                state=getattr(status.status,'value',str(status.status))
                if state=='downloaded':
                    job['terminal_error']=True
                    raise RuntimeError('DeepL에서 이미 내려받은 문서로 표시됩니다. 저장 폴더와 번역 기록을 확인하세요.')
                label='DeepL 대기 중…' if state=='queued' else '한국어로 번역 중…'
                if label!=previous:self.stage.emit(label);previous=label
                if time.monotonic()>deadline:
                    raise TimeoutError('번역 상태 확인 시간이 지났습니다. 이어받기로 같은 작업을 다시 확인할 수 있습니다.')
                self.msleep(1500)
            self.stage.emit('번역 PDF 내려받는 중…')
            destination=Path(job['download'])
            # 사용자에게 보이는 PDF는 다운로드와 PDF 검사가 모두 끝난 뒤 만든다.
            with destination.open('wb') as stream:
                client.translate_document_download(handle,stream,chunk_size=64*1024)
            job['downloaded']=True
            self.result.emit({'kind':'translation','job':dict(job)})
        except Exception as exc:
            message=f'{type(exc).__name__}: {exc}'
            secrets=[self.api_key]
            if self.job is not None:
                handle=self.job.get('handle')
                if handle is not None:secrets.append(getattr(handle,'document_key',''))
                if not self.job.get('downloaded'):
                    try:Path(self.job['download']).unlink(missing_ok=True)
                    except OSError:pass
            for secret in secrets:
                if secret:message=message.replace(secret,'[숨김]')
            self.failed.emit({'message':message,'job':dict(self.job) if self.job is not None else None})
        finally:
            self.api_key=''


class TranslationStatusDialog(QDialog):
    def __init__(self, owner):
        super().__init__(owner)
        self.owner=owner;self.setWindowTitle('PDF 번역');self.resize(510,340)
        self.setWindowIcon(corner_icon('translate'))
        layout=QVBoxLayout(self)
        self.status=QLabel();self.status.setWordWrap(True);layout.addWidget(self.status)
        self.progress=QProgressBar();self.progress.setTextVisible(False);layout.addWidget(self.progress)
        self.log=QPlainTextEdit();self.log.setReadOnly(True);layout.addWidget(self.log)
        row=QHBoxLayout();layout.addLayout(row)
        self.retry=QPushButton('이어받기');self.retry.clicked.connect(owner.resume_translation);row.addWidget(self.retry)
        self.open_button=QPushButton('번역본 열기');self.open_button.clicked.connect(owner.open_translation);row.addWidget(self.open_button)
        self.copy=QPushButton('내용 복사');self.copy.clicked.connect(lambda:QApplication.clipboard().setText(self.log.toPlainText()));row.addWidget(self.copy)
        close=QPushButton('닫기');close.clicked.connect(self.hide);row.addWidget(close)
        owner.translationChanged.connect(self.refresh);self.refresh()

    def refresh(self):
        owner=self.owner;job=owner.translation_job or {}
        self.status.setText(owner.translation_status)
        self.progress.setRange(0,0 if owner.translation_busy else 100)
        if not owner.translation_busy:self.progress.setValue(100 if job.get('published') else 0)
        text='\n'.join(owner.translation_log)
        if text!=self.log.toPlainText():
            self.log.setPlainText(text);bar=self.log.verticalScrollBar();bar.setValue(bar.maximum())
        self.retry.setText('저장 다시 시도' if job.get('downloaded') else '이어받기')
        self.retry.setVisible(bool(job and not job.get('published') and not job.get('terminal_error') and (job.get('handle') or job.get('downloaded'))))
        self.retry.setEnabled(not owner.translation_busy)
        self.open_button.setVisible(bool(job.get('published')))


class TranslationSettings(QWidget):
    def __init__(self, owner, dialog):
        super().__init__();self.owner=owner;self.dialog=dialog
        layout=QVBoxLayout(self);layout.setSpacing(10)
        title=QLabel('DeepL · 한국어 PDF 번역');title.setStyleSheet('font-size:17px;font-weight:600;');layout.addWidget(title)
        self.key=QLineEdit(owner.deepl_api_key);self.key.setEchoMode(QLineEdit.EchoMode.Password)
        self.key.setPlaceholderText('DeepL API 키');self.key.setObjectName('deepl_api_key')
        row=QHBoxLayout();row.addWidget(self.key)
        peek=QPushButton('보기');peek.setCheckable(True)
        peek.toggled.connect(lambda checked:self.key.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password))
        row.addWidget(peek);layout.addLayout(row)
        self.remember=QCheckBox('이 PC에 키 저장 (Windows 계정 암호화)')
        self.remember.setChecked(sys.platform=='win32' and owner.settings.value('deepl/remember_key',True,type=bool))
        self.remember.setEnabled(sys.platform=='win32');layout.addWidget(self.remember)
        row=QHBoxLayout()
        apply=QPushButton('키 적용');apply.clicked.connect(self.apply_key);row.addWidget(apply)
        remove=QPushButton('키 삭제');remove.clicked.connect(self.remove_key);row.addWidget(remove)
        self.check=QPushButton('연결 / 사용량 확인');self.check.clicked.connect(self.check_key);row.addWidget(self.check)
        layout.addLayout(row)
        self.key_status=QLabel();self.key_status.setWordWrap(True);layout.addWidget(self.key_status)
        form=QFormLayout();form.addRow('원문 언어',QLabel('자동 감지'));form.addRow('번역 언어',QLabel('한국어'))
        row=QHBoxLayout();self.folder=QLineEdit(owner.translation_directory)
        self.folder.setPlaceholderText('비워두면 원본 PDF 폴더');self.folder.textChanged.connect(self.save_folder)
        choose=QPushButton('폴더');choose.clicked.connect(self.choose_folder)
        row.addWidget(self.folder);row.addWidget(choose);form.addRow('저장 위치',row)
        form.addRow('파일명',QLabel('원본이름-(번역).pdf · 중복 시 (1), (2)…'));layout.addLayout(form)
        note=QLabel('번 버튼은 현재 전체 페이지를 화면 순서대로 한 PDF로 보내 번역합니다.\n'
                    '순서 변경과 편집 내용도 포함됩니다. PDF 번역은 파일당 최소 50,000자가 사용량에 산정됩니다.')
        note.setWordWrap(True);layout.addWidget(note)
        docs=QLabel('<a href="https://developers.deepl.com/docs/best-practices/document-translations">DeepL 문서 번역 안내</a> · '
                    '<a href="https://support.deepl.com/hc/en-us/articles/360020695820-API-key-for-DeepL-API">API 키 안내</a>')
        docs.setOpenExternalLinks(True);layout.addWidget(docs)
        self.usage=QLabel();self.usage.setWordWrap(True);layout.addWidget(self.usage)
        self.status=QLabel();self.status.setWordWrap(True);layout.addWidget(self.status)
        self.start=QPushButton('현재 PDF 번역');self.start.setIcon(corner_icon('translate'));self.start.clicked.connect(self.start_now)
        layout.addWidget(self.start)
        details=QPushButton('번역 진행 / 결과')
        details.clicked.connect(lambda:(dialog.accept(),QTimer.singleShot(0,owner.show_translation_status)));layout.addWidget(details)
        layout.addStretch()
        owner.translationChanged.connect(self.refresh);self.refresh()

    def apply_key(self):
        key=self.key.text().strip()
        if not key:self.key_status.setText('API 키를 입력하세요.');return False
        self.owner.deepl_api_key=key
        self.owner.settings.setValue('deepl/remember_key',self.remember.isChecked())
        try:
            if self.remember.isChecked():
                encrypted=protect_deepl_key(key)
                self.owner.settings.setValue('deepl/key_dpapi',encrypted)
                self.owner.settings.sync()
                if self.owner.settings.status()!=QSettings.Status.NoError:raise OSError('API 키 설정 저장에 실패했습니다.')
                self.key_status.setText('키를 적용하고 이 PC에 저장했습니다.')
            else:
                self.owner.settings.remove('deepl/key_dpapi');self.owner.settings.sync()
                self.key_status.setText('현재 실행에 키를 적용했습니다.')
        except Exception as exc:
            self.key_status.setText(f'키는 현재 실행에 적용되었습니다. 저장은 실패했습니다.\n{exc}')
        return True

    def remove_key(self):
        self.key.clear();self.owner.deepl_api_key=''
        self.remember.setChecked(False);self.owner.settings.setValue('deepl/remember_key',False)
        self.owner.settings.remove('deepl/key_dpapi');self.owner.settings.sync()
        self.key_status.setText('저장된 키를 삭제했습니다.')

    def save_folder(self, text):
        self.owner.translation_directory=text.strip()
        self.owner.settings.setValue('deepl/directory',text.strip())

    def choose_folder(self):
        folder=QFileDialog.getExistingDirectory(self,'번역 PDF 저장 폴더',self.folder.text())
        if folder:self.folder.setText(folder)

    def check_key(self):
        if self.apply_key():self.owner.check_deepl_usage()

    def start_now(self):
        if self.apply_key():
            self.dialog.accept();QTimer.singleShot(0,self.owner.translate_current)

    def refresh(self):
        owner=self.owner
        self.usage.setText(owner.deepl_usage_text)
        self.status.setText(owner.translation_status)
        self.start.setEnabled(bool(owner.pages) and not owner.translation_busy)
        self.check.setEnabled(owner.usage_thread is None)


class PageState(list):
    def __init__(self, pages, original_path):
        super().__init__(pages)
        self.original_path = original_path


class InputBackend(QObject):
    itemReady=Signal(int,object)
    progress=Signal(int,object)
    completed=Signal(int,object)
    cancelled=Signal(int)

    def __init__(self,parent=None):
        super().__init__(parent)
        self.proc=QProcess(self);self.buffer=b'';self.active=None;self.closing=False;self.cancelling=None
        self.drain_timer=QTimer(self);self.drain_timer.setSingleShot(True)
        self.drain_timer.timeout.connect(self.drain_output)
        self.proc.readyReadStandardOutput.connect(self.read_output)
        self.proc.readyReadStandardError.connect(lambda:self.proc.readAllStandardError())
        self.proc.started.connect(self.send_job)
        self.proc.errorOccurred.connect(self.failed)
        self.proc.finished.connect(self.process_finished)

    def start(self,token,path,directory):
        if self.cancelling is not None:raise RuntimeError('읽기 프로세스 종료를 기다리는 중입니다.')
        self.active={'id':token,'path':path,'directory':str(directory)}
        if self.proc.state()==QProcess.ProcessState.Running:self.send_job()
        else:
            self.buffer=b''
            executable,args=worker_launch('--input-worker');self.proc.start(executable,args)

    def send_job(self):
        if self.active:self.proc.write((json.dumps(self.active,ensure_ascii=True)+'\n').encode('ascii'))

    def read_output(self):
        self.buffer+=bytes(self.proc.readAllStandardOutput())
        if self.active and not self.drain_timer.isActive():self.drain_timer.start(0)
        elif not self.active:self.buffer=b''

    def drain_output(self):
        # Yield to mouse/keyboard events even when the worker has filled the pipe.
        started=time.monotonic();handled=0
        while self.active and b'\n' in self.buffer and handled<16 and time.monotonic()-started<.012:
            line,self.buffer=self.buffer.split(b'\n',1)
            handled+=1
            try:data=json.loads(line)
            except (ValueError,UnicodeError):continue
            if not self.active or data.get('id')!=self.active['id']:continue
            token=self.active['id']
            if 'item' in data:self.itemReady.emit(token,data['item'])
            elif 'progress' in data:self.progress.emit(token,data['progress'])
            elif 'done' in data:
                self.active=None;self.completed.emit(token,data['done'])
        if self.active and b'\n' in self.buffer:self.drain_timer.start(0)

    def cancel(self,token):
        self.active=None;self.cancelling=token;self.buffer=b'';self.drain_timer.stop()
        if self.proc.state()==QProcess.ProcessState.NotRunning:QTimer.singleShot(0,self.finish_cancel)
        else:self.proc.kill()

    def finish_cancel(self):
        if self.cancelling is None:return
        token=self.cancelling;self.cancelling=None;self.buffer=b''
        self.proc.readAllStandardOutput();self.cancelled.emit(token)

    def process_finished(self,*_args):
        if self.cancelling is not None:self.finish_cancel()
        else:self.failed()

    def failed(self,*_args):
        if self.cancelling is not None:
            if self.proc.state()==QProcess.ProcessState.NotRunning:self.finish_cancel()
            return
        if self.proc.state()!=QProcess.ProcessState.NotRunning:return
        if self.closing or not self.active:return
        token=self.active['id'];self.active=None
        self.completed.emit(token,{'errors':['그림/폴더 읽기 프로세스가 중단되었습니다. 파일과 Pillow 설치를 확인하세요.']})

    def stop(self):
        self.closing=True;self.active=None;self.cancelling=None;self.drain_timer.stop();self.buffer=b''
        if self.proc.state()!=QProcess.ProcessState.NotRunning:
            self.proc.kill();self.proc.waitForFinished(1500)


class PdfBackend(QObject):
    metadata = Signal(int, str, int, str)
    thumbnail = Signal(str, int, object, str)
    preview = Signal(int, object, str)
    editInfo = Signal(int, object, str)
    edited = Signal(int, str, str)
    siblingReady = Signal(int, str, str)
    neighborsReady = Signal(int, object, str)
    released = Signal()

    def __init__(self, parent=None,worker_flag='--pdf-worker',lazy=False):
        super().__init__(parent)
        self.proc = QProcess(self)
        self.proc.readyReadStandardOutput.connect(self.read_output)
        self.proc.readyReadStandardError.connect(lambda: self.proc.readAllStandardError())
        self.proc.finished.connect(self.finished)
        self.proc.errorOccurred.connect(self.failed)
        self.buffer = b''
        self.serial = 0
        self.active = None
        self.jobs = []
        self.closing = False
        self.worker_flag=worker_flag;self.lazy=lazy
        self.proc.started.connect(self.pump)
        if not lazy:
            executable, arguments = worker_launch(worker_flag)
            self.proc.start(executable, arguments)

    def request(self, op, path, page=None, token=0, priority=False, max_side=1800, payload=None):
        self.serial += 1
        job = {'id': self.serial, 'op': op, 'path': path, 'page': page,
               'token': token, 'max_side': max_side, 'payload': payload or {}}
        if priority:
            self.jobs.insert(0, job)
        else:
            self.jobs.append(job)
        self.pump()

    def set_thumbnail_order(self, keys):
        rank = {key: i for i, key in enumerate(keys)}
        self.jobs.sort(key=lambda j: -1 if j['op'] == 'inspect' else rank.get((j['path'], j['page']), 100000))

    def pump(self):
        if self.lazy and self.jobs and self.proc.state()==QProcess.ProcessState.NotRunning and not self.closing:
            executable,arguments=worker_launch(self.worker_flag);self.proc.start(executable,arguments)
        if self.active is None and self.jobs and self.proc.state() == QProcess.ProcessState.Running:
            self.active = self.jobs.pop(0)
            self.proc.write((json.dumps(self.active, ensure_ascii=True)+'\n').encode('ascii'))

    def read_output(self):
        self.buffer += bytes(self.proc.readAllStandardOutput())
        while b'\n' in self.buffer:
            line, self.buffer = self.buffer.split(b'\n', 1)
            try:
                result = json.loads(line)
            except (ValueError, UnicodeError):
                continue
            job = self.active
            if not job or result.get('id') != job['id']:
                continue
            self.active = None
            error = '' if result.get('ok') else result.get('error', 'PDF 처리 실패')
            if job['op']=='release':
                self.released.emit()
            elif job['op'] == 'inspect':
                self.metadata.emit(job['token'], job['path'], result.get('count', 0), error)
            elif job['op'] == 'sibling':
                self.siblingReady.emit(job['token'],result.get('path',''),error)
            elif job['op'] == 'neighbors':
                self.neighborsReady.emit(job['token'],result.get('neighbors',{}),error)
            elif job['op'] == 'editinfo':
                self.editInfo.emit(job['token'], result.get('info', {}), error)
            elif job['op'] == 'edit':
                self.edited.emit(job['token'], result.get('path', ''), error)
            else:
                pix = QPixmap()
                if not error:
                    pix.loadFromData(base64.b64decode(result['png']))
                if job['op'] == 'preview':
                    self.preview.emit(job['token'], pix, error)
                else:
                    self.thumbnail.emit(job['path'], job['page'], pix, error)
            self.pump()

    def failed(self, _error):
        if self.closing:
            return
        # 처리 대기 항목에 오류를 전달해 조용히 빈 썸네일로 남지 않도록 한다.
        jobs = ([self.active] if self.active else []) + self.jobs
        self.active, self.jobs = None, []
        for job in jobs:
            if job['op']=='release':
                self.released.emit()
            elif job['op'] == 'inspect':
                self.metadata.emit(job['token'], job['path'], 0, 'PDF 처리 프로세스를 시작하지 못했습니다.')
            elif job['op'] == 'sibling':
                self.siblingReady.emit(job['token'],'','같은 폴더의 항목을 확인하지 못했습니다.')
            elif job['op'] == 'neighbors':
                self.neighborsReady.emit(job['token'],{},'같은 폴더의 항목 이름을 확인하지 못했습니다.')
            elif job['op'] == 'preview':
                self.preview.emit(job['token'], QPixmap(), 'PDF 처리 프로세스가 종료되었습니다.')
            elif job['op'] == 'editinfo':
                self.editInfo.emit(job['token'], {}, 'PDF 편집 정보를 읽지 못했습니다.')
            elif job['op'] == 'edit':
                self.edited.emit(job['token'], '', 'PDF 편집 프로세스가 종료되었습니다.')
            else:
                self.thumbnail.emit(job['path'], job['page'], QPixmap(), 'PDF 처리 프로세스가 종료되었습니다.')

    def finished(self, code, status):
        if not self.closing and (code != 0 or self.active or self.jobs):
            self.failed(status)

    def stop(self):
        self.closing = True
        self.jobs.clear()
        if self.proc.state()==QProcess.ProcessState.NotRunning:return
        self.proc.closeWriteChannel()
        if not self.proc.waitForFinished(400):
            self.proc.kill()
            self.proc.waitForFinished(500)


class ImageBackend(PdfBackend):
    def __init__(self,parent=None):
        self.resetting=False;self.frame_header=None;self.last_engine='';self.last_note=''
        owner=getattr(parent,'owner',parent)
        self.engine_mode=getattr(owner,'image_engine','auto')
        super().__init__(parent,worker_flag='--image-worker',lazy=True)
        self.buffer=bytearray()
        self.cancel_timer=QTimer(self);self.cancel_timer.setSingleShot(True);self.cancel_timer.setInterval(250)
        self.cancel_timer.timeout.connect(self.restart_stale_request)

    def request(self,op,path,page=None,token=0,priority=False,max_side=1800,payload=None):
        payload=dict(payload or {});payload['engine']=self.engine_mode
        super().request(op,path,page,token,priority,max_side,payload)

    def read_output(self):
        if self.resetting:self.proc.readAllStandardOutput();return
        self.buffer.extend(bytes(self.proc.readAllStandardOutput()))
        while True:
            if self.frame_header is None:
                end=self.buffer.find(b'\n')
                if end<0:
                    if len(self.buffer)>16384:self.protocol_error()
                    return
                line=bytes(self.buffer[:end]);del self.buffer[:end+1]
                try:
                    header=json.loads(line);count=header['nbytes']
                    if type(count) is not int or not 0<=count<=IMAGE_FRAME_MAX_BYTES:raise ValueError('frame size')
                    if count:
                        width,height,stride=header['width'],header['height'],header['stride']
                        if not all(type(v) is int for v in (width,height,stride)):raise ValueError('dimensions')
                        if not (0<width<=IMAGE_PREVIEW_MAX_SIDE and 0<height<=IMAGE_PREVIEW_MAX_SIDE and
                                width*height<=IMAGE_PREVIEW_MAX_PIXELS and width*3<=stride<=width*3+3 and count==stride*height):
                            raise ValueError('stride')
                    self.frame_header=header
                except (ValueError,KeyError,TypeError):self.protocol_error();return
            result=self.frame_header;count=result['nbytes']
            if len(self.buffer)<count:return
            raw=bytes(self.buffer[:count]);del self.buffer[:count];self.frame_header=None
            job=self.active
            if job is None or result.get('id')!=job['id']:continue
            self.cancel_timer.stop()
            self.active=None;pix=QPixmap()
            if job.get('discarded'):
                self.pump();continue
            error='' if result.get('ok') else result.get('error','그림을 읽지 못했습니다.')
            if job['op']=='release':self.released.emit()
            else:
                if not error:
                    if count:
                        picture=QImage(raw,result['width'],result['height'],result['stride'],QImage.Format.Format_RGB888)
                        pix=QPixmap.fromImage(picture.copy())
                    if pix.isNull():error='그림 화면을 만들지 못했습니다.'
                    else:self.last_engine=result.get('engine','');self.last_note=result.get('note','')
                if job['op']=='preview':self.preview.emit(job['token'],pix,error)
                else:self.thumbnail.emit(job['path'],job['page'],pix,error)
            self.pump()

    def protocol_error(self):
        self.failed(None);self.reset()

    def pump(self):
        if not self.resetting:
            # 새 파일의 우선 요청도 이전 ZIP/원본 핸들 해제보다 앞서지 않는다.
            release=next((i for i,j in enumerate(self.jobs) if j['op']=='release'),None)
            if release is not None:self.jobs.insert(0,self.jobs.pop(release))
            super().pump()

    def cancel_pending(self,release=False):
        """결과만 무효화하고 정상 처리기는 유지. 오래 걸리는 이전 읽기만 강제 중단."""
        self.jobs=[] if release else [j for j in self.jobs if j['op']=='release']
        if self.active is not None:
            self.active['discarded']=True
            if not self.cancel_timer.isActive():self.cancel_timer.start()
        if release and self.proc.state()!=QProcess.ProcessState.NotRunning:
            self.request('release','',priority=True)

    def restart_stale_request(self):
        if self.closing or self.resetting or not self.active or not self.active.get('discarded'):return
        pending=list(self.jobs)
        self.reset();self.jobs=pending;self.pump()

    def reset(self):
        self.cancel_timer.stop()
        self.active=None;self.jobs.clear();self.buffer=bytearray();self.frame_header=None
        self.resetting=self.proc.state()!=QProcess.ProcessState.NotRunning
        if self.resetting:self.proc.kill()

    def failed(self,error):
        self.cancel_timer.stop()
        self.buffer=bytearray();self.frame_header=None
        if self.resetting or self.closing:return
        jobs=([self.active] if self.active else [])+self.jobs;self.active=None;self.jobs=[]
        for job in jobs:
            if job.get('discarded'):continue
            message='그림 읽기 프로세스가 종료되었습니다. 정 → 기본에서 다른 그림 읽기 엔진을 선택해 보세요.'
            if job['op']=='release':self.released.emit()
            elif job['op']=='preview':self.preview.emit(job['token'],QPixmap(),message)
            else:self.thumbnail.emit(job['path'],job['page'],QPixmap(),message)

    def finished(self,code,status):
        if self.resetting:
            self.resetting=False;self.buffer=bytearray();self.frame_header=None;self.proc.readAllStandardOutput();self.pump()
        else:super().finished(code,status)

    def stop(self):
        self.cancel_timer.stop();super().stop()


class ExplorerTarget:
    """드롭 지점의 Windows 탐색기 폴더 후보. 인증정보나 문서 내용은 읽지 않는다."""
    def __init__(self):
        self.available = False
        self.folders = []
        if sys.platform == 'win32':
            try:
                import win32gui
                import win32com.client
                self.gui = win32gui
                self.shell = win32com.client.Dispatch('Shell.Application')
                self.available = True
            except ImportError:
                pass
            except Exception:
                pass

    def sample(self):
        if not self.available:
            return
        try:
            p = QCursor.pos()
            hwnd = self.gui.WindowFromPoint((p.x(), p.y()))
            root = self.gui.GetAncestor(hwnd, 2)
            cls = self.gui.GetClassName(root)
            candidates = []
            if cls in ('Progman', 'WorkerW'):
                import win32com.shell.shell as shell
                import win32com.shell.shellcon as sc
                candidates.append(shell.SHGetFolderPath(0, sc.CSIDL_DESKTOPDIRECTORY, 0, 0))
            for win in self.shell.Windows():
                try:
                    if int(win.HWND) != root:
                        continue
                    folder = win.Document.Folder.Self.Path
                    candidates.append(folder)
                    # 폴더 아이콘 위에 놓는 경우도 찾을 수 있도록 후보에 추가한다.
                    for item in win.Document.SelectedItems():
                        if item.IsFolder:
                            candidates.append(item.Path)
                except Exception:
                    continue
            for value in candidates:
                if value and value not in self.folders:
                    self.folders.append(value)
            self.folders = self.folders[-20:]
        except Exception:
            pass

    def find_copies(self, sources):
        def match(folder):
            copies = [Path(folder) / p.name for p in sources]
            try:
                if all(p.is_file() and p.stat().st_size == s.stat().st_size for p, s in zip(copies, sources)):
                    return copies
            except OSError:
                pass
            return None
        for folder in reversed(self.folders):
            found = match(folder)
            if found:
                return found
            # 폴더 아이콘에 드롭한 경우 한 단계만 검색. 네트워크 전체를 탐색하지 않는다.
            try:
                with os.scandir(folder) as entries:
                    for index, entry in enumerate(entries):
                        if index >= 200:
                            break
                        if entry.is_dir(follow_symlinks=False):
                            found = match(entry.path)
                            if found:
                                return found
            except OSError:
                pass
        return None


# 붉은 PDF 블록 + 파랑·초록 사진 카드. 생성 아이콘을 여러 해상도 PNG 프레임 ICO로 내장한다.
_APPLICATION_ICO_BASE64 = (
    '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'
    '3vne3MxkIAMJJIEwqYAi2s4KtmBLq9h0t6K2ig0i7UCIojjh1M4DtoqopEVskFEEHACVSUJCJjJyM9wpdzjnnvO+e1et7x9rqLXf'
    'c0kuaWx/n5+nkveed9i7dtWqtZ411KoqYLNsls2yWTbLZtksm2WzbJbNslk2y2bZLJtls2yWzbJZNstm2SybZbNsls2yWTbLZtks'
    'm2WzbJbNslk2y2bZLJtls2yWzbJZNstm2SybZbNsls2yWTbLZtksm2WzbJbNslk2y2bZLJtls2yWzbJZNstm2SybZbNsls2yWTbL'
    'Ztksm2WzbJbNslk2y2bZLJtls2yWzbJZNstm2SybZbNsls3yOS/0r92AfzuFPzOtGZsj8W+6EP+rPflf68H//12Y8NzrEi7bQ7jx'
    'AOO65+V/7RZtlv9fLsov+/cQvui9BddeW/5fPXkTAD6X5RpOeO97E973zD5+TQRceDPPjT92wwh7ABwA8rihPG6orDQEAKPx1tJs'
    'K5yPHvbv0yRzsyVzPt4Qdkld9fqpMslu5PGDhEOAXYND8qfZsoOBg2i27WQckO+mk6OpzFndOzgfJyonjhJ2AGmSXROVuYaAHUjL'
    'hZspczMtDAB5fJjy8T1U5o4SAOTVJO1ptxTgMICdkL9AOSFtTYtSr9RZ72mWCuNBeV5azIzDQJmv95QTDeXxMWqmW71dR5utBTgI'
    'YDd4jmgnAHuu9QMP7gDwoNf54FLm3diNLh9L8jtwZHEb7wTkHgBpcRvb+yOL25hPHCVa3MY4fBi0tIPT1sLlWCKeI7L+7dS+NpPM'
    'ebWhwzsBPnGMaPE83qnXHMZOSF3Slp07gWayg5uthQ8AOPeC0yYfeSJ1QxOACc9FwnUo/9LWwSYAfC7KNdck4JXAtVQA4FHvuWP+'
    'gb9+4En9Sv9UnpSrSs8XcJd3AjwCCiEzwCBQSiCQDgPLy34jQskM5gKA0CQARGAmFGZwLgABRWoASO9jlvq0upQYieT3UuSaggQq'
    'jJQYnEiemQFOrPcRkEifpz+CtZkEIKGAkJgBSuAEEASQuAAMBhEASkKgwvJrAhJRdYdYnkdgFLa+JxAAIvb+oei9DYMzg8FSBxFS'
    'kvsBQilSL5M8MxGDEsDMkKYmcNE+AaDESImkraEUlkcyAyULIUsGkhKyFGlfIkJq2KWoFAKYQUnHS4ehaGUsnQUBSMwoRCCsUZPu'
    'T226NbWjD87v2vq3Kz/7hFtd6p/7huZf0oLcBID/26IDRAC2vurvrjpxiL6pO9Z9LablUswvAdvGGG0jjBeFV5iFX0h5Eiz8xywv'
    'lR4RPzBIuAZECZQIpbAJsvIUDAHE1IBWxMKrDAAp6U8szA15X1h+TySyXMCgAB9gMkgCkmASgcGFwcbTzCBSvJAOgUDyqCJ9UygB'
    'EYGRwIUVKKQtnLTJ2q9k2MHGoKxQocLDIsNyHUlXWWlqOKU4wyrcRl+y3wtbozAQA5a++U9sbTWaoLa7SSBKir1yGZUiHUiGcYBj'
    'p7bOnsYElI4xPd4hrxdgfQr0aydoof3geOvS65d2pesOX/vUY8A1CfxKFlD83JZNAHjEhQnXgHAtlblr3nMeH6FXdcfz83huy2j+'
    'zDF2P2ZL3nPx9nza2YvYvdzS3CgpqySQqE9kUW8AgILEBQBKIUYCJSDpLyjyrklAhioUoDJl5F/9J+IEjNf1UiIgM5D194aABlVI'
    'EpQ5gyIkApPgg1+XAzuKWTDEILVR0KQKAgVV9ou1H/49W/tQBFes3qxtCXaSgwubncJDXV6K1gvHJqmPwmetqxhtQt1WmeEAQt/Z'
    '6qXh94HG3hd7WR1QzGQCdx2wttrzyrGOj993nA5d/0B75J5VKicymlG+vZ3Hqye/8YW/A+BfxBrYBIBHUq65JlmgZvSyv/3P/ZHy'
    'as5ze5YuXciP+cpz8hWXbEvnNiltATBCAeeCAqCDCrC+RLORj4LaiMhqT7NyumhOu2b4N8VrEQWKkHn2OxVS60dg3vo9wTRVZh4I'
    'aVQ/wcnwHyh8j9lrOQhAfDaqUULhQTRT0bDO4Y/WxtjOaiRJZd7n0FaffWGI9aMWRrK+mdCHkJzVqT4EittgrIBEA6ESD2VYn7Uh'
    'kXoV6ulMS8LqBHzfvkm5/YP384EP7RvziSma+XLdeCm/eO1X/929n2sQ2ASAz7ao8D/qmt+b33fswl/tj7cvHO8a4zHPO296xRN2'
    'tOcjYXvfowFjFQkPFGB/z1jLQFcIPbNrEBEMcendLEQQFjZJGEYJQDPCFIWU5UeGqUW7ltwVTWHU3XxG+GuPKlVbc3hWcDr84dGQ'
    'Zq3Y3AMiiNsAMSuqKR/6QrGPQTKt9xxMe0h9gIJHbN/AnYr3PTT9yNoQUIxj3XYf6r0DmrCEBay/QB0+0gZEF48ZGLWM+TlgcR7Y'
    'sgAszwOjEdBRwqH1hDvvWC93veO2cvQTh8ep7e8ZLfX/ZfJbX/ZOfOF72tlA8yMtmwDw2RQX/vds3/cg/Vl/vP3ibY/fOX3af3p0'
    '8+TlEW3peqyAcR8D900TDq0Rjq0VTCZqthMxl0LJDVX5Wwo7s5kQSNxK7EgzTdVhZxFsIvNXvSr32U3wyeNf0HqjiTsQFNS6RBNq'
    'LYVI3GCNNwRNrsKiklil2vvi9jwGoCRWz4zU2ocSvrbKh+jjHeDCDqL2PNZnGRnBBPJAi3zrJJLvyPo1CAcYCDnxFHioxhAHgFlY'
    '4w08EHh9hYZK29W9YRCQGtDcHGP7MnDmbuD03YTFEWPKCfetJtzw7vv7e//y1jFSn9ul8s3db3/Jn3yuQGATAE65MAGvpL0/+/kL'
    'h++Zf1u3Mvf0vV+yc/2Lv+nC8WWFMeoZDzaEm04Adx1hrK0xGibXlYXYFIAG0wisnGsMLNqqmuBswEDVPGZVJCROOoGDe2CMXzx0'
    'qBoXVdUDAkQMud+7VzWdhvrkusw0awEw+8QDV0GW/ri9otrfLRkMLQkTuqpuh1rbNX29PSKD+9t+bZXJKv0RqdzIqr3Uq8l+clxm'
    'q5/DlwEwKVTDVD+ar0P1UQxmHpIZRiKbvGBmKkTgArSJsWsbcNE5wDl7gELAA12LT37gwXz7H368YepLWshfm3/vy972uXAHNgHg'
    'VIsSu/1vf31dvzL/DXu/dO/kq59/wejirsM6CDcX4LajhBPHGcgqxO5fihaQwaeg6Zk8KjwAAIEALqSzY4IARAFFjJOKfEkgcAIz'
    'MzjLZCBAqrE9Ni6iHZQYivBhbRs7H9vnGgBTf7VUl8WwAiG8bW8oCj6Hi11a9G0xbQswDYWKA0BSvU1cAMM+tQgci1yAB5jhSKmx'
    'eHY05lqvX8ODDnk/Cs8ITTRRqPad4XTjAUjbw3TQza2xWyW4ypgfEc4/i/GYR4mrcCCP8Im/e7Dc/ocfS9x0x9od7dO6X3vWDbiG'
    'k00/P5KSHumN/6aKCf/3vfd7+5XFb9h61Zbps55/wejirgeI8MkMfPQB4OhhFshOGugrEgkvRWNRZvQxEzOjsNrZpU5zsQuszljD'
    'rib269jwQlMC7G9hv8kAxV0A5d4aX0BVvAYI6ldzAkMs/+oHc1X4yUXANasZtK559bksjafBc2v7MWyfgYP/GN5DQ6RFXiI/BDIr'
    'y90Xa41BWp0PNaRK4cJh2kRt5CCUxwjpOAyS0aj0s2erpq9uF1m0MAKmpBDE75hR9DYi8KghzgW45W7Ch24C1rqE00YdrnjGjnTu'
    'sx+Teb3dno+XN+y85q1bgVcKIR5h2QSAhyvXcMJ1zy1z1/zjBXmlvGq0J+UvfOElzWNLjykBH+sJ1z/A4BMS8c3MyFmlCpWnhoJH'
    'qmhVSFADdnAgqGraBKX4e5I6bCLf1Yt8V7V3cGrt0mLPjy/7XQW1hLqFYwftsGKzFvWfCgIqHMTFZUVjHSqPChJD3iWv0NrifeAA'
    'OvYK05IujdJQE3riGfpYP70HRDYIOmZUxw6xr/LUFOb19AEWHPCui1EVYgbBkNDML7mCJLdCeh7QERLiSIlx937CR24Gpl3C7ibj'
    '4i8+vdny+DOmZW3usmN3j1+Ma68teO4jl+P2kd74b6bceB0Bzyv9wb9+FWN+yyX/4fzuSVtGzXja4UZK+OcHCvIqIY1IE1yAynHV'
    't0zsqlIZQoSlEIBS2dpdU1JNy1C7n2peizuiCP6meaxUbV11MJhsBoAsSa4qH6JgosqDyXUoO4PWRxIs3YasoVSBgbxv7H31JD+b'
    'X1PaWCwwQAAZbWz6rpJEG2AJdi7UTCCxA0x5+yzDhmJ0IX2W2WTEbIEEtrY5LarFbh1S76F4jbVdIMmrUMOiRkjMyjDLQ6+VKeFU'
    '6Qfrg3waJeDTDwALI8ZVlxL2LmSc9+UXNjfccbj0q91/W3rRO35j9TdwoDbssyubAPBQRU3/xZf/7dUn7ps+d/mK5fykJ+xuFqcd'
    'DjaETx4C+hOE1ACcVUidieSTMAPRiUyYMIt2UHNUVL9cScFiULVGMeikoWpyxtfgnmTECXfFBCEKDnE0wWMEmwGgiNo1S9g0EzhM'
    'Jer1WptjHJ2kv36vK7Q67WntpYqCHicgRNO58jGpRHDRuXp12TnXqAappDptzDMpZhWwW/mh8ajBwUgrRLGtkmx+A1vKkGVDAoF4'
    'w8BD7Kg9OwCBJHsRxlSw2Nol5LQwCreJcPu9wI4tjPPOZpx3/pgOf/55/b533rZnbXXyHQD9uMwK4LOeFdgEgFMok+Pdd6Cdby/+'
    '0rOn5wDtBMDNa8DRo4w2ERc1AwfCQISGGUd7YI6AJy4Bj5kn7GlkcHPQfEmliVliBgDQEnFhScRplJFmXVWTl0RMRDXzzq9DMJYB'
    'jRcERQRptbU5oWbsQZ+TSw18mXBbElO0O02eEmkGnjO7mvswgDQ9xVEeKKGa4iXUF9vCDFAS9ZjVfUhRO4fWDKY/w8+WNyBTfvUa'
    'z7IdPD+Cm7ae6hgM2mUEhI0ho0nVIrIU8JoSKKi+b53xgQPAR48A4wZYbhk5uG6s7ciFcOvdjL27EnYuFJz1xL3p/r+/k/PxlW/d'
    'c817fuHAtV+0+kisgE0A+IyFCddR3vYL79l+9KPdVzfnLvP5l2xptnQdDlDCXUcZnMEkZm1NQVd7sQFwpAeeugh6yV7GUxZJ15Iw'
    'aq6ZsWUcM4cF8sjWoMzYkqdWaFbsh8+KqmnwG9e2ntSu5mAXh7qSvQl12++x/XafsPnGPs6282RtBwI9TyLysQ0bvrS3M8/2e2b6'
    'EG+L8JdQxypBHLuBuufho4e0WO+Bt90P/Mj1jNtWge1joDcLgMUqaAk4ukq49wBw8aMKdpzepsVzl/vj77vz0ccOLn8eQO8SixWf'
    '1bTgJgB8pvLc6xKuQ+7upc9Hbs7Ye8WO/txxmzDtcWfPOL4GHhP5mhIGaa48IxXgSAZeuAv0yjMTUinoMotmCIkk7Pa+DrTJHABC'
    'HohA/b6a/tXCDL56/Cea2saS6lvX3BSYz+GPqfYGAC7Bop2Rh5q2gCoAQQmZHx//Qp4nV3H9zfUuMMi99cdRgE4eyqN35DMJcugs'
    'aV3Mw5Q9wzePGhI0QhPEX2ifSJKx2KkU5TsHF8AsCK6BGTbLRtvA4BaFnnM24Wm7E3/TBxl/f4ix3IZFozZmBbjnAPCoM4Bti8DO'
    'K8/G8bd8lLub93/3Nczvvpauw2drBWzOAnymsn8PAUB3rH865uZwzuW7yh4ARwn49CqAHkAyZjIjG5yYcLgDvmQJ9GNnynxgV1Rw'
    'LfKtRfQiVcY0Uxtwk5HYvpdnsL5PJPFkAvS91smxXqDyPqMGEBRtWBetaXQcNqWmwkoMSkRIIJm2MvMZcg+FvHef+x9cRzXZhyX/'
    'jQgS6bPfvY9Kh/i91muR82o3ab3WXh5O2xkqxTqIQU6T0DYatIP9ekM3vz+0ReMGPgK1D+x1wt5XmmhipAg+FybJZBQgmvQJe+YT'
    '/fFTic5dANYKu3tjoaKmAY6uMB48Acw3GXvP39a0Z+zJ5d7Vr3vVJT/3G8DzMnBdGgLhQ5dNC+AzlS/6ooL3Abmjy2nrPHadsUBN'
    'zjjKwOo60CJM1QW56guwrSG84gwARfy5UUroC2Oc+DNAbgyPRxN51uykz/CXZ+6LZurJTH/MfDd738BcPUVmcuhC1Z4DkzyYD5+p'
    'HbNm/cnaNvu8h6vLnms21slo95nu/0xdn73uZONz0rHTi8N1RVY6zjXANBfsmWe89FLCiz4CLDZ1oZQB0mQKHFsBdu9gLG9tMbrw'
    '7NTffe+0HJz8V5z76oO4+3k/BFyTNrpEJy+bAPCZyrVUiIDS8+njLQ22LLZUCmO1EPoeotTYtLoMaCJgpQDP3k64YIEx6RhtYmQk'
    'tC3htiPEr/14xv51wtyIwtw+69QcV3lj1IU0OphmKMt6gtBWM2sR2wSAiBswMRGXohH0wsQAWo1Al1IDgxHITFm6FvL04eJCxOYT'
    'WICLYWYtQMSFa2J/Uv634KAtcLT7LIAI1gQqqQMp8rBNX2odqSE0iZAlB6rCKNskZZ0Zkdx70u1PGKVnKkxo1X0vIG4amVHoe9Xe'
    'lq3DCMlatlxaErPM7hEviN2jsYCpt1XHNfcMMDiB6LFnEr7t8wlb50kCuFxQMvC1ZxB+cgk4vA6MDF8Y4AQumWj1hASOm3mAxgU4'
    'c1eD9eNTHOv/B877uQXc9dLvB+OUQGATAE5axI96TOHxjf/p3VtTW9C2QsoJM0o2M1DdURlTz8t/ymINbuUCjEfA9QcZX/K/e+w/'
    '2mi4Pfqd8tDB54FiCtpVxGY4qDT7gYJfq9cWuz9s+cGo8SrMPPMzkibxhuvMBSraNo+JhYZZnwbGjv5eQoVxcVN8c7J+2wYEIWfA'
    '2+PTEPF7s8lJ6BCmTR0BGTygCdlCoprV59fHV6SDv/TzYCqDrO+MXPBnNzG95YUjLI7l9wzC3gXC5VsL3rFK2D7SjFFILgkDmPZw'
    'YCFioG0JV13V0vU3T/nwyovpvJ/ZwXe+7NvANzaQbUo+48huAsBDlNX33pnAhQjAGMq7TOAMnbeXAZXxrkGqPUrV6iMzfvafMvYf'
    'T1jYprv6ULBGq6JQ6LFQH4beAIcbwm81ADhcVuzv2f5xzALZ7lnOrENT2NcXyCeVMXN5QuzPyoY6zCphv5DCirxBUDAKDYVr3fYJ'
    'ddnt1tmhlW4bbWhyVU0IJg0yWl4BStJpR31OHaqhNWSRk9g1yWjkYMPUGwsBeZD8DwV2eVI2o4HQNA3+5gbmN3680AueTOj72pnd'
    'Y0IfgKn+IuHhwkDJEEVPDdC04Csub/Hxf57iweMvwDk/dQR3v/zFwHUPCQKbAPAQZXRW56HeZMJjguSTv/ZZ7uEwaFF671wB01hT'
    '2X0tKFfP2IQEQAmMXhUIO6+xBZVNwcBmAXTxUFgdB8/cUZ4cxIdEu4nAuIUwbIwbHeH7WRMg3oMorDy8lMEeFDSUY7OgaHC9BywH'
    'gcb69A2ThgSYT0VkGYVsVYALqagHk4KgSCIw4xgJSDTXMIFD94qmDw8gFobcatlBVLmhJHG1HlonDQFAagruOuzThERat2dPOsjU'
    'ZWOk/pj8liQ6aL7OlY9tccMNU+w/8n0451Ud7nneDzxUTGATAE65mL9OIMswY8JAnNh3ouFg9wEgNI2k5KbGBpWBUjNNTIsj6dQS'
    'V7FAwoB7q3oxTUig5JigTyX5Tdepi3WicMEws9smJAkNSaJhiRYrg1wQqnA6vrmfGwSdaq3yUe8tUoFpdgBsTr8lBrnwQ+sGK7hh'
    'AFxBtp2nU/BsALDET8x8D4ARr2NbspzcUvG0axCz3k9ZF2KBdf9TgB30jAbk+OlWiDSWK0lMhBlmVJUEjNp6rfWreJZh7awoDJJx'
    'NF5IGixNBPS99Odxj2vx8es7HDj6Upz3U7vxgh/8z7j2lTPmo5RNAHiIMr7oIgbugpn3sjVuSAF1OxTOBKUwJOk9lmJmhAa7GGBi'
    'TpUZuWKB8I7FCOSZbDN9VHlOtKnn3BAjGSLJ1rpxOp38X2EiThTT4rTxM0E3BgiJKaYgMwQoRHvWFTDWXHLFqmRhJFZhr+aRtCZM'
    'DJhQezUevA8ekP4YEvSQqN6DFHRcgqcNW4yAwKA6t+YAbnlcMlWafArWFLCNk6w65LocgG3cbZTqTZTAHCwjiiaLjQMR0MD3ToaP'
    '5yAsUuE0pHRDgaZuPip9ZGZQLuDHPq7BJz4+xcHVb8Pv/eQ6cO13As9tgOsGiUKbAPCwhdUsl/3fbMzhwX9Wv46cqQyvpegAEQON'
    'rBisMSsX8AAk+g8Fr1eYL6wmUgEZYLp8SUnNesAmnqslCsBiFsRcFyWRMmhGVV2hen+m9d1D+bDN9PxCW7/DYFARhAg5RQGIKm2j'
    'xxKfaen3rjWVjAakdn0KFo60rKKGP6+RJAQi2Umci5E3oAkEsGTFMSFrog7ZrsWMQYLm0CvShJ24pgNGz/gMe08ifSNrZIQcmy0h'
    '9a4q+pYiBqjdQfENkSBPYYAK8NjHtbjhExMcOPYinPUTt2DfD//CLAhsAsApFC5FNsgMmgKFKMq6+fOKCTRbR2ogjJvYE1ssiCgs'
    'WxfZmPkLBEanqqiBqBbs94AMcq3kutTlRn6TbYdhpgSZ00EI22yF/rMCi7Uv+SxelQIauEPi29uW+SoRVOfpoE/3v0NdTD7x4Uwe'
    'LBDXfkFwPEnHLrLYhg2GEjKRLK5By5j0oLUeMq3rz2AgEUYNMBLzgjKLQSZ7LpDulErV8nHrIRCOrVUYgKoDA1iWDbZAO8ZMCVpd'
    'zE/2jECrw549M9thJGGW3aTpcVe0/OEPZTx45FW44Kffgtt/8FaJCcimtpsA8HDFTVnj4xnJM98vap+qb72ClKBnW8CYhEhRw1S7'
    'x+uAGeYW4IjFTV3XlFz5kXmYA+QWgrQ3KfC4oFOI+DNpzLg+wKCuMnTtGlNFO7dnuGbHVWa2a6qAxImQ0LNqbhOc6StYBSZXIm6s'
    'j9wXl48m/PL8oz0hE2HPAuPyJcajtjD2LjKICw6cINy9Qrj1WMIDK6Lt58esZ4rocGQjNjlfyI4e0qgawOTwHepfoak0pgE1Lc12'
    'wCEyhChnrBpbqDWkoHMeJVApYLSE887rcfjGRayvfxOAH0NYvLAJACctQtQ9QAFzloQU1XQh8MeZCBw0t/0S5+1hzFdAScxPZRy2'
    '6JBPVs0wNROHOo3TuH6lN/ksgc4OsFcSzG9vT0A0mOJW4VJNY0k7an6Sia2iAKjAs+ApzJn77+zNcVAYgoQ+L34X+NgOBDA/m8zC'
    '0t9Ca6D7eQCky6KDLCGJUCaSswlWOplae8bZPb75YsYXnZFx9mJB2/gASkMKsG8V+Ot9DV53S4N33pOAwlhoJa0bxMSF6pKEOPMS'
    'NbRZRa49FAxMVSTSNlrP2ZuRB1YGIRDZmiivDVOvXJdYJQLlHry8hTA/ZkxXn6SXeXRoEwAevqi6Bir8DlbBwKfBiIMpPByYpiU0'
    'jTCiXVrCgEfscCCojoE/hmauQwqMkblW5YEGBRMEbeSdGkAJGsgU9rRnMDGNE2EEQm95CRb8tGCbA1SdrxcBiHn0tSdm2pul4SCk'
    'NfjuOEbqMHvm3Qyg4vYEV3qEWJu0Tg8lOTQFHr+H8Yon9PjaczogSSJE7jOmHdgWNxMKEjHOWmrwLZcWfMulBW+7u8HLPpDwiYMJ'
    '83OEvugJLTYVZ/LPCNuV6T8WVS1K3DidkwC0gzb7WEh81rIP2QEVRCwrKlSG44yLWniVa5TYqQG1iXjK24XY1/pNmwBw0iLMdQBI'
    '4NKg2PEPQGQ/02TRvK6DPCwm/JQ0o4tAySf8gxyGKHxM7DHsIaAGwYLJKI+PlkQAKFj02ISGXY8K88p1x6YgSowztghvHlxnHJsC'
    'i2NGCyATVa0M6a9NeJCFxsM0Ym0iR+DSHQ41YhJAoFoCBhq2K1KVfoo0UWvH1hGmFKhGts8C4fAU+I7LC37myRNaHmV0XUHJCYlG'
    'IIzRJIa5LtaYvvTIuYDQ4yvOzXj66S1e+L4RrrsNmJsDesktYrWc6m5QQRcgWbID1TEr6m4RgIYJLSG1G/lFu7cx1gOVf6OZnftI'
    '8CPN6u7jNmPlgLBhqfAmADxEmd4KkgM8STeXMY2PoOApvPc9K0MRlUnEoDALwExc3K8PGkGrrDgeNAY5PqgkDLV8NanJ8ciXAwOw'
    'oHYM1yUiTDPjRAaedz7wogsYl20FWiLceQJ4/R2M37oNmBZgvgX6LLON/kw3fVVLNSa6XLtlMxFJmDdt0JSo/fCqgxVBZiPMRFed'
    'LEoOj6fIdB8R4cEOePWTe7zsiilKXzDpGA21aJEAHGbGPnA5BPC60mkJSKcDdA4aWgR4ism0YLnt8IYvJfzHtsXrbwLG84TcQzMq'
    'Wbc7U1obf+g0hu96RMQ6+yDA2CCAPtnFAIhthtYtOScpcbGdnBn16CFjxahS2P9RYvEIM2UTAB6idKM7CU0LJEmhKa6nDAg4oLQu'
    'PgGx+c1S5PpEYuKmRnMFUHyBCNtl+t4YfpAOq9eoy16RyOIF9rRB1sww80tm75PP3LWJcHTKWBwRfv+JjG95lN6mB+Lu2km4emfC'
    'c85hPP+DwH2rwNaW0DE744sZYH6GRsMNwEqd5tM5eCadbEBjrVO3oM5GeG+cgoOFhPUat7KBKiRSI9oGODglvOxKEf5J1yMRYZTm'
    'wDjEKB8Bl7sATKQSPQAZXIBMYGwDNY8HmivQJsI0ZzTc4bXPYNx6rMU/PZAwHhPlHuyHeAdZc3AOBqK3vxpm4ttEv8VcAF+nkOo+'
    'kCTN5MLV5ZnRIZEXjB+YNVDDAs/RrtgEgFMpRGg0yUKmgqBR3wqyPn0lEgwhdF3ZktqE1AJIGj9gCcdXRUGDxarGMfo7mfkLi8c7'
    'IrAplDA359ao1cRmLrN6u00CDnWMx24HXntVwdU7GdM+UdJ+AmD0Eqd42mmMdzyD8BXvY+xbB7a1hI7EPOfEeg5CdQvcz9dYAcFo'
    'wpLUWK1W6AQXzDlxK4eiXFAldB2UysYuU2yuAB3pCF9+TsarHj/FtMtoABCNmPk2cPkAwCuQLJw5vbmAiAXBAYBPAPk9QHMPMP53'
    'SGjRl4y5UcZvfkGDp70VmAJIIxBnyMkvYF8ExQT2yL21NRhsstqQgUaDgTMcV6B+ovFbkt5pkpIPr5yobPGAIQZVRkjCbIQ+oCgD'
    '1ejcLCcpo/POY3Bh29hf9LYKvgXE/BBKqODUIRgs4SDWlwhGakn+Jmg0WObJKUHmz/X7ZN/p7ykxGs0eS40siU0tcWoBSiBKTHZf'
    'SiCiWpeuGQEIONAxvukc4L1PI1y9E1ifgmTBTMaobXWqP6MBY33KeMx2xtueSXjUMrDSM+bUfE0JoBGQWiCNgDQGqBWAaZK2TwNx'
    'iQgpMdLI+sPev9To/a3ssJzaUGfLoJZBLSG1jNQC1Eo9aSTPk+8AakGZErbMMX7qqimAHiAG0RyYbwHKewBMAZoTMeTCQGZQYcmD'
    'LkxgJrTMvAh0twCTd4CI0KYGkw54/O4e3/jogj6TrBLV9ThCYwK1kjxUz0WHtsF4AaL5EwGNbRUXCzu4MYI1gPrdzPILrbgQJdf2'
    'bjXCYg4nKZsA8BBlrCPBhf0EXssI85kdBDCIWgmmgfVfgiYCkSA/iSZMSdYHpEQOAEmn9kSICU0ibhI4NcSpETeiaSWwmBpGY4LU'
    'GCNyTTpKEouiJJtOThiYgPGzlxFe9wRgR8vU5USt5g20NEJfOhARRmkMRsYoESYd4TFbCW9/OuHMReBYzxg38pyUQMlAyUChZRHM'
    'hpFGIsAupIkVvPTziPV7AbjUsABHwwH45DcDw9SQ9lfqkr4S2oZwLDOef0HBY3b0WJ9mJIwA7AfKByFCz4y4dR4DdsCIaP8izhxl'
    'ZiwB3aeA/kaAFmAg+V8e3aMdFfQgDfCxjqsOOcn3tpUS2WdPCJDxRtOgCVJocyfZg/waPynqHCSiAqJSgmuo1pELeZKLuVZq5tQG'
    'ed90AR62JBDZWkAdXY2mewgacf+bSPlQizGDCpouNWGb2qvWLivvWHzAEoHE1U7Vqa5mdLUsB+6lhceZCA2YDnfABYuMX7mc8Mzd'
    'jEnHJGBT0LYjlNzzPx3+Ndy68k6Mmy14/Pb/QhcufiH3PMWoaWnaA4/eSvzmpwNf+TeMQx2w3KLucMzBNUFtjDRVCCTN19wFdhbW'
    'ayrh4kyC1WWBUesrIZJarswMbJkHvuX8HkBGIhCQmcs/Apgyo4GbbdFgZviqHc/QZJUjHhMmHwa1F6KhEUrPeOIu4LIdjI8fYswn'
    'iw9ZdVwXVbBVbO+1rRIjYDSF2sZ0ujp9hQM8DWNAlsxUZywqrc31MmrwDIVwklmATQvgIcr01ls1eZwG/hUA+NSKjYMNSGGdBYhr'
    'Aiy11Zw/qtaAawzhB7EaSbUcq5ZXXjELwTQ+sddji0pSNLtbWYVIxDjQA19zOuGvn0J45u4G0z5RQwQuPVqMcLy7j996/4vxgYO/'
    'iqPr92D/2ifwtvv/O19//E1o2zEKZ7QJmHQFl29n/MXTCTsWgAkIY2kfNW7hhHZEdyWRWjrqDnlfGNRYXyBmtFoxKVhJpJaBuzgN'
    '0OgzpH6mNSY8bifjcdsyck9ItMDAPhDvAzhm3ZhDV5fdWZL9YJmFRGkY/WFwfwdAc+gZGDeMJ+wQU1DaFKyfJBN9tkzbrD5KBGoT'
    '+5hF62BgLwZP3cwSZtgpo2FFJWoCAgA2LqwxFQNmVVgbVNMmADxEGV90ESPGdrSYCwCNywDKNJoOWqlcNZw6wfDQbbKIFTyim4KA'
    'e6DMTUVUAdEVbTX5RQN7ilXmfo4SYwJgDYQfv4jwhiuBvSPGtO+pTcJ442Yet66+g/9s37fgrtX382Kzh0fNEuZoGSPM430HXo1P'
    'Hn0r2mbEOXfcgLHeMa7aAbzxKQlLLWONGWPtX7K4hnU3kbsqItSSA0AMTiBORJxkcSInE35f4mt9VuExcGmMDvZiB8gOjCftKmgb'
    'lg01KAFlH4DeJMn/Dvw5NwOC821v7Pf8QLC1gAsWBTysv4Yc1l7YjjAS8TMziai6DMFUt9xgVJ6xt/ZIjfd5s3Xs7XrpVW2/GzlW'
    'HVEzy+ObLsDDlhqLnjWxhcCy+C5O/RHVRFAbmsggAHQJKPs8upu8qZrKfhQIwU//qaF9cu3BkGOGfZwhLsShDjh3AfjlS4Ev3kXo'
    '+qKzSRkJc0CT+f0HfgUfPvLbaDBGmxZReAqC5D0kajBCg3fefw167vC4rV+HaV5HSy2mmfCkXcCfPIXwvA8y1hmYb0A9m6OkKwGd'
    'gqrKWGMdlVY1iipIpt4BhXutX8FlCAMhp6QrnjbAJctxxDoQjkFMfwC2ptMDtmzWnExCuOpl+JcggBqgrADcwVZd7Jx3tGVKBXVd'
    'CNVtB4qsnXa1kBDWCthX0SpxjkH1DauGZ8COiB7QQOljnCN8UaA7wHn++oaDJjYB4CHKnjvvTLbaQpPcwKz+ue3KIOZB5U33aw2P'
    'RRwSsZrAyiCWsxkdWiiik4FAsEUdRExw9Gvy94zC1EJ2LD/UA1+7l/HTjyactQBMe5apTGS0aQ4Pdnfxex/4Cew78WHMNzvA6MGc'
    'AfUwmYDCPUANRjSid93/SjQY47LtX4E+d2gJmPSMp+0GXvckwvM+LAHGuYbsJCFfReTCbp0lCnLNmtBu0sCuOGe6X4WBw/oHmKLV'
    'zEECdozEtBdw6cG8Dgu+kPn4sLEyEECdy3crIClgkqCxrwaSYE6v5zzYmCnOedV1Stj0uqt7tdzI3RwrNpSZB0zhmj9mTkaDpVJD'
    '35Ohjm3iSpBBxqBsugAPUQ6cd14BpRKOgo7/AIr05rAxSxZgLoXiVSK8Zh6S+e7ssbzEDhDVpMVgRsCn8kh9ZovwA25ljghYLXKg'
    'xKsvAl73OMJZY8akk90MCIS2HePm43/Ff3Lnt+GulX/CKG1BRs+Zi/IXD3iklB7ghDEW8Lb7Xolbj/8N2maEwj3MHfjivcAfXS1t'
    '7MFoB+a5vszn12mvFKY2qSGdFtNgqYGax0wYcTGATLEpUAZ3yACVnOrmOzFsrtyGj9z1J9g5BRULagqtJDfpXsJpCTV9D7hvAnjQ'
    'lszyAhpi1ephClaBYvZzBYAwUZfkeHDZe1CYSmagWDZl5uruWU8jX9r2UURqlRaS7ZGJmuhdAJsA8DDlBkBTL9wyDOIhiC+OWNwi'
    '3Ob/a8otBX8dSEk25KnTfkFI4hSgCgElPQMvMJAFxxAY78AUuGiR8aYrge8+B+h6oGMgUcGIRsiY4t0P/BzevO+HMMkTjNIW9KXT'
    'vQ5kx+/CQNFApslE5sKEEVoa4y37fgS3HX8/2maMUnq0BEw74Mv2En738bJeIJME51wta7thO+volJkDWyOsmRr1bFToY4C0Bk5R'
    'gxxJ04OtThWoEyyCLw9vAcyDkGtKLnQcxZ5WzUoq7ATSKTfX4oos1JyGuttTwc0rOlDAYNqViFjGmNiaXnkl9FsDNlKF2/FAkclG'
    '0fDKT4phnAWhY0hJBqsGBzwxkwHfxVlMmQ0xgE0AeIiygMvZKF0BlmwgfDG4/zYwryLUmqkahTxoBWXyCgIAiNij3WodNKlqGtvj'
    'v2GmrgftXwc973TgLY8netJ20LQHbGXbqJ3D/ZNb8bq7vwMfPPg6jGgZicYomvhWdF25Gs4oJECQWf1rEHr0DG5QCvBnn/4f+NTx'
    'f8B4PI/CmRIxTXrGV58O/ObjCGvMyCQzGEa/GMSDfk9NtXg0ih8sBs2Q0+ss6cl+F6tciGp/UxJlt29dxI25V2rtUo1OKiwMZo2o'
    '6edhWECBgAkixgWUFoH2UQB6jBvG4bUGHz2aMGp1mo6qQBv8e1AwABSJ+6jBXxqesKouUrGcUHMndJshSUCruShF+LBqlg28l0IQ'
    'Js3wp17xcELwb77I2fHIFuNhsaaGAeQIApbFxRtmXYyxpVrVK27q13GkRDxwEzy6Tz5gnJlaBo51hIaAX34M4bcvJ2xPjGkPEGVK'
    'aNA0I3zk8Jvxv+78TuxbvQnzaRcysp9Ln1n+FiYUTshM+jJQqMDQIzOoYS4Ff3r3D+KulY9hPJpDQUYDpkkHPOdM0C8/LmFNcxCa'
    'BLIkpaQpFYJ9NRqeSPdbMBeIzCVgF3Yihi8gdMEyNFTJJdnF54ZVob+Quic0jwJhXrcBUz8t5u/bBihu5mkIkxMxGoCnwOgCgHYg'
    'lw5IDf72IOHuNcJSGzyRAObuEqiMJ7PiEjjpdK8N5sAqr94lDBCAoVvmXTD+q4yDChx2r9FIGXCmbALAwxSD3uxmFNV04FlUDt7n'
    'bC110VaNB+hHNmsAANCo0Kdq6fpiGMhzUpEduvZPgccuM978eMILzwamPVPHAHHmUTPmCVbxhrt/HG+468fQ5R4tLaPjnnuW0FhP'
    'zBki9IUTmIhZAI8LJS5EnBGBAeg5I9EImXu8/q6X4+6VT/C4nePCmVtiTHrGfzwTeM2lwPEsAtBUDwi2ak9WR5mmr9l+slEme46E'
    'CRWbhlXmJhLr1lNwk8TplkfEHzne4OD6iFtKYPSgdAa4OR/EExVsy9/Wiit+uEXHRZMruAPabcDckwFk90Fee1fSjUYErMVto2ru'
    'A+bOMSV9NYk1u5MVfQggmwVgF1gWReOJU7p+wgOHFJSPTx85geHC79NQ7its4O9NAHiYYhGAxgkLQM2vkkElM3GRhXYxRRjhcoEG'
    'NjOfo99f/V4RgEYNAJvqplANM6Fh0CQDRzrGt59DePMTCFdsBSYdI8kaFIxGY9x+7KP4pZv/C95/8E0YNVtQiLhDZtPwfQH6ou85'
    'IVPDfUnoS0KGvPpC8mIEy4DQl4IW8zjRr+J373gJPr36SYxHc8icRV/2jBecQ/ipi4FjvWnIao1SQ2ydqya/dDT592zqkz0PwOjk'
    'LhP5PUliDlhogX3rwFsPNUhNy4UTwJnQPBFMW8BlQigNufCblPhmKQRwS0QNwD0oteDFZxHTMuXS07hN9Jf3JHr7Awk7xuJxD1L+'
    'w5qPZLVToEG4NkWdoUNMGgAZ5CsFdyDqCgEq0/JR88PM/hr0EEzYgACbAPBwRQNBMXoSkzGGWiT4koMigyJMoFFw8oBRDfZFaw02'
    'd1xHu2WmIx1h64jwO48l/MzFjHkwpj2DkNGiRduO8M77XodfvOW7+N61O3k+7UAGc2aZWuoh04QdCB0TOk7omDDJTB036LlFzw36'
    '0qBTcOg4CQiAkAH0RDzljERzWO9X8Zuf+gF8evUWcQe4RwOZdvyv5xJ+5NGEQx3XQGdIfKr+vFkBNfjnIEAAu5Zld2eje1tfwuEL'
    'CfidexJOdAlNImbuQbRENPflAG0FeF0FPUFmAZKOYQvwiOTzBNQugJe+kqg5F1wmaBvC0UnCD97QYJSqgCdKAQQ0toNo1QxdPHMR'
    'LBOw8XA+wbaedZsgmiXgEGOYZa9CPgXiWuOk2mhQNgHg4YopbyNkWISRCIzEPFwFSDOwzjCgT5qtlgCd/iFnjKScIfsJiAawV8og'
    'ykz7J4Rn7ATe+njg2XuBSQf0hcGcMR7N4cFuP37pxh/g193+Syh5jlpaRFcy94XQlYQuE/pM6LJo+r4kdCwzBR0IE2aalELTTJgU'
    'UFcSdZAtwXp3A5Ic3gnijgsaWsBKdxS/etNLce/KHWIJICMpMH3feYSXnid5CW1i77OnM6cq6Bb4szRf8piAgAAjAghtMJGYCMxM'
    'yw1w4wrhl+8aoW0IGWBZFbiHsPANROMrwNQQYQLwBKV0xJwJ3BF4Cm4aYPEy8PLXA+25KLwOSg1SGuG7P9rgltXEW1tdl0B1fOuL'
    'ydKCLYirrFHbnOqy6GZGChnws2K1Y3q7/fXq4AeDALAVgKT3OI2SVVY2MwE/m7IsDrtvzkI6zWdzyALKVD8QaYAwaG4pLIIv19bc'
    'b3tvgUNZtW3pxAxCC9CJXjTvy84HfuB8oEHB+lTgIlGD0WgOHz7wd/j9T/0iDk4/jS2j7chgdEWErMgeF0hINa4weL7ClpqQtniU'
    'KanbWLx/gBycocFBLihoaYGOTA/hl29+GV562S9h99yZmOQJEhp0GfihRyeso+DX7wFOm9NjUkjMZzLyqcYi02IaA+VELNIg8ThZ'
    'cCQatlpacgqH3obMjO0t8It3JVy6PMazT59g0jMn9ERYBua/DFTuA/efInT3ATwBMAKnRZnqax8FTntAyNSXdcwlWUf90usbvu6+'
    'hN1zQO8nN5HxhZnb5Au+4HsrwDc50DgSIMu27VplE0k4o8FX/r0gYbXqk47bIDddc6rk2YAdFqNwtbkl2KkVEYrTRDKLknmg2SX4'
    'B3HMdSecok4We4L2MAcubuElA6QMEkZbs3FITEvgYAecOw+85hLGF+8BptOCKQOMjMXRAnru8NpbfxlvuftPMdeMsTDajo57tAxm'
    'Tkil+qgaI4Za3cKpBNUcIVLnNg7X9yHgxLDNUUgFrudxs0QHpvfi5296OV566Wuwc24PJnmKBg26nvFjjyasZ8bv38/YOwf0pNl8'
    'zDU1uE68C9UouOWIC2EA2XFD7k+yuYrEZgiSoQfGXCJ89ycbgObx7L09Ss7clYJU1pBoFzA6DTzqtEcN2JdrZuQyISLC3KjBsa7B'
    'iz/W8B/fk3DaPKEv4IQCPyDU2MKEXdpCkojnXfBOsRK7+vMceIQq2esokGBkHZdq+FjUUndmIaVNDCIUW6bOmwDwiEq0uZT5SQDA'
    'eFh/1iERC0D/EdXOQJ3LKVXresxA0J0AcQe6AhyZAl+3l/Hqi4EzxgVrE/FzwQWL4wXcsfop/M+bfw7XH/kIto+2AgRMSkZDckZO'
    'YjWjIdaLaU53PRDbzXW9AeqP1Zz0FmsfSacJpVt9zhjRMu5evQM/ecMP4Icv/znsmNtN0zwFKPG0B37mkoSSGH9yP7BzxNTb7kBG'
    'IddwJPErCYcNtCTZPwzJRCyE1U6EPjNjDGBRN75qSfbd/G83JNy4MsL3nNtgy6gHckbHHRhTITklRfNMiRgjIrSjBkCDd+1P+NEb'
    'G/7EUcKeOT2x1+fzmZBldlEaS5DZymqdGKhGnK9xAMvvcFH2Uuk886VW5LEQ9ykAlORhAEkFLr7uSbcV2iDvmwDwcIUwjPHpgHiQ'
    'JlwYhUPfbPw9jKzXZU4fEUbEONLJSr6fuhj4jnMYOWesdgRCwSiN0I7m8H/u+T/4jdt/Bet5DVtHO9Fxj0LgVmMQhcU0TcEdIea6'
    '2QhqPr3BUdxX3zEgMHIkitGj6LMY4L5kGtMybl+5BT/+iZfhmiteg23tDqz360Sp4T4zfuYiYL0Ab9wP7B4z9UAFAefsGWl3s1Ya'
    'YlGWB/uEc+YKPf90woVzEuD8xHHCX+1nHOyApVbGbp6BX/gU4c33N/i2cwhfswc4c6GHpwn7w8QAPzIhfPDgiP/gHsJb7yc0IOye'
    '070Q/USPumCLYNui8wyhzEAYEE/6QmLNNEmzJhEZy/iMvA5tXFwOMGy2X066OzQPeC34q4OyCQAnLTJst3/4wwkke/eWDAkSD0x2'
    'IBhi8jfSPYyqBnxt4VAwCwB3v5mxf0q4civwMxdnPHE740QHNbd7bBkv42h/DL90w6/gL+/9SyyNFjHfLGOSCxI13BcRgkaTTmSG'
    '0bYyFXvTTq8mmBug4m8an9KwR0E+ova19Gjrr65+52nJtNBsxS3Hb8FPXH8NXvG4n8B8WkBfsudP/MKjCWuZ8JcHGXvnQH2iGvYe'
    'EheeTZeZGAkjYkwLcCwDzzsNePm5CXvnWLJiNLp6y9mEV95S8K5DEgtgELa3jDtWgZfe2OAXFhtcsaXgii3AeQuMOWJMC+PT6wnX'
    'HwVff4xw54qYzVtH0uWuMCwhQ8OR8DRkDrOKQgx3rSrtKtDKTUXBuO4dUrEjul8D2lPcgk5OBjoZvcxdspF2jtx0AT6rcvXVAP11'
    'CC6h+u1wRYk6bUODLcF9bIrNyJotqEEtiDXZELDey157/+lcxjUX9NiSCo5NJEkkEbBlvIx/PPRR/PQnfxF3rNyBHePtKFywngtS'
    'Sqxp8OgJSEUzzwAQZEty0/gEIGm02HkR1Q1wLUtx5Vz9bTDDQbYFulQiNErIzFhotuGjR/+Zf/Tjr8CrHvcqmmvm0HMGCqFNjF++'
    'uMFqAf7hKLCDmCaWHWUWi8cCSEPiCSOSvIItI+A15zP+w14AaLDe9eCSRZiahIuXG/zBVcArbmX8xp3AlkZmX+Yb4qUWWFln+qsT'
    'CW+/v1pyhQm5FLREWEjA1pEIdw7HtNvG5Aaalo9g3zKin4dAVbEMmAFK9bynaHvAaEtw/qqqv1ocZjkAIQjqjzRXJNRqDyMAKBtm'
    '/TYB4OFKmNsvpAdEVqtaf5K8fEBWa3kqsDv4koctGYOyLbjKHloARzpg5xj4uUsLvuH0jLWecawHmHvMtfNIKeFXb/1D/MYtf4CG'
    'gC3jbVjLPYv2aHwriSQ+KAAxKwnQPfnlyzRjXRPgG1JSYO2amWgLnJSVZwxISY2uTK5WAUsKbcFCuxUfOPyP+OGPX8M/fdVPoEFC'
    'xz2mOWGuyfjtSxr8p5uAjxwDtjVMU6iWddNfnpN0ZevBnvDELcDPXAhcssSYdkBKPeabFhgpKxdg2ndIIPzkJYxLlhJ+9GbCJNvR'
    'XoQ2AdtkYxIxyNS3q3gtsxwSElTRs2YF94h0+X0V+QqSVcrNWjB33ehqad0cxsSnEtgUifGSUTk8qsq13k3gcORLdCvIDIoZc2ET'
    'AB6yXHDDDfQRgGzXqKgpwbblnuzS4AFsW7ddZDPRCgIkq+309wRZcfdAR3jWHsZPXdzjgoWMo+vQw0MKto234I6VT+MVN/wq3vvA'
    'B7CzWUJqCKtdQUoJliw0yKdHdQsbnQdOM3vg2XJRAQxyRrK7oxsbN7NgCANzncryu6rrU+3VzBlb253420P/gB/5+Kvw6iuvATFR'
    'QeZpbrDUZvz6xYTn30C4aQXYOSL0DKIEJs3bb0hiBqsZ+JYzgFecx1hMjLUpU0OF22YOk/44rn/wzWhoDpdt/XLM0RImZYLSNXjB'
    '2YTHLAHfdT1w+ypo+0h2CrJjk20LdGbYiQUwYTKiUEB8Gngr5gZUGhj9Zu2m6G8R1xmXmsfAQW+blSmWWNFzCCXxhGkIOnXA3XAw'
    'RcAk+UHGvSV1tfHypE0AeLiSUQXAnC9g4CIzE7gU3QvaZM0WAzGgRzWzAkACYbUXg+xlF2R8/6N6AAVHpgQgo6EWW8Zb8L/v/Cu8'
    '4vpfw5HuKHaMt2PKGakvkkrrgpmQNLBgPmVcZER6FBWVahm6oKf6vfmysPd6jXXclUci49VBPoOeOoQqNbZYpWBrswNvvfd9oPKz'
    'ePUVL8OEpwQUrPWJd1HGb19E+MYbWxyYANtGhJyFxROAIx1hxxzjpx8NfN1pBX3HmGSJ8I9Gc7hn9SN45/0/gQfWbkNDLT5+9P/g'
    'q8/4MeyafxT60mHaM568A3jTExkv/GfCBw4Bp80zskmRex1By7JKprsjCDLjcz06O2HBXarC7LY5KYBQlXoMx0GSwFCZSaxMKtHP'
    'jDzHaoXaLTMxAAouRIUU6wcNL8YmADxssVEYRsEBM1Hr+ARY1qWm7i4UBjjJcVgF2D8hPHoJ+JnLezxrR4ejU1t/32PraAlrZYLv'
    '/9Av43dufhOWR/NYHi9jvc/KMInJzt+j4OcryNvWc87MpmlKjfzbeXKUAVsSJwktyrCqebRXXhcTMLCGyObiKwhA2wMAWZIoAGZa'
    'Tjtw3Z1vRSot/+QTXkJr/ToYGcdBOHdc8PrLC/7zJxLunRQsj2Th0cEOeMq2gp95NOPCLQnrU4A5Y0RjtKnB+w/8Ad63/zfA3GGx'
    '2Y1EhPvXbsEf3fVd+KqzfhQXLj8VXTehtUI4e8z4iycm/sFPJvzRPsK2VrRyXwjgUpW1C7xZOaoAzHRHvEYJVMzvrua8biESriXd'
    'bJgtB2AwXl6h8xAZTwXbSi2D7E2T5cADfrWj39jdwepwcgMfLymbAPAQ5fjdYwLQFLazAVETgDA0BYUHJAaQMwOl+FQccqbSJUyn'
    'LQ5nxnPOKPyTl3Q4c45xeGJR4IKd4634hwM34cUf+Z/40KFPYs94GwjAiU53CyJRqzbdZJtCpASgqOZvAEqpKiLTNMpHvuw2+oom'
    '+K6JLBYgHXTr1QJZqFpMamYM2JSILVhqXi2Xgm3jHfiDO96MNi3ytY97Ea3kE2hSwvGecOE847cvZ3zjPwP71hiLDeG/P4rx387K'
    'aErGylqDtmEsjBZwbHIIb7r71XzT8fdgy2g7WprHNGdQArdYpOPTo3jdHd+LZ+79Tjxjx39CQo9JyZhrE375CsJVWxnX3gx0zBiR'
    'HapMLvQ089lElGe1gEi5rGfggAmDvAW2vR0dRwxKbF1IdLGsuIDXuQWPVbhlZu/MyFcwr+4HA6kQuLHFCBvU2CYAPEwhzrobqzJ0'
    'sUg/e762bNfk4yBn/5WCYoc5cMH+9Ywut/ifV/R4wdmFjnc9H1gHmsSYS3M0Si3//I1vxCs/+gdYLxPsGO+Q6T1L5CmqNUwD23y+'
    'voxpyVasmunpEsu+JLlao5IrIkEJ0/4GCtp/X+JqJrF+r9+ZCwTdxsKRhAGUpIcA1+DntvFO/Nonr0NeT3jVE7+TTvAqN2AcnRRc'
    'NM74pYsJL72txY+cM8HXnJ6wlgnrGUjImG+X8KmVj+MNd/4k7lu/DdvGu9AVRo/i23oxZU48JuIGf/HpX8J9a3fzc876QZpL85Ir'
    'kRu88LyC85eAb/sY4eAaY+cIyMwEkubaacPWQ5+0CdmHpD6TgSRndc/ts9EM8Mi/BlHkfiWV75Y0YLrhx5hU5PBrDBdkmuvygqGl'
    '4hMXvDkL8NmULStTRinZ1JudACSnstRATdV2oj1KYWR9NURYZ8JVWwte9KgVfOXegkPrsiajlA7bR1uxb/0QXvKPv4033vk3WBwt'
    'YSEt4kRfkJqElAFoxFgYRZ+bmKgQEuv2YvYCoHt7Dv36REh2Ii+AwCLCF2aSmvCb+UuaP6aWjupC1XIGigBxAjd2n2o006TQLa6I'
    'wAXYMtqGX7j5Dby0uIwfefy34OjaCggZRybAExcZ77yyYBE9jqwnUALmmzFSafDn+34f77z/D9AmwrjZg7XSYaqbeSQipAKSXZIB'
    'oMVCswd/d+AvcN+J+/Ct578SO+dPR587THODZ+4peMuTCf/5Y4RPHk3YNWZMC6gUF24DNOmFJdh4n5QOHAivKt63H0yyaFH2bDbi'
    'VXfSrCw7HdzcOl+0GzwCH3dHkij7PLg+Wm8CWkWZYuN+AJsA8BDl+PLdRHqInyp1PSaMFAhMHKp/IBq1IOeMXAhtIpzIhB+8iBml'
    '4P41UKKMNiXau7SDr7v1b/Hi9/8m3zs5gIWl7SglY5IlNz1DE3fYEk6gZhz7pn22X4afMajawQ6mFNNd/MHUGILATi+pqaolaibz'
    'UVUYJuG9hc97o1LIYe+r6yp0gbsXXEkELsDWpZ14xc2vw2g8xg9e/FwcWDsqZ++VhCYxVjiBS8a2diuO5iP49dt/Hu8/+C7sHm/D'
    'PLWys0FpSLY4l+PMLcvR98RDxnzag1uP38i/eOtL8MILfgTnLT0Gk+kEaz3hccuMd39Bg5dcz/jTuxlbWqCEOXYNcpJnbjFVdxpG'
    'SkT5g88eQDMyiZmYKVHiaMJTkgVRqbihEArJOn+ZmgiVD+ZjPiPfMgBikkOBdbyoMGb2HwPwrwgA1wDpcjyX9mA/vRfve8hrvwjA'
    'ez/L+r9I/3629wHAfXginQEw3nL76N3NJW2bCE3OoL6g6YGmF+HXM0PEr2bRRJgScpfBfQZ3hI6YiAgnID4clcKLoznqc8HL/uZ3'
    '8ZqP/zmIE5bmtqBb69XPhwhcX8cfifR8OFVIBgyJkIioFPgGGcQkJik0PpBk8qpkZxyCuRRVedX1NilEtLXdAMKiHXMH7HvyoDkX'
    'FRxyo8GtJwOBQgnIhO3Ygpf/3W+hOdrjv1/xDTg8PY6madAToeSMFg3e/+D78Zt3/xYOTPZh++g0TLqMnBltImrUAW8gQNsmQzdo'
    '2xowM0ZpKw6dOIifu/El+KazvwdfsOsr0JcJTTpgqSn4rSvBF80V/PAnCMstsKQb/1KpyT7SHx3oRJ75KN4B+wIftnQIDbpY4FTO'
    'EDd7XKcFLN1iY7HDKGHCTghGhPZSOKFWUGM4LH4Z6aYJxbMc/vXPBWCArgPS84AMXPdQQObl2kfwnEdyTy0flj+vfekKXvge6rZt'
    'Q3/aCB2AEwAObxUa64nysluQnBmJ3AL99jHmdgDjUsg8iNQkNInQIOHv77uJX/zXv46b9t8AbN0BpIRVWwxji489ugfUVYRa7Eho'
    '31ZIzQMz3Y1LrDT6sah3G21Qj1zYXSRBQsCdTzNDfVdd1UR6TMUgIOhmaxoObNF9+DxoUVgm+Mdb8AP//L+o27EdL3nsV2Ei5g22'
    'IOFN978HP3zXj2HLaAHLS9txkAoatGiI/UUkgbyGgNY24HCuZ1kvzwTCAtbyGl594Mfp2aM78K27vwtzoX0/cBnwqDNA3/MJ4ADA'
    'Cw08lOHulBKj6YD51d7jAUZBcmEFwCA0OiiR3KR6WC2qOlzukkmNdg/DkhQ8oCrugL5Vf0M2iU2MVGxEtDaq2cAbM4H/3wLANTr0'
    'APJ7zvrCs4/uf+Bpq93xy5Ns00IFCQ24JABF9oJlQuEWVIptEiUbnNuuyWSeN4dzO2yRa4PEBcVkk8xI1nuBauyigPMEXKYifWmJ'
    'mBpa2PJrH37jad19p/GTFs+nJaxjYZWx5T4gWZKPTK4hM4FzwXomLP5zobv3MI52hH46AUpB27a0OD/me48ewm9++I04ffUYzhst'
    'IvMqmlbm5DMTci6S2NPKKi/RvkUiyUn9y8JIskoZ3CTpFQN+jnRKThXZ0TZVcNFYRUrCUEUtl5gtmOT0Ep/5MCvBzgyQCAZJ6MA0'
    'Pwu4ECXPcMvQjDpS8DEzNiVwzshd73kI7/3Aq/DUq27G2Vv2oMsZCylh2+o9eMY9K0i0ipGeAyjdEIFoSfsH9aWT7EAqnkpxszen'
    'gp4zSia0mfBh/gUsnfYJPH3LUzEtBevTKSbrUzxlzPj5/cCb78vYmjrkktFx8WPXuDB4rsWnH/tk3Hj1FwHTQn6oCbmmFpPb9zEw'
    'wRbOS7DZ1gHeosIAa+vrd/p9xWsFiJhu4DBeyAITdRaSSAJFJyn/zwDgDUDzPCB/6IyrF+8+vPrqA/vu+Na9aWH7o3afjZyAac6q'
    'TUkOPdCtZJMzFzRTK2bXATULi3UsxK6SU3Akv9u0kxlgPsWiDC1WN6MrBVMVkvlEmGsbvOLOdyLf2pUz3z6ijIxnhtWXgjTJF4OU'
    'xAQqONEV3NFLxawHYYxAONZnSiXjJ+YWObVzOJGnBDBaZeKCxBkyB5/Aut8b67791t+kh0KQbGZbCrK7IkmZKUmc0KbguNSAHImm'
    'sr0BelY+hewurOE6EWSSk3Fy0T2EKaEQKHNBQ4RxalFKQceSOKvgwE1KRGD0hZFF67DIBKFVxp0WRq9WzHjUokXGsT//LezjhFaT'
    'm7alBt/dzqPjDCoFLQhMCSUl5QGxk4saQ21iFM7oVWgBoOdM0g6B/6ZJmEt70PV/i3v4fcipwYmup67r+V4kvmhhjFcQY9r36LmA'
    'm4SGEkZE6Atj9cQKCl6Fv/ia78L/eslPYv6Ei75qe+WzGk5BFWTFCvXTZALALDJJHGuIJF3EUhSDVWVGHqsLJm4Vhfoh1g4Tcyp6'
    'Ql1iR4JZswz/jwDgPUD7TKD/u12ff+ZtD+y/brlMP/+xFz+Wz3/q53Xtzm2MXGRpE3NNqmgbeZUCTKbSgTHJBvHxOos65wL0JCtn'
    'mmag8UBcj1FhVk1pR81g6Ib0BcgaRp9r0Y9GLecCzgw5/pZ8L3ZqCKynOMh+90lMvF7iBaCENN8CbYPSZ+DEFCgZeZyIxyOxY6yN'
    'cgqMxZ2kqX3xDSXQgGx/fclAk35YsMiTPohAlCSZXA7hhDEXmb+SWFRMCcvGUlJr0awO8a9lqTwDXQYakPQZ1aG3gGOjdldhO8xA'
    'd07l4DPoq0B/g9jt4xZgRlMk7x+5oEx7OTF0qSWihDLppb1m50PHUdqq0ySNKL4CydNX68kiuJRkTJEImMoY06hF6gpwogOahLww'
    'lkBgJ5ArORYFpcvgpsHcygo+9K6348I3/zouftqX4ZNPfiaWVjrZ8ikUW1tR43VcAyKo0/IE2K7A5ri40MOGzn+tLplPCJgy9LlC'
    '1OxAUoxUV4WImsr0Uv7FAcCE/x3bnnL1px/c/yfLJT/6Kc/6isnuxz22ndx+RzO5+05pq8Za2Y5D0gAXGCh9L71NjQaozDeeATRd'
    'QsFsioyrjWrWg4EHAGqYierRjOYQ1Ais2VDAACUcxZPDMw+vUMuimgussQAAHqzz5FPV9KLFJcAkwl1cp1CTkJK2tRQgswaWjA4z'
    'NqEyfuGCweIeJKpx7eJtNBM/MJ4SRKcguEBO7qy7CLnZj0oKp7HTLFpcqPWn8BgdHmmj9jszkBIlA3MwStFd/zjEsmRsuQpI0hVJ'
    'xbRvTdYH1Zg+w+MtpA/X5b0Wz3Og41zQT6ZYbse4aW0VHzixikQjnPvhv8UnPu+ZAt7J+qtLh2TqTwG1jonNygQuwYbiPJp8NJ1G'
    'YtpTpVslbkhSdrdgQOS6t63/9C8JAHQN0DwT6P9y+fH//vDRB157WtNuffI3fGO3fM5Zo5WPfgx84gTQttJaM1dDBWzWuxxzCuSs'
    'yTWSFmubpTsJg71UMyi13vDeCMcZYOojuGrShznb4aQ8B1UVXiJ4zngAgVh4ZnB9mXiI8EaZAFDnywWAGGpNcsmonjqrOagMbDqE'
    'YlsFglg0JfuSVL9HKMhUwrpSoMqu7RmkwEWJiGRfAotjCz3grlesB7UJ4YPeQaTpdwqypDv6eUBBaZMLOEeQM9AJ18wKkI4JMes+'
    'uaJjQeE2Mm1s37FvrinRFlZvk30mbnFuhH964F78n3vuxLY0xtk8wlzf1cM5CitraKhUZ3/Y8qOisLOTdNh2s5DqG2Fv9QeUhx2d'
    'bCTlwlRna/QEQGYJkhoAMfnkrXP8vwgAXAOkGwG6ltC/ZeGqlx5fOfyzZy1vwVOe+/y+XZpvVj/8YSAzaG5etRyRSe9gWbh1OiWx'
    'YCxhBWIqyX6dwqgOsqx57CZtVlkKtKuMqeNVFQjbybWedWPmgote9eucuQ3ANqJ51MkDwDfDJGob6bC1pwI6DxeS2KDH9+EpoRmk'
    '8SCNIFAKcBm4jYJWJYCRyFYWsoeo1Io3ayNEpA0U3cqyXyq/b6SNMzpbrrFe25Bkz2Sm2ekPBwkFg5NpT9I+O6vYCSTWRIadQc4+'
    'HtVDEZCUaQqxkRhLTYsP3LcPb73rDjAl9EmWEafUCs8UILCmd1DRG3UFgQ260qmwrAjjgBERWbVVkZ4c3Ii6F0PlByQnj45ZkQEi'
    '35JmUD7nAMAW6SfgL+au+PnuxIPf/+gzzuqv/vpvRL+2mk589GNAagiN+vdUbUH2XEtgoE6YBk9wT9V8vJjgEAhuVkANxKgsJSWh'
    'UxBuqCFgR3W+yFuk29kOvI/KisEMcLEZ2BFDJakPYVRuLKr/AzzAsn4YjW9IpU+r/bRnucViHB8E0DWg1FEZ1JqpU1NGDQO1CFCx'
    'PkRz3yq2C8JaCaVPzaUPRBDTu+bKyrxXtXRgIA+QnWCMmTLAXhPrWIcJlY7/DA28vUSwhUxFXdB5Snjn3Xfg7/btw3xqMQWj0/tW'
    'CnxOivUUbk3H1dgceQjKEoSYAWp40CDjXv+WiCsmVsCAmgHm8AgWh87bDsDOyqy5Kk73f9lU4DdIiCl//Nyv2nHz/bf/Slk/8vzH'
    'XHxZd8lXfU2a3LuPpnfeAYznpTUl14bHIEYoxktslDTWcxV+EoYK33g4K67iMFkztofRkMhQ0xiqWhiISrgOCAqLxXCSdriw1WlY'
    'ffzwfUAa1+c6/KzPYlXSxgEimzanr1t5cjDubQm4kklSToqxjy8K9ecbjVy7z4yDtZlmoEfoyOEaGtxvvMkzFQ5+9OQma4h10exC'
    'abBjKzuoVrUeAZvBvq2ZweKQxoIwpArHqa7tELhtUkOJmN96+2348AP3Y7kdoVMaz1FCB6LzFgncg9c7YLGtsym+alJbD9NtCrBi'
    'NSh3lEqs+o5DdJ/dSPWNzwddIdF/TaH400aO5OFHLRtzAx9heQ/QPg/Ib9/1eZdev+/m985PV5//hCc/bXrJV35Ns37rLWl6512E'
    '8YKkStmcMEzwTfMAHgBR/wtMVA9uHHZB15mctJBropky+50RNuR0x62nN1xvATMownpE0f+pfywIVGNQg+qiOqtTNZVp6579CbJx'
    'mF1X6tWmLcnaxl5DiH3NYtPgWeR/o7DU9lSmMqtL6YYKNJ6Z5s+haiaZkKq1P6AVFODDvRqUg02KiGg6ctceDsldLT0GJP2RqLZN'
    'VYGqUuYM2cbJ9jeW6GUumcdNg5Iz/vSTN9CHHngAC+2YelHkaAAsEmEVhG/cS/iTx4OAgpUJ0DBLXCmrgDPpBjFMLGk8VBS7Odec'
    'DgSaQltpS8ljBiXARNYD/U3Mi2ruOWyYfhv6Yf8yAPAGDfa9eevVT37g8L737MzdFU//qmdPzn3aF7RrN1yPfOgQ03gsWt+0rMNV'
    'jJTWthIgUzd1cyRB0HARz/TKE17sWz+TWvkrGg12T5RK42eneI22mEBFTo2uxVApVoGQvphurEIRXQj/zfuj/rhH1OvMiFICCi/k'
    'SjhaUQpqHNoVHlXfeFCQahT+pDQy+hexisR5ZQoPnNU8w5stmEaugIf3VDVO5lRwcjzy603gWUGDibzNVhfREPgIAtKsbhSX+uTA'
    'Q9I0xnzbYq2b4PU334BbjhzB4mhMGUAx6COD38wPTgqevRt41xcTnb8EHFqXrco5M6HIdHEprBvBSCo3dD2JnVDMuUIWQwWyahhP'
    'DPVQYghZJTL8D5s3nKw4CJQy+9P/FQAwQNdoWu8bl6583oFj97/j7Hb+9C/+j9863XbRo0erH/owyuoKMBphIOFegeFysXi19kMN'
    'vDDFsbFT9pPNiQg1BjMs9leFwyzjQQUnlRBHAl9NN3slDb4YmnE2GgFIXMApMF+9m2otPuD6fMyMLYMoJH/Uf+PoGyCEB1W00oC6'
    '1usCGYDpJHSvlsKgkYNHipCeZKxcuIfNtMZQbWxtu5NUVKRqaHV1PIIL2HGaIHhqbTQZvZmO5UFjiNKgJD7/QjvCobVVvO6m67Fv'
    'ZQWLozGy0YkI5lh0XDABg3KHDODqncA7vpjoGacRHjhBMtcmCwXklKeilkE5ySsPaV+M7jouVI2Xypb20USfCdC8BxsyD6sT+VLv'
    'kw3OI44BXKMAlIjKny5c8XPHVw+95NJte/kpz/3GnhtuVz/4D2BKkpST63xxDPDAgz9QSCdYZI45MA38GmeiQezJ6uV6oRvDA/Co'
    '4TL7a0Jrhdwpdw2uOa/s51PINYV9Mq3eXRsK+FFgte+iccUuDf0LfZmN9NKw+eZO0PC5of1QLeFa0PRL9F2ilVQByGZRjSpxVyCp'
    'p9G5cnMFPBgCokS2UHAo5MGyccWcoG44TKg9IEcaK4956xysBMZw7ChZYEM1PEHn2wM31EBgjNeYgsmFsdy2uOPog3jj7bdhtesx'
    '344kU1Gf1mgLGxBG1KAHYYzEDQqt94TT5oA3PQP03z/E/Lu3AbvmJIkoZ83542pcxbwoLhaRllYmRMUH1O0c2QTYxMiMOAeH0GHU'
    '8wq0LtkR9nMTBLS0Xn7uc5s//Ivrf49OHPqWJ5x78fSxX//1qTtyKE1vuAXcas6BhSxBgEZKdfXUYDAkBl17NRAl4zOqhDLhqWAS'
    'Bjp4jlWWCJaY4ZfM+B3un85qZ6d0FBXymzy5w+Va2lt9Uh03qnVa7CY+Sfkb/iRXV/KsOtUk/yY38wOSWLCSIh30fgBmlohCCIFP'
    'GnY96b/khAltRwZx8lq8VXEnHAoATAmMontaVqJ6liIC08vgOMDFNBqd+4H47aSbI0lyDUEUQKI6OpVUBM8dCmMAAIULlpoWnzh4'
    'AG++83ZwAcapEeHXJ1tjagsJCQkr43UACaMmYZoZo0T4tacmXLKVcc3HWJIciUT/qftaXS0Wy6PURkV2saF3Y8VitHpgav2F/QY7'
    'kY4rLjtPQPIpBjoTeAQAoDTO71m+evcf/vlHf3/Ur33lU5/w+ZNznvmsdvrJG2l6373A/Dx42leqiSpl0zdWURwQ1mgHmzANftRX'
    '8FnlHlMHGv/lokwZ5rspoGBgcgeYIGQ+DLb3VimiS4gG8QUJYrJqQ/ve2LV432oIS9uqcWCpRJlAZSgGyuumFojPCzTh+jaOabjE'
    '4x3WBreQqlYz8RKmTADrqgIHNaKBtVDfkdPfW2TEHVBXn1/jOPa/AJykMg/4lQiEpuImQ2cwLLU2WBOa38T1WRXSbLsuAtq2Rds0'
    'KCTrGoy+XECLbYsP3X8vv+WeOzGPhDYRusoxFYNR+zpFxhKW8MZj78G+A6/Ht29/PkBZmpOJvu8y4guXgf/6AeD4hLG1JUyL2TDs'
    'acAMgLOulAQ5PTlQbKCPOMK/isVA7cNlx3UmA+xbVf9frgWwab4/33blVQ+sHv/Txdxd/PlP+aLpGU96ymj/378fvLaC0Rm7kNpG'
    '2qMrs8AQV46qvLGyqG9hyAzkoucqk3aAwVkZ14SQNbdbc6/V80EpgbFJFsvE4CoBeg/Dp5aJwDlrKmeCzYFr6wxl4LYbmyFSUzvM'
    'mpCsruRrvy3wZ1VINtdQ5cl0j1RqAOOa0LYV12fHZYwiGCI5ZLGw2Falpyb6z8K+yrYsqCnKaYkA5ALf2Uilx6Lv5DEweV7EZtuj'
    'JD4fRDPbos9cb0JWCkrOAkBJjzRrElObiEuR9RAh8ykhbFSuayE8I5RI+Ickc9Jo2K9PwatrWABjy/KyLAzqesyB+H333IW/2bcP'
    'c01DBLDvCOTEErljdpZE4YIMBvqWfuXm38an527Hy696CRZHC+hyj2lP9NXnMr99ifCC9xJuPMa0awz07E6uRHE0DjAYGEDcGAMF'
    '47vIyRS/rG2NOURCZ71+FsVCOWUAuEaDfX88f/k5qytrb17Ja2dfMr9tcsbWbaOjt9+IhQtPx8LZZ4CaBF5bl520UmRoV+K68KWw'
    'p0uqecSZ6jVQ5ikaCAGBG1a7j+SoFxNWsxACVsomelJZXChTITXYEm4eBq3JVcOZpjWfimjmefGeYiFJW5GiFxd7TmhjDNoo4xYA'
    'ZOv9bWFtUhF3DpRtwcEOEIxUJBjGssipcI42xdBQMCMHBk5KgJ7hvrn/OhRuc19sQ0xlU71Gxy9sEOJnV5kmMosKIkiwiLhO2LCO'
    'E9niosyuDksIijqQw7SpNjpJvMY2Tx0vLaKdm8fk2Ar23/lpHDtwBKctLIEAvOmuT+Fj+w9gSztCb6BufY+qV38Q00KiDA0KMQPL'
    'c9vxl/e+Gw/wYbzqiv+BPfN7MJmuY33S4MpdwDu/MuHb3st4293A3kXIZijMtpWCzgKQ8yMGjzSeQ9VibDND4ToAchBoBQ1bOVg7'
    'Q6iMXsspAQAD9EoAb8WXzx2e3vH6rnRnn7O4fXrlJY8ZdTsXse2MPej7Hqu334kTDxxAd2QFJRf4XLwS0yGUzR+QPKVSn6Od1cCQ'
    'm9BJmMWxEzrFyroDjQ2c5QtZOAveBgvp2ULYzLpRh64sK+5OiIbjwig5SKw59GQEhSdoFAUrS7vmar56BJZt9RtYffcKMDW8KO3g'
    'Ist327YBUUIpxfaE0Ch49XLtvZAsAJIbx4QC9jQgBjRNNkyA2m9cqTQ0X7SYR8CsM1meQeHV6NjUxsGx0QAB5l30tlmKnF6CRnPi'
    'cikoLJre8uWz7JUP2+pMoxOoi8gqGFk/EgHzC3NY2rUNZ194Ds697EI6dmyF126/DzffcRf+Yf8D2NFKpN+saxu6mGBX03nJOAqt'
    'tnONM++a304fPXYDvuNDL8O1l7+UH7fjckymE0y6BqctAH/x7xK+5+8Yv/lJxp4F4eusfFsyVOUbBdU6ogoKMsIFxMkVEwMS0hvC'
    'fPi8QdnjEc8CvBKga4Hy+ubOnx7l8rTTl7dNn/6kJ7btlRcjtwkHbrgZx2+9G7y+DtuyugQzCmDLttP99NiZUQ2CIaIZygV5szhx'
    '0J9+LcI1dZahmm8WPLLLjQ+BqvQNZdncSraFOYPncVxH4m0wKyTITMXt+AAV2GCmw3Sa7XnANc0nK7IxF1n7gATL2Y/WXUzOgfe5'
    'spPONrldBdSUcWu0C687KhskwAHazVILr4RLtY5BfNDeQl0CRdSKPsobNmti4+PRGzKxDg2NRWnmwxLGZbK6jkMPHManbr4TZ59/'
    'Jj/py74Ap33+FThy8Cj24l5MoGcEG8AGByAoWrhgetsZmZkzAevU83y7hLvW7sd/+YeX4Ucu/358zTlfgj731PXi8//GFwKX7iD+'
    '4X9ktMQYN5CdpktFy4HEcHyu8j/LLIftBwATkRRgO7DCgFcTDWq18rAAYBH/6xYe/8Rj68e/Z8eo6Z9+9ROa9kmXomfGwX/8KFZu'
    'vRupbdG0rVkpsqEFxUfGKbiqInlGf8gn9fURWRSQJH4VNo84OyECI8FjUgUe+6/+O1fiOK47eTj0IfAbQ1EYzEk8kQF7cB0E+Vx/'
    'Y++EBA0j4LgByPVpntjliGL6euifhmorOlX33FmWwGhcJoJyVnoNivd7aL0N1qjom8GUGuIC3AFpaomHEyKMrrkyRigyeiYHEPP7'
    'K93MHRDBSPGBbKAjLRyNGjTMuP+2e/B3K3+Fp37FM3DxUy/H+Qfuw8cOHcbW0UgtTMC2AD8ZzngbtJ0M2ZK0Z0buC8ZYQFd6vPxj'
    'P4t71w/iOy76Dyi5oMs9ckl48RWJLt4GfNu7GcfWgO1zkH3lwmhZzxyRquZQfpU3vhW8MXOIpG5ouyPiRgvgYROBbtBbT3RrP0Bc'
    '0pV7zizjyy6kMt/iwY99AiduuhPtqNUzzt1CZfsAlkBMsaCWrXPXRrFpe3ZMEEYPmslMbLY6WOvT4BRJxF7SIRQhar3MxIWJxfEa'
    'xAtKfS77PfUQEFdzXECcOXFhQgGVgiSNQeLMSaPnNWtL7mUuKKx9tRpZtgsvOSstMorSowRaaJxE+2mEDdXLE6r2d0apf9nb4YSs'
    '91jfa2Kf12Xugvc/kMz/uhUno1O4jo2MlQboGDWtVSsQTom2K+neBbGeQH9rs71gbYfSDpoyywPaEAdeATBemMfB+w7ig3/1AfTz'
    'c3j6E6/AztR4jr/JSFQK3kRgA6gxEzom5CIm/bQAqR1jabwFr7n5tfihj/w8pqXDXDsGiNHlhK98FOGvvjbh0m3AgRNAE/nFx4/D'
    'MA6zZMF1josYQGZGJtYzAAfwyhS+kUo2yPtDAsA1QLoWKG9aePyZ67n78q3NiM+57LKm7NyCE7fvw/FP3gkatwEVZbCKpy9ZtzYi'
    'qpi68EYGNo6RHos+85B7ZkvVDqx1Rl2jhjQSmJOySV1oagxWGUCuk1TXRIWTG6S1ftM9Q3NeGl+Zx/4tAkJhqKPY1pdnqgeaAkS1'
    '7YTCKUbGlJgD+prtGi2wKMEMNatD/4fklFRiGoKMcxipJxxdIUtac2EiTU4zENVnUNXn9i6Qyunrz1BLxOhB1r8wDux8Ed0ZCtaN'
    'BIL7XDCeH+PA3ffjjtvvwZlXXoqLztyLE91UVg74oyMDehPqP9quwkDOhJwl1TeDMAWhB2Fbuw1/fOfb+Fs/8EN83/oBHrcjBjpM'
    'uoIrdgPvfg7hy88GVo7zhsk5FwCGmFOGe9anwYYoPmCQbEhssAJhdI9mqZaHBIDL8VwCgPU8/bwx563n7d6dRxeeRbnrceSTt4P7'
    'Hr62NqC8aLMwEIPO1TZXGjsnOQh6Nrza46yNN4ZOYE4UkohraD4IX32ZgDMYSacWYjMIhRuAG2a2wzYrg5EPiu/lAQzm62d7GdtZ'
    'g5S2Lp90Go4CYNS+k14j17nXB9eIbCZyFQJ9qg7FrNXAsIQskxNWQY731vGQIunqwewlb5aPpYHvQGKCljbmEBC0r3kgvBUKKhVN'
    '+C32WhvmZkBVbpHyHPqkjKZRFHl+IYyIsO+WO1FGDc4563QUZvSIsh6UF5/sOaz0SegVADI3yGi558RTTryWmbeNd+CfDt+A//DB'
    'l+P6I7dh1IwYyJh0BbvGBX/xVRkvuhroDOh13NVgrbQNT9XV0rWPfgwUgTkxOMU8Un1ZrsrGPICHBIAbsJ8AoOPuqnkQn3nW2QXb'
    'lzA9dgzrBx8EtaPacmE4P0pbZMChHOYzRZHzODSpwtGkGuMTP1xTdK1bDKwoZ1rYws5xP3ojmZOQNEPK4YE5sWjVxJoURwxdr6Hb'
    '1gWTPDIAm8vFrn1F0GV5ToEGO01g7IkAEgr79tr2EiFHAnNDzERQbe+G82A+2HnSbOWoPSGzKpkBj9BFLgqqQWZagkC5I1I8jlcl'
    'X4HaLB74mA9M7zAhp19wXRuvNA6NHdBwUIs/IAAO22zNyX30CszDrtYFNDqF17Y4fuhBrBw8gtN2bsc46W46sW9hzIbqVD5YjKvn'
    'hGyvTL7Kr6BBR4m3jbfj3hMH8B8/8MN4273vx9xojokL1rPEc379WYSr98iZDbrwfNh4GwKhBzmoq5IMLB1uMZ4w98+13WfnAlyO'
    '9zEAZMbZLbW0tG2Z0CZ0x4+Bu96TVxiyfJHY0k+CqNQkDRdO03hiQmtro0k5MxAlQOGGQeXwZdRnbJlj+tl+5xnWYYbuMu4VmeiZ'
    'XrKfPFcwai+TH7IkFbFMEgm4uNq1HYV4o4tRGbqSohZDd7jb7O6Tf6o5ee4qOxTAtai3WZkmpYpEZKyl3BXSqNiPEUKNk8yKSjQu'
    '/U63kKK7MVuGSqkmAYfqOYBKEAADFpstN6CsXqOU4k8nH8AT0w7HDxzGtqVFbBmPgrUy27JqzQ1/ZmYm9JzQQ04ZziWhL/K+gFAo'
    'YQLwHC9ifdLh2//hp/CLN/0xxu2Y29RwhmxyP59sVXAEa6qqXq17QyPm4SpiJxcDkm8f6nC+3aD8ATysBSBVl5KXmRiNavxudc3n'
    'Y43YZNt0QL0Rl2dVMw4LNShVLYTaAQ/ewQVNsCwF5V4BXbuZGFDzhxNT8BeMWcBcM9PsWf5JkydQtYsJf2UqY/Kaa2ABrwHBldzJ'
    'xI2AzMmSlcOz4ZYTIl3iV/aLwmoQ+oElUGs1eut5xiFyJsLt4Tj9zuShGr+VYdQ4d7p4iK4+Nwi4daVOnRrgJDl2AJbD72thQ8/h'
    'dLbaHOihLoLNhFAiUGP7tg3uJ7OPjXlI7k/Q0xs8bTuhY0bf9WibFnOp0T7GUaxjWi01c0kk6bz0jB4CAJnlVYpaA4XQM5A5YQri'
    'lOZ5gZb4xz72v/Dd//QL6JExblvOmsgiejIowuHgKr8MdLxQsQ/c4g2vigpE4GTHQNUD3ayc0nLgQqIquO91jb61Qoc/TnmdxC9m'
    '50HRHiDigZpzrWVmurGoCr9PEcFnaARtqD6Pqp9eq62mZQSWSqmhOWtxC9pwf+2uj8uMlAoqm9YNF/oOw/J5sFw5IDdHGrJZ9tr6'
    'AB5hfGvbvTrdZoaGGSIGEA5kTgvp7QDGGGCPhBM03xiWncpSHEYqgFd9ab/WnYcIsjdfuI/Jx0VH3mFnlq7M2cEHCNmlNg4qPJWG'
    'Zl9W8S0szo4uw0digEYN0CYUSTIaoonXhMoq+luCHEfGBNX8DXqIRs9IkLBxQsmku58TOha3bOfcLvzR3e/Gf/jgj+H+9cMYNa2m'
    'sQcaMssyYcMka3hdm+ya0ZPtAkPKPUqLUgeUBkIn5SEB4EZrUfSFWSPozJ7SSconrh0HGh2Ss83WLGbWhTSsLDuYyhL28TWESha2'
    'jaxYGs1J8cGDSZUjXRM5S7m2Dm0KxKpzl3wSYjqEeD3GimbBzAoQwD4nL19kjn5yRYLg39svA0nULyi4+rMIEFvKcAAFGZ9EEKsD'
    'Q/4Is8hK/XlQb7UOBrTya03KVasbQ4SgY5j+8DolWjJ8lmOSQVb9vgqot8HoOKTBUH2K+Z/1Ov/WrJoEoCVb5gB2JWw0DARhtTCk'
    'T9RADijpM0kg0DQ/JRQkZG5kvqZUa6ADYQLwjvF2vG//Dfiqv/tRfPTB27ltW1mTUTmeOUzyyLSaorLtNMRqnTXVjBSCJnZVaNOD'
    'laafXQzgsjoGrRBOIv5y2g65ycLQZVjBknSSRmFiOHmZ2cPLhUHGOm7/DYxV6DS+AYT5+NE3tNRj2X7JODya1RJApEDoilYWTxMd'
    'XgHP1YYSsRhIWX1Cehs4HSMbAqO9dZVDjHQ4o2DBzTpWGpAk83SGmjYQxnWu9xnBuzBAspbaGJkVwLU/DnQAip8rJHcRGEmZriZa'
    'G/2L12AJUdUiCHPWHsyI7Rm6EVXmIiPVWNMsYFZrzd5YvzKDexZJSrVWE36Qrqca6sWMun407iVB4a+ASpGpv0LoC9BnKBAYGEgs'
    'oM+Erifuc8M9J/ScsJ7BW5ot+NSxB/BV73slbj66D6Nm5AuzIghtSN1RsCZSZ0pl0ad1Gaj+NrlLEWzdQTklFyCBGslf12WFhaNc'
    'V6KfpK2uI1gO0TIyaoCuunJVcSlSuJqt1oc/ztAdANsJP0mxvjKftcJvdyEeTumdTPMUmHb0nSYissFbSyTnrhE82OpAwpVO7o+5'
    'kzejxYdY6YAh3qauFApCOahhA+nZ+1RBKPYzWruGu+H5DhrxWnPP0kAYalur+zV0WVgBMAQECRQSd4PiM4tqGNQbuhiVvoPhCCwi'
    'Qgo9hiO5HcZOeVdesj9foGYdlfBdjJFEVsxAn0Xz9xYAzOr7FwcANiugaOi3FMJ6X3ghz+PIiVUcXD8mZm0cSKpj5i/9KRoHJ9nl'
    'S0CaQjurpbyBU05pLUCiVBLpQoxSfCg8cw2meXW2iuAayZkPrC2rQqaaiNzElCCOeodkq/Ihtwbj2HmHRegtvbYUVzQxTu1nCjLc'
    'LC/OFXqKLAgBc4TQ+jTrE9ztqcgaeB0RaeLqZLN7BNwK62hDlnjUZ9rUogTSkqxIAtW8f4Zr1KGpG0XR+s0uOHVlWGUxE7L6KY6T'
    'xBAG6bfhFAs7mczgjrVmn4z1HYNiErZebfWQtXbY9jp1OYwGVMFkX2BonC5PZZdw9f3dxRhSSNOGSTdU0WzN2pqgibhSs4ITqwsq'
    'gJgLoSsy/ZeQ/GRaa4+5bgzoWjbl9Y6QKSOlEUbJDuyBTCUxBhuYWIjVWMhjnSyL2TybOGnqli90yQRuHPI3SD9OfTlwGWy+GAWQ'
    'pUVDbRAEg228XTerV1uvh/cK5iZ4PXovC0NYXeRsJ1Vmm/DyBle/3h8A31zTZSeIADHczSSo5kW8G7IcJ7Q7+BdRmIbCNhRXc6Oq'
    'yQ5ntOrbmqXseYYKkHX8B/bDYO3nMB5Bg5bIXXb+nLVz8GzR8mRgVAUoiFAdNJE/xWsJrpG5p/puRu/YtkFsqxTsb+Qg6eusVVmt'
    'FKUKi91H7iZFGg5qkz6waH42EwGALyMMvDMwcdgABZFHJa5QAKjZzwQ5DszmrF1ao8bWuTPlF0ZCLjlYXqxHvpk5ryCig2ezUCAO'
    'zaZB0yvPVboTzC2iDeeDPyQAWBCQUQpxApKe0+ZRecNZiqMTWmKfK3iY3GkgKQJ7zW6zb0z5MSr4hAsGsxFGnPoM177+no0Ypu2j'
    'wPPAsrD6TY8pAtuYhN/kidHsrd0mf66fghAk38DI9kSYGbcAjhU1SV0dCwyygiHzxns2jMGghP7Y7zMOp1tyoZ6ZK6wNqqfYTUA6'
    '6dXVHCcfj5AjwAZXDDk3N1opdT4/drEGWoNAzPjuDDoJbRkaefO9Ftwq4UpzqYMqQbR9BZAp95J0y8sE3/IOqW7bZaaVPbco/0Bn'
    'KuTgniHGhtazIRcIg8BgmBkbIH74O7C96CRaDQ8TA3iu10udwFYAkIA8PoGigQk+ScNqcAlu9gqAWCWKfKzjEIkRphYNPfUHOx7T'
    'Lx88HwlcZ+SrMDvih1+inyctc3NfCCm71Xj8wDPaIkvpDvNWfewDIwhs6IP9ofDRFxCF76onK+ATI4gYNF21jwiQu1Bc4x6zYGCj'
    'w4bOrjH0WkIIUvpIMtuWOwEKa1vqGFXNNfw+Kv1gAdigDOp0ctjME1cSs/etcN2qFXU9A8OrdPtMQZNSI3tCMKyDrhAGpHKSERrI'
    'EealEaEvJaFkSyJPKGg0+p+QS0OlEEqWQ6eL5QoU0sONk8mAaYPa7Rik8mwm1j0wGCmaozbOG+huPFMUmQZDf2ouAKFoRrqLUA2M'
    '6DPMzzbzx/1tBti1lbkMtcEcCFulAZVfwBUtA5oab8qJPcF318EzrerN4FB/GGADItdCGzuvyDuT32D9ocHSkaqtBwjAtXc8+wRz'
    'jWr4MgwhTAvE92x7cAXRiy6F6ZOaC+l6d9hHqyugTaUDhVGpc/Z2EErsi3hPdZ+fwSNZ+WFgq7L9H8mAOlqA7x5klFEQMdoy6XLx'
    'UI+DnAGODTchaGdUcEukKRNUX7Dm06BdvsRZaZZAbC4Aa/ZTIQtzS8fJaMQxtcqYIRFIt7IbYA0T15lJ6WtRe7Oon8rV0LGTpd3v'
    'cj63CgqBm41sp+UhAcAyARmY8+2bnMvCW67eNBH5CbdOQYRBSuavGVdXyDPwrTcYGwaBDj0plqRi5DUmCj5hsBCr4DPc5ObBQA8F'
    '0H9QsKtdYnUZCJZPZ42ugl57xrGu8N53PHCti/qsIaYYBNqiBUQNGmMdsuNyNZkMnkp4fj0xNoXBDK30YY7Wme3IlFwg69oAEX6L'
    'u6RghsseASlUFWlg1wX9b4A7sDbqGIW5BB40kgFyczICmYHrsA5rtR9Hbz8yoCd7V9JYhTysmScF6JOcYIzkm+C41QjGYOVebap+'
    '1DWe+mnIHcN+VMGgqlB1t2G7uN5fgaw+luIFXk55SzBHYY+G2jM0DsA+5jPCsFGrkv866CIsXj2jjmpyC+DCXWZth3inClIMZAWI'
    'gmnuk/ZVmdiZe6Yx0RSt7OWd8sYUyIgWVJM0cpNRp26HRv78qqqMxhzZg6VqWzoiH/V0e0tpNtSagRwDnIpk1csO03je0hrbIDBX'
    'YIhkkQvsWG27h0Cag2KjHTS586bPHIBrZ3WMuf71FlohcJjbF6Hd0PjQ76r97ZqiiM5O8ziEgf5WnTHZbCkEcNLDQUkaQjPcGYDD'
    'NVIJge5BtRV0pRmMQpVKNhPPrLvNNeE0rJJkb0jDVbVO2Q8g5BnKnCIAFD1pHVQfZoE5GkQmAuIy1AejAeE2aliTnzhyXJkkBs0I'
    'ktJJ7MhJHMx/e0awTioAhOqNsQKm8cwAB5xHnV5iZ5CK4nZbZTK71/fDDOqE3B2aUSpkZrY9t5q/wWaCxUpih8jzAxhVTrkOt1s+'
    '5N9FsCTWVB630lVHmjvuCAe3nBD6ABOjoHHqGRbD+2aDlYyQpsP1e7+nftCqUr3GBJ/C+/Dbycrg+YOM9GolKMIO2lFdOu8xgRKD'
    'G9nwRmcYEgElgSlBXRITQq2UoYwsmhzZpx4j7vrI2gP9H0aNDSTIgjy7WZso76nKEEFkN23Ueqc2DUjUCCpqy2zrZQwHMmot+3Yg'
    'LCZzZjLodwW2ueQw9uOmG/Og3w4XLEtNeAZg3ESHZHbVusMAY8gw9tYClDZ0bjEE5rS9fuVR7ExFoAFDztJD0Fx/MKblk+lqS5Qa'
    '7E2EWkvU10PiWrHtTCuuGdSZBqFQU3FJcD6Ny3YBVB++8NCf11+hXqh5H4NgD8WqBvxAhOoKuSWwsWycV9BrI7Dre+kfx5vl+uAX'
    'MotHm5IH4SrQ+rRBFX6DZJuik92bE9AnoOi25oBljaDOaGgDzHWyHmQdDtvMt6qs2JLaUZNuUnc4DfsZnA6HDadAImjE8JEBQKqH'
    'MHpWSWFJDR1aRdoIGmrJDawa3eaoFRj1g0kHAvAFu11FkznQCIBtOuufWbZ8lCGfsQZSqMwEPO5kXPtmJqn9FM065WKu5K+AEPWF'
    'nfhaoxKO2gAYyfLjeMiG1TGyuobCMlTHtkuuE065gW0jKa60kadwSEEO7srAFQlATsnDnpEmZplUDhsCRAT2KLd13AId9T1FLqZw'
    'Ow967v9Ua5Nq7IeAmPRUbRJtM8fPockeSa33WmyAUZOB5LQRAjc14crcR8MRjv0w0hZNpyozYJqiwpROmCsbIUK22Qs4O8uvfh/Z'
    'DRguFZZyajEAop5Mi6j5XEpB0pVh1deoramWO/s9ofu1bv3nZKnEEfVl558a+pH4oRFWGcfRl/09qReuFrA/cKBRnMmCYM80h8iY'
    'VBkqanDEy034lAnjDIizH3ugS7UKGcRZz/1qGtQaLAa9jkO8XplNnkeIC46gm3gLoBR9WuhP5Tqwbchqlg7ZNqE+D0RDclVmNxEw'
    'UIj5G/7dST+nGZMfMGuiuofs//n9IeALjopnxkjRr9iqVmYdWHCBTzeO68YPxAAyqRlf5+QKJ6KkKTxkkM0KkgXI4WSV7DNzDlcM'
    '8mnecNBUbTyA3IdsU2t/4jriNjZuDpQh8ms5tWlAloxjcqfJDKHwdH2aE1g1R7hCG6LddbNN2a/ObPkNVejrCFuAhlH3hq9LkA2p'
    'YWQAQY4gEXkzfA7Cjwg+QW14jdqHwBjDPvtbcuCrOrwKsGkS4QMPWOvyaOklD62H2DYDV1Ka+KBLDwEudUYvau2AkcQEna7jAZMA'
    'mt9LGrewMIJCCyHQN1E9ZoydE8zBjNtzV+EPWtT6ssEdNT+5DkX114c2ndMm0MfrwKziAMhAMhpLirdE9fQqi3k4mEZWCGjQaIQg'
    '9wB6Auew/FpBHYWIU7EYLWBze1zbRsRkpwTXYnyhbUlUZ1aVwgZ0A3G2xOcBcaw6o8QjBABpYwwqEXSFljOTw4FJ/0D4uT5aqZp1'
    'Bn2wgsZohboazdFc66nMaMxdPcjaPRoIjupJGk6uyWBEeY7aOrofG+jGlVmreZ6CtibDNCeajINGFshlVPmjgKOUaB1WnW1BPhQZ'
    'o3aMBnCltQUVrfUic2RBU+kGufkYe8n6dFcezHqe72DTqkBumzar1t9QvmfoRxEcA3i7kFHICg3A6YQcVh3hW8kMBwMdYxNyHjwx'
    'WgkmLeTGg8d6BhZsGKgCoKOwtbe2oq4nJCRN6C6xi+ztpBKS4awlNrUW/JiYJg4E+rprwEPFQIGZQJBTRNKGlUOnmApMxUfeqGkL'
    '1GCoNhQYjgNraKbCUFTydBGp2xROoKgJuA5NCp0vBcjVtgoDVQKhAwFmtHrkSY5vVFpmA0az0GnuJqMmiZhWTCBdxsskewPWZ0eA'
    'lniDnseHGmfObmNDrwqC7AQyK6O206Uc4ZdACA5JPFWYqnDZdwF5g1CRuuRVmxKSJ6gJMAdNG5o67Lm895OEHURjUTsi+j/VrKgC'
    'yqHm8Hugjv9WXUfAszxTkm3F9QEFw9Rzn8jg2kdjDQ8SZwA9aewpdBzuRhEnZtJjfIT3LCsjccqF7EQkqmzB1FDomM5R6WfDBqeB'
    'DBwPs50ivWwwOaw6kvKQAFD3Ayia+2THW6EOjAmMP5NV05V6DQDziMwPraYuD9oIoC48U73tIR+y6ykgXENeUSIwWrI99bnoOUQ6'
    'VgVymnyN6yooMWryR2CqaKpW5A4BJhCyzZ0pgyUJlsqmkSG/t4bRrB8UxpbsM4H1DNPBAanFpzsHIFw/yF/PsoqOtsOrktSCeax1'
    'Jt0N0GYCiCw8agKjQwECoQlBRhOWoYlePXZ/cp2kRA3IVc0XNXZUFHALZQBpA7aKizKiK1ip4wKCWMhU24wy8Pq52mCsN5hlVPuS'
    'gJyAXGaEX8fbUKcxl8naoDEVJnBf+8VATbYLIKy3UkRqtwDcAK58apdV91PoREg829VTXA3IKmXS8GHAiOsgmesIHvCgNkjYYH0K'
    '7jIAlkMRIOe+pcGcTmUMZnWeKGgEAGA5oMMhk9lPky0gYG4MWpgHRi1R7n3Dj0w6owHbjNMEqwbevNjz3ASMZrECCgFlfQLuOx8j'
    'C+uB6xZUzuAWiKPKnOR0k37JseRZn9eCFuZAcyNh1+wWg2/LKMqSZkmOIIJSv2oLJttfSZ7gK0T0T0wxJ4jllacTcDd1AChMPiNv'
    '6zvkjqSrEKoaItTp1RrCI/+vin4djxAGDZpb7ushOz+kZgy0rdyhi4eM2dwVtaEcjKtaJjPxg1mQqGxg38s5i1lGmJFZLIBi4J3Y'
    'tH+tKcmuLsa/0SThIrs3xlQaSyY2UHPg4DAPrjPpG3oXAMvG29GNBpJr5RT3A2jI9+Vj4WrLfzawivOQjtz+bAalhPzgcZz2fd+M'
    'rV/zRVQmU6RGTqjTXXZOEhayR9TkaEd29300DLY2QX/4GLpP34+1m27H6vW3YnLTnegPrwFbl0FzI6DPcSESJXPmbXlf0GzehhqJ'
    'GiaaUAKlBv2Rozjvvz0fe57/Fchrk4rUrgqCL2bjb/SxZ7mJmbisT9AfOU7TA4exfvunefUTN2PlE7dhfd8BAfvFZaRxi5yzViFR'
    'It17W2ljoTgLJZOGWhLYsjCErsw2shuTxNRASZieOIZHff2X4fyXvgBlbd2PZhcUkxGxMTSAMw4lAFzsALwAcrCx07Y5yYYKJPrH'
    'RLLnfSkMGiV85Pt/Gg/84/UYLSxrykQxIwoGij7EXkcNVCcidlNLEaYCozFA/ACvqFhUz5c3wxdpMSUlsu7WE/Wa6ZSs/etm1uMl'
    'tRxN1sxCHaywFBMgJeip0hg8I1oB9ZYCgD47F2BQGGDWM9e5WOyO1diBCb+ze1wzK6MBmnaYf8wFWHrKlUrEU9yS6OHLBu7tp1Ne'
    'v/5WHPrjt+HwH78N/X0HUXZulaYp4mboTmYhiOXRcWZdPx6ByIAnVW3e91i46DxsedIVJ1cf/3f9oAKgu/8Ajn3gY7j/f78TB//y'
    'b3ly5BDS4lagbdSySW6azDr+vt+KorQ8QAigceGKd9pBNt2p9+YyxcKZe7H9KVedrJ18ku9O9vlzUQZ1LuzZzsS9WYoDOagNIx/P'
    'DS02d8iuC7RjoMYA/B6/ERq2BTiB+gIeGYqSrlMS28lvdoVlbWqA1IDWe7RowjOGVps9dxgCrnw6tIptJQhHFlAAkMGdJeip5QEw'
    'FSQ2u6n2yelizBa+lIg62fdUFH0nUyAX9NMpqEm6T3Fs7caPn+nrOOADtCOAmoYWr74cy1dfzqd/3zdj/0/9Lvb91nXg+XnQ/Bil'
    'z3rWqMXbCvs8vYf463MA06dRI8kQl/V1IBd0kwlS22IoVSdrf52tjmk9sQseuEiE0el7sOc5X4o9z/lSrNx0O336V16HT//OGzmf'
    'OAHatg226SorHJvq888CWuLho7BvfmKqArW7PpJqGCQALRK6tVUgF+q7KSglhFwu+owDdrKipI1W44bfI9FRrzUjlrlgNBqD1AoK'
    'LInqOvBQC/qsiE2PngQQwocQt1VLSJSEJQC1ABpOSFMG9WLhoiGdmzbtbxUkhq9LltaluTFNJqu48pzzcPHuvej7HuaZdoWwnmN7'
    'tDHGntrnEhcDqcE38PsBUEkhVfYRbghSwKXmilOlDs8QedDgGOpzC0kWLzQJSAncNKCqbxwlVcn6jYx6SVKrKHbSIt8ekde2la5D'
    'yYXmzjmdz/nVH8bylzwFd3znj+PE0VXQ8iKQs/tSNZBlnFf52i0bM0tDG9S7JTRJmCAJ8lvO/0ArDWSuinxdveFPHk6jdT16NZsX'
    'L70Al/7KK3DGt3wdfeolP837//7DoK07DOFRPWrA1+8773Bgwco4PgQnA10FOY9O9gRo+qxbRN5q7ZdOn0m98oChFRVPXrZgp/7O'
    'mAnA1ZUOpOm0VAA0CSU8OTa9xhl0NsrVuV1g8sBIiQKtqf7L9Y2AaKUsAWhB1PUZ5fgqpicyY3EMtJqf6yt2dLeK5GJbpXd9gsvO'
    'OAuvffY3Y2luDl2vh5MlwqeOAA+uNWhafZqpe4IcgUFALrUbDgKufEkQy1nWCb/BKjvF1YBcsg1mk6pgsE2XBYYacDkP8g8Y5IsX'
    '/PfA/DZOhNheHlo5Aw08HFQTMuOGlBI4EXLXEZeCHc/5EsxfcA5/8mu/B2sHD4MWF4SSsHmOweRRbKX3jcIPdSbDG1Q53HGtzmkP'
    'GuezC8PPYHbvyR9FEK3LJKDGwLanXIknvPcPcdvLX4NbXvN7SEtbZBLAT+YI9gap5p8BGX3cwBDA7BWmOWn408kyN6UadoAMsTMV'
    '7Pq9g0B874+l2m9nctPCFTjr3Lg9p86XBz+mGnVQYNH26+YhNtWEoc0/C4yVKxIlHMAavvryK/Fd//U7wMdOYDQ3cncxESFsfeiz'
    'HFZyKZhvWlx99rnYurCInAtGbYuJBsffeCuDeyCNZNOQAK0QfoKF4ioTsk3ieF9JYjzWCgIkGWBQTmkakIGWwbIDaZZ9AZTMCjN1'
    'DYx31bUcD0S4RGHwJA2qjGNNdSawODH5bQA8cj4rUANRU03CSYCnn0yxcOUldMmf/Tzf8qX/FevTDty0sq5BKWhHUxltI0NvEBLX'
    'bAOEcg4X4VJwozqAUudwzpy1T2zzz/atc6BcaLvX5OkUSIke/XMv4/H5Z+Om7/0J8NwC0DS2si+cRkQIKDQoG1TCDI7XkOlQME5W'
    'SVCaQcNzaIJ+JPlQuAp45Rn4sEb6wPkgSDZx5ACPA9RwWR1HDK6xlGjohhyuOof9sMYoA8hmpyLgJ1DwmOXt+JpHX4zJigRGCUCT'
    'EppkVu7JKF5L7nt0XY+maTHtC+ZGjOv3A79/A9DMJcv1tygtLDPB//G+OYqTtV6dQAUBNnKl2aE7tRgc6WS7IYwT3aa0IsFlUggG'
    'GKHUOVn5JN6EcUWt3xkqZIjUn9gTNewXDtSI2jj6egQgtQ369QmWnvhYnPs/fxh0fLUyD2a0ifXRpIEjU9hHiyhTqCWSLXam1jec'
    '/56pO3CrwYX96j4wGGgkcNRPpnTudz+fLvv1a5DWTkCzLUJ66QCWN0o8EdmpK/6ypB8VFklmsmWn5JpmQCMXZgqLi1DHlWt/idkt'
    'PcASvE4Coq7OKIBt7Uqwn4YAYm+0IQN3Si0Ago6Ds9iQTrXZ7EJWIKGsDNAICVwKjuSCQ6sn6MjaOo6sT/Dg2joeXF/DsbU1HF9b'
    'x+r6Ok6sT7A2meLEZIr1aYdJ12HS9ehFi1NfMo1b4MAa4VvewTg2rTkgFncjsyWChSMzDuS04pmeWGark+Mk0n5q5wKwDhKRzprI'
    'ez8OF1zdARbmY1+WZx6UaYAI83FglLnqB2GSgZoMwx0Aw+8y6+AkAubmYtugn3a065u/Gjuf8yzkB4+I72bwxXUaxpKOnKw+jyuf'
    'XdtsMK1N2DTsZNPApgkR/mpHKQ4ecejXDJO6cOk3TUKZTHH2tz+PLrz2ezFdeRA+S+FtqQd3VEE0ksroyFUq/FXtVveS6kiYBhpo'
    'SpefEMEOY7mBNqH4ueHxTq6z1jHOMNTmlWfIYZi9TrYMBxtL/d394mErZjsCiylZyNbkkcBYBGG+JTSUMCbGXENYHCUsjhIW2oSF'
    'EWGxTVhqGyyOGyyMEhbnEubHhLlRwtyoxdwImBsTj1vgA/cynvUnGf98H9CONTfAjleaoaWtH7AdgXwDKJYzMhmmivTleQafZRAw'
    'kIZd01NlfGOGyJAbzWFBOVuNXPo8S/mBVqzjwJphUqoG0QoFvQO6MSQCG+MJFOdNKxHNxAdAZ77iRXzwHe9H6XtdL11J5z6VO8nC'
    'YkWX7ZomnsFc91OtGEA4extjc6kBXG22i1iTvNlm8joDB41GOr/PTUI/7XDBK15ED37kRt73F+9As3Uncp+tTjIIJCcJqfqwhttU'
    'ooEnB8CiwY60tkT2pIFDW7xSLDUoJsXEoefBW1IFMDAZYN/ZJ0l74xIzUod847MbRlwLjRuR9TpLfioeVNDnqEAFig+gwcZ7jISV'
    'KeGG/RnTB4HlJaBtgJTIX40e9qF7Dwd5YQAZaxm46TDjz28B//mtjL4ktHO0YZWfxhA8gcG7EUg4iKOHzEv/5+Sod+rnAtRbi6l8'
    'sE4osbXAgl/hUcXW/KAKgBdlSWdDrhqXQGhGG/IWHqKBAE87H+xBiqe3XVshgUEsX3kp9jz7Wbj/9W8Gdu8g7nPQeaia14CM4kq8'
    'eKTHUDgsGBXpYHDUNIM+bWghAOScwTmH7Z6q2rYka/mWK3iSLNG+/Nd/lI5/5AZeeeAw0twcuGTTDmT600CBFNSMNSp+Wl7Eyacz'
    '6yBb66U1ko1IoLb5XOV3PGRpRyOIWzSM+ruZXFsbQiB6bQC0QQCLaj2DLsb6mHgeoD+9nvHm3yG0a4lpIcHy96kBkETriaYu8lui'
    'OhsIxpQJ3URnDuYJbZuQS5hBKYb2cjyVe8uzS3po+NY2eyFAjgos/hvNjucpTQMmoiyLbKq+c/9k8OSAvhD09uAZK7q2JgBaF828'
    'V+3YjEY48o6/x+E/ehOahUW26UJ5rNg/qR1jtHsn5i87nxaf8STMnb1Xzi3MWcxgGvKpSbO3H6DTvv3f84Hr3o6SRcoLg5IGT+Pm'
    'pgYERMNoQUFYwzur6/wmAEX6tP+6t+PgW/6KR4tLKLlHLgVELY+2b8fSRefS8pMei6UrL0EzN0bus25bQ/CdjzUFV2hrgVMGUkLp'
    'e8yfsQeX/fzL8OHnvhhlPK7mMxGARBzA0bI7k40T4La9gbCbWTO6YzAVqmBXuKAdjXD845/Enb/4v1Dahks2dTbUqgWgwjKPn+zg'
    'V5YdnKS55tMyLKRYuCBpHIuRcegjNwHNvB77XgfZhb8ahLMsoGwmYm5b+G9kFrMaa2U22AXg9WnGlBI6jMBdI3sDJJKp0igPiWrW'
    'WxTWRGjnhK9LYTH7izYvWJEi/ORj4wxGAFHyYKoZq2Ki6vVUzFgHD1fyADjlDUHEAiy62sLAUxgytCgZ55AOcIQctRUGRKbKbFT7'
    'Bg0erv3zzbj/D/8UTbsblLNeXlNo7OiIBObR3l3Y/e3Po9Nf/kJgfg7c9TIthmrKDmA8JeScsfzUK7H8uItx5PpbJTfANJ8OoDOs'
    'n+m0gTp6tFS9zxeBQC0BIRQA4Og/3sh3/sEfYYxdAHo/Z4DAaEA8t7iIpasuxenf/lyc8YJnEwDkrnMLvebtm2DXPlHToO86nPYN'
    'X0Z7v+IZvO9t7wNt2aZTnQZkQxDfEMAMuG6/ml5FHL2g9eNUFACs3n4XPvV7f8AF2/TMplmApAHV7FsNHQfbI7bWAMH6UdBgCRiN'
    'JTXYXIjPyGMzA2eWIs/0CxVyYuPM5bGpdNlfp7WwGAoX2YHbYmTqC9qMR82b8KQGoDB6VqAduMAMJzgTZI0B+7mrBki+ODsGjmeB'
    'mgK482cJAL4asJQkjJcYuiexD6nJRLB3LVE4ypujaU0cqIS1966h9Zv5MZp2B5rTdoD7evCns7J2LhegW13H3df+T155/8fowjf8'
    'HGjLYvXnzKyztFh7Xp/Rzo1pyzOfzIc+fD1aLMGXohoqQTV+7eSAXQYgaIMZgMIFRD+nxTGadjt42w5Q7jVxrGqtSc448f6P4d73'
    'vx9nvuHt/NjX/iRGe3dSP+1kqslN1Fk+12/0Oef/6Itw/7v+HtwXj/5KP8zsZ9dQgwAhOKyMDLQanEqDAOYKEgEISkqgdjtGC9uR'
    '4u5DgYaM4hu62FMiLYZQQD4WzlPMKLkqFW+dNcNjQBvPE4r/sR3CEq0Z2jjOFFwwaaNAAmeAcwYz1fCDGbkpsZyVRvAzeRQbMGij'
    'E181YeiQmFZg0mEkS/+fBVUbB10SDEA9h8obJ1Ffp+SqGeiQHsZQ48TkSGql1BF2YKqLboDhkp9KeOn70ExEZqDPzFmW9spf8Y9L'
    'zih9Rplm5L5HHjXgvXvwwLveg7u+/6eRzNe2wdqQVVJpsfwFV8osh597YFNZLLsQyyEOAtkzkkEgtg0hYxCyPmdo3XCfwX0GcpH2'
    '970wUM7IOSODwFu2ot2yF/e+9d340LNegLW770U7HokvqVM+PhMTugRmUCL0XYcdn/d4OuPLnw5eWxFaRC1hGBzbxQgzOaZts3Fl'
    '7JF13FnK/VoyriCgLyi5yFj1dcy4zyi5R8lFPudevyvIudfvMkqR30su8l6vKbm+B3iW/ezpmLUe7L8B36lwyZK0aJ1URTzAfsLg'
    'YcQMdAB65sga9cXgDEYBUzxAybKEPZWXPXZUH1wVqD3aOzsrdlzbbX2fnRXRDxvk/VQBQGcBENJAA6G0IcXsoyADll0HBbYBB9m1'
    'FDpZa/XrfKPOYZdEQM03Low87dDs2sP3v+7/4Oh7/glN29rcloOqaz5IXwqAxUvOx2jrsjAjiXbydlhElW1STzLqYgykHpwbhEWm'
    'SVE1mV1irTCtXwNx/ksRYRlt34MjN9yCjz/ne9EfXZHMRsutqABk8DzzDOCc734+NakJa8yH02jWNrc/BgxeOWw4GqGrEXxmlIvw'
    '9zAYZ/ZUbabrhXBFnRCtu/XG+1Fno3Sb+srqPHjWrCC55iK44A0RFIEX67WpMg8YTJ5wxGD0EOHXRXIyA2J1q+Wgws8G0gBsdZ9Z'
    'FhwAgZTtHFMHABe4bKBL9RlFF9Zz4ho49LF8xACgrU0OPUJQHtAORHUQGEi6HMWj526faYOdwYaYXe2LeG3tdT2WrOK6+UVMCV3O'
    '/MDv/llomixqoWBamWvAAMZnnYZm93bkaQfLVTR/q7aFwLB93cROtWOZapyjIpyzpbsgUur+M4G6/oQ4ooTS9Wi278L+j3yMb/mB'
    '1yA1jQOPz3JYUDJqKI1v7HjmU7DlisdQPnECaIJlpeNU4vMD3nmWJTdUdSPNsGEtzl8+XMX5wKbAZGyi1UEOkgMsmeHs4fgqhYNU'
    'RPmwWEsV+5l2GmBrn9yiIuVBN8kDrTALWoEWRZPeOPABQ9YqSOIewQ72DKxsmtDwh8yEUrpLqHEIqNYSAxMM6FLH0C0F/cOaGwBq'
    'ANqQCHiKiUBauUXfuZgGM+dSmZJnLGSCD7A3M8C5T7YE/5A3DNwwfJNIdggZTGgoJYQJC9L8PFY/dD36lRNI45EhN2rad0D+vkez'
    'dQnj03eDO1mbqBAgx1oF4R6akeHhQS3WzT6VjXxQ7ZKTyJFVETjdxrV0PdrlXbj7tW/Akff+E9qRuAIxv5x8DAymCKXv0cyNcfq/'
    'fxZKWfcglF8LhEQrbQaZgAHmOsVxqP9GuqNaA1oXc9D+FEbQwz+qKIwWRrOo6mFa2PUxnD9OJhsz7TQm5PjZGTM8hkiPLxuCMoV+'
    'VRpV7iyQEB90Y39fCVvqe7KEOATLmGM8xGgaGhUtS3Dd0oHFajDFQ355CfQPQER1wb5PEZyEcqc4XatIzZAEj1Js/32urQNosK9t'
    'eJo9nxn1SFOqTHMSJvT7wCGPjb2yBOZEhRMKk233o5fQeITuwIPo7t2PmuMHH4d6dJ60ISGBtm+V+ALF9sL7JgBjk0ak/xsKV/Vk'
    'vnDVcvCFxvbsys6VuQcsqGBmrk9Kcv7c3a/5Pf19dtiqJJpQJaXznq/5Qozml1G63kG3Mt4M4cM4Fw90Kf3U9VBsGIyRWzoBAUpg'
    'j1jq04G4mKtm8c9qYfPzE2Jza11VsD3VOFJmQKua68QMSY0Iq4vYr4l0QeDo+GQMp8MKD92zwuCeJffO/f8I2Ea7wBv+QKsDAibm'
    'VhRA3DgBejNGB0Rm0sNEAaLim19JQsLGnpwSAGTfdsSeYVpODzhz30qn3cBsR4YV19Vs6GVcosxUTWWtFFXchxooVftuEExMBCQS'
    'KonLn9CfWOf84DG7VZ8xRN5QKM3NQQWIEKeuIuMpWX0blqRCl23gTQhDrsHMo+qMBFeT1H4zILXv9E3JGWlxmfe/6/18/EM3oB21'
    'sI3aQ8PqZ2aAxA3YctlF2PqYC5HX1obqnqMAkoOWTw0a46vWLjnXS0Md0WoxBmc6Ocy4uWr+qtPGWUItg8DUNn3mNcbfht2PTXHN'
    'ra7mQKzZ4nAW0a87PdCMZRmtAqMTIBZOATROypbYYPPlcE1euMZSlZ4UusDDIRmgjemrgYyzZN97P312JuaEiNOtMatK3I18f6oW'
    'AJPwfU1RtUBFHMkSosuuzKoaGXTQmiNjZPbWTDGGoXp/RX25QFLZ7YGOoR70K6GaKo80mB4EUAOwMcpLQYIjeBqjWns4/IDANBas'
    'ipxEG68b8DsbThHAsjKhFEZpGqxNVnD/G94+0x4KTzb0UAHuM9KoxfanXw3GZOZKZX7dTGQ2IMaB3kVhPT42shPpD/VzcstoEMgL'
    'zavUpFCbkZsqUTjQJ4xhBNBKBeWBGKcCJCZBsc025kkshJgK6Nlj8co4WvFpZIQcgHjcGIeZZc2MnwY6ZCWxzmdMG69c7UwzG2kY'
    'IQmtcMPB2n7SEMLGxYCnGARkT79CJEnkAt/ZVFth++8GIxJDctbgWPSxYtiTUmLLvVI0GzCIi5GjaSLojN14aQHNrm32MP9jWiEy'
    'UAFQJlNJLLL2+wjU8/msnz53rG0oNBzAatEEqebBrx7CiDPhZfC31FAaCROntIAD7/p75PUJqB3BYhnsZCPUIGF95O5nPEG2neLZ'
    'qLu1x7jSfPMIevJqRg3He0y4qxlaQS4RYUxJdqIPIOBuFCVQEkMqBvcqaKDSX62JwRjO0NJnXNwQsfEN0BI1K2RnHyKAGlm+Owj7'
    'MVyDzIpmAjiR7ADWhFSmyP8ejNRAkB+Fqa8AifWdPdPe+98Q5A3D4sa3z0BFxVW/I05h0DcizSkBALkKC6ZSuNPxLzScVYsVVss2'
    '0GC28lpHQH4ApbDJo6oNy2qySHqsUXzzRASaSErs+Ky9GjCjWofXN2gFl6PHQbpnYrKlr9oW25FU/hQOPdYuDHRhcE9m6AJdfw52'
    'ATITQpdRK7SE1XvWbGakuXmc+OSnePXG22TNeWH/3cDABIdZdrsBgKXLLqR2cQvKtB9qz4Ez78os9D30KT6rBpWCFT4DK1xkr7wu'
    'A10B+gL0GegLKMsLfQG6rL/J9dRlUFeQ9Dueyk7P3MnW6ANuiRYAEaL1Hlvjs0YiOYPfi/cj8EYos5q09pcgphl7O0T4AygD1dxn'
    'N29knJirpVciP83Agyu8mXaZdWRtmeFJ6TdQbYaTmgSnfDKQmIHSWmXHiiduxmivJXAHclEZANjQlLKZADMjZ/1U727USqa0Qr80'
    '3CE7Da+fwPLnPR7twjzyZAoKSUEkUV/YXEAajZCPraC7/xBoPNKnhZXiGzTmRq2w4YIB18wgzexQyVwNiOUU9wGdDD8Kg5CANmH9'
    '+Akc/dD12PqEy/VKpW+wODxrmWT3mYVzz8T8mbuxftunQaOFGncJbS/xjF4izHI+57CS1K0Xe5al4ur3owQszVGzMEJbMjvDmO4N'
    'MQLlKxBqMowJo+bQQLZYI+TVKbq+6AGa2ge22Z8qZxw+W3uNOg6Q1tmS/YxEGTqdmYoG3OzYMaOHuPYm7IPrGBIPkOcJZdqYFB+4'
    'okCOFjdHWHdWLggZsbPWicbaiq2WhWUBDq/2u5JpvI0gcIqbgnLJpUgGW+i0LAWspLWREB0moKCzoNU0dZPFKFXNp2C4yN82wVKJ'
    'ZD5ZB912XVVFVNRQJCJQzxgtLOC0b3+ePMKbVacAa/RdJjLX79uPcuAIMNLEITKws+M4zBGpFju5yEVflF2g44i5FQOZcfBrjRMo'
    '9JqsZS7OSqk68bf6sVtmqqAg1NpDTeelUjBaWsTCo87Ag7fdgUSaIu0iWY9YGWhzIlSzmGo0nbWlxHV2w0BAT9rZ9YzPw7NueKvM'
    '+PiMmg4gW4uhprvywYA3g7JUw7Odn8MH//OP4K63/jXa0TZQriLidNoAvHVcONRn07yV+GEsQhNqzaaVFTNgQcCkO2QV0XYGK4mq'
    'cmKGz79788Lv9uzsE3dKy9ieOrIAEGf+artDfwONGUWSiPUDZsqpHQ6qcw5ygIFsUhD9dh4MA7tG06N6ahtnTE4AdeFM1Pb1VxQU'
    'OYZcoY/U9rEBtTlcO+e9338fzv6h78XS1Y+hvuuAprE71ScLAqozEic+8Snujq0gbd+qJro8O6bK2Im5chSIo/uGFlfdMsuclZhD'
    'jTJr4IVkqoEGMCYcYfXmO+V9U2cokqfvBpoS+QzF3Nl7IdKYQFQqr4Qn1KeSr+bwMwJTjI4GWavqXZ5XCprlBSwtn6vjo+2rVwPC'
    'w9g4sYeT3WML6TgtLbhmnNVyG7Se9YN5+D0zoCtkY3833Dxobv25epECsjHzj4sqOAM0cu0HDpbKcCmlyUa0S0hZ3Ha12AhWfk6A'
    'KxBTHMWNjo2RwPLZ7QkYO14NDXmUaF5VBQgmHSciKkwq/pmH7RwuKqkdcgENGJFLQW6F0YWfyUwO73UCxLc8ehxp2uGs73wBnXHt'
    'i9B3HXxoZ1wLUgRm9QePvOef0HFB49ck61bts66DqCBO1QXyOAZqcmQI/NW8A6gFRGb26rDTSZhPoZUYasOJcmnGWPv0/dwdX6Vm'
    'yxK46xxBqjIwCa3WyfwZe5EULi1dyMnI4Y3zZmTIAb/aDQ5J1mmC2CmlL2DOg6tPBpGzXf5Mn7kUpLk5QimyIGYQv4hhVBszDBTU'
    'sNhYEaqardfIuRxDHrN/GYzMoETirChXDmwFC8DCwUc/BXGOqtuHKkU3yngn7OxB2lIiogZI0OxWn8WwexMTCpmykzqLMlzaIO+n'
    'ti04216z2h6OGhgh/MJGWrCemCInCgbcpDg+VUikv8MUSF5bw7Q/QOmBxA3Xw6dEhKoZ2SzNYcsTL8PpL/422vHcL/WdcHyFmlM5'
    'EIoZadSiO7aCo+/6AGhuIexhKPBpviDHNuqznQlRexN9R4dKml2EPZvoopaAN9EkUHpbvC4189sG08NHkI8ex2jL0uBg2iq3UT1L'
    'mT9tOwgl/FQBd6DpXEfXSMig8xj2byCI5soRED1YGt468NnjY4VvtH77sEFbyjgOMkyD0Lngh8rN2TEeq5LGQJN0tAvqvodaF+y+'
    'ABLMyABJ7KJYltLAKgFDTRy1CvR51dodqG0Yk51sKIbwdHLCmcMoVesSwECfwe0z5dRcALDuPWjqQLWLX8EeePJ/B1NfQfh45puI'
    '1IZ0iVBKwbZnPhkXv/JH0cwtDLGa5ZpmaZ6b03dh/tLzsXDZRZRSQu7irkCxExEEGJwLmrbFwbf/PVZuuR1p505ZlQfTz/DFPIAz'
    'NA9bPIMMqPX7N4Y/QbAs0QbDK53xZqdMrQXMYomXlXV0R1Ywf/ZgkFwwWdseo+KjHVtq63jD6A3Gp9oHrO1lDCqz5zkQah0GhGz3'
    'R8HRz6GewfhHLedgEmGkXlTZHcNrAn8O0pmp5ssMYJdto6sQczmJkBjtRSKDYPme3cG91GZapl5s+sYYNyMe6FvrMdrC21/7L+5E'
    'qV5crS/gvuuBoShuwIRT3BacU/XYwjZgocbaWXYhVR3mwcACHmjZgTenqEXC5SilYOmpV2HrU696qCY6afq+9739qhYw7Ga/2JuZ'
    'EkoufP+v/DFK04KCnnbzCRWVqVbnFCXWjLISKB98zo0aWbL6ChgtBvmGOrloI1UBQvb9C5YLEbjrUNbWnO7udwYGqpuSSGkXFiHT'
    'sralWIAAru8jIwZYwKCyQM1BDDjQqzYuXj4zVUXD9yYgfqgKhcpn7quzAKiC6cCDSi9n/goeBEictwwdG7BZtHYBuTWjVEEBo4EI'
    'TnXQK38NoJXTgH5kwXO3cmYUwWDMQr8ZiEZ2Ztn0qpRIxI2KR95oIgIBQ/9byim5AIbxRASkhgemoRUL8EaRM9QNl3Mp3sXqUgRk'
    'tIgyAHQd+kGbZzSsexaalKKBQIMemy5xAikallLQjse8//V/iUN/+4+g7TtkhgPJ01ht2y1Ybzh0hAUk3FNMQz6qTXUp9iYXT9E0'
    'wspzjIX8lF+DXgBmChsPlMLgvp+RDAncRYUaCzVN1ZRRNZE9N5LVxlKeX+BGUegfV5zSMfPRIWzg4yEeBUsg/G6fTTBM7IqfLiN0'
    'KspnkcTusnilrEAx9MWdtBsphNlCMbaBWZ4naJp4ZXj2XyIIkgeEjH8IHheq3DqcdXEaI1xkg6RTjHXyhPy6qm+0PtsUBAmP+Hjw'
    'hFSYCygRIzU16MWi/ioD14YNkNBpRr5IJXxZYQZcGcWEOvxGM3lLQpPKPRGBYwy+/kIAF6TxGNODD+KO//HzcpiGtZmyTTa4P+4C'
    'iGD3KOG5SIyjaZoK1SZQMVAVRLVJtr9djfWznSLrgCUXSyKwrrlUqXK4iPyqbgWFNNbhnvdQUCW5ztw1rS+EaBTcLCdAqJhMHc6M'
    'WZ1SNTBQkeVqDQhDVimJIbM4kPVp7BaYa8WAFRms4Bzoal2I8SMbI6D2j4eRiaEiGyoKOHBAeVEepvmUCg2NzwLI+faB6xj14GAF'
    'ILJ9AVG5dPB4Q8/AA9ESssz0ZJ+1a5Y/ovk4mlAhljfYBwT/X3vfHmvpddX3W3ufe+698/KM7bycOI6dF3lCBaVQqoKEKJSojwQ5'
    'UimIUipalUpFKlRUAjkG2pAS1AcFASXkj6YC2TzVqikhAkIglIQkJjh2/IhfM+N5eN4zd+aee863V/9Yz/3da/s6dkLGPtu+c+/5'
    'zvftb++113utvTbTNuJ76kzANwZUKkHy1ELVVCCnbBzmtPEJJt0SQIS4EltL0j6tgdnejcUL7p5rUviYhCCEzWTfAV5kQRCL/G12'
    'VlsB8Pnvfxc2HjuGsmdd4rgwizFGLvAOVPYE4cRbhOFtY3U+xuDm8sty/HTTjcyu862YEkxkibSZuRKkFv24uKpDfWR42qc230JE'
    'FeC58emfNNwxrRMy7rC/J629jz8+Cz4wpAR6812pOc/RCZUFv9wQ812nMZ8GYAFj5LoyHGvlA+bRHEZNksGM0XD+IsFsvKaJ6Hym'
    'HJlMoKgHEGDIvD9WIzsBvfcdcMhCh8rJjc1uv89uyQyNcmLBjt0Du84EpEIkJTjdxg1Cj9j8+EHlaCYBmnENH7X9qSzcVNhM1Hpr'
    'D7J4Nsib+zu4z07joQG1otaCB37gJ3Dst34X9dD1ovoTVH0OVVyJM20gjKhACE0yYvaXM8Olhd2c8TEJNMQGWyLNQEqgCKlsjAgQ'
    '5Cq1ok7X9PseKk/mgZ9f2tCxbIdiUWjllclMmYHIpuy+S9oWxVOpLDiPHxm1ndDyySk3fSXgJ0/Vsrkl1hLSr+PYnHazavJY90ZC'
    't3yAviM8/TvhovuZTOPPkQZ70o+V51gsuyOZB5kpA9BECKN97unZ7830ZJoX4pknabuMAuTK4so9VQrEQAK53AOc2IIhfhs7XtK8'
    'bag2Zidumw3nuxC04yYA+/2aroSmkmRldRVttoUH//lP8NH3/SbqwevQ9HjpAKB8srKgxA3cBW8b23HinADPWT32GBf7Z18Mh42f'
    'WZNa8Rutb3LsVogSgdqAun8N9dABB4FN2Bi0xeMzom6dPJ9JQ57yKY+WRBl3Jw1dkYmgWCIrmXIbMJlOcfZjn8I9P/xetDpFawth'
    'nkUYyIAGL+KbxSTSK7TnZlp6Ay8YuHD/I1ive9HakO/fxjFCe9Nvt/kvhKgLRDExGJKsgl5ykQsKjq6Hq5NWpHZOnRIaVQM3nBwV'
    'Pen8ml7yPZhRMAb2UbHtUjM05aS4UKxyrFgvDOXEIMb2AwV26QQk8OBKCmd1a7SAFJLK11eArXYTi3fNaZwTko6cSJwm5KItR2QT'
    'g6EMEEipJ4izrExXuAC08Zf34/4f+Ek+89GPY3LoReAm1X9cFQZpfEPfGpqKbcs2cmDd3wWHSSdCAptDwwwEDGke6N5xP0sNIu7Z'
    'KxERkVQyvv7FmFy7HwPQhSqDYA2d4/OlIycwoKDqGNTlANU6uoSziIB3M/KeufuU7tBfl0+ewuGPfYQJB9A0U8Gksx3Wxd3EMwp3'
    'M2HxvBMGACtYA00mZkrq+9xF17eRJA1ep/AF1Lsp4rp/PrLXzA0kZ3zk7bh9zoq9xP0qJvUZAJeAeYKnZCrCYS6Kr+OPWBKuFRuS'
    'j7T5LPhlL7kjljmUUyLaNlVglxqAJuPa6cDOZ5Qo3AtM1Ax9dOkESsn70S16z51tgTpFbgjlw2WGI2ssJjM8y66srLgKuvnY4zj+'
    'C3fykZ//NczOXxa1f1holyEA2OoW6mGqjjvK1IKgehiylGDJF3y8HREqpXD+THlFQiA6hCzDizR3nyoNbQurr3gZ6t691ObzQF3u'
    'QBIw1e8vHz4KQGsKbuM6gNsxTnIi+xyHE9Pfidg6NlQIVPejrh4AtUF9+LKq5sDbZnobQzd4h5WNAsYEGsJMjthw+mdpl1YoDUpn'
    '083cjjsMRieZpnHf2AMjLTbHDTB/YC4tnn1QphpYPcrGkSNhOJZ8wMGDYUyB0UezZMTqWklXCaCIsMU8OZyBO7RdMYABjczxEiV+'
    'RD+rrG4Yc8Oy+dDZkS0GQBYyc9LKnNmTJ5RV1lqfboTbhFEDMDt8DFc+cx+f/p2P4Inf/jAuP/EEyr5rUA/tQxsWRpiO2gypC5e1'
    'kUz8Ckadi1wmEHULuVMzPYFj22khLSrGiCrkac7mQOq2PZtaBMKAOfa85bUo0HBgDdkZXQXjKZMVzK9sYvOhoyCs6NZTWcumT3kV'
    'ZKfyeJ5NbrvaPSJ/2uFvPZ2ptYZhiAKhJjWNBQlsjHAMzimiZMifzMsgjVgmH+d4Icxf1V+UThTenJh3PxWVyYlbcepBGFO+aCpV'
    'ULKz1DzhxPVNeDofc4e4JA6bT8w1ZetTTYxmn5V7mKPckvPdNeUniT7DvQAWBWiS1Ohs1CRYZFsFwCUsGBMSfEsSNIk8M3sCHPqh'
    'MSa1YOPTn8OFP/kkl/V1IivCoQaF61SN0TauYHHqHC+eOI3L9z+Ki/c9jNnJMxjQQOv7UA9dL17ldEIOVM+ItVEuy0SytL6f0zl1'
    'xpBsCyfxPnIoab870UySmt6PIYamWnkIVEMfpMi6/6+/ue8rdRqHyBGIG0oBNo4e543DT6BMpsr30jan/FyaUQPrbk/lSan0lGcZ'
    'ZjHeUVmOdBjBUBDsGJbpcyeNfYiUcgsCcMGg4KsRkSDAZBYSohnrV41EFCuXyvB8fXfEaiqyECR2bhlBKByFya/a3Wvfh59QsSj1'
    'nxlcpwEwkCgucVKbdRPXRCtpRZ25bxvPLjcDcQ01ONAkaWP2mkBoBgaUkKEG4LSvPCYcEofAIm1WJrjwoY/xAz/yYyjlRQyz2btx'
    'GQI4SIG6AqxOgWsOSNosNz0rUGPgClUmEHfHaDeQ6X/Ih4Dqm5S7+/HZbNqAW9AWyOgSYbw+YMd4omXtRzaRx33mfRaZTsDWAqv7'
    'D+Dg175VbtEEpGQeOqCdSQK4+Bf3YbFxHmX9oKitdj+S/UzFBV5T45bgoexk74aHgP1ThwgKTbjtaagXJ+LkVQ+Y5H6N0INJigGR'
    'nxPdJK1RapzuNEZq9T/tpGpdPQGl+e8ZcJOWQWT7qtPMrX6QizrFDXmNjdZeYngTc44xUr8GiQs625c+PdDizt1UkDs/ROgFDgOy'
    'LbsU7FQSbJfbge3QP4gkhUooAxIMYeSvhqZqiskZcmGRdBDqFr2TCnp1bRVlch3KtQeDcThXhIeA4jHS+LEiv6Yd56PCk187eYoB'
    'C8Mph+VYtLG4Cg3IWEpu24mR87xJXPu+tD6q0JwYjELsfet9tYAvX8D1f/vrseeWG2lYLJw8/XDPxH1JGR4AnP6DP4epm+wnziqR'
    'jlHCJpewlgCv5mwSK0CTsNVal28ywnxKTIMBC42R/xtQSI+4hDcgp0/ITCOZ4mkEmeMYg0Ro7crQiQoTscdiFc8pF1sBOKJgJiRs'
    'WCoLiOHHscXoqINT8OoQEO4wNhiZJLVzBkdQNdHgI5NEGU4Dckegqz2jtssoAC1ysUNXBzl2qxVk0pIpFcWUbk2SnmPoJSgf9mFA'
    'joGFHSeVt5cqsphDyyY5FkZEKAjCCrkRmX6hflE8578Zudt4B/uHnn48NORg8KjgGLiyevCThhwWkVdsY2gMTBoBWODl3/UPUErB'
    'sFiASnGCtPmSwkN8hhWL2RbO/tGfo2AVzEPMw+cXkqOps5G0jkPIKPLyYv6khzctUatHL4dZIrD4jUQB4mjjpGGPllIvup+p48kd'
    'cRnEkl3tkSnX2AzOavVofL0RUG1gZK8wbp5mRFC8G6IsnpoR4RQHQCV4MomfmKwwlbE7ZzRjkZ0EifYPJqYCP5XIX0M676TxZTe6'
    'Z5k+SdtVJiBzqx55VYCF9FTvPxeSMmBEzVRox4pe2gGe8uMIyCNCtLsb2D3D7n9ASOEAekKsIKHeL6QLaxxc+FjpuGgeaegn9mPB'
    'ucwmODmS9C4ba69i5GFg1IXOiSj3olMAEWHY3MCB174GL3rHt9DQmktZ9zsBrtYDABqj1oJzn/oszt37edDqujgNmWLtHK46W4bv'
    'jwsGpfMdYlOG+Xs7p2FagizJexEZwwvtOfrp06PTs+ZLYGNWhn8Jvmn9GeF3683UtP4WZ7br9njK9+59REAFcWHiCYFXULmgctYo'
    'wCP8sc/2ZRpUyGkh1x7r8z+6wL5bzBiyg11BFPpSPI943nWTvu3uXACwnA5cijKA7M1VO085WRoHjGtmMjQCLz79xKBGMSxP89Tr'
    'ei5C+qFekhizF8i7gRAEHIgfL3c7296aEDtYXIdJI26R97X0mkl/n05qdDHZyflZRyBCKRUYLuHmf/t9mOzfK4d8OLx2GEhqJ37j'
    'wzxbXEGblH7+ic4N/Roi1MY2b4zs3bRuMgSVBromNscGlT4mnHxWWc03cKTBmHTpDMQen02mRMQgLY++b2AmP69T5kOyjx+SZs25'
    '4lCsc6Okx3QaTTAYAsG3VukLfehQUlM8VAe8ehKMe5Gcj9ER+QgWYJi3P+GjvjLBm+N942yGDqYg8A67AXd5LoDvfqDkQUmOpgBO'
    'AXMZTYUyb6eUD9BRJQJT0ug5Xx6z85gh1J2rv42mQ4JFERMK+6+boJWJ8ivu54hLug/NoxoK/BLOKVkR/W47PcIryOo/rL15dDjF'
    '9QGWMN6ls/Syb/pGesX3vJ2GxSCFT8k72M5UmFGnK9g6ewFH7/gQQOtow8KJ37UFTk/JdaFnspOWlPhBaG4D9Egm0O2vNR6UqMKP'
    '4oxNVWWDdTCa0drG7T38ElOw0fTRhtQFSbHYoVdOtBy5Ciw7uNOYAxuD6udE0a2uVAO4dc4I46sMAxoIrFlj6TQP+TNzGnYmmlhI'
    'R1p50sxaitBKdCY6cd5OgQuepxL17rztlgEgXN2NUHqpGG4MDlxwu1SLdioLyKfaddpCstsyFmTiNdt9e1hNUYCxfem6DwqurGhk'
    'QI3HZVdaQmBHYrmRnaR8Ij3W9koNTHfLCqZJJOdden+tK+CNSzhww4vwxvf9OLAyASWbztmsY57OQRn947/xu3zu8OdRVte0nmMA'
    'ZCTQocTKblP41zu4LBOftrR3dFMuYdF3SDxWdne4BWkd0tWYIvsuSQCe179d2TKfVeveGHxTBXBr2MZltr1VsYbsWcbQxfiSJiJs'
    '1KeSs4yIjf/Tdg0GarkbNhFTJCGRoh1lkHRcMGsg3H0JYQBt6Os6atvt6cDC0U1soQeYgCmMlLDjGEMj5aoAe7qNTysEmBG2qyxA'
    'l2M/lhL+sXF28zlfSuwz7ORO5uv9eS5jp15+l83JfljhgpGWoCyI9cX224iWisKSk93IkSfJsk6TuoLh0gWsH9qLr/n1n8XeW26U'
    'akda/CPCsokalflQLRg2Z3jwZz8A0GqU/O7EoAxVC61xk4Bpkp4jkkraY88QBEiZB5SU9+FrYFIyx+OdCWZAJxLm7fjO6TmPRIXU'
    '0b5dnOrsuO/E5kGEiEJ0s9Xv+4fM79BYUpNdnJqW4yQ9cmaXQBvs2IxhGKK6x1/TLVJ/AxRn0DF9W18/R6wpNhNAR44AWzOAuri3'
    'Dm0XrdnYCQDJ8WBEqvpm9p8IxRqnPwpKjzicgOybWdJTDjF2IMu9hkSNxwc92P3ZgdN8WAzJ+Q0V3oDv6KL3ccrs0jycuL1jpD1T'
    'sbcj3Z4+ooCl5FkhSZkthFILqBJKrSi1oMy2MFw6jmvffDO+9vfeT9d8/VdhMdtSM4UC5slOdqIeGmqtOPw//xef+czdKNN9fhiJ'
    'DE4cqwM3HjBwA/OCGwZlAWz2O8ZcNaolZ3jb34Ko9ll1vXyfAsIccD07sU5c2iI3J2uDLYLP2h2xs1IZPXP8ndaCEbtSCxHqdIJa'
    'skcqvVf5yM4ZQBkm0OUYBYaFm4cxxeymF3OvD+XfEhIkh6lNtd+uSVKPpFC/GIDUHQDEbn/kMfDJUyqMeDGexS4LgqisbS02/Csh'
    'UIjbbnCAOe90MfLfecqJCQThBJJZCaZ+FRkgDZ+plB0bEJ2pkOzZ6GOnheXuBvOQ56QZAUB1ld2iFHlOPkT/LiIFPJ+jtU2US1ci'
    'QYkZDQMa5lgBYf8rX4Ebvuf78Kof+qeYHNiLxdaW7P8fU1rW/SBDK5OK2amzuPf2nwOVPaG5URBPA3cbHvIKZheYLSUDnnSUU1zs'
    '+z5cFlLaYB/mY3qR3RiqQbqecMxvjTnrcjhTt/4zHRBpOm3SDrzMSQ5FE1malfcQeQOkMsMJkTTKjwLiIiqUj8uXQ/Fd/CkuxWC7'
    'BPOWojw3AU/AkhwuvXgzGDm2JTtfYMOyXg8fAU6dBioJ1y3lQXn4jgK8cwB2zQBqrVALfGEWsE4G7BlKGC06R5QyFMJsfCry02ix'
    'XZJK/nK6Zsyk90kbuY7RM5eCQoyGE3gFeRQxTXF0tZI7fFURG4qpuzbTaMyW83Ubbwe9fj/te83NvL7vOgzzORozynSC6cGD2Pf6'
    'm3D9N30tXft3/ham1x7E0JoQfyn+DpnRtvQjmXtrqCtT3POj/xnnDz+KlfXrJV+AYmwtdcR5jPa/ImDvbyU3CXLO2pOFl4295KO7'
    'LDeh+Io6V4rnaIe/dZwMy8jR93NmXOxwyc8a7dlWlOpoymShYG6D+8aythDj1jGk+RbQWJfVeSsGaglbljJBMU2WMSlwHMc6v6/u'
    'P+p8ARE+sAGAofvyUk4OLMmrMOjhR8GnzgArFdi8QtQWxFT+z3jMu8wElC0nhuxG68bpPRFkDBAIwnjYDv1NQbJG2IHoAFCKOJN4'
    '3CuPPppEN0COSNyR2J138XaYOspG1IBPKNm9ulnOyIhzwk4nUXwg3CETFTmu+1U/8N141b/4TkJV3sgMmkwwWV31uwcA89kMVIon'
    '+xAw0miQKJBkm/DqFMd/+/fxyC/9Gqar12JuG3gURs2r6VEyi5DcWRZdcM6QwL0DtY8Yd9BssuzJPNrG1G0ulGS3zMWkp3kUbCm0'
    'KoOOJVzOwtQjmrYt3bbTAuIGIuhmLpLciNHoHbYc/TnKuO+nGcH2+OTvFonimXgkP7m8hEeEyPYfBCLbJilO3aEQUBnTNcLAjK0r'
    'AM+kCrYX2y0EevgIcPIUsFKAYWhYzCtj6zB4+nty0ztdb9nt0WCcFCN3hkSiSwOnyXcEa9IV6Rn9wnVMu5FHi6FmQ8DYWKy9h7uF'
    'YrsvsCX1tt2hRH5P2JfeR7M1i2u5h5A4tKMo7BQ3No2AUVanItHlWG6yZxfzuaYum1+gekfZ9rOgoZfJJICHhsnqFBfve4jv+mf/'
    'DqWuYQGAmhKaORwzg1RlNkjNQMZI2x189mmVwrfp19gZvTWpsp/13/zQeCUMoNslSSMVgs4F0WkHDoPx3Lx70/B66W6erO20G+LY'
    'tTjLdQCgvvne0+X8Mkkhwzo2whY8MWiaYHNwEGBVij1JwWGS0iQLsL4XWDTC7NIc2LxsJCaI8tBj4FNPABMCtQZsbQ7MdYIyeS9O'
    '3H4JuKOa+g/sejMQLTLq25nykdIRXE7MHCMlAbOo+ezPej+J3INJpiwye8YhHszDfK5dXD335o7gQhJMUJmXkMaRiZucmcOkQds0'
    'WypJkw1MMUFJYJZjPTO8ErYimQMEr3XnvZlBRQSu1ViKJz9xGqshS6ThSpnxlemUF+cv4VP/6Iexcfo8aO2AVM0x3qg4ZF0zGCWf'
    'pw1D7sRsHJo7M7mM5rYCoVGUdAZiwM3NNGfMGYNiHPFU9ucrHkEdZFlu+ANxs2eiJkEgZ3RIYU8AwMCMAcJhEHTe0bP2a9Az5ZJB'
    'PIy5FUIbMaYIZYw+P0KntUB9EECYwiaAAPiJQYDIh7pOOHgQ2FpUbJy5DGxcin3JDz8GnDoFTJQQ51fmGHiVMP8gn3jrzwG3lSz9'
    'gd1HAZpIb3MCssOVTDcmJWlz+ugM+yUllFLS8ud/w7mTmyyEeZXN6u5VTPkJJuEkzIFs2RZnG2sab352vJ2K7D+yqEeMMws0J7Yk'
    'RZLw7mGhTiIXqQkxOD88Fr2UJLIR/4UNfPw7/hXOfPpulPVrMOgBJ2yrB+uqKFV1HjdHVBOUxj+7OQaZd4Ny8uV+qCVPQ4VAAmjA'
    'Oo+DVUOk8Xf6pgznkWM32DL5982y7Sj9ID/AsNXtmP749p5PgiEaTr+e9suo3XAGDldO4yNfb5du4LLNkwpqBNbQH7YYh14EHNgH'
    'XNwANo5eEK5QCHj4UcAkPxFo69ICW/NV8OJurovvToTfDXtXGgCgVVDM26iEENldacwdIZmOm8CZikvGZPtl3P6bjf1jtOJpNqQc'
    '2tiD8mAOeeMPGJf1obe4pBRAtmAsW3TFju2TLZ15FePdKrHyXj6XijYGtUqTdeqbQmyKgUPBGBGbYRmMpjb/5tET+NN3/iBOfeyT'
    'WFk/hEXeNMVAS0HkOBUXgLrUvChJksXZJLBvLLlIVAj9m5Jk7/wgVldIVyLzjAz/9B5X4cFR5zo/ltA2NPKR1MzPJHgXiBUb3v7A'
    'heJrYCuaXwRnYHndTcRU0fwMGGNthNK0nARcu9CeSOcmj7MkYzXR8UxQEQBsATRlvPyVAJhw4gQwP3oStLoCHH4cOHMWmOgGgdnl'
    'BWazKRc8gIq34fH3nBbpf/u2TMBdVgVGbap+oU40/i+zioW0VclEiw45GEi7+jhWUn9nLm/3h8SXm8TDXnwZ+mXR9xh15+VMYa80'
    'PKRbMweDRQfcIZUZTvfi5r5CGZuiGMczwdd5pGZnFAk1c+zjDwYBcf1OKiarEz73sU/jE9/9wzjz0GFM1g5hPgyOnEb8jcWtbBER'
    'f5sdH0kjGIyap9mmNXQPOANWhp4j07VjsDJn6hAd3GFJMnfkC4ERITLhEHA1xu4CCHFdxpqsHfndMpD1q8aMVphIKyo1ADWZkxR3'
    'K7zsWkggLpMR44vXdj05HvT6k4fJc7cAQFKCzxEaAC8YL3k94SXXAqcvVJy85wTo0lng1Dng+CnQygTMTSX/lSkT3YvC345j73kM'
    'uLUCt+djJL3t1gQoTRcSVTYE2cLZshtkY0r2L4+icTHTLHOgKlFGwiDxpBobIlJwYr+A3Lcxj7TqZDTO/ttH2aV12Y3WtYf9nXFk'
    'qnFUizCEXqcIkdrQOgETCSghZYwZ2iREBEn5ckJdXQHN5/zgu38RH/3mf4ILDx3DZO0aLIZFWGcUlZtD87D5k0YEZCOyFWmO+QXq'
    'Nk5hbh+zcjDKnxN/VbgO6kVlhQenfjORcFoXYXL65Q4lBRxCJlgEaWDc22L6QVTBDHNNCB+F4ltLgqLj7caMkJl20iJiP7A/Yr2T'
    'hr4MpGK52QhGhE+GLQ5AfZWWHJ4B6y8jvPp1BW1BeOzwAvPPPQRcvgA8fgRc5LgUzDcXmG1OGfwQVvjbcOI9jwjx37kj8QO7rAdQ'
    'ga6MD7OohOFNzvqNkp3BWFAJzKKe0GTikNLpudpt2kLs7HRFuteuFEaMMEMovU0QMmkIrkrlaIQ8kR1SemtoEgkWcgxb0/oQ+Xv1'
    'DShsQoHOFBH8IosiipeD2Ap0CBW3xgA3UKmglRVJhlos8PgdH8S97/5FnLrrbtRyAFhdxzDMk3JPZB6b9Cb5y2mGAiu5Y6M6rgRn'
    'hVdXDyA4YMe4jMjn8xnNMfDUmBeC+IiFOdmRH+SHspsp0WtA6VXoRIb27ULDcShW0cdHcFzNEysws0tGomXQEiNH32zEAE/AqE7h'
    'AQPTdDi9x8MGxCANteb0EPvO+gn6B3gOTK4FXv9Wwv4p47HTFac+9Qhw7gz48RPAxkVgbR00vzRga3MKovtA5dtx7KceezriB3Z9'
    'OKjy2cBXh3F2yMm9Iz4LO3hC8pupqsuyFopQenBEgMEloDMOL1oSRVxh57RkiqGz4SQpFGHsT7gNnhEPvX8svSVwqjFzoc5hlxyD'
    'THo4abEhFK9MJChn++TsivZRCWPfubWNRw7zqQ/+MY68/zdx4hN3YcAEk9XrMFhEwbGGnLBMco0TVoz5mZRKUdTeA65Ew2AsAIAK'
    'AyDLTfD1gAjCoqsscCjI8jZH/KXH5uENf18nRTkoJI8tRGQicTgejlYs7tO0bsURgYvlCBhD9JHqc0QjFuqrKd2hZEQM5prtvib9'
    'cwmvpuGml/Ty5wngRlLSz0UI1l8KvO7NhOsPME5emOChT54B33M/6PxF8NlLwGQKml0aMN9aAfNneNL+Xqj9T038wO4PBiFBTQIG'
    'OebJV58JjZkkOYaC8CiQyXbTDSDfy86bW4xalIl3uzWl/NekYmixhRXKEJtLCHbJKl8XLTJClLP/k26xTTqAgWZplwxjc4m52ZhC'
    'nkprLIU11IUkR7VyuzwDqlzLZ3pkVA7UzGxAJeUwoG1cwdaZc7jy8GFcuOtenPnjT/MTH78bm+dOg7AKWrsGhWNnpyJq1sB9lmGQ'
    'JY5o8GDJGeHRM72OorMFZN2GhnZlU8zA0YMDSMZPa6ggnmCSxuBQdGcbiFFVAthK+Vq5tAxYmVRuMQnn5Xk9AwUp3RBxqQwHNE28'
    'dduHiEaL7zkOKioS1+9YXB5C5K8IIYgrnMCNiOSAATiq2mjMocoQr38BDr4aeP2bCAfWGE9cmOD+T1/A7KMfBy6eB06ckj4XWwue'
    'bU1B8weA9q049t7j41j/U7Vd5gGoLG1NziaOgrmmjDkwGiU/QIbXMHDZv5cee/ev4PGfuwO8GIzz8oi9OxBnZy9gsueA1gNUfwM3'
    'rTJOEr3lcP6BB8scdDXdNATTY8ZVeshfmGbhn+OybstKHJuBxYCytg+P/pcP4Oj7fwfDMKBYbol6BlnEjZs7I/4Dk1JoDYthgfnG'
    'FczOXcBi85La8StAWUNZv1Zs8nwwvOJd60SiOv3Q3QaTYb5YJLvaJDU3qMQ2ochQCTw0rNV9OPJbf4AzH/uH3NTRSBwyvUEc92BG'
    'JWB2eRNU9oBbUw0kEmB00xeZkR9KeyfTA8bZpk/cWTNLu0QB26WevVKA5O07HijMzP+z2BqwaAMzpDCopgimpbJ/CQXETQlV9lgs'
    'QO4BNs6j7EcJXCsokx3v5dpIyu1hhjpcCFhl7H0J4aWvItz4cqCCcfj0BA/fdQGzP/p/wLlTwPEz4PkCxLMFbW1NQe0+Rnsbnnjv'
    'cZH8uyN+YNdhQIJkA4Dg5blN88xopuiYFdmEdaVWXDl+Cu3wcX2il42m+pFx3EkFVleUZYbFH4seElsMX1XrSer7eoxfFoMxroeQ'
    'VMpQ8oJB+P4G+2x/GhUxwKXiwokz4CMnvVrsGJV59DvPOJ8g3wCgFPCkgtcO+U6vXF9f8Ks/qDNry/27kzZDNm79RifSlBXI3QXj'
    'yr2ioq3g8plLuHjmLHIOW+gWzQt8yIpUoKwgZ0AqwTp5ElKmtY0trwdTctwhrw+rXCabfz5HMQSC6YPkeazxZn1LA3gxMJg1vx9o'
    'FpFIQ1NW6MBTMwYDNfB0AuYapYaJhNCDxynj088p7siFgBXCZMqYrAJ7rgFe9FLCi68jrE+A85crHjkJnPyLY+BPfBo4fRI4dRaY'
    'z0E8X2A+mwLD53jSvhXH3rtrtT+3XWsAjAKq4IwYgrSkG4SzHsCucLmDxUTzdIq6OnWksBcYl5XP6s1lyzgkCVulJZC7GBLPNr++'
    'Sy/P50uPkO41YNEfTNpn4tdZkCJnolwjIHdKEpxhYToFVlddYsk4m4EpqYQGnU5YwJQgU3+FZzZgQDcugARpjP8YYoNTKDIp0/6C'
    '4vhrPM1Q2oKYPkxOY4NcbCz7FSpNE/yDUMzpS3q/O4kBDHoSYMh5MlYfuJLjh8YjmBPctV8dEBnyIeBQ/ISR3JeuWXZ0kMKHgMYN'
    'ZVJpUgoTS5SF2M6QTgKO0rhZRjCAsf8lU9z0dWtYOQ/MqMj24gmkIrABsxKokqS/VIAqINFDBhdgZcpYXwNWp4TVicSFzl+pePQY'
    'cPKxi9j8zH3AvQ8AZ84Aly7LhNrmghdbq8TDvbxavgVH3nP0CyF+YLcMgFRlKoUwKSCqsbmHCA0gYtkD5s7lLIcIKtlD9WoZY+Ut'
    'mnOj8l/VNdE9AEYh0i3AKgEUVwwZIj9ekCXJ2070kuNJv803hhPsJCSL266pT50WzMGoXpDuHgZgJw+PRgGpbhMjcJ6jSOpE4vge'
    'WWTWunAfd73r/+y5B/mWOJw0ec7ZGJaDNL2MgTYkCSCGbFNAcMsACQqyejyZZXiUSG/imGjkW6TB5rLcCiPPEAitJUWA7D7uYZWW'
    'XiS+qAggKlQwsMj1HRaqRyDJGQCwtjrB6n5guljB2mpFrZrnpu4yKgBN5KdWACtaVlPvYWhpLwYuzIDLp4ELFxrOHT2D2X0PA/c/'
    'CDp1Drw5B81nDAwDzzcKGq2Chk9ynX8HjvzMF0z8wO41AHaCqESoxIaMgXPk3vWmAWmiUPiy9tWSuicEYpJYv/AFL2rn+4mDilTQ'
    'BWf3qsovV/GNO7g2IAKb0Q0k3S1jjVCWoa0rukQ9GjBgtQjGQTeX136sRieAXGplT7tHH+wLsyUN+C43yZkvG2vYxutaJ2kJviUG'
    'vm5sYThIKjxpYfc0DGF8YwdoEDrbb07w0aGH9pGFgXknEv13PVO6OzGS/JcyqOBm3AG3k+Au+XvPuo2fSsnrRlYM1d5sOE8dBATy'
    'EwAXT1zh+//sYptsnAP27kWdTGQL9ASO8mUClBVS/7iWHC3CHJgKtwUwXNnC4ux5Kdxx5jzo7BmUk8fRNudgmgBtVnjYnGAYKrXZ'
    'Foj+E9PwYzj+Mxua4fcFET+w27MBuUkCfxkvmTUh0g4TydBQpHcgVoalAFMUBydO4+EmUz24yoJATg7ejf24mDG1Ul5ajMyUyI2p'
    'KxElU6QjXxj7YhCKuR9cwwwn1tgNkv3XcT31rUSts0/S1pmWPyYJWLYHwrLdglD6N2WY2CyUCboWoQXJnIDUQ51ltDI123Rj9rM7'
    'R23s3DsbrTU0Lr5WytO5KFsn78cPalOeZ9zOQqwhvRWLFLSD529pmHi0fqZBOczJ96IZeJ3Ui3JaPy9lpDaQTsDMWgZQG7CJCU7e'
    '/6mKM++rrW2iTfZjQRUYZjKPuiKi3yDUGsCD9m97SvSnsTzX9NzKgcFtAaIGxgxoM2DYfAKFPsgr9b/i2E99Uka3c3rvM2m73gtg'
    'Cx4IglDhgLAZ7brHmJNPNku51FPmut37jDRY82PGC53pC5S15l7COOrtJHViBPntxkIC5ylQVhCU3G7ParIzAR3ZiPiDYMy3AcQO'
    'HMdrgORIEyZJoVrsIIcCrnCUto9N+8t2PYO5WfEsLvbuWB+7K2lJ0r8mgitlZpjFk/pbfSwDYmrmpOvYk9FtN5FohHQ9HBIYsssz'
    'fac7VHLybIoZ9euuiVLuAjXREQi0g6BLCMVgXlAte2enT9atCx+uhduwKA1gtDYTyd8qoUwEQHKsXYGSNAhUULm1NgeYUOoERAzM'
    'gfkWmLEgWjQAW4XqY43ap1D5kzjx3pMyglsrcGd7tsQP7D4K0JrVkiHVswCYGm7I51o84j6wFc9QZHHO10EUgQGmUhrKJh+SS7+4'
    '3TQHUZaLP+Pf2erq2UXmxHGzQ0VbZJTZnCXWL9RuY0fqUR52D2+oHwlu9gJTxxmSBENgiQ8xsu/ThY9nqDE4a1L5HQleyJfVEDLh'
    'Aobupk/VdCm8/TapJG07+dedrKTgMFOKYxyU5hjxAULx/Iw0Zv9aYN6fXtOvr8DFtILE4swL4Nqe322Mj7v5wcKEer9Xyh7AzKgQ'
    '310bFdlrbujB8YqI2xaVeuP8yH3t6G3/eKT7Asipszu3p/t+Z754awXeyM9G5R+3XWsAMprG2KGKsuNPclYB5tTj9EBi3qmTUC8B'
    'cy4FU0nYObLpxrxd0BWu/jvCqKR2Zxt36AhKaVkdL4JhTCe7YNQVB+YqCmhaSYaK13jzqhzOtNSoIbazALNGZfdG7qDOeruqlVJc'
    'OMRu4sPRXWJWOo2GxpUK0QheOwnB0GjitgyXzltAJDUHeES4/nXoETsxIWG4ctHDfMavKRiNmjiyv4FH2sG2twZAGKI1hGunT5uK'
    'bgTTdCUB2PZ7xhyV+Faub7zzXfUeoAFvGvOBUftsGsqbuP88bvn7exi4owH0nBG+tV1mAmrMtTGkJiCURmURs6pN5tSCAtK3diYi'
    'cgzPktoXhmWJO6Iw76De0ZLbu1dDLQGDoKqnayscQnoHDPdeOLkS+3Hl3+TvgxJmYjJ+AwjUnf3XRwmCBEKagSyurYFlFtu3Zfil'
    'MWWEJS3IncOrxECjxrZFWSRgAZleIP4FtqB7TikMpYJBKHGSRXKW9vl6McbizKYDc/poaxkfHTa62jmzVFCBwoGcltDRyWP4jGYp'
    'konpMaC7NCWpTPBFtNOmL02O054hAlhAGM3AjDkaFjwMuLMMt4L59u37pp7j9hS84lm03W4HDsWwNdDQFKCqovsYzUkFl9QwmWjr'
    'za1zqDth9ayXZfnJkqhMBeiQzJxiwcaTiQCVMk5fSjQhaPXfxI7MqeS9j6WBAMNSUMhPFDaiZzCHJcmjUmku3XWkvdXA7PcToyi1'
    'NQ9xGTMj58CpxOf2/jnSYWJu+pwROwnTAKDWk0UY2HPm3MdhnI9dg/GUVgn/Rj4BIO7bgnQc2bjpmEKTQ8wlAT5rh42YIqPSUaLf'
    'Xg3TzxS4I6eqQc5+27vthGWLZDuHcTNHyjguWsN0QlhQQdM5377T/K6StqvtwEU3y7pJ3H1rhCB/pxCVXErquES9LdiiXyOkjF+I'
    'x/Il1zi62LSLDu7GxRw6RqTgSLDPA5SWIph9GN3MrF+2OIK/xQuPuF0dUl4us0qtJEUoyxj5LFtutXgGW3IOMIBhu/sbMSzHohsd'
    'I6n/ee7BFBs3dPD22GwCMKjvAOYis+As+62MxFR1P0xzdkMhKNAz08SJEQPnbvOVSG6mlmyY9IT8jqBu73geSUg/12EbzvgsAnXc'
    'TrJRS8dF+aaWVgQ1xnohvG59Pw6VijWV+rfh6m27rQk4yOGgBNQKquTbgYllKxCDSPaWN8T54Yk0eYy+RjhF02SUMbAgqdjxJe5T'
    'p1ggoyBcuGySGLH1tviPbfhJeO6WunE1Y/zJbc6BazZofU3rM2ud6ZlHvWUtXH5TMAUboJ+fl2AC0PgMjm2MzYkfYmGxQiKy1oxB'
    'AY3ARQs4mMTr3zqaCBGIC+X6QWYdy/qockzMduYAI7QJd6pTDh2OdamkuXVuA806zMSa5AL3XWRfLNC9x7Q9jbSAfa8iEdm2awYR'
    'UZEKVY0YVbUlk3GGj1XHWwvhpj17saeuAAxMUYYn0W+umrbrRCCniGRTSyPjnDm0rDjOwh7EcxP9mQ5AQRUcDyVpbAWrWM3XTPzJ'
    'vkMgEyEjVZYwwVxMtmR5LnhjjMZUD+4MO0OtEIiByCBJt7VNHqIdK9iyaQSpJ2AZjApLtuOqu8IZFj5zNQmIM3AiEctkeSOKXY2u'
    'Uam7zAjV8dXGjliL3Iio6WwIaT8rVMszBmoooNIzR3nCVEnrG6/vNJPQ/HRevhswwsyF5KBdJN0iO/W8o27JbaDxfkq3bXN8jpVL'
    'Enm2SgWv3bMPq7VihoZNMDYxXN3Uj2dwNuDQg1gVpVgs2RVgtVUEimYh+0MjzdNIXxJgOL1NrutRVT2WpHARJyQK61/IwpzuRiTs'
    'wtX8FqJwK89Pqivg8WFKV33M1mMgkiBoiKpcPosRDG8AgkB4dLhEdJsuZX9KRtbMvNKKJFVdknfU3ueAau49Eh0ovV/6iKTros60'
    'GKblK9mbKXc9gnlisuj0jiQ/jDfkNFxWE820psQtx0BKGGd7SLbfZvNywWE42uRYNIdv2I2yOUgl/y179mJPqdCQoY3xOffKf6nb'
    '7jIBwdiSwtlAHybNgjNpBUhaH6m6ZXxbSdUeopJ5BiR1g329LOBjkmeEw+gxabzuRqi2fTNpjgg5Yk/mPQwSTlRM5xydD4aT3+P4'
    'rx7z8UCz8jJmIpYRl7UgH77ppJ2aDtUq7M29luNBcA5NwedpeQ92u+2UBSHX4ANFCU3nDw5vko789Ao59LXfv6CP5uHZPE1tTzDy'
    'OhgEj940AtFoe6Jup0+uFUYX9rA9J0kL8sVw2Mj8vK4Bs1tdxh4qJHlvWgpu2bMX62WCGaQw64DGAwgT1LNAVM66GtuuNIAFeMLG'
    'XU3bdW4ZkjaBWpDMFsn9bewZYLYjy224pLpxs66Tg82YTBaa+u6Ix+vvzsllnt5QmRnd4eypjSMa/gH5ryxBrM/G0sgN/XifaRgW'
    's04atO8Q7Yg0MVLD3Hy4RN4OLHTjbkSHPbo+Yy+GueYUqgDL+0uGkRFvggz5t8o0GZ5Et03YxgMpV8Ockkh7IOQ7l/w2sOTZZGNF'
    'aTDlSV7ZtexbGA2MHUaEOplghSoInBgcMG9SBu2W9T3YRwXMDVUX78p8wafbAlzobgA4+XxlAMbZVlA2GMB8kALlZUVznHP+PwWy'
    'C2/QRU/+4aSfZrmlqjjYZCOQJX9cJXNhUyF2eQW/hxPKa8fqXbdr3o/th0dwljwHJASy5/KpqLmZGWR1AyFajFZOMWOEwGx7EoYO'
    'f4NN9FDh7XcoMVkJpayGq3uUrSSYaUfh006v8VcVfx/FQ87astahUhNOjKpOOIE7sQdc3IfR6UsyR8OJYMoJljr9ftnIGXuexjhv'
    'kbN9gnQ+gffLasIUFAa4DSilYEIVFSTVlphBhXDj2jqmVDFPfHUV4AubV+oJng2TOv2/APBNX/QcgC9ee7qagAQAk1IPt2Hg8xcv'
    '8g1bc6ztXwdNKlobYP6vUMmkRRlnw0XeTjtprTpVNsXvmYrpdM612Z/NslREi5iALoFV07V+S3gFCcgcRJCDupEwFdJcvEQeuVE8'
    'TGl63eUkTk36K/W2xOS6Zwz5/Vvq5sEsNfik1IzWOZG5kw+kk+JZF4Bpwk7gzU6V5GJifftkfY7spygQgOqWU3aYZICQvkN0P9cA'
    'yVLG3I0bdK5agvHnsYMypVrkte7wYVS0DGYqMDEGZkxXJ7x/7zqdO3UOl+cL1EKgJnGZtVLwyrV1rFHBwA1FcW5SCrZmw+Lh2cYq'
    'qP7h++aP3nUjUG6/ihnArkyAtVL+Aqh05NRpwunz2HfoINYP7gMvJIc7on6irHbUQNQhtxCyf5nsWABsT4e5AUgqKOlwI/SzXbXL'
    'Wghbwr/fxYJlicdsl1xErAoxU6VQnW1OMe7cL2l/kYIsv4vF3FVjMY9RMc1EYRK5E9pjToIAdP7ku2CF+IiICxXIDznAMslTByMj'
    'NOTvyMeQwhL6Pn2ZS397fqRtWf21bi0TvJq6iTNzUxMgtuJ02hu5cCgRtEnrOF78wL8qRc14/K3Mh1GIsMUD9l93ANfs3YNjx05j'
    'Np+jAJiDsVILbl7bgz0kx7RV81UUwsZsq/3ZxqmVw5hfPlTXf4Rwddv/wNMwgHep4/rQZO2jTHTpntNPTC48fILXV1Zxw1fcrNHu'
    'SlKH3sAr/J317Lmx9O8RPb9tu3wFJM8gf0fp31Dt4/FePUyaBALx5HPJAUJhXB2Bew+ubQhdSs6DhMZojImjORnBGkOQC2Y4OSzy'
    'oM2v4lK0JMYWPhGTmW4e6e2WN2GswHSMLJztM0kFYzbyAJRfGe12AzQ/TAw2Eph68hW4MTEztZwK6YybI1Lp6patkyQ99dFb7veU'
    '2JJ7yFbFg4d+HFp+n/1diDAB8Ja3vhr1yoDPPXoEs9LQ2oA9peKmtb2YUtEkLI3/U8Ew22r3Xzpbj/JsVkBv/5nFA392G0B3Pv2+'
    'ni/r9pQMgAC+Fajff+Uvj0xr/Y0T8yt09wOfX+DsJdzwptfg+ltejs0rM6BMSApK9I0BYQTUZ4UJkopkt3vST3o/BQGpuCCInSZ/'
    'J6RA/OkJOR0WJc+3WuaNiZiLvBculdL4R32bJNZ+RIOxzMKi/Qn5GIJ7zjmUBbB5BjraClGon0u8yTgXTGqb5c6cdE8Ceo0HSmwZ'
    'nmlWOgliohJ5wj5ZHn2OdbMekgaTgM8gDAjrKhhJjx2s6oAxLOvNVQUoQSujcwYvCKOBBIkwEZsPyZZFgE+jsVIpmC9meMNbXo03'
    'ftUb8fBDh/meUyd5UUVbe/XaHqyT1e9UR3chzLa2hgcvna/HaH55tU7f/ks4/KHbgMntV7Hqb+1pTQA9G4D2VPpxEC796cnD9cRd'
    '93PdXOB1X/+VuO5VL8PW5U1gkAqwsrfCVHj7XeULMtW6EqlaTCiwzD9PqKFChEKFClEpzuStjgIVghzUWYlKkfe6ANfcdtKtMfas'
    'qf7pmlkjuSadPWNmSPFnTJUvpPQuzIhsLIVAUjO/FBkbSpWeqO+jlCJHgFOhCRWqqsLbnCelUgFpj9B8J32t9ZOaJTMWPWqhUPGw'
    'XEnvNuZhVfuzZUMJRuwwENZWDQ5AmAx5AMQyb4Er0ahPmavB3RZRR5jH5/fra3zceR3NSFPzgKirr+H9WFkuyPuHNuDsYgMvveml'
    '+Bvf9g1YXNzCn3zmbmzwgPU6wY1re0EgqWalc6yloM2H9sDG+cmDtLnZCr3jF4ZHfleJf7FrKvsybvT0twB3APWdwPATk1f/UFss'
    'fvrl0z2zd7zlq1eu+bo3YGu14vCn78Xxz34es0ubIs0KwcNDJgn9Ta6/deqvmwX6l8tutnz2kGXiA0qapRe2FikpKqOKHpe07M/K'
    'mMxDnqR8+t5C3G2E7W4SwE4fSOq6DVylh1k+MpIIneazBLP6bNcIhBRfUWU0C2kyeTyGlqvgueUZ2jdtNPNOmnfjCb3B5mB7FCh9'
    'b29Nynuo3bGhN52qy6ONwoQxMnL61/6Kd+4UC4xv7D8b6+rqGl77+pvwDV/zZqyXVXzoD/8UH33wQRxcW8fLVlcxgUQFJiQFP1EI'
    'mA/t2MaFei8uX5hxufV9OPx73whMPvI8IX5glwwAAG4F6q+Dhh+tN/0KD+17b5ru3fq2N/+1+rKv/gqq1+7DldNncfLRozh36gzm'
    'V2bgod9U2yD/eFUxO1/Q/jFVET0SMkvRBln9hGwUUkyLXIWyF5p0TJCDbbC/O5gQxW2wWkBiTjZ1crqGEeOjCPQVeEqwl9BIdNkV'
    'QY3pBvp7lxY4FBEojIYjP94YQdPKd13F29QTMRITsbRpB7gfnZKl+hj2CmhnMsbMBq0r5GvAdnA7kWsnaT2JtFAuA81CmJzClSVp'
    'YZFGgdaCMRlN+nwp5pRDhgYlK1a6ur6GF734OrzmdTfj2r37ceGRo/jgp+7CJ44ewS1r+/DK6ToWBGzpNs8C8Q5dWSzakY2L5Sht'
    'bmwV/vu/OBz9w+cb8QPPgAEAoNsAetdtt+E//uQHfrkNw/euofAbDr1s66Wvenm98eYbyrWHDkqJ7IJQ9fz8RAa4SXoVFSmTSgTw'
    'QBi0nq8TOYXNSATPGrRAu+ilAJqUVc3I4+F6AnLBeJJXBM0VMRIXVuGE5Hhli/mMHclGwEUrOhZLOUNf4J5JSkC1piVgIU7pQZlY'
    'nbCUjwVpIVodn46BW4RGVJtA424oAAR+1rd/X9jhLN3K/IfGMZ4ClGI6PjoVxOA4NN8w6bDMecvMQCmii7eWtmw03WmT1936M3tE'
    'v/cCKWSnKbGUyG3BmWw8ZpSTcQV7TsfYNJeylIQ3Rb6fVGA2x6Wz53H/A4/gI/fch8c2N/Catb24sU4BlkzXRuLNIwA8XwwPXL6w'
    '8hBtbnGpb3v/8NiHn4/EDzwzBgBOpPYfJq/5l48PV358xu26FTD21NXFDQeuaTddc6ge3LOXBtuBB7PLjK2rTCqVrMY9tabSRf36'
    '5Afr6Xujxj6rXVgUh4aW0lDN8SO+LZUSeaLknmuo9GqtgayUTCFwKWRhTTL7HgzwoKFkdzbEoR6qKbhU5MYu7RJzIoh9zmbcM+S0'
    'JYAtjN4YpFXD5HwJmAkEgIpXt2Q7rVPpyPwguk0T4ncRfoRBTnRiI/pSUvyCtMoyu0S3k59ABUM6y9DyPQgsY6tF6FFPK+JUOKDf'
    '0WeF+SgpLLbLg8CFqIgzT/lpMAD2/A9ZscIjo4siDN1cG2jiBwHAWw3nL17C4XPncHlzjv3TVRxcXcV6kaTiKRNWiDAAuLhY4PjW'
    '5eHM4srKOSwucp185y8Pj/3v5yvxA8+QAdgztwF0O9C+a/WVN68u+N8QD29vrd0wgZwRcwVtPgPXLRViE5BvoFC5DYBpEBHFNQ2F'
    '5F5Pdm1qx9mBWFFom3zPvDu14M6qtHsteImpk1ZLH7DM8bCOCUxmH5de7Om/SS1NqUQ6RlQQqlq0DREDr4hjuJr2EHav5eHR6DvS'
    '+cf7k01O/TXKmjxqpxAHLEeWswfmKD2vFX3BZiokg4r0c3OgRKC+KFuNt7Ktt8cwig6nQTdmJWLW86NFaQDDtktRd4/PX9cyVsfP'
    'SEj9TVGwigmmWMH+MsUqCuY8YCEGCyYgrEIiS5u8GI5ja2UgPr+PV97xARz9/ecz8QNfGAMAEI5BAHj/NV958DMbp79yP+rf3DPQ'
    'Dw7Ai4nK1l6s1KYE1bh5UYsGYDCKBFwaBQsQzFJZB90GzE6iUGKxQLL1RYqso6oxDKvgC0BPGGJVRkwrNZvYanVaKMk0haIMx6RT'
    'OMVsjBTbZG2DjUukgHRKa+4WoAF+PFw+P5j9h7vFCvvDYNI7VTUu4c39CDonI0qbau6bu3/kS88tIPNBaLyehVHudPiJdKYmmhbo'
    'MAbOXs2INa+H8ut8PbroA8fGYtKLtpbmdIUKhEoBIQstNhJLrsIYhkOPGTyfo60twCdXgLf9Dxz/8+c78QPPggEAwG1AuQd9MsS7'
    '8dpb5jT/b1Omv7sCwirKvIC4odmmD04SxJ01YLL9Z1bxTzflMsw0aBI7YnnEvP3c4Wpnuof2jQEoekucHkJmjYaMk4NZQ88wYi5U'
    'sBBmRC2RR2gD8cbml+SNKtGcoXkmgVtGgoKDozBoAOuOP2ItBEr6lEhpgZnPfxxNsMgYkjZUdFNhA6jJMUtUQGnXlo4FysAAM8Zg'
    'A2br0cCTfgz+xiikjzR2UkolOT+j+d2w8eUqbh77sdSrMcNyE8IH78tAqQ41WtqgpVoGgeQQ3i00mvGwwsQojM8T+Dt/FSc+/kIg'
    'fuBZMgBrDNA7gfJGMQ0WAPDvy6v+dWvtRwrKS0uWUPCUDxBY7bZeemTpmhc2FNEwBZrfn1V96p42BVnCQjFx0QJSGW1BSpCyAGhB'
    'bivBwSpBRmZAJ6+bjqlB4gXkp+AmddWxNza/UGC03KvEtEjMMsph5cBjhEStD0ZEW7IvFZzUeiXQgLtqBh25G6zC8Bh8BbM5gnSv'
    'Em3PADryNHC30eeiGoprAOk5P27P5LU/aOzU4JmNHPncm4jCTAbI2g9gzNGOFNB/XwX9/K/i2KlbgXq1Z/jttj0nDCC322RzBAPg'
    'n8YtL97E8M0L4A1ztFcM1KbEPAwgLroYTFoBWE4fcp+3iQbT8AigFlLcSwM0cXk3ITgUdjSJfDYGVeM3HGiZbFHZ3mLHfrC66sRm'
    'BwBqWpuCmhyEbbtaSbVU80tjEKbi+cuWFyPvK4kRmCcERXsaCLRQ3aI22ajFDY0XRDyoH605XJiFsZLxU/nf8+Sb79glUFN9XTIR'
    '9QzcUBLAIGrMTQO15CdqA37aAhFY0r5l+3zKviuF9H1yP0H88cQM1tBDM0bXGNSYG1tBUllPqkytMGhB3BqjFAU9gb3YGIhJcwma'
    'ViopAyknZa/V1ipAVefPBYWLHIbeEu5cBuhIBd1zAPUj78ORM4CEu18oxP9FbXfA/X7Ltmxf9u1WwdfnXCB+ubcv6oRZ/APlswC9'
    'CeA7Ady6w313fjEHsWzL9iTtJEAvFrzc6XCfZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2ZVu2'
    'ZVu2ZVu2q6O94FIfl23bmi8z4F7AbVcHgyzbsi3b87MtNYAvr5b25i5bajvh6RJGy/a8a7thyJR+v1AY+Atprsu2bLtqS6JYtmX7'
    'K2zPhPgysS6J9tm1JeN7DtvSCfjs2jNBxK5o3TN8dtmW7YvSlkj47JpVJvtCnhu354NTK8/r2cxn6Qz9ErUlA/ira08F+6dC/DFx'
    'fKFMaLftqZjV+N27YWxPd89zxUSWbRdt8lc9gBdweyrC2E2yztXCvL9Qab4k/i9Bu1qQ6Mu1fbGl75O9E1/C9z4djjwZI+Mn+Tzu'
    'c0noy3bVti81A6XRz9XWrsYxP6/b0gR4du25ll67le5Xo9RcEv+yLdvTtKtVsi/bVdqWeQDLtmzLtmzLtmzLtmzLtmzLtmzLtmwv'
    'jPb/ASDaxbq2fXIFAAAAAElFTkSuQmCC'
)
_APPLICATION_ICON = None

# 사용자 제공 후원 QR PNG 원본. 별도 파일이나 네트워크 연결 없이 표시한다.
_DONATION_QR_PNG_BASE64 = (
    'iVBORw0KGgoAAAANSUhEUgAAAH0AAAB/CAYAAADCSM0uAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQA'
    'ABJ0Ad5mH3gAAFLwSURBVHhe7X15dFRV1u/v3porVanKPE+QMARCIBDmQRAE27FtRVREBRS1eY3Y37O/FgfQtrv99MN26FZBu1sR'
    'RJwaW2kREbBRCPOQhBASyDxVqlJDah72++Pdc9atSiIBu7+31tPfWmcR6p5hn3Pv2WefffbeRyAiwo/4QUGM/eFH/P+PH1/6DxA/'
    'vvQfIH586T9A/PjSf4D48aX/APHjS/8B4seX/gPEjy/9B4gfX/oPEMJg1LAsiyAIsY/+5ZCTM9j2+qNvMPUQUZ9n/f3G0N9QDZT3'
    'fwr99f1iGPRLJyJEIpHvHJSLQd6UQqGAKIogIoTDYf5MFEVevyAIF22XiCCK/5dhsbKsTCQSAfoZEHlb8jLyfsaWkw8ua4/lHah+'
    'QRCgUCj43wzhcLjfcpcK1ndBEHgaDAb10gHA7/dj27ZtqKmpiXp5lwOFQoHrr78e48ePh91ux8cff4xz586hoKAAixYtgtFoBKSB'
    'crvd2LlzJ44cOdJvp5RKJaZOnYq5c+dCoVDwPO3t7diyZQu6u7v7lCMi6PV63HbbbRgyZAj/+CKRCE6ePInt27cjGAz2KSMIAvLy'
    '8nDrrbciPj4eFRUV+OKLL+D3+/vkBYDCwkLceuutiIuL4zT09vbi888/x5EjR/jHc7lQKpWYP38+Jk+ezD+uQYEGid7eXrr55pvJ'
    'YDCQTqf7XslkMtGGDRsoFApRQ0MD/eQnPyG9Xk+zZ8+mzs5OikQiFIlEiIjIYrHQAw880KcOlsxmM61Zs4YCgQBFIhEKh8MUDofp'
    '5MmTVFpa2ic/S+np6bRnzx4Kh8O8j4FAgDZv3kzx8fF98ut0OtLr9TRt2jRqbm6mUChEr776KqWkpPTJx/JeffXVZLVaOV1ERJ2d'
    'nbR8+fI++S8nJScn00svvUShUIj3YTC4pE8tHA7D5/MhEokgPj4eycnJPCUlJX1nSk5Ohl6vh9/vRyAQ4HUKggCj0YikpCQYDAZY'
    'LBa0tLSgpaUFzc3N6OjogCAIvA6WDAYDgsEg/H4/3G43Ojo60NLSAo/HA0Fi136/Hz6fD4IgIDExESkpKdBoNPD5fAgGg7Db7Wht'
    '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'
    'PMmNJEwmE0pKSjB27NioOmKNBBnrrqysxLFjx9DS0sKFpdraWhw/fhwtLS3Izc3FmDFjMHToUC5Fs76o1WoMGTIEY8eOxYgRI6CV'
    'vGrZTC4tLeXqUL/fj9raWhw7dgw1NTUIhUJRrJipYeU0jx07Fvn5+X10HHJ4vV6cOXMGJ06cgNVqxciRI1FaWsr1GwOV6xexX8FA'
    '6O3tpfvuu4+KioooNzeXtFotKZVKuu666+jMmTNUX19PVquVwuFwn326IGnuFi1aRJWVlXT+/Pl+U2trK9cysS/earXSf/7nf1JB'
    'QQHl5eWRVqslQRBo3rx59O2331J9fT0vf+rUKbrxxhv5eTpLBoOB8vPzacSIEfT8889TSLKRX7hwIQ0ZMoSuueYa2rVrF9XV1VFH'
    'RwfXrpHMjKqlpYXq6uroo48+ooyMDBJFke666y6qrKyk06dP080330wKhYLUajVlZ2fTkCFD6Pbbb6eenh7ZKP5fG/+urq4ous+f'
    'P08dHR0UCASi2pbPdI1GQ7m5uVRYWEj33nsvnTx5kurr68lms3GOMlgMaqZD+pI6Oztx4cIFtLS08PNfjUaD/Px85Ofn8wOKWLCZ'
    'Hh8fj+zsbOTl5fWb0tPT+exi9UQkr9YLFy7wQx5IjoA5OTkYMmQICgoKUFBQwD1NY+F2u9HY2IjGxkbY7XaQpHfo7OxEQ0MDuru7'
    'kZqaiiFDhiA1NZU/j0gnZ6IoIiMjA/n5+cjJyYEo7aXZGUJubi7f94fDYbS0tODChQs8eBED43pJSUnIz8+P6jvbWrK2GbdjQm0o'
    'FOL19vb2Ijc3F/n5+TCbzbzewWLQ+3RBpopNTk7G5MmTkZCQgMTERGzduhWC5OLEXH/kYB2ora3F+++/H3VmLEdKSgpmzZoFncz+'
    'HDF7ZAb5EiCHfJBjIcgsd+V/MxARzp8/j4qKin6FQiJCb28vFixYgEAgwNXPRIRp06ZBqVTC4XBg//79sFgsUcIVo9Xn8+Ho0aOo'
    'r68H+umbQqHAyJEjMXbsWKhUKsyZM4erf1netLQ0fPjhh1Cr1SgrK+Mq29i6BkTs1B8Ivb299NOf/pSUUviRb775hqxWK23ZsoWS'
    'k5MpMTGRnn/++T6CnJzNqlQq7o4THx9PJpMpKl111VX9Bvln0aXkdTFzKTnsdjvddtttfdg7S3q9nh5//HEKSm5Ns2fPJlEUafLk'
    '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'
    '+QQ+nw/FxcVISkrCkCFDYDKZ+tQTS3ckEoHZbMY111wDm82GsWPHciOO48ePc5evkpIS5Obmoquri9u3jxw5EsXFxQiHwzhx4gTq'
    '6+sRFxfH+yNvo7a2FpWVlSCZPsJkMmHu3LkoKSnhH6lKpUJRUREgjWcsvQMidpEfCHJBLtZrNda5nyUANHr0aO6O058gd+HCBZo3'
    'bx4JgkCzZs2i5uZm8ng83HNT7tZUUFBAR44c4dGfQlKQ/2eeeYaUSiVBduDB9AF6vZ7f6yKKIqnVatLr9ZSVlUW7du2i3t5ecrvd'
    'UXtikoIPLF++nEeXYnbvrM3e3l5Oo91up2XLlpFer6eSkhLav38/eTwe+vTTTykxMZEUCgWtWbOGrFYrNTc305IlSwgAFRYW0smT'
    'J8kju2TAarXSY489RgqFghISEugf//gH12MwWllet9vNLy24FHxv9v59wdiUSvJolZsjhWV3sLC8Guk+E5VKhYgUzZnVwUyVSLJg'
    'ZerUkBTwj7HDgBQIUCEFNmQHMaxsSDKzYmD1sa0m86iVC2Vsvx4MBnlbarUaSuneGKXkqauRruZm/WV55P1Wq9V8LOR9ZCplVp7l'
    'YzQOFpd9nv76669jzJgx2L59OxYvXhx14sVARBg9ejQ++OADFBYW4q233sLq1asRDAbx0ksv4Z577oHH48HevXv5GXRjY2OUDj0g'
    'XaV15swZ5OXlYfv27SgpKcGpU6ewZcsWOJ1OpKamIiMjA36/H1u3bsXhw4e5RC4IAsaPH49FixYhTnbRgFarxbx585CZmcnbYoLp'
    'li1bEAgEsH//fm7wccUVVyAzMxMFBQVYunQpkpKSeF0sb11dHXzSNWG9vb3Q6/XcFamsrAxjx45FKBTCgQMHUFtbi5B0waHcyYIt'
    'c+xK8qamJvT09CAnJwfLli1DcnIyjhw5gm3btiEYDOKGG27A7Nmz+RI5KMRO/YEwEHt///33SavVctZ6qeydJBcir9dLe/bsoYyM'
    'DFKr1aTRaHhi6tX8/Hwec+Zvf/sbFRQUUHx8PK1Zs4Z8Ph91dXXR7bff3ueU7bbbbqOuri7y+/3k8/l4kusJGB2bNm3iV33J61Gp'
    'VKTRaGjatGnU3NzMy7C9djAYJJ/PR5WVlTR16lTSarV01VVXUXt7e5TFrjzv2bNnqbi4OKqvJpOJ1q5dSz6fj9rb2+nqq68mrVZL'
    '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'
)


def app_icon_pixmap(size=256):
    return application_icon().pixmap(size,size)


def draw_empty_drop_mark(painter, rect, dark=False, active=False):
    """속을 채우지 않은 굵은 [ + ]. 글꼴 없이 그려 배율마다 같은 모양을 유지한다."""
    scale=max(.1,min(1.25,(rect.width()-80)/212,(rect.height()-120)/108))
    painter.save();painter.translate(rect.center()-QPointF(106*scale,54*scale));painter.scale(scale,scale)
    path=QPainterPath()
    outlines=(
        [(0,0),(32,0),(32,12),(12,12),(12,96),(32,96),(32,108),(0,108)],
        [(180,0),(212,0),(212,108),(180,108),(180,96),(200,96),(200,12),(180,12)],
        [(99,17),(113,17),(113,47),(143,47),(143,61),(113,61),
         (113,91),(99,91),(99,61),(69,61),(69,47),(99,47)],
    )
    for points in outlines:
        path.moveTo(QPointF(*points[0]))
        for point in points[1:]:path.lineTo(QPointF(*point))
        path.closeSubpath()
    color=QColor('#ed647d' if active else ('#7f899e' if dark else '#8d96a7'))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(color,2.2,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(path);painter.restore()


def application_icon():
    """내장 ICO의 PNG 프레임을 읽어 Qt/Windows에서 같은 아이콘을 사용한다."""
    global _APPLICATION_ICON
    if _APPLICATION_ICON is None:
        import struct
        data=application_ico_bytes();icon=QIcon()
        count=struct.unpack_from('<H',data,4)[0]
        for index in range(count):
            length,offset=struct.unpack_from('<II',data,6+index*16+8)
            pixmap=QPixmap()
            if pixmap.loadFromData(data[offset:offset+length],'PNG'):icon.addPixmap(pixmap)
        if icon.isNull():raise OSError('내장 프로그램 아이콘을 읽지 못했습니다.')
        _APPLICATION_ICON=icon
    return QIcon(_APPLICATION_ICON)


def application_ico_bytes():
    return base64.b64decode(_APPLICATION_ICO_BASE64)


def set_windows_app_identity():
    if sys.platform!='win32':return
    try:
        import ctypes
        setter=ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID
        setter.argtypes=[ctypes.c_wchar_p];setter.restype=ctypes.c_long
        setter(APP_USER_MODEL_ID)
    except (AttributeError,OSError):
        pass


def install_windows_launcher():
    """사용자가 요청할 때 실행 사본과 아이콘을 고정 경로에 준비한다."""
    if sys.platform!='win32':raise OSError('Windows에서 사용할 수 있습니다.')
    folder=Path(os.environ['LOCALAPPDATA'])/'KRS'/'PDFMagnet';folder.mkdir(parents=True,exist_ok=True)
    interpreter=Path(sys.executable)
    if getattr(sys,'frozen',False):
        installed=interpreter;arguments='';command=f'"{installed}" "%1"'
    else:
        import subprocess
        installed=folder/'pdf_page_dragger.py'
        if Path(__file__).resolve()!=installed.resolve():
            temporary=folder/(uuid.uuid4().hex+'.py.tmp')
            try:
                temporary.write_bytes(Path(__file__).read_bytes());os.replace(temporary,installed)
            finally:temporary.unlink(missing_ok=True)
        gui_python=interpreter.with_name('pythonw.exe')
        if gui_python.is_file():interpreter=gui_python
        arguments=subprocess.list2cmdline([str(installed)])
        command=f'"{interpreter}" "{installed}" "%1"'
    data=application_ico_bytes()
    # 디자인이 바뀌면 경로도 바뀌어 이전 아이콘 캐시와 구분된다.
    icon_path=folder/('pdf_magnet_'+hashlib.sha256(data).hexdigest()[:12]+'.ico')
    if not icon_path.is_file() or icon_path.read_bytes()!=data:
        temporary=folder/(uuid.uuid4().hex+'.ico.tmp')
        try:temporary.write_bytes(data);os.replace(temporary,icon_path)
        finally:temporary.unlink(missing_ok=True)
    return {'folder':folder,'interpreter':interpreter,'installed':installed,
            'arguments':arguments,'command':command,'icon':icon_path}


def create_windows_shortcut(launcher):
    """현재 Windows 바탕화면에 아이콘/앱 ID가 지정된 실행 바로가기를 만든다."""
    if sys.platform!='win32':raise OSError('Windows에서 사용할 수 있습니다.')
    try:
        import pythoncom
        from win32com.shell import shell, shellcon
        from win32com.propsys import propsys, pscon
    except ImportError:
        raise RuntimeError('바로가기 모듈을 설치하세요.\nCMD: py -m pip install -U pywin32') from None
    pythoncom.CoInitialize()
    target=None;temporary=None;created=False
    try:
        desktop=Path(shell.SHGetFolderPath(0,shellcon.CSIDL_DESKTOPDIRECTORY,None,0))
        description=APP_USER_MODEL_ID+' · '+APP_NAME
        def new_link():
            return pythoncom.CoCreateInstance(shell.CLSID_ShellLink,None,pythoncom.CLSCTX_INPROC_SERVER,shell.IID_IShellLink)
        number=0
        while True:
            target=desktop/(APP_NAME+(f' ({number})' if number else '')+'.lnk')
            if target.exists():
                try:
                    existing=new_link();existing.QueryInterface(pythoncom.IID_IPersistFile).Load(str(target))
                    if existing.GetDescription()==description and existing.GetArguments()==launcher['arguments']:
                        break
                except Exception:
                    pass
                number+=1;continue
            try:
                with target.open('xb'):pass
                created=True;break
            except FileExistsError:
                number+=1
        link=new_link()
        link.SetPath(str(launcher['interpreter']));link.SetArguments(launcher['arguments'])
        link.SetWorkingDirectory(str(launcher['folder']));link.SetDescription(description)
        link.SetIconLocation(str(launcher['icon']),0)
        properties=link.QueryInterface(propsys.IID_IPropertyStore)
        properties.SetValue(pscon.PKEY_AppUserModel_ID,propsys.PROPVARIANTType(APP_USER_MODEL_ID,pythoncom.VT_LPWSTR))
        properties.Commit()
        temporary=desktop/('.pdf_magnet_'+uuid.uuid4().hex+'.lnk')
        link.QueryInterface(pythoncom.IID_IPersistFile).Save(str(temporary),0)
        os.replace(temporary,target)
        try:
            import ctypes
            ctypes.windll.shell32.SHChangeNotify(0x08000000,0,None,None)
        except (AttributeError,OSError):
            pass
        return target
    except Exception:
        if created and target is not None:
            try:target.unlink(missing_ok=True)
            except OSError:pass
        raise
    finally:
        if temporary is not None:
            try:temporary.unlink(missing_ok=True)
            except OSError:pass
        pythoncom.CoUninitialize()


def pdf_badge(count, size=96):
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor('#202637'))
    p.drawRoundedRect(QRectF(12, 9, 64, 78), 9, 9)
    p.setBrush(QColor('white'))
    p.drawRoundedRect(QRectF(7, 4, 64, 78), 8, 8)
    p.setBrush(QColor('#e52f48'))
    p.drawRoundedRect(QRectF(7, 37, 64, 27), 4, 4)
    p.setPen(QColor('white'))
    p.setFont(QFont('Arial', 13, QFont.Weight.Bold))
    p.drawText(QRectF(7, 37, 64, 27), Qt.AlignmentFlag.AlignCenter, 'PDF')
    p.setBrush(QColor('#e52f48'))
    p.setPen(QPen(QColor('white'), 2))
    p.drawEllipse(QRectF(51, 62, 42, 31))
    p.setPen(QColor('white'))
    p.setFont(QFont('Arial', 11, QFont.Weight.Bold))
    p.drawText(QRectF(51, 62, 42, 31), Qt.AlignmentFlag.AlignCenter, str(count))
    p.end()
    return pm


def corner_icon(kind):
    """폰트/비트맵 없이 그리는 [+], 디스켓과 번·한글·정 모노그램."""
    pm=QPixmap(96,96); pm.fill(Qt.GlobalColor.transparent)
    p=QPainter(pm); p.setRenderHint(QPainter.RenderHint.Antialiasing); p.scale(3,3)
    if kind == 'clear':
        p.setPen(QPen(QColor('#ff8f9e'),1.5,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
        p.setBrush(QColor('#293346'));p.drawRoundedRect(QRectF(4,4,24,24),3,3)
        p.setPen(QPen(QColor('#f4eef2'),2.2,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        p.drawLine(QPointF(10,16),QPointF(22,16));p.drawLine(QPointF(16,10),QPointF(16,22))
    elif kind == 'save':
        p.setPen(QPen(QColor('#e4e8f2'),1.7,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
        p.setBrush(QColor('#293346'))
        outline=QPainterPath(QPointF(5,4)); outline.lineTo(23,4); outline.lineTo(28,9)
        outline.lineTo(28,28); outline.lineTo(4,28); outline.lineTo(4,5); outline.closeSubpath();p.drawPath(outline)
        p.setBrush(QColor('#aab8ca'));p.drawRect(QRectF(9,4,12,9))
        p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#293346'));p.drawRect(QRectF(17,5,2,6))
        p.setBrush(QColor('#edf1f8'));p.drawRoundedRect(QRectF(9,18,14,10),1,1)
        p.setPen(QPen(QColor('#758499'),1.2));p.drawLine(QPointF(12,22),QPointF(20,22))
    else:
        translate=kind=='translate';hangul=kind=='hangul'
        gradient=QLinearGradient(3,1,29,32)
        gradient.setColorAt(0,QColor('#a4c9ff' if hangul else '#68e9ef' if translate else '#ffb09a'))
        gradient.setColorAt(.46,QColor('#5576ec' if hangul else '#437de9' if translate else '#e75371'))
        gradient.setColorAt(1,QColor('#343d98' if hangul else '#4b36a9' if translate else '#871e49'))
        outline=QPainterPath(QPointF(9,1.5));outline.lineTo(23,1.5)
        outline.quadTo(29.5,1.5,30,9);outline.lineTo(30,23)
        outline.quadTo(30,29.5,23,30);outline.lineTo(9,30)
        outline.quadTo(2,30,2,23);outline.lineTo(2,9);outline.quadTo(2,2,9,1.5)
        p.setPen(QPen(QColor('#c0d7ff' if hangul else '#b3eafa' if translate else '#ffbdce'),.75));p.setBrush(gradient);p.drawPath(outline)
        p.setBrush(Qt.BrushStyle.NoBrush);p.setPen(QPen(QColor(255,255,255,65),.6))
        p.drawRoundedRect(QRectF(4,3.5,24,24.5),6,6)
        p.setPen(QPen(QColor('#f7fbff' if translate else '#fff5ed'),1.9,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
        if hangul:
            # A compact ㅎ/아래아/ㄴ seal, drawn in the same beveled icon system.
            p.drawLine(QPointF(10,6),QPointF(14,6));p.drawLine(QPointF(7.5,9),QPointF(16.5,9))
            p.drawEllipse(QRectF(8.5,12,7,5))
            p.setBrush(QColor('#f7fbff'));p.setPen(Qt.PenStyle.NoPen);p.drawEllipse(QRectF(21,10.5,3,3))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor('#f7fbff'),1.9,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
            foot=QPainterPath(QPointF(10,21));foot.lineTo(10,25);foot.lineTo(23,25);p.drawPath(foot)
        elif translate:
            glyph=QPainterPath(QPointF(8,7));glyph.lineTo(8,17);glyph.lineTo(16,17);glyph.lineTo(16,7)
            glyph.moveTo(8,10.5);glyph.lineTo(16,10.5);glyph.moveTo(8,14);glyph.lineTo(16,14)
            p.drawPath(glyph)
            foot=QPainterPath(QPointF(9,21));foot.lineTo(9,25);foot.lineTo(23,25);p.drawPath(foot)
        else:
            p.drawLine(QPointF(7.5,8),QPointF(17,8))
            glyph=QPainterPath(QPointF(13,8));glyph.quadTo(13,13,7.5,17);p.drawPath(glyph)
            p.drawLine(QPointF(12,12),QPointF(17,17));p.drawEllipse(QRectF(10,21,12,5.5))
        if not hangul:
            p.drawLine(QPointF(22,6.5),QPointF(22,18));p.drawLine(QPointF(18.5,12),QPointF(22,12))
        p.setPen(QPen(QColor(255,255,255,170),.85))
        p.drawLine(QPointF(4,6),QPointF(4,10));p.drawLine(QPointF(4,6),QPointF(7,3))
    p.end();return QIcon(pm)


SHORTCUT_DEFINITIONS=[
    ('previous_page','이전 쪽',['Left','Backspace','PgUp','WheelUp']),
    ('next_page','다음 쪽',['Right','Space','PgDown','WheelDown']),
    ('zoom_in','크게 보기 확대',['Up']),('zoom_out','크게 보기 축소',['Down']),
    ('previous_file','이전 파일 / 폴더',[',','[']),
    ('next_file','다음 파일 / 폴더',['.',']']),
    ('clear','전체 비우기',['Ctrl+N']),('save','전체 PDF 저장',['Ctrl+S']),
    ('open','파일 추가',['Ctrl+Shift+O']),('options','옵션',['Ctrl+O']),
    ('translate','번역',['Ctrl+T']),('hangul','한글 변환',['Ctrl+H']),
    ('undo','되돌리기',['Ctrl+Z']),('redo','다시 실행',['Ctrl+Y','Ctrl+Shift+Z']),
    ('copy','페이지 / 선택 그림 복사',['Ctrl+C']),('cut','선택 그림 잘라내기',['Ctrl+X']),
    ('paste','붙여넣기',['Ctrl+V']),('select_all','전체 페이지 선택',['Ctrl+A']),
    ('delete','선택 페이지 / 개체 삭제',['Del']),
]


WHEEL_MODIFIERS=(('Ctrl',Qt.KeyboardModifier.ControlModifier),('Alt',Qt.KeyboardModifier.AltModifier),
                 ('Shift',Qt.KeyboardModifier.ShiftModifier),('Meta',Qt.KeyboardModifier.MetaModifier))


def is_wheel_shortcut(key):return isinstance(key,str) and key.split('+')[-1] in ('WheelUp','WheelDown')


def wheel_shortcut(modifiers,up):
    return ''.join(name+'+' for name,flag in WHEEL_MODIFIERS if modifiers & flag)+('WheelUp' if up else 'WheelDown')


def shortcut_label(key):
    if is_wheel_shortcut(key):return key.replace('WheelUp','휠 ↑').replace('WheelDown','휠 ↓')
    return QKeySequence(key).toString(QKeySequence.SequenceFormat.NativeText)


class ShortcutBindings(QObject):
    """창별 단축키. 문자 입력, 다른 대화창, 편집 개체 이동을 침범하지 않는다."""
    GLOBAL={'clear','save','open','options','translate','hangul'}
    def __init__(self,owner,settings):
        super().__init__(owner);self.owner=owner;self.settings=settings
        self.bindings=self.defaults()
        try:
            current=settings.value('shortcuts_v2','',type=str)
            saved=json.loads(current or settings.value('shortcuts_v1','{}',type=str))
            if isinstance(saved,dict):
                values={**self.bindings,**saved}
                if not current:
                    # 기존 키 3개는 보존하고 새 휠 기본값만 추가한다. 기존 사용자 키가
                    # ↑/↓를 사용 중이면 그 키를 새 확대/축소 기본값으로 빼앗지 않는다.
                    used={self.normalize(key) for name,keys in saved.items() if name in self.bindings for key in keys if key}
                    for name,defaults in self.bindings.items():
                        if name not in saved:values[name]=[key for key in defaults if self.normalize(key) not in used]
                        elif values[name] and not any(is_wheel_shortcut(key) for key in values[name]):
                            values[name]=list(values[name])+[key for key in defaults if is_wheel_shortcut(key) and key not in used]
                self.bindings=self.validate(values)
        except (TypeError,ValueError):self.bindings=self.defaults()
        self.reindex()

    @staticmethod
    def defaults():return {name:list(keys) for name,_label,keys in SHORTCUT_DEFINITIONS}

    @staticmethod
    def normalize(key):
        if is_wheel_shortcut(key):
            parts=key.split('+');modifiers=parts[:-1]
            if len(set(modifiers))!=len(modifiers) or any(part not in dict(WHEEL_MODIFIERS) for part in modifiers):
                raise ValueError('휠 조합에는 Ctrl·Alt·Shift·Meta만 사용할 수 있습니다.')
            return ''.join(name+'+' for name,_flag in WHEEL_MODIFIERS if name in modifiers)+parts[-1]
        return QKeySequence(key,QKeySequence.SequenceFormat.PortableText).toString(QKeySequence.SequenceFormat.PortableText)

    @classmethod
    def validate(cls,values):
        result={};seen={};labels={name:label for name,label,_ in SHORTCUT_DEFINITIONS}
        for name,_label,_keys in SHORTCUT_DEFINITIONS:
            keys=values.get(name,[])
            if not isinstance(keys,list) or len(keys)>4:raise ValueError('동작마다 키 3개와 휠 1개까지 지정하세요.')
            result[name]=[]
            for key in keys:
                if not isinstance(key,str):raise ValueError('올바른 단축키를 입력하세요.')
                if not key:continue
                if not is_wheel_shortcut(key):
                    seq=QKeySequence(key,QKeySequence.SequenceFormat.PortableText)
                    if seq.count()!=1 or seq[0].key() in (Qt.Key.Key_unknown,Qt.Key.Key_Control,Qt.Key.Key_Shift,Qt.Key.Key_Alt,Qt.Key.Key_Meta):
                        raise ValueError('Ctrl+S처럼 한 번에 누르는 키 조합만 지정하세요.')
                    if seq[0].key() in (Qt.Key.Key_Escape,Qt.Key.Key_Tab,Qt.Key.Key_Backtab,Qt.Key.Key_Return,Qt.Key.Key_Enter):
                        raise ValueError('Esc·Enter·Tab은 취소·확정·입력칸 이동을 위해 고정됩니다.')
                normalized=cls.normalize(key)
                if normalized in seen and seen[normalized]!=name:
                    raise ValueError(f'{shortcut_label(normalized)}: {labels[seen[normalized]]} / {labels[name]}에 중복 지정되었습니다.')
                seen[normalized]=name
                if normalized not in result[name]:result[name].append(normalized)
            wheel_count=sum(is_wheel_shortcut(key) for key in result[name])
            if wheel_count>1 or len(result[name])-wheel_count>3:
                raise ValueError('동작마다 키 3개와 휠 1개까지 지정하세요.')
        return result

    def reindex(self):
        self.lookup={key:name for name,keys in self.bindings.items() for key in keys}
        self.wheel_state=None;self.wheel_remainder=0.0;self.wheel_time=0.0

    def describe(self,name):
        return ' / '.join(shortcut_label(k) for k in self.bindings[name]) or '미지정'

    def apply(self,values):
        self.bindings=self.validate(values);self.reindex()
        self.settings.setValue('shortcuts_v2',json.dumps(self.bindings,ensure_ascii=False));self.settings.sync()
        self.owner.actions.set_ctrl(self.owner.actions.ctrl_down,force=True)
        editor=self.owner.preview_dialog
        if editor is not None and not editor.closed:editor.actions.set_ctrl(editor.actions.ctrl_down,force=True)
        self.owner.update_action_states()

    def matches(self,name,event):
        return self.lookup.get(QKeySequence(event.keyCombination()).toString(QKeySequence.SequenceFormat.PortableText))==name

    def context(self,widget):
        owner=self.owner;editor=owner.preview_dialog
        in_preview=editor is not None and not editor.closed and widget is not None and (widget is editor or editor.isAncestorOf(widget))
        text_input=False;current=widget
        while current is not None and current not in (owner,editor):
            if isinstance(current,(QLineEdit,QPlainTextEdit,QSpinBox,QDoubleSpinBox,QComboBox,QKeySequenceEdit)):
                text_input=True;break
            current=current.parentWidget()
        return editor,in_preview,text_input

    def key_action(self,event,widget):
        owner=self.owner
        if getattr(owner,'closing',True):return ''
        editor,in_preview,text_input=self.context(widget)
        modal=QApplication.activeModalWidget()
        if modal is not None and modal is not editor:return ''
        if QApplication.activePopupWidget() is not None:return ''
        if (in_preview and not text_input and editor.mode=='edit' and
                (editor.selected_text or editor.selected_image or editor.restore_selection or editor.restore_image) and
                event.key() in (Qt.Key.Key_Left,Qt.Key.Key_Right,Qt.Key.Key_Up,Qt.Key.Key_Down)):
            return 'move_object'
        action=self.lookup.get(QKeySequence(event.keyCombination()).toString(QKeySequence.SequenceFormat.PortableText),'')
        if text_input and (action not in self.GLOBAL or not event.modifiers() & (
                Qt.KeyboardModifier.ControlModifier|Qt.KeyboardModifier.AltModifier|Qt.KeyboardModifier.MetaModifier)):
            return ''
        return action

    def handle(self,event,widget):
        action=self.key_action(event,widget)
        if not action:return False
        event.accept()
        if event.isAutoRepeat() and action not in ('previous_page','next_page','zoom_in','zoom_out','move_object'):return True
        self.execute(action,widget,event=event)
        return True

    def handle_wheel(self,event,widget):
        if self.owner.closing:return False
        editor,in_preview,text_input=self.context(widget)
        modal=QApplication.activeModalWidget()
        if (not in_preview or text_input or QApplication.activePopupWidget() is not None or
                (modal is not None and modal is not editor)):return False
        angle=event.angleDelta().y();pixel=event.pixelDelta().y()
        delta=angle or pixel;unit=120 if angle else 40
        if not delta:
            if event.phase()==Qt.ScrollPhase.ScrollEnd:self.wheel_state=None;self.wheel_remainder=0.0
            return False
        key=wheel_shortcut(event.modifiers(),delta>0);action=self.lookup.get(key)
        if not action:self.wheel_state=None;self.wheel_remainder=0.0;return False
        event.accept();now=time.monotonic();state=(widget,key,unit)
        if self.wheel_state!=state or now-self.wheel_time>.4 or event.phase()==Qt.ScrollPhase.ScrollBegin:
            self.wheel_remainder=0.0
        self.wheel_state=state;self.wheel_time=now;self.wheel_remainder+=abs(delta)
        steps=int(self.wheel_remainder/unit);self.wheel_remainder-=steps*unit
        if steps:self.execute(action,widget,steps=min(steps,100),zoom_position=event.position().toPoint())
        return True

    def execute(self,action,widget,steps=1,event=None,zoom_position=None):
        owner=self.owner;editor,in_preview,_=self.context(widget)
        if action=='move_object':editor.handle_move_key(event)
        elif action in ('previous_file','next_file'):owner.navigate_sibling(-1 if action=='previous_file' else 1)
        elif action in ('previous_page','next_page'):
            if not owner.pages:return
            if editor is None or editor.closed:owner.open_combined_view();editor=owner.preview_dialog
            if editor is not None and not editor.closed:
                index=editor.nav_display_index if editor.nav_target_uid is not None else editor.current_index()
                editor.request_navigation(index+(-steps if action=='previous_page' else steps))
        elif action in ('zoom_in','zoom_out'):
            if not owner.pages:return
            if editor is None or editor.closed:owner.open_combined_view();editor=owner.preview_dialog
            if editor is not None and not editor.closed:
                editor.view.zoom_steps(steps if action=='zoom_in' else -steps,zoom_position)
        elif action in self.GLOBAL:
            method={'clear':'clear','save':'save_revision','open':'open_files','options':'show_settings',
                    'translate':'translate_current','hangul':'choose_hangul'}[action]
            getattr(owner,method)()
        elif action=='undo':editor.undo_edit() if in_preview else owner.undo()
        elif action=='redo':editor.redo_edit() if in_preview else owner.redo()
        elif action=='copy':editor.copy_selected_image() if in_preview else owner.copy_pages()
        elif action=='cut':
            if in_preview:editor.copy_selected_image(cut=True)
        elif action=='paste':editor.paste_clipboard() if in_preview else owner.paste_pages()
        elif action=='select_all':
            owner.canvas.selected={p.uid for p in owner.pages};owner.canvas.selectionChanged.emit();owner.canvas.viewport().update()
        elif action=='delete':
            if in_preview:
                if editor.mode=='edit' and (editor.selected_text or editor.selected_image):editor.delete_selected()
            else:owner.remove_selected()

    def eventFilter(self,watched,event):
        if event.type() not in (QEvent.Type.ShortcutOverride,QEvent.Type.KeyPress) or not isinstance(watched,QWidget):return False
        editor=self.owner.preview_dialog
        if watched.window() is not self.owner and (editor is None or watched.window() is not editor):return False
        if event.type()==QEvent.Type.ShortcutOverride:
            if self.key_action(event,watched):event.accept();return True
            return False
        return self.handle(event,watched)


class ShortcutSettings(QWidget):
    def __init__(self,owner):
        super().__init__();self.owner=owner;self.controls={};self.wheel_controls={}
        layout=QVBoxLayout(self)
        note=QLabel('키 칸에 입력하거나 휠 열에서 위/아래를 선택한 뒤 [적용]을 누르세요.\n'
                    '휠은 크게 보기에서 사용합니다. 썸네일은 목록 스크롤, 편집 개체의 방향키는 정밀 이동입니다.\n'
                    'Esc·Enter·Tab은 고정 동작이며, 다른 동작에 같은 키를 중복 지정할 수 없습니다.')
        note.setWordWrap(True);layout.addWidget(note)
        self.table=QTableWidget(len(SHORTCUT_DEFINITIONS),5);self.table.setObjectName('shortcut_table')
        self.table.setHorizontalHeaderLabels(['동작','키 1','키 2','키 3','휠']);self.table.verticalHeader().hide()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeMode.ResizeToContents)
        for column in (1,2,3):self.table.horizontalHeader().setSectionResizeMode(column,QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4,QHeaderView.ResizeMode.ResizeToContents)
        for row,(name,label,_defaults) in enumerate(SHORTCUT_DEFINITIONS):
            self.table.setItem(row,0,QTableWidgetItem(label));self.table.setRowHeight(row,34);self.controls[name]=[]
            for column in range(3):
                field=QKeySequenceEdit();field.setObjectName(f'shortcut_{name}_{column}')
                if hasattr(field,'setMaximumSequenceLength'):field.setMaximumSequenceLength(1)
                if hasattr(field,'setClearButtonEnabled'):field.setClearButtonEnabled(True)
                self.controls[name].append(field);self.table.setCellWidget(row,column+1,field)
            wheel=QComboBox();wheel.setObjectName(f'shortcut_{name}_wheel');wheel.addItem('미지정','')
            for modifiers in (Qt.KeyboardModifier.NoModifier,Qt.KeyboardModifier.ControlModifier,
                              Qt.KeyboardModifier.ShiftModifier,Qt.KeyboardModifier.AltModifier,
                              Qt.KeyboardModifier.ControlModifier|Qt.KeyboardModifier.ShiftModifier):
                for up in (True,False):
                    key=wheel_shortcut(modifiers,up);wheel.addItem(shortcut_label(key),key)
            self.wheel_controls[name]=wheel;self.table.setCellWidget(row,4,wheel)
        layout.addWidget(self.table)
        self.status=QLabel();self.status.setWordWrap(True);layout.addWidget(self.status)
        buttons=QHBoxLayout();reset=QPushButton('기본값 복원');reset.setObjectName('shortcut_reset')
        apply=QPushButton('적용');apply.setObjectName('shortcut_apply')
        buttons.addWidget(reset);buttons.addStretch();buttons.addWidget(apply);layout.addLayout(buttons)
        self.fill(owner.keys.bindings);reset.clicked.connect(self.restore_defaults);apply.clicked.connect(self.apply)

    def fill(self,values):
        for name,fields in self.controls.items():
            keys=[key for key in values[name] if not is_wheel_shortcut(key)]
            for i,field in enumerate(fields):field.setKeySequence(QKeySequence(keys[i] if i<len(keys) else ''))
            value=next((key for key in values[name] if is_wheel_shortcut(key)),'');wheel=self.wheel_controls[name]
            if wheel.findData(value)<0:wheel.addItem(shortcut_label(value),value)
            wheel.setCurrentIndex(wheel.findData(value))

    def apply(self):
        values={name:[field.keySequence().toString(QKeySequence.SequenceFormat.PortableText) for field in fields]+[self.wheel_controls[name].currentData()]
                for name,fields in self.controls.items()}
        try:self.owner.keys.apply(values)
        except ValueError as exc:
            self.status.setStyleSheet('color:#d74c66;');self.status.setText(str(exc));return False
        self.status.setStyleSheet('color:#399c77;');self.status.setText('적용했습니다. 다음 실행에도 유지됩니다.');return True

    def restore_defaults(self):self.fill(self.owner.keys.defaults());self.apply()


def normalize_github_repository(value):
    value=str(value).strip().rstrip('/')
    if not value:return ''
    value=re.sub(r'^https://github\.com/','',value,flags=re.IGNORECASE)
    if value.endswith('.git'):value=value[:-4]
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/[A-Za-z0-9_.-]+',value):
        raise ValueError('https://github.com/계정/저장소 형식으로 입력하세요.')
    if value.split('/')[1] in ('.','..'):raise ValueError('저장소 이름을 확인하세요.')
    return 'https://github.com/'+value


class CommunitySettings(QWidget):
    def __init__(self,owner):
        super().__init__();self.owner=owner
        layout=QVBoxLayout(self);layout.setSpacing(12)
        blog=QPushButton('블로그 열기');blog.setObjectName('community_blog')
        blog.clicked.connect(lambda:QDesktopServices.openUrl(QUrl(BLOG_URL)))
        layout.addWidget(blog)
        address=QLabel(BLOG_URL);address.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        address.setStyleSheet('color:#888;');layout.addWidget(address)
        layout.addSpacing(12);layout.addWidget(QLabel('GitHub 저장소'))
        self.repository=QLineEdit(owner.github_repository_url());self.repository.setObjectName('github_repository_url')
        self.repository.setPlaceholderText('https://github.com/계정/the-viewer')
        layout.addWidget(self.repository)
        save=QPushButton('주소 저장');save.setObjectName('github_url_save');save.clicked.connect(self.save)
        layout.addWidget(save)
        self.status=QLabel();self.status.setWordWrap(True);layout.addWidget(self.status)
        for label,suffix in [('코드 보기',''),('업데이트 · 수정사항','/releases'),('오류 제보 · 기능 요청','/issues')]:
            button=QPushButton(label);button.clicked.connect(lambda _checked=False,s=suffix:self.open(s));layout.addWidget(button)
        note=QLabel('새 버전 알림: GitHub 저장소의 Watch → Custom → Releases를 선택하세요.\n'
                    '저장소를 만든 뒤 위에 주소를 넣으면 하단 GitHub 버튼에서도 열 수 있습니다.')
        note.setWordWrap(True);note.setStyleSheet('color:#888;');layout.addWidget(note);layout.addStretch()

    def save(self):
        try:url=normalize_github_repository(self.repository.text())
        except ValueError as exc:
            self.status.setStyleSheet('color:#d74c66;');self.status.setText(str(exc));return False
        self.repository.setText(url);self.owner.settings.setValue('github_repository_url',url);self.owner.settings.sync()
        self.status.setStyleSheet('color:#399c77;');self.status.setText('주소를 저장했습니다.' if url else '주소를 비웠습니다.');return True

    def open(self,suffix=''):
        if not self.save():return
        url=self.owner.github_repository_url()
        if not url:self.status.setText('GitHub 저장소 주소를 먼저 입력하세요.');return
        QDesktopServices.openUrl(QUrl(url+suffix))


class CornerActions(QWidget):
    """비우기 / 저장 / 번역 / 한글 / 옵션. Ctrl을 누를 때만 단축키 이름 표시."""
    def __init__(self, parent, host, save, translate, hangul, options, clear, right_inset=0):
        super().__init__(parent)
        self.host=host;self.ctrl_down=False;self.right_inset=right_inset
        layout=QHBoxLayout(self);layout.setContentsMargins(0,0,0,0);layout.setSpacing(3)
        self.clear_button=QToolButton(self);self.save_button=QToolButton(self);self.translate_button=QToolButton(self)
        self.hangul_button=QToolButton(self);self.options_button=QToolButton(self)
        for button,kind,tip,callback in [(self.clear_button,'clear','전체 비우기 · 새 작업 · Ctrl+N',clear),
                                        (self.save_button,'save','전체 PDF 저장 · Ctrl+S',save),
                                        (self.translate_button,'translate','현재 전체 PDF 번역 · Ctrl+T',translate),
                                        (self.hangul_button,'hangul','한글 변환 · Ctrl+H',hangul),
                                        (self.options_button,'options','옵션 · Ctrl+O',options)]:
            button.setIcon(corner_icon(kind));button.setIconSize(QSize(22,22));button.setFixedSize(28,28)
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus);button.setToolTip(tip)
            button.setStyleSheet('QToolButton{background:rgba(29,34,45,220);color:#e4e8f2;border:1px solid #465064;border-radius:6px;padding:1px;font-size:11px;} QToolButton:hover{background:#4b303e;border-color:#ff667a;} QToolButton:pressed{background:#78283d;} QToolButton:disabled{border-color:#303746;}')
            button.clicked.connect(callback);layout.addWidget(button)
        self.shortcuts=[]
        QApplication.instance().installEventFilter(self)
        self.set_ctrl(False,force=True)

    def place(self):
        self.setFixedSize(sum(self.layout().itemAt(i).widget().width() for i in range(self.layout().count()))+12,28)
        self.move(max(4,self.parentWidget().width()-self.right_inset-self.width()-6),6);self.raise_()

    def set_ctrl(self, down, force=False):
        if down == self.ctrl_down and not force:return
        self.ctrl_down=down
        owner=getattr(self.host,'owner',self.host)
        for button,name,label in [(self.clear_button,'clear','비우기'),(self.save_button,'save','저장'),(self.translate_button,'translate','번역'),
                                 (self.hangul_button,'hangul','한글'),(self.options_button,'options','옵션')]:
            keys=owner.keys.bindings[name];key=(keys[0].removeprefix('Ctrl+') if keys else '—')
            text=f'{label}({key})';button.setToolTip(f'{label} · {owner.keys.describe(name)}')
            button.setText(text if down else '')
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon if down else Qt.ToolButtonStyle.ToolButtonIconOnly)
            button.setFixedWidth(max(84,button.fontMetrics().horizontalAdvance(text)+32) if down else 28)
        self.place()

    def eventFilter(self, watched, event):
        kind=event.type()
        if watched is self.host:
            if kind in (QEvent.Type.WindowDeactivate,QEvent.Type.Hide): self.set_ctrl(False)
            elif kind == QEvent.Type.WindowActivate:
                self.set_ctrl(bool(QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier))
        if kind in (QEvent.Type.KeyPress,QEvent.Type.KeyRelease,QEvent.Type.ShortcutOverride) and isinstance(watched,QWidget) and watched.window() is self.host:
            if event.key() == Qt.Key.Key_Control:
                if not event.isAutoRepeat():self.set_ctrl(kind != QEvent.Type.KeyRelease)
            else:
                self.set_ctrl(bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier))
        return False


def fit_document_window(widget, single_file, screen=None):
    """한 파일은 A4 세로 비율로, 여러 파일은 넓게. 작업표시줄 영역을 피한다."""
    screen=screen or widget.screen() or QApplication.primaryScreen()
    area=screen.availableGeometry()
    max_w=max(120,area.width()-24);max_h=max(160,area.height()-54)
    if single_file:
        height=min(1050,max_h,int(area.height()*0.9))
        width=round(height*210/297)
        if width>max_w:width=max_w;height=round(width*297/210)
    else:
        width=min(1280,max_w);height=min(850,max_h)
    center=widget.frameGeometry().center() if widget.isVisible() else area.center()
    x=max(area.left()+8,min(center.x()-width//2,area.right()-width-8))
    y=max(area.top()+8,min(center.y()-height//2,area.bottom()-height-32))
    widget.setGeometry(x,y,width,height)


def edit_icon():
    """첨부 예시처럼 열린 사각형과 연필을 벡터로 그린다."""
    pm = QPixmap(64, 64); pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm); p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(QPen(QColor('#e4e8f2'), 3.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    path = QPainterPath(QPointF(33,16)); path.lineTo(12,16); path.lineTo(12,53)
    path.lineTo(49,53); path.lineTo(49,33); p.drawPath(path)
    pencil = QPainterPath(QPointF(25,41)); pencil.lineTo(28,29); pencil.lineTo(49,8)
    pencil.quadTo(51,6,53,8); pencil.lineTo(58,13); pencil.quadTo(60,15,58,17)
    pencil.lineTo(37,38); pencil.closeSubpath(); p.drawPath(pencil)
    p.drawLine(QPointF(46,11),QPointF(55,20)); p.drawLine(QPointF(29,30),QPointF(36,37))
    p.end(); return QIcon(pm)


def clipboard_edit_payloads(session):
    """클립보드 그림을 즉시 스냅샷으로 보관. PDF 페이지 클립보드는 별도 유지."""
    clipboard=QApplication.clipboard();mime=clipboard.mimeData()
    if mime is None or mime.hasFormat(CLIPBOARD_MIME):return []
    pictures=[]
    if mime.hasImage():
        picture=clipboard.image()
        if not picture.isNull():pictures.append(picture.copy())
    if not pictures and mime.hasUrls():
        for url in mime.urls():
            if not url.isLocalFile() or url.toLocalFile().lower().endswith('.pdf'):continue
            reader=QImageReader(url.toLocalFile());reader.setAutoTransform(True)
            if reader.canRead():
                picture=reader.read()
                if not picture.isNull():pictures.append(picture)
    if pictures:
        folder=TEMP_ROOT/session/'paste';folder.mkdir(parents=True,exist_ok=True)
        result=[]
        for picture in pictures:
            path=folder/(uuid.uuid4().hex+'.png')
            if not picture.save(str(path),'PNG'):raise ValueError('클립보드 그림을 읽지 못했습니다.')
            payload={'kind':'image','filename':str(path),'width':picture.width(),'height':picture.height()}
            if mime.hasFormat(IMAGE_CLIPBOARD_MIME):
                try:
                    size=json.loads(bytes(mime.data(IMAGE_CLIPBOARD_MIME)))
                    if len(size)==2 and all(isinstance(v,(int,float)) and math.isfinite(v) and 0<v<=20000 for v in size):
                        payload['pdf_size']=size
                except (ValueError,TypeError):pass
            result.append(payload)
        return result
    if not mime.hasUrls() and mime.hasText() and mime.text().strip():
        return [{'kind':'text','text':mime.text()}]
    return []


class ColorStrip(QWidget):
    colorChanged=Signal(str)
    COLORS=['#111111','#ffffff','#777777','#e53935','#ef8c23','#f4cf35','#259b54','#2385dc','#7144bf']
    def __init__(self,color='#111111',parent=None):
        super().__init__(parent);self.color=QColor(color);self.buttons=[]
        row=QHBoxLayout(self);row.setContentsMargins(0,0,0,0);row.setSpacing(4)
        for value in self.COLORS:
            button=QToolButton();button.setFixedSize(22,22);button.setToolTip(value)
            button.clicked.connect(lambda checked=False,c=value:self.set_color(c))
            row.addWidget(button);self.buttons.append((button,value))
        more=QToolButton();more.setText('…');more.setFixedSize(24,22);more.setToolTip('다른 색상')
        more.clicked.connect(self.choose_color);row.addWidget(more);row.addStretch();self.update_colors()

    def update_colors(self):
        for button,value in self.buttons:
            border='3px solid #ff5971' if value==self.color.name() else '1px solid #969ba6'
            button.setStyleSheet(f'background:{value};border:{border};border-radius:4px;')

    def set_color(self,value):
        self.color=QColor(value);self.update_colors();self.colorChanged.emit(self.color.name())

    def choose_color(self):
        color=QColorDialog.getColor(self.color,self,'글자 색상')
        if color.isValid():self.set_color(color.name())


class PageCountLabel(QLabel):
    """Small, persistent, click-through count overlay for either viewer."""
    def __init__(self,parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('background:rgba(22,27,39,135);color:rgba(255,255,255,215);'
            'border:1px solid rgba(210,220,237,28);border-radius:7px;padding:3px 9px;font-size:11px;')
        self.hide()

    def set_count(self,total,index=None,unit='장'):
        self.setText((f'{index+1:,} / {total:,}'+(' 항목' if unit=='항목' else '')) if index is not None else f'{total:,}{unit}')
        self.setVisible(total>0);self.place()

    def place(self):
        viewport=self.parentWidget();self.adjustSize()
        self.move(max(4,(viewport.width()-self.width())//2),max(4,viewport.height()-self.height()-9))
        self.raise_()


class EndOfContainerOverlay(QWidget):
    """첫/마지막 쪽의 명시적 파일 이동. 주변 압축파일을 미리 읽지 않는다."""
    def __init__(self,editor):
        super().__init__(editor.view.viewport());self.editor=editor;self.origin=None;self.container=False
        self.setObjectName('container_end');self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet('QWidget#container_end{background:rgba(24,29,40,175);'
            'border:1px solid rgba(220,229,245,48);border-radius:10px;}'
            'QLabel{background:transparent;border:0;color:rgba(245,248,255,225);font-size:12px;}'
            'QLabel#end_keys{color:rgba(232,238,252,175);font-size:11px;}'
            'QLabel#end_name{color:rgba(240,244,253,215);font-size:11px;}'
            'QLabel:disabled{color:rgba(205,215,234,115);}'
            'QPushButton{background:rgba(245,247,255,20);border:1px solid rgba(220,228,244,42);border-radius:5px;}'
            'QPushButton:hover{background:rgba(183,49,78,175);border-color:rgba(255,141,160,205);}'
            'QPushButton:pressed{background:rgba(135,33,56,210);}'
            'QPushButton:disabled{background:rgba(245,247,255,8);border-color:rgba(220,228,244,15);}')
        layout=QVBoxLayout(self);layout.setContentsMargins(12,10,12,12);layout.setSpacing(7)
        self.heading=QLabel('마지막 페이지입니다');layout.addWidget(self.heading)
        self.buttons={};self.key_labels={};self.captions={};self.name_labels={}
        for action,title,direction in (('previous_file','‹  이전 항목',-1),('next_file','다음 항목  ›',1)):
            button=QPushButton(self);button.setObjectName('end_'+action);button.setFixedHeight(52)
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus);button.setCursor(Qt.CursorShape.PointingHandCursor)
            box=QVBoxLayout(button);box.setContentsMargins(10,5,10,5);box.setSpacing(2)
            row=QHBoxLayout();row.setSpacing(8);box.addLayout(row)
            caption=QLabel(title);keys=QLabel();keys.setObjectName('end_keys');keys.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
            keys.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Preferred)
            name=QLabel();name.setObjectName('end_name');name.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Preferred)
            for label in (caption,keys,name):label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            row.addWidget(caption);row.addWidget(keys,1);box.addWidget(name);layout.addWidget(button)
            button.clicked.connect(lambda _checked=False,direction=direction:self.editor.owner.navigate_sibling(direction))
            self.buttons[action]=button;self.key_labels[action]=keys;self.captions[action]=caption;self.name_labels[action]=name
        self.hide()

    def sync(self):
        editor=self.editor;owner=editor.owner;origin=editor.page.input_path or ''
        if origin!=self.origin:
            self.origin=origin
            self.container=bool(origin) and (Path(origin).suffix.lower() in ARCHIVE_EXTENSIONS or Path(origin).is_dir())
        index=editor.current_index()
        at_start=index==0 and editor.first_page_hint_uid==editor.page.uid
        _origin,containers,_library=owner.navigation_context()
        visible=(not editor.closed and editor.mode=='pan' and containers and self.container and bool(owner.pages) and
                 (at_start or index==len(owner.pages)-1) and not owner.clear_pending and
                 not (owner.pending_import or owner.imports or owner.import_cancelling))
        self.setVisible(visible)
        if not visible:return
        self.heading.setText('첫 페이지입니다' if at_start else '마지막 페이지입니다')
        owner.request_neighbor_names()
        for action,button in self.buttons.items():
            keys=owner.keys.describe(action);title='이전' if action=='previous_file' else '다음'
            path=owner.neighbor_paths.get('previous' if action=='previous_file' else 'next','')
            name=(Path(path).name if path else ('확인 실패' if owner.neighbor_error else '없음')) if owner.neighbor_ready else '확인 중…'
            button.setToolTip((path or owner.neighbor_error or name)+f'\n{title} 항목 · {keys}')
            button.setAccessibleName(f'{title} 항목 ({name}) · {keys}')
            self.name_labels[action].setProperty('full_name',f'({name})')
            button.setEnabled(bool(path) and owner.neighbor_ready and not owner.neighbor_error and
                              owner.navigation_request is None and not editor.busy)
        self.place()

    def place(self):
        if self.isHidden():return
        viewport=self.parentWidget();arrow=self.editor.nav_next.geometry()
        right=arrow.left()-10
        self.setFixedWidth(max(140,min(360,right-8)));self.adjustSize()
        y=arrow.center().y()-self.height()//2-24
        self.move(max(4,right-self.width()),max(8,min(y,viewport.height()-self.height()-8)))
        for action,label in self.key_labels.items():
            text=self.editor.owner.keys.describe(action)
            available=max(16,self.width()-64-self.captions[action].sizeHint().width())
            label.setText(label.fontMetrics().elidedText(text,Qt.TextElideMode.ElideMiddle,available))
            name=self.name_labels[action];full=name.property('full_name') or ''
            name.setText(name.fontMetrics().elidedText(full,Qt.TextElideMode.ElideMiddle,max(20,self.width()-46)))
        self.raise_()


class PageNavButton(QWidget):
    """Vertical displacement controls repeat speed, not an absolute page position."""
    DEAD_ZONE=7

    def __init__(self,editor,direction):
        super().__init__(editor.view.viewport());self.editor=editor;self.direction=direction
        self.setFixedSize(32,72);self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAccessibleName(('이전' if direction<0 else '다음')+' 페이지')
        self.setToolTip(('이전' if direction<0 else '다음')+' 페이지\n'
            '누른 채 위/아래: 한 장씩 연속 이동 · 약 2cm를 넘기면 가속\n'
            '그대로 유지: 계속 이동 · 시작 위치로 당기기: 정지 · 우클릭/Esc: 취소')
        self.pressed=False;self.dragged=False;self.start_y=0;self.start_index=0;self.target_index=0
        self.start_uid=None;self.hovered=False;self.displacement=0.0;self.slow_distance=76.0
        self.fraction=0.0;self.last_tick=0.0;self.filter_active=False
        self.repeat_timer=QTimer(self);self.repeat_timer.setInterval(25)
        self.repeat_timer.setTimerType(Qt.TimerType.PreciseTimer);self.repeat_timer.timeout.connect(self.repeat_step)

    def drag_threshold(self):
        # QScreen physical DPI is already in device-independent dots (Qt 6).
        # Bad/missing monitor metadata falls back to the configured logical DPI.
        screen=self.screen();dpi=screen.physicalDotsPerInchY() if screen is not None else 96.0
        if not math.isfinite(dpi) or not 40<=dpi<=400:
            dpi=screen.logicalDotsPerInchY() if screen is not None else 96.0
        return max(self.DEAD_ZONE*3,dpi*2/2.54)

    def repeat_rate(self):
        distance=abs(self.displacement)
        if distance<self.DEAD_ZONE:return 0.0
        if distance<=self.slow_distance:
            return 1.5+1.5*(distance-self.DEAD_ZONE)/max(1,self.slow_distance-self.DEAD_ZONE)
        tension=(distance-self.slow_distance)/self.slow_distance
        return min(120.0,3.0+18.0*tension**1.5)

    def fast_drag(self):
        return self.pressed and self.dragged and abs(self.displacement)>self.slow_distance

    def border_color(self):
        if self.fast_drag():
            tension=min(1.0,(abs(self.displacement)/self.slow_distance-1)/1.5)
            return QColor(255,round(185-135*tension),round(65+28*tension),
                          round(215+40*math.sin(time.monotonic()*10)))
        if self.pressed:return QColor('#ff8e9e')
        return QColor(208,221,242,205 if self.hovered or self.hasFocus() else 125)

    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing)
        color=self.border_color();fast=self.fast_drag()
        p.setPen(QPen(color,2 if fast else 1))
        p.setBrush(QColor(25,32,46,175 if self.pressed else (145 if self.hovered else 95)))
        p.drawRoundedRect(QRectF(self.rect()).adjusted(1.5,1.5,-1.5,-1.5),6,6)
        at_end=(self.editor.current_index()+self.direction not in range(len(self.editor.owner.pages)))
        p.setPen(QPen(color if self.pressed else QColor(244,247,255,115 if at_end else 230),
                      2,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
        x,y=self.width()/2,self.height()/2
        path=QPainterPath(QPointF(x-self.direction*3,y-6));path.lineTo(x+self.direction*3,y);path.lineTo(x-self.direction*3,y+6)
        p.drawPath(path)
        if self.pressed and self.dragged:
            tension=max(-1.0,min(1.0,self.displacement/(self.slow_distance*3)))
            p.setPen(QPen(color,2,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
            p.drawLine(QPointF(6,y),QPointF(6,y+tension*(y-9)))

    def enterEvent(self,event):
        self.hovered=True;self.update();super().enterEvent(event)

    def leaveEvent(self,event):
        self.hovered=False;self.update();super().leaveEvent(event)

    def mousePressEvent(self,event):
        if event.button()==Qt.MouseButton.RightButton and self.pressed:
            self.cancel();event.accept();return
        if event.button()==Qt.MouseButton.LeftButton and self.editor.owner.pages and not self.editor.closed:
            self.pressed=True;self.dragged=False;self.start_y=event.globalPosition().y()
            self.start_index=self.editor.nav_display_index if self.editor.nav_target_uid is not None else self.editor.current_index()
            self.start_index=max(0,min(len(self.editor.owner.pages)-1,self.start_index))
            self.start_uid=self.editor.owner.pages[self.start_index].uid;self.target_index=self.start_index
            self.slow_distance=self.drag_threshold();self.displacement=0.0;self.fraction=0.0
            self.editor.nav_side=self.direction;self.setFocus(Qt.FocusReason.MouseFocusReason)
            QApplication.instance().installEventFilter(self);self.filter_active=True
            self.update();event.accept()

    def mouseDoubleClickEvent(self,event):
        self.mousePressEvent(event)

    def mouseMoveEvent(self,event):
        if not self.pressed:return
        dy=event.globalPosition().y()-self.start_y
        if not self.dragged and abs(dy)<self.DEAD_ZONE:event.accept();return
        first=not self.dragged;reversed_direction=self.displacement*dy<0
        self.dragged=True;self.displacement=dy;self.editor.nav_scrubbing=True
        if first or reversed_direction or abs(dy)<self.DEAD_ZONE:self.fraction=0.0
        if first:
            QToolTip.hideText();self.last_tick=time.monotonic();self.repeat_timer.start()
        if (first or reversed_direction) and abs(dy)>=self.DEAD_ZONE:
            self.advance(1 if dy>0 else -1)
        self.update();self.editor.view.viewport().update();event.accept()

    def advance(self,steps):
        if not self.editor.owner.pages:return
        target=self.target_index+steps;index=max(0,min(len(self.editor.owner.pages)-1,target))
        if index==self.target_index:
            self.fraction=0.0
            if target<0:self.editor.request_navigation(target,scrub=True)
            return
        self.target_index=index;self.editor.request_navigation(target,scrub=True)

    def repeat_step(self):
        if not self.pressed or self.editor.closed:self.stop_drag();return
        modal=QApplication.activeModalWidget()
        if modal is not None and modal is not self.editor:self.cancel();return
        now=time.monotonic();elapsed=max(0.0,min(0.1,now-self.last_tick));self.last_tick=now
        self.fraction+=elapsed*self.repeat_rate();steps=int(self.fraction)
        if steps:
            self.fraction-=steps;self.advance(steps if self.displacement>0 else -steps)
        self.update()

    def stop_drag(self):
        self.repeat_timer.stop();self.pressed=False;self.editor.nav_scrubbing=False
        self.displacement=0.0;self.fraction=0.0
        if self.filter_active:
            QApplication.instance().removeEventFilter(self);self.filter_active=False
        self.update();self.editor.view.viewport().update()

    def mouseReleaseEvent(self,event):
        if event.button()!=Qt.MouseButton.LeftButton or not self.pressed:return
        target=self.target_index if self.dragged else self.start_index+self.direction
        self.stop_drag()
        self.editor.request_navigation(target);self.editor.nav_timer.stop();self.editor.perform_navigation()
        self.editor.refine.start();event.accept()

    def cancel(self):
        if not self.pressed:return
        index=next((i for i,page in enumerate(self.editor.owner.pages) if page.uid==self.start_uid),self.start_index)
        self.stop_drag();self.editor.view.suppress_context_until=time.monotonic()+0.5
        self.editor.nav_timer.stop();self.editor.nav_target_uid=None
        self.editor.first_page_hint_uid=None
        self.editor.request_navigation(index);self.editor.perform_navigation();self.editor.update_navigation()

    def eventFilter(self,obj,event):
        if self.pressed:
            if event.type()==QEvent.Type.KeyPress and event.key()==Qt.Key.Key_Escape:
                self.cancel();return True
            if event.type()==QEvent.Type.MouseButtonPress and event.button()==Qt.MouseButton.RightButton:
                self.cancel();return True
            if event.type()==QEvent.Type.WindowDeactivate and obj is self.window():self.cancel()
        return False

    def hideEvent(self,event):
        if self.pressed:self.stop_drag()
        super().hideEvent(event)

    def keyPressEvent(self,event):
        if self.editor.owner.handle_file_key(event):return
        if event.key() in (Qt.Key.Key_Return,Qt.Key.Key_Enter):
            self.editor.request_navigation(self.editor.current_index()+self.direction);event.accept();return
        super().keyPressEvent(event)


class TextEditDialog(QDialog):
    def __init__(self, parent, sample=None, title='글자 넣기'):
        super().__init__(parent)
        sample = sample or {}
        self.setWindowTitle(title); self.resize(460, 360)
        layout = QVBoxLayout(self)
        self.text = QPlainTextEdit(sample.get('text', ''))
        self.text.setPlaceholderText('내용 입력'); layout.addWidget(self.text)
        form = QFormLayout(); layout.addLayout(form)
        self.size = QDoubleSpinBox(); self.size.setRange(4, 144)
        self.size.setDecimals(1); self.size.setValue(sample.get('size', 11)); self.size.setSuffix(' pt')
        self.font = QComboBox()
        for label, value in [('고딕 / 한글 자동', 'sans-serif'), ('명조 / 한글 자동', 'serif'), ('고정폭', 'monospace')]:
            self.font.addItem(label, value)
        self.align = QComboBox()
        for label, value in [('왼쪽', 'left'), ('가운데', 'center'), ('오른쪽', 'right')]:
            self.align.addItem(label, value)
        self.bold = QCheckBox('굵게'); self.bold.setChecked(sample.get('bold', False))
        self.color = QColor(sample.get('color', '#111111'))
        self.palette=ColorStrip(self.color.name());self.palette.colorChanged.connect(self.set_color)
        form.addRow('크기', self.size); form.addRow('글꼴', self.font)
        form.addRow('정렬', self.align); form.addRow('색상', self.palette)
        form.addRow(self.bold)
        hint = QLabel('선택한 글꼴로 다시 쓰며, 길면 영역에 맞춰 축소됩니다.\n원래 글꼴·줄바꿈과 다를 수 있습니다.')
        hint.setStyleSheet('color:#888;font-size:11px'); layout.addWidget(hint)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject); layout.addWidget(buttons)
        self.text.setFocus()

    def set_color(self,color):
        self.color=QColor(color)

    def operation(self):
        return {'text': self.text.toPlainText(), 'size': self.size.value(), 'font': self.font.currentData(),
                'align': self.align.currentData(), 'color': self.color.name(), 'bold': self.bold.isChecked(),
                'white': False}


class TableEditDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('표 넣기'); self.resize(600, 420)
        layout = QVBoxLayout(self); row = QHBoxLayout(); layout.addLayout(row)
        self.rows = QSpinBox(); self.rows.setRange(1, 30); self.rows.setValue(3)
        self.cols = QSpinBox(); self.cols.setRange(1, 15); self.cols.setValue(3)
        self.size = QDoubleSpinBox(); self.size.setRange(4, 72); self.size.setValue(11)
        for label, widget in [('행', self.rows), ('열', self.cols), ('글자 pt', self.size)]:
            row.addWidget(QLabel(label)); row.addWidget(widget)
        self.table = QTableWidget(3, 3)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        self.rows.valueChanged.connect(self.table.setRowCount)
        self.cols.valueChanged.connect(self.table.setColumnCount)
        self.white = QCheckBox('기존 영역을 흰색으로 덮기'); self.white.setChecked(True)
        layout.addWidget(self.white)
        hint = QLabel('셀을 더블클릭해 입력 · Tab으로 다음 셀 · 빈 셀도 생성됩니다.')
        hint.setStyleSheet('color:#888'); layout.addWidget(hint)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject); layout.addWidget(buttons)

    def operation(self):
        self.table.clearFocus()  # 마지막 셀의 편집 내용을 먼저 반영
        values = [[self.table.item(r, c).text() if self.table.item(r, c) else ''
                   for c in range(self.cols.value())] for r in range(self.rows.value())]
        return {'values': values, 'size': self.size.value(), 'white': self.white.isChecked()}


class ImageGeometryDialog(QDialog):
    def __init__(self, parent, rect):
        super().__init__(parent)
        self.setWindowTitle('그림 위치 / 크기')
        self.replacement_path=None
        self.ratio = (rect[2]-rect[0]) / max(0.01,rect[3]-rect[1])
        form = QFormLayout(self)
        self.fields = []
        for label,value in zip(('X','Y','너비','높이'),(rect[0],rect[1],rect[2]-rect[0],rect[3]-rect[1])):
            spin = QDoubleSpinBox(); spin.setDecimals(2); spin.setSuffix(' mm')
            spin.setRange(0 if len(self.fields)<2 else 0.71,10000); spin.setSingleStep(0.1)
            spin.setValue(value/PT_PER_MM); spin.setKeyboardTracking(False)
            form.addRow(label,spin); self.fields.append(spin)
        self.lock = QCheckBox('가로·세로 비율 유지'); self.lock.setChecked(True)
        form.addRow(self.lock)
        self.fields[2].valueChanged.connect(lambda value:self.keep_ratio(2,value))
        self.fields[3].valueChanged.connect(lambda value:self.keep_ratio(3,value))
        self.replace_button=QPushButton('그림 교체…');self.replace_button.clicked.connect(self.pick_replacement);form.addRow(self.replace_button)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject); form.addRow(buttons)

    def pick_replacement(self):
        filename,_=QFileDialog.getOpenFileName(self,'그림 교체','','그림 (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)')
        if filename:self.replacement_path=filename;self.replace_button.setText(Path(filename).name)

    def keep_ratio(self, field, value):
        if self.lock.isChecked():
            other = self.fields[3 if field == 2 else 2]
            other.blockSignals(True); other.setValue(value/self.ratio if field == 2 else value*self.ratio); other.blockSignals(False)

    def rectangle(self):
        x,y,w,h = [spin.value()*PT_PER_MM for spin in self.fields]
        return [x,y,x+w,y+h]


class ThumbnailToggle(QToolButton):
    """좁은 버튼에서도 글꼴에 따른 말줄임 없이 두 꺾쇠/더하기를 그린다."""
    def __init__(self,owner,parent):
        super().__init__(parent);self.owner=owner

    def paintEvent(self,event):
        super().paintEvent(event)
        painter=QPainter(self);painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color='#fff' if self.underMouse() or self.isDown() else ('#c7cfdf' if self.owner.dark else '#4b5668')
        pen=QPen(QColor(color),1.25);pen.setCapStyle(Qt.PenCapStyle.RoundCap);pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        cx=self.width()/2;cy=self.height()/2
        if self.owner.thumbnails_collapsed:
            painter.drawLine(QPointF(cx-4,cy),QPointF(cx+4,cy))
            painter.drawLine(QPointF(cx,cy-4),QPointF(cx,cy+4))
        else:
            for offset in (-2,2.5):
                path=QPainterPath(QPointF(cx+offset+2,cy-3.5))
                path.lineTo(cx+offset-1.5,cy);path.lineTo(cx+offset+2,cy+3.5)
                painter.drawPath(path)


class ThumbnailRail(QWidget):
    """내용·스크롤바 바깥의 18px 테두리. 접힌 상태에서도 같은 자리에 남는다."""
    def __init__(self,owner,parent):
        super().__init__(parent);self.owner=owner
        self.setFixedWidth(18)
        layout=QVBoxLayout(self);layout.setContentsMargins(1,0,0,0);layout.setSpacing(0)
        self.button=ThumbnailToggle(owner,self);self.button.setFixedSize(17,48)
        self.button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(owner.toggle_thumbnail_panel)
        layout.addStretch();layout.addWidget(self.button);layout.addStretch()
        self.sync()

    def sync(self):
        collapsed=self.owner.thumbnails_collapsed
        tip='썸네일 펼치기' if collapsed else '썸네일 접기'
        self.button.setToolTip(tip);self.button.setAccessibleName(tip)
        dark=self.owner.dark
        background='#252b38' if dark else '#e4e8ee'
        border='#454e60' if dark else '#b6bfcc'
        self.button.setStyleSheet(
            f'QToolButton{{background:{background};border:1px solid {border};'
            'border-right:0;border-radius:3px;padding:0;}'
            'QToolButton:hover{color:#fff;background:#653647;border-color:#f06a80;}'
            'QToolButton:pressed{background:#8b3048;border-color:#ff8295;}')
        self.update()

    def paintEvent(self,event):
        painter=QPainter(self)
        painter.fillRect(self.rect(),QColor('#1d222d' if self.owner.dark else '#edf0f5'))
        painter.setPen(QColor('#363d4f' if self.owner.dark else '#cbd1db'))
        painter.drawLine(0,0,0,self.height())


class EmptyPreview(QWidget):
    """항상 남아 있는 크게 보기 자리. 첫 입력은 새 문서로 연다."""
    def __init__(self,owner):
        super().__init__(owner);self.owner=owner;self.drop_hover=False
        self.setMinimumSize(200,240);self.setAcceptDrops(True);self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setToolTip('PDF·그림·폴더·ZIP/CBZ를 놓거나 더블클릭하여 새로 열기')

    def paintEvent(self,event):
        painter=QPainter(self);painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(),QColor('#181b24' if self.owner.dark else '#edf0f5'))
        draw_empty_drop_mark(painter,QRectF(self.rect()),self.owner.dark,self.drop_hover);painter.end()

    def dragEnterEvent(self,event):
        if self.owner.accepts_open_drop(event):
            self.drop_hover=True;self.update();event.setDropAction(Qt.DropAction.CopyAction);event.accept()
        else:event.ignore()

    def dragMoveEvent(self,event):
        self.dragEnterEvent(event)

    def dragLeaveEvent(self,event):
        self.drop_hover=False;self.update();event.accept()

    def dropEvent(self,event):
        self.drop_hover=False;self.update();self.owner.dropEvent(event)

    def mouseDoubleClickEvent(self,event):
        if event.button()==Qt.MouseButton.LeftButton:self.owner.open_new_files();event.accept()
        else:super().mouseDoubleClickEvent(event)


class ZoomView(QGraphicsView):
    zoomChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.item = None
        self.pdf_size = None
        self.auto_fit = True
        self.fit_scale = 1.0
        self.editor = None
        self.gesture_start = None
        self.gesture_end = None
        self.hover = None
        self.suppress_context_until = 0
        self.image_handle = None
        self.background_pan = False
        self.open_drop_hover = False
        self.fit_timer=QTimer(self);self.fit_timer.setSingleShot(True);self.fit_timer.setInterval(0)
        self.fit_timer.timeout.connect(self.fit_if_needed)
        self.controls_timer=QTimer(self);self.controls_timer.setSingleShot(True);self.controls_timer.setInterval(0)
        self.controls_timer.timeout.connect(lambda:self.editor.position_controls() if self.editor is not None and not self.editor.closed else None)
        self.setBackgroundBrush(QColor('#181b24'))
        self.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setMouseTracking(True)
        self.setAcceptDrops(True);self.viewport().setAcceptDrops(True)

    def dragEnterEvent(self,event):
        owner=self.editor.owner if self.editor is not None else None
        if owner is not None and owner.accepts_open_drop(event):
            self.open_drop_hover=True;self.viewport().update()
            event.setDropAction(Qt.DropAction.CopyAction);event.accept()
        else:event.ignore()

    def dragMoveEvent(self,event):
        if event.buttons() & Qt.MouseButton.RightButton:
            self.open_drop_hover=False;self.viewport().update();event.ignore()
        else:self.dragEnterEvent(event)

    def dragLeaveEvent(self,event):
        self.open_drop_hover=False;self.viewport().update();event.accept()

    def dropEvent(self,event):
        self.open_drop_hover=False;self.viewport().update()
        if self.editor is not None and not event.buttons() & Qt.MouseButton.RightButton:
            self.editor.owner.dropEvent(event)
        else:event.ignore()

    def paintEvent(self,event):
        super().paintEvent(event)
        if self.open_drop_hover:
            painter=QPainter(self.viewport());painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor('#ef5974'),3));painter.setBrush(QColor(239,89,116,14))
            painter.drawRoundedRect(QRectF(self.viewport().rect()).adjusted(5,5,-5,-5),10,10)
            label=QRectF(self.viewport().width()/2-48,16,96,30)
            painter.setPen(Qt.PenStyle.NoPen);painter.setBrush(QColor(35,39,50,230));painter.drawRoundedRect(label,8,8)
            painter.setPen(QColor('#fff'));painter.drawText(label,Qt.AlignmentFlag.AlignCenter,'새로 열기');painter.end()

    def set_image(self, pix):
        if pix.isNull():
            return
        first = self.item is None
        if first:
            self.item = self.scene().addPixmap(pix)
            self.page_rect = QRectF(0, 0, 600, 600*pix.height()/pix.width())
            self.scene().setSceneRect(self.page_rect.adjusted(-18, -18, 18, 18))
        else:
            self.item.setPixmap(pix)
        self.item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.item.setTransform(QTransform.fromScale(self.page_rect.width()/pix.width(), self.page_rect.height()/pix.height()))
        if first:
            self.fit_page()

    def set_page_geometry(self, width, height):
        self.pdf_size = (width, height)
        if self.item is None:
            return
        self.page_rect = QRectF(0, 0, 600, 600*height/width)
        self.scene().setSceneRect(self.page_rect.adjusted(-18,-18,18,18))
        pix = self.item.pixmap()
        self.item.setTransform(QTransform.fromScale(600/pix.width(), self.page_rect.height()/pix.height()))
        if self.auto_fit:
            self.fit_page()

    def fit_page(self):
        if self.item is not None:
            self.auto_fit = True
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.fit_scale = self.transform().m11()
            self.zoomChanged.emit()

    def fit_if_needed(self):
        # 이전 resize에서 예약한 자동 맞춤이 방금 수행한 확대를 되돌리지 않는다.
        if self.auto_fit and self.item is not None:self.fit_page()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # fitInView가 스크롤바/viewport를 재배치한 뒤 실제 크기로 오버레이를 맞춘다.
        if self.editor is not None:self.controls_timer.start()
        if self.auto_fit and self.item is not None:
            self.fit_timer.start()

    def wheelEvent(self, event):
        if self.editor is not None and self.editor.owner.keys.handle_wheel(event,self):return
        super().wheelEvent(event)

    def zoom_steps(self,steps,position=None):
        if self.item is None or not steps:return
        self.auto_fit = False
        self.fit_timer.stop()
        position=self.viewport().rect().center() if position is None else position
        before = self.mapToScene(position)
        old = self.transform().m11()
        new = max(self.fit_scale*0.25, min(self.fit_scale*12, old*(1.18**max(-100,min(100,steps)))))
        self.scale(new/old, new/old)
        after = self.mapToScene(position)
        self.translate(after.x()-before.x(), after.y()-before.y())
        self.zoomChanged.emit()

    def mouseDoubleClickEvent(self, event):
        if event.button()!=Qt.MouseButton.LeftButton:
            event.accept();return
        editor=self.editor
        if editor is not None and editor.page.is_document_card:
            page=editor.page;self.clear_gesture();event.accept()
            editor.owner.open_document_card(page);return
        if editor is not None and editor.mode=='edit' and editor.ready():
            self.clear_gesture()
            hit=self.hit_element(self.pdf_point(event.position().toPoint()))
            if hit is not None:
                if 'id' in hit:editor.select_image(hit);editor.image_geometry()
                else:
                    editor.select_text(hit)
                    editor.edit_gesture([0,0],[0,0],hit,override='replace')
            event.accept();return
        if editor is not None and editor.mode!='pan':event.accept();return
        self.fit_page();event.accept()

    def pdf_point(self, position, clamp=False):
        if self.item is None or self.editor is None or not self.editor.info:return None
        point=self.mapToScene(position)
        if clamp:point=QPointF(max(0,min(self.page_rect.width(),point.x())),max(0,min(self.page_rect.height(),point.y())))
        elif not self.page_rect.contains(point):return None
        return [point.x()/self.page_rect.width()*self.editor.info['width'],point.y()/self.page_rect.height()*self.editor.info['height']]

    def scene_box(self, box):
        width,height=(self.editor.info['width'],self.editor.info['height']) if self.editor.info else self.pdf_size
        sx=self.page_rect.width()/width;sy=self.page_rect.height()/height
        return QRectF(box[0]*sx,box[1]*sy,(box[2]-box[0])*sx,(box[3]-box[1])*sy)

    def hit_element(self, point):
        if point is None or not self.editor.info:return None
        # 글자를 우선 잡아 스캔 배경/사진 위 텍스트도 같은 모드에서 선택한다.
        for key in ('spans','images'):
            hits=[e for e in reversed(self.editor.info.get(key,[])) if e['rect'][0]<=point[0]<=e['rect'][2] and e['rect'][1]<=point[1]<=e['rect'][3]]
            if hits:return min(hits,key=lambda e:(e['rect'][2]-e['rect'][0])*(e['rect'][3]-e['rect'][1]))
        return None

    def clear_gesture(self):
        self.gesture_start=self.gesture_end=self.hover=None;self.image_handle=None;self.viewport().update()

    def image_corners(self):
        if not self.editor.selected_image or not self.editor.image_target:return []
        x0,y0,x1,y1=self.editor.image_target
        return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]

    def image_handle_at(self, point):
        if point is None:return None
        radius=9*self.editor.info['width']/self.page_rect.width()/self.transform().m11()
        return next((i for i,p in enumerate(self.image_corners()) if math.dist(p,point)<radius),None)

    def mousePressEvent(self,event):
        editor=self.editor
        if editor is not None and event.button()==Qt.MouseButton.RightButton:
            dragging=self.gesture_start is not None;self.clear_gesture()
            if dragging:editor.cancel_move();self.suppress_context_until=time.monotonic()+0.6
            event.accept();return
        if editor is None or editor.mode=='pan':super().mousePressEvent(event);return
        if event.button()==Qt.MouseButton.LeftButton:
            if editor.ready():
                self.gesture_start=self.pdf_point(event.position().toPoint());self.gesture_end=self.gesture_start
                self.hover=self.hit_element(self.gesture_start)
                if editor.mode=='edit':
                    self.image_handle=self.image_handle_at(self.gesture_start)
                    if self.image_handle is None:
                        if self.hover is not None and 'id' in self.hover:editor.select_image(self.hover)
                        else:editor.select_text(self.hover)
                    editor.image_drag_base=list(editor.image_target) if editor.image_target else None
                    if self.hover is None and self.image_handle is None and not editor.busy:
                        self.clear_gesture();self.background_pan=True
                        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag);super().mousePressEvent(event);return
            event.accept();return
        super().mousePressEvent(event)

    def drag_selected(self,point,modifiers):
        editor=self.editor
        if editor.selected_image:editor.drag_image(self.gesture_start,point,self.image_handle,modifiers)
        elif editor.selected_text:
            dx,dy=point[0]-self.gesture_start[0],point[1]-self.gesture_start[1]
            if modifiers & Qt.KeyboardModifier.ShiftModifier:
                if abs(dx)>=abs(dy):dy=0
                else:dx=0
            editor.set_move_offset(dx,dy)

    def mouseMoveEvent(self,event):
        editor=self.editor
        if editor is None or editor.mode=='pan' or self.background_pan:super().mouseMoveEvent(event);return
        point=self.pdf_point(event.position().toPoint(),clamp=self.gesture_start is not None)
        if self.gesture_start is not None and point is not None:
            self.gesture_end=point
            if editor.mode=='edit':self.drag_selected(point,event.modifiers())
        elif editor.ready():
            self.hover=self.hit_element(point) if editor.mode=='edit' else None
            if editor.mode=='edit':
                handle=self.image_handle_at(point)
                cursor=(Qt.CursorShape.SizeFDiagCursor if handle in (0,2) else Qt.CursorShape.SizeBDiagCursor) if handle is not None else (Qt.CursorShape.SizeAllCursor if self.hover else Qt.CursorShape.OpenHandCursor)
                self.viewport().setCursor(cursor)
        self.viewport().update();event.accept()

    def mouseReleaseEvent(self,event):
        editor=self.editor
        if editor is not None and event.button()==Qt.MouseButton.RightButton:event.accept();return
        if editor is None or editor.mode=='pan' or self.background_pan:
            super().mouseReleaseEvent(event)
            if self.background_pan:
                self.background_pan=False
                if editor.mode!='pan':self.setDragMode(QGraphicsView.DragMode.NoDrag)
            return
        if event.button()==Qt.MouseButton.LeftButton:
            start,hit=self.gesture_start,self.hover
            point=self.pdf_point(event.position().toPoint(),clamp=start is not None)
            if editor.mode=='edit' and start is not None and point is not None:self.drag_selected(point,event.modifiers())
            self.clear_gesture()
            if editor.mode=='edit':
                if point is not None:editor.commit_move()
                else:editor.cancel_move()
                event.accept();return
            if start is not None and point is not None and editor.ready():editor.edit_gesture(start,point,hit)
            event.accept();return
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self,event):
        if self.editor is None:super().contextMenuEvent(event);return
        if time.monotonic()<self.suppress_context_until:event.accept();return
        self.clear_gesture();self.editor.show_tools(event.globalPos());event.accept()

    def draw_navigation(self,painter):
        editor=self.editor
        if not editor.nav_scrubbing:return
        painter.save();painter.resetTransform()
        x=12 if editor.nav_side<0 else self.viewport().width()-12
        top,bottom=28,self.viewport().height()-28
        painter.setPen(QPen(QColor(180,194,215,120),3));painter.drawLine(QPointF(x,top),QPointF(x,bottom))
        index=editor.nav_display_index;fraction=index/max(1,len(editor.owner.pages)-1)
        painter.setPen(Qt.PenStyle.NoPen);painter.setBrush(QColor('#ff4059'))
        painter.drawEllipse(QPointF(x,top+(bottom-top)*fraction),5,5);painter.restore()

    def drawForeground(self,painter,rect):
        super().drawForeground(painter,rect);editor=self.editor
        if self.item is None or editor is None:return
        painter.save();pen=QPen(page_border_brush(editor.page,self.page_rect),2);pen.setCosmetic(True)
        painter.setPen(pen);painter.setBrush(Qt.BrushStyle.NoBrush);painter.drawRect(self.page_rect);painter.restore()
        if self.page_rect.width()>self.page_rect.height():
            painter.save();pen=QPen(QColor('#6bafc8'),1,Qt.PenStyle.DashLine);pen.setCosmetic(True)
            painter.setPen(pen);painter.setBrush(Qt.BrushStyle.NoBrush);painter.drawRect(self.page_rect.adjusted(-6,-6,6,6))
            painter.setPen(QColor('#6bafc8'));font=QFont();font.setPixelSize(max(5,round(10/self.transform().m11())));painter.setFont(font)
            painter.drawText(QPointF(0,-10),'↔ 가로');painter.restore()
        if editor.pending_cover is not None and self.pdf_size is not None:painter.fillRect(self.scene_box(editor.pending_cover),QColor('white'))
        if not editor.info or editor.mode=='pan':self.draw_navigation(painter);return
        painter.save();pen=QPen(QColor(255,66,92,60),1);pen.setCosmetic(True);painter.setPen(pen);painter.setBrush(Qt.BrushStyle.NoBrush)
        if editor.mode=='edit':
            for element in editor.info.get('spans',[])+editor.info.get('images',[]):
                box=self.scene_box(element['rect'])
                if box.intersects(rect):painter.drawRect(box)
            if self.hover is not None:
                pen.setColor(QColor(255,100,120,130));pen.setStyle(Qt.PenStyle.DotLine);painter.setPen(pen);painter.drawRect(self.scene_box(self.hover['rect']))
            selected=editor.selected_image or editor.selected_text
            if selected:
                source=self.scene_box(selected['rect']);destination=self.scene_box(editor.image_target if editor.selected_image else editor.moved_rect())
                if editor.has_pending_move():
                    pix=self.item.pixmap();sx=pix.width()/self.page_rect.width();sy=pix.height()/self.page_rect.height()
                    crop=QRectF(source.x()*sx,source.y()*sy,source.width()*sx,source.height()*sy)
                    painter.setOpacity(0.75);painter.drawPixmap(destination,pix,crop);painter.setOpacity(1)
                pen.setColor(QColor('#ec173b'));pen.setWidth(3);pen.setStyle(Qt.PenStyle.SolidLine);painter.setPen(pen)
                painter.setBrush(QColor(255,35,65,18));painter.drawRect(destination)
                if editor.selected_image:
                    radius=4/self.transform().m11();painter.setBrush(QColor('white'))
                    for x,y in self.image_corners():
                        point=self.scene_box([x,y,x,y]).topLeft();painter.drawRect(QRectF(point.x()-radius,point.y()-radius,radius*2,radius*2))
        if self.gesture_start is not None and self.gesture_end is not None and editor.mode in ('cover','text'):
            a,b=self.gesture_start,self.gesture_end
            pen.setColor(QColor('#ff4059'));pen.setWidth(2);pen.setStyle(Qt.PenStyle.DashLine);painter.setPen(pen)
            painter.setBrush(QColor('white') if editor.mode=='cover' else QColor(255,64,89,24))
            painter.drawRect(self.scene_box([min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1])]))
        painter.restore();self.draw_navigation(painter)

    def keyPressEvent(self,event):
        if self.editor is not None and self.editor.owner.handle_file_key(event):return
        if self.editor is not None and self.editor.handle_move_key(event):return
        super().keyPressEvent(event)


class PreviewDialog(QDialog):
    TOOLS = [('edit','글/그림 편집',''),('text','문자추가',''),('cover','흰색 덮기','')]

    def __init__(self, owner, page, embedded=False):
        super().__init__(owner)
        self.embedded=embedded
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.resize(1050, 880)
        if owner.single_file_layout:
            fit_document_window(self,True,owner.screen())
        self.owner = owner
        self.page = page
        self.token = 0
        self.info_token = 0
        self.edit_token = 0
        self.requested_side = 0
        self.preview_ready = False
        self.closed = False
        self.mode = 'pan'
        self.info = None
        self.loading_info = False
        self.busy = False
        self.edit_source = None
        self.pending_cover = None
        self.pending_cover_path = None
        self.selected_text = None
        self.selected_image = None
        self.image_target = None
        self.image_drag_base = None
        self.restore_image = None
        self.after_image = None
        self.image_filename = None
        self.image_preview = QPixmap()
        self.move_offset = [0.0, 0.0]
        self.queued_nudge = [0.0, 0.0]
        self.restore_selection = None
        self.after_move = None
        self.paste_queue=[];self.paste_serial=0
        self.nav_target_uid=None;self.nav_scrubbing=False;self.nav_side=1;self.nav_display_index=0
        self.first_page_hint_uid=None
        self.nav_timer=QTimer(self);self.nav_timer.setSingleShot(True);self.nav_timer.setInterval(65)
        self.nav_timer.timeout.connect(self.perform_navigation)
        self.move_timer = QTimer(self); self.move_timer.setSingleShot(True); self.move_timer.setInterval(300)
        self.move_timer.timeout.connect(self.commit_move)
        self.view = ZoomView(self)
        self.view.editor = self
        self.view.setBackgroundBrush(QColor('#181b24' if owner.dark else '#edf0f5'))
        self.view.setToolTip('파일 드롭: 새로 열기 · 우클릭: 글/그림 편집 · 키/휠 설정: 정 → 단축키')
        layout = QVBoxLayout(self); layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
        self.backend = PdfBackend(self,lazy=True)
        self.backend.preview.connect(self.got_image)
        self.backend.editInfo.connect(self.got_info)
        self.backend.edited.connect(self.got_edit)
        self.image_backend=owner.preview_image_backend;self.image_backend.preview.connect(self.got_image)
        self.guide = QLabel(self.view.viewport())
        self.guide.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.guide.setStyleSheet('background:rgba(25,28,38,225);color:#fff;border-radius:8px;padding:8px 12px;')
        self.guide.hide()
        self.move_panel = QWidget(self.view.viewport())
        self.move_panel.setStyleSheet('QWidget{background:#343b4b;color:#e4e8f2;border-radius:5px;} QDoubleSpinBox{padding:4px;background:#202530;}')
        move_layout = QHBoxLayout(self.move_panel); move_layout.setContentsMargins(8, 6, 8, 6)
        self.move_x = QDoubleSpinBox(); self.move_y = QDoubleSpinBox()
        for label, spin in [('X', self.move_x), ('Y', self.move_y)]:
            spin.setDecimals(2); spin.setRange(0, 10000); spin.setSuffix(' mm'); spin.setSingleStep(0.1)
            spin.setKeyboardTracking(False); spin.setFixedWidth(125)
            spin.valueChanged.connect(self.coordinate_changed); spin.editingFinished.connect(self.commit_move)
            move_layout.addWidget(QLabel(label)); move_layout.addWidget(spin)
        self.move_panel.setToolTip('페이지 왼쪽 위 기준 글자 박스 좌표 · 0.01mm 입력 가능')
        self.move_panel.hide()
        self.actions=CornerActions(self.view.viewport(),self,self.save_copy,owner.translate_current,owner.choose_hangul,lambda:owner.show_settings(self),owner.clear)
        self.actions.save_button.setToolTip(owner.save_button.toolTip())
        if embedded:
            self.setWindowFlags(Qt.WindowType.Widget)
            self.setMinimumSize(200,240)
            self.actions.hide()
            for shortcut in self.actions.shortcuts:shortcut.setEnabled(False)
        self.nav_previous=PageNavButton(self,-1);self.nav_next=PageNavButton(self,1)
        self.nav_label=PageCountLabel(self.view.viewport())
        self.end_overlay=EndOfContainerOverlay(self)
        self.shortcuts = []
        self.refine = QTimer(self); self.refine.setSingleShot(True)
        self.refine.setInterval(180); self.refine.timeout.connect(self.request_image)
        self.view.zoomChanged.connect(self.changed_zoom)
        pix = owner.thumbs.get((page.path, page.number))
        if pix is not None:
            self.view.set_image(pix)
        self.changed_zoom()
        self.update_navigation()
        QTimer.singleShot(0, self.request_image)

    def position_controls(self):
        if hasattr(self, 'guide'):
            self.guide.setWordWrap(True)
            self.guide.setMaximumWidth(max(160,self.view.viewport().width()-24))
            self.guide.adjustSize()
            self.guide.move(max(8, (self.view.viewport().width()-self.guide.width())//2), 42)
            self.guide.raise_()
            if hasattr(self, 'move_panel'):
                self.move_panel.adjustSize()
                self.move_panel.move(max(8,self.view.viewport().width()-self.move_panel.width()-14), max(62,self.guide.geometry().bottom()+8))
                self.move_panel.raise_()
        if hasattr(self,'actions'):self.actions.place()
        if hasattr(self,'nav_label'):
            viewport=self.view.viewport()
            self.nav_previous.move(8,max(4,(viewport.height()-self.nav_previous.height())//2))
            self.nav_next.move(max(8,viewport.width()-self.nav_next.width()-8),max(4,(viewport.height()-self.nav_next.height())//2))
            self.nav_previous.raise_();self.nav_next.raise_()
            self.nav_label.place()
        if hasattr(self,'end_overlay'):self.end_overlay.place()

    def resizeEvent(self, event):
        super().resizeEvent(event); self.position_controls()

    def showEvent(self,event):
        super().showEvent(event);self.position_controls()
        QTimer.singleShot(0,self.position_controls)

    def message(self, text):
        self.guide.setText(text); self.guide.setVisible(bool(text)); self.position_controls()

    def ready(self):
        return not self.page.is_document_card and self.info is not None and not self.busy and not self.loading_info

    def document_card_notice(self):
        self.message('PDF 카드를 더블클릭해 전체 문서를 연 뒤 편집하세요.')

    def show_tools(self,global_pos=None):
        menu=QMenu(self)
        if self.page.is_document_card:
            page=self.page
            action=menu.addAction(f'PDF 전체 열기 · {page.document_pages:,}쪽')
            chosen=menu.exec(global_pos if global_pos is not None else QCursor.pos());menu.deleteLater()
            if chosen is action:self.owner.open_document_card(page)
            return
        for mode,label,hint in self.TOOLS:
            action=menu.addAction(label);action.setCheckable(True);action.setChecked(self.mode==mode)
            action.setEnabled(not self.busy)
            action.triggered.connect(lambda checked=False,value=mode:self.set_mode(value if checked else 'pan'))
        if self.mode=='edit' and self.selected_image:
            menu.addSeparator()
            for label,callback in [('그림 복사\t'+self.owner.keys.describe('copy'),self.copy_selected_image),
                                   ('그림 잘라내기\t'+self.owner.keys.describe('cut'),lambda:self.copy_selected_image(cut=True))]:
                action=menu.addAction(label);action.setEnabled(self.ready())
                action.triggered.connect(lambda checked=False,fn=callback:fn())
        menu.exec(global_pos if global_pos is not None else QCursor.pos());menu.deleteLater()

    def set_mode(self,mode):
        if mode in ('move','replace','cell','image'):mode='edit'
        if mode not in ('pan','edit','text','cover') or self.busy:return
        if mode!='pan' and self.page.is_document_card:
            self.document_card_notice();return
        if mode!=self.mode and self.has_pending_move():
            self.after_move=lambda:self.set_mode(mode);self.commit_move();return
        if mode!='edit':
            self.selected_text=self.selected_image=None;self.image_target=self.image_drag_base=None;self.move_panel.hide()
        self.mode=mode;self.view.clear_gesture();self.view.background_pan=False
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag if mode=='pan' else QGraphicsView.DragMode.NoDrag)
        self.view.viewport().setCursor(Qt.CursorShape.OpenHandCursor if mode in ('pan','edit') else Qt.CursorShape.CrossCursor)
        self.message('')
        self.end_overlay.sync()
        if mode!='pan' and (not self.info or (mode=='edit' and not self.info.get('images_ready'))):self.request_info()

    def request_info(self):
        if self.page.is_document_card:return
        self.info_token+=1;self.loading_info=True
        self.backend.jobs=[j for j in self.backend.jobs if j['op']!='editinfo']
        self.backend.request('editinfo',self.page.path,self.page.number,token=self.info_token,
                             priority=True,payload={'images':self.mode=='edit'})

    def got_info(self,token,info,error):
        if self.closed or token!=self.info_token:return
        self.loading_info=False
        if error:
            self.owner.cancel_clear()
            self.paste_queue.clear();self.set_mode('pan');QMessageBox.warning(self,'편집 영역',error);return
        self.info=info;self.view.set_page_geometry(info['width'],info['height']);self.set_mode(self.mode)
        self.view.viewport().update()
        if self.mode=='edit' and self.restore_selection:
            target=self.restore_selection;self.restore_selection=None
            candidates=[s for s in info['spans'] if s['text']==target['text']]
            if candidates:self.select_text(min(candidates,key=lambda s:sum(abs(s['rect'][i]-target['rect'][i]) for i in range(4))))
            dx,dy=self.queued_nudge;self.queued_nudge=[0.0,0.0]
            if self.selected_text and abs(dx)+abs(dy)>0.0001:self.nudge_text(dx,dy)
        if self.mode=='edit' and self.restore_image:
            target=self.restore_image;self.restore_image=None
            candidates=list(reversed(info.get('images',[])))
            if candidates:
                chosen=min(candidates,key=lambda im:sum(abs(im['rect'][i]-target[i]) for i in range(4)))
                if max(abs(chosen['rect'][i]-target[i]) for i in range(4))<0.5:self.select_image(chosen)
            dx,dy=self.queued_nudge;self.queued_nudge=[0.0,0.0]
            if self.selected_image and abs(dx)+abs(dy)>0.0001:self.nudge_image(dx,dy)
            if self.after_image is not None:
                callback=self.after_image;self.after_image=None;callback()
        self.drain_paste_queue();self.perform_navigation()

    def edit_gesture(self,start,end,hit,override=None):
        mode=override or self.mode
        rect=[min(start[0],end[0]),min(start[1],end[1]),max(start[0],end[0]),max(start[1],end[1])]
        operation={'kind':mode,'rect':rect}
        if mode=='replace':
            if hit is None or 'text' not in hit:return
            dialog=TextEditDialog(self,hit,'글자 수정')
            if dialog.exec()!=QDialog.DialogCode.Accepted:return
            operation.update(dialog.operation());operation['rect']=hit['rect'];operation['rotate']=hit.get('rotate',0)
        elif mode in ('text','cover'):
            minimum=0.5 if mode=='cover' else 8
            if rect[2]-rect[0]<minimum or rect[3]-rect[1]<minimum:return
            if mode=='text':
                dialog=TextEditDialog(self,title='문자추가')
                if dialog.exec()!=QDialog.DialogCode.Accepted:return
                operation.update(dialog.operation())
                if not operation['text'].strip():return
                self.mode='edit'
        else:return
        if mode in ('replace','text') and operation.get('text','').strip():
            self.restore_selection={'text':operation['text'].splitlines()[0],'rect':operation['rect']}
        self.submit_edit(operation)

    def submit_edit(self, operation):
        if self.busy or self.closed:
            return
        if self.page.is_document_card:
            self.document_card_notice();return
        self.busy = True; self.edit_token += 1
        self.edit_source = (self.page.path, self.page.number)
        output = TEMP_ROOT / self.owner.session / 'edits' / (uuid.uuid4().hex+'.pdf')
        if operation['kind'] == 'cover':
            self.pending_cover = list(operation['rect']); self.pending_cover_path = str(output)
            self.view.viewport().update()
        self.message('수정 내용을 반영하는 중…')
        self.backend.request('edit', self.page.path, self.page.number, token=self.edit_token,
                             priority=True, payload={'operation': operation, 'output': str(output)})

    def got_edit(self, token, path, error):
        if self.closed or token != self.edit_token:
            return
        self.busy = False
        if error:
            self.owner.cancel_clear()
            self.pending_cover = self.pending_cover_path = None
            self.view.viewport().update()
            self.restore_selection = self.restore_image = None; self.queued_nudge = [0.0,0.0]; self.after_move = None
            self.after_image = None
            self.paste_queue.clear();self.nav_target_uid=None
            self.nav_previous.stop_drag();self.nav_next.stop_drag();self.update_navigation()
            self.cancel_move()
            self.set_mode(self.mode); QMessageBox.warning(self, '편집 실패', error); return
        current = self.owner.by_id.get(self.page.uid)
        if current is None or (current.path, current.number) != self.edit_source:
            self.owner.cancel_clear()
            Path(path).unlink(missing_ok=True)
            self.pending_cover = self.pending_cover_path = None
            self.view.viewport().update()
            self.message('페이지가 변경되어 수정 적용을 취소했습니다'); return
        self.owner.replace_page(current, path)
        if self.after_move is not None:
            callback = self.after_move; self.after_move = None
            QTimer.singleShot(0, callback)
        self.drain_paste_queue()
        self.perform_navigation()

    def sync_page(self, page):
        if self.closed or (self.page.uid,self.page.path,self.page.number) == (page.uid,page.path,page.number):
            return
        switching=self.page.uid!=page.uid
        if switching:
            if page.uid!=self.first_page_hint_uid:self.first_page_hint_uid=None
            self.restore_image=self.restore_selection=self.after_image=None;self.queued_nudge=[0.0,0.0]
            self.view.fit_timer.stop()
            self.view.scene().clear();self.view.item=None;self.view.pdf_size=None
            self.view.resetTransform();self.view.auto_fit=True
        self.page = page; self.info = None; self.loading_info = False
        if page.is_document_card:self.set_mode('pan')
        if page.path != self.pending_cover_path:
            self.pending_cover = self.pending_cover_path = None
        self.selected_text = None; self.move_offset = [0.0, 0.0]; self.move_timer.stop(); self.move_panel.hide()
        self.selected_image = None; self.image_target = self.image_drag_base = None
        self.info_token += 1; self.token = self.owner.next_preview_token(); self.requested_side = 0
        self.preview_ready=False
        self.view.clear_gesture()
        self.backend.jobs = [j for j in self.backend.jobs if j['op'] not in ('preview', 'editinfo')]
        self.image_backend.cancel_pending()
        if switching:
            pix=self.owner.thumbs.get((page.path,page.number))
            if pix is not None:self.view.set_image(pix)
        self.changed_zoom(); self.request_image()
        if self.mode != 'pan':
            self.request_info()
        self.update_navigation()

    def undo_edit(self):
        if self.has_pending_move():
            self.cancel_move(); return
        if not self.busy:
            self.owner.undo()

    def redo_edit(self):
        if not self.busy:
            self.owner.redo()

    def save_copy(self):
        self.owner.save_revision()

    def save_page_copy(self):
        if self.has_pending_move():
            self.after_move = self.save_page_copy; self.commit_move(); return
        if not self.busy:
            self.owner.save_copy_dialog([self.page], Path(self.page.label_path).stem+'_수정')

    def changed_zoom(self):
        self.view.controls_timer.start()
        percent = round(100*self.view.transform().m11()/max(0.001,self.view.fit_scale))
        mark = ' · 수정본' if self.page.source_path and self.page.state_key not in self.owner.pristine_pages else ''
        self.setWindowTitle(f'{Path(self.page.label_path).name} · {self.current_index()+1}/{len(self.owner.pages)} · {percent}%{mark}')
        if self.embedded:
            self.owner.setWindowTitle(f'{APP_NAME} · {Path(self.page.input_path or self.page.label_path).name}')
        self.refine.start()

    def request_image(self):
        if self.closed:
            return
        picture=is_image_source(self.page.path)
        if picture:
            if self.view.item is None:
                viewport=self.view.viewport()
                pixels=max(viewport.width(),viewport.height())*self.view.devicePixelRatioF()
            else:
                pixels=max(self.view.page_rect.width(),self.view.page_rect.height())*self.view.transform().m11()*self.view.devicePixelRatioF()
            # 물리 픽셀 기준. 잦은 1px 크기 변경은 64px 단위로 묶고 확대 시 원본을 다시 읽는다.
            side=min(IMAGE_PREVIEW_MAX_SIDE,max(256,math.ceil(pixels/64)*64))
        else:
            side=1800
            if self.view.item is not None:
                side=max(side,math.ceil(max(self.view.page_rect.width(),self.view.page_rect.height())*
                         self.view.transform().m11()*self.view.devicePixelRatioF()))
            side=min(5000,side)
        if side <= self.requested_side:
            return
        self.requested_side = side
        self.token = self.owner.next_preview_token()
        engine=self.image_backend if picture else self.backend
        self.backend.jobs = [j for j in self.backend.jobs if j['op'] != 'preview']
        self.image_backend.jobs = [j for j in self.image_backend.jobs if j['op']=='release']
        engine.request('preview', self.page.path, self.page.number,
                             token=self.token, priority=True, max_side=side)

    def show_thumbnail(self,path,number,pix):
        # 늦게 도착한 썸네일도 첫 화면에 사용. 새 파일/수정본/선명한 화면을 덮지 않는다.
        if (self.closed or self.preview_ready or not is_image_source(self.page.path) or
                (path,number)!=(self.page.path,self.page.number) or pix.isNull()):return
        if self.view.item is None:
            self.view.set_image(pix)

    def got_image(self, token, pix, error):
        if self.closed or token != self.token:
            return
        if error:
            self.requested_side=0  # 다음 확대/더블클릭에서 원본 읽기를 다시 시도할 수 있게 한다.
            QMessageBox.warning(self, '크게 보기', error)
        else:
            self.preview_ready=True
            self.view.set_image(pix)
            if self.info:
                self.view.set_page_geometry(self.info['width'], self.info['height'])
            if not self.busy:
                self.pending_cover = self.pending_cover_path = None
                self.view.viewport().update()

    def shutdown(self):
        if not self.closed:
            self.closed = True
            self.view.fit_timer.stop()
            self.refine.stop()
            self.move_timer.stop()
            self.nav_timer.stop();self.nav_previous.stop_drag();self.nav_next.stop_drag();self.paste_queue.clear()
            self.backend.stop()
            self.image_backend.preview.disconnect(self.got_image)
            self.image_backend.cancel_pending(release=True)
            if self.owner.preview_dialog is self:self.owner.preview_dialog=None
            if self.embedded:
                self.owner.remember_preview_split()
                self.hide();self.setParent(self.owner,Qt.WindowType.Widget)
                self.owner.restore_empty_preview()
                self.owner.focus_content();self.deleteLater()

    def done(self, result):
        if self.paste_queue:
            QTimer.singleShot(100,lambda:self.done(result));return
        if self.has_pending_move():
            self.after_move = lambda: self.done(result); self.commit_move(); return
        if self.busy:
            return
        self.shutdown(); super().done(result)

    def closeEvent(self, event):
        if self.paste_queue:
            QTimer.singleShot(100,self.close);event.ignore();return
        if self.has_pending_move():
            self.after_move = self.close; self.commit_move(); event.ignore(); return
        if self.busy:
            event.ignore(); return
        self.shutdown(); super().closeEvent(event)

    def keyPressEvent(self, event):
        if self.owner.handle_file_key(event):return
        if event.key()==Qt.Key.Key_Escape and (self.nav_previous.pressed or self.nav_next.pressed):
            self.nav_previous.cancel();self.nav_next.cancel();event.accept();return
        if self.handle_move_key(event):
            return
        if event.key() == Qt.Key.Key_Escape and self.mode != 'pan':
            self.cancel_move()
            self.set_mode('pan'); event.accept(); return
        if event.key()==Qt.Key.Key_Escape:
            if not self.embedded:self.close()
            else:self.view.setFocus()
            event.accept();return
        super().keyPressEvent(event)

    def has_pending_move(self):
        if self.mode == 'edit' and self.selected_image and self.image_target:
            return max(abs(a-b) for a,b in zip(self.selected_image['rect'],self.image_target))>0.0001
        return self.selected_text is not None and sum(abs(v) for v in self.move_offset)>0.0001

    def select_text(self, element):
        if self.has_pending_move():
            self.commit_move(); return
        self.selected_image=None;self.image_target=self.image_drag_base=None
        self.selected_text = element; self.move_offset = [0.0, 0.0]
        self.update_coordinates(); self.view.viewport().update()

    def moved_rect(self):
        r = self.selected_text['rect']; dx, dy = self.move_offset
        return [r[0]+dx, r[1]+dy, r[2]+dx, r[3]+dy]

    def update_coordinates(self):
        visible = self.selected_text is not None and self.mode == 'edit'
        self.move_panel.setVisible(visible)
        if visible:
            r = self.moved_rect()
            for spin, value in [(self.move_x, r[0]), (self.move_y, r[1])]:
                spin.blockSignals(True); spin.setValue(value/PT_PER_MM); spin.blockSignals(False)
                spin.setEnabled(not self.busy)
        self.position_controls()

    def set_move_offset(self, dx, dy):
        if self.selected_text is None or self.info is None or self.busy:
            return
        r = self.selected_text['rect']
        self.move_offset = [max(-r[0], min(self.info['width']-r[2],dx)),
                            max(-r[1], min(self.info['height']-r[3],dy))]
        self.update_coordinates(); self.view.viewport().update()

    def coordinate_changed(self):
        if not self.selected_text or self.busy:
            return
        r = self.selected_text['rect']
        self.set_move_offset(self.move_x.value()*PT_PER_MM-r[0], self.move_y.value()*PT_PER_MM-r[1])
        self.move_timer.start()

    def nudge_text(self, dx, dy):
        if self.busy or self.loading_info:
            if self.restore_selection is not None:
                self.queued_nudge[0] += dx; self.queued_nudge[1] += dy
            return
        if self.selected_text is not None:
            self.set_move_offset(self.move_offset[0]+dx, self.move_offset[1]+dy)
            self.move_timer.start()

    def handle_move_key(self, event):
        if self.mode != 'edit':
            return False
        directions = {Qt.Key.Key_Left: (-1,0), Qt.Key.Key_Right: (1,0), Qt.Key.Key_Up: (0,-1), Qt.Key.Key_Down: (0,1)}
        if self.owner.keys.matches('delete',event) and (self.selected_image or self.selected_text):
            self.delete_selected(); event.accept(); return True
        if event.key() in directions and (self.selected_text or self.restore_selection or self.selected_image or self.restore_image):
            step = 0.1 if event.modifiers() & Qt.KeyboardModifier.ControlModifier else (5 if event.modifiers() & Qt.KeyboardModifier.ShiftModifier else 0.5)
            dx, dy = directions[event.key()]
            callback = self.nudge_image if self.selected_image or self.restore_image else self.nudge_text
            callback(dx*step*PT_PER_MM,dy*step*PT_PER_MM)
            event.accept(); return True
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and self.has_pending_move():
            self.commit_move(); event.accept(); return True
        return False

    def cancel_move(self):
        self.move_timer.stop(); self.move_offset = [0.0,0.0]; self.queued_nudge = [0.0,0.0]
        if self.selected_image:
            self.image_target = list(self.selected_image['rect'])
        self.update_coordinates(); self.view.viewport().update()

    def commit_move(self):
        self.move_timer.stop()
        if not self.has_pending_move() or not self.ready():
            return
        if self.selected_image:
            self.restore_image = list(self.image_target)
            self.submit_image_edit('image_transform',target=list(self.image_target)); return
        source = self.selected_text; dx, dy = self.move_offset
        self.restore_selection = {'text': source['text'], 'rect': self.moved_rect()}
        self.move_offset = [0.0,0.0]
        self.submit_edit({'kind':'move', 'rect':source['rect'], 'text':source['text'], 'dx':dx, 'dy':dy})
        self.update_coordinates()

    def current_index(self):
        return next((i for i,p in enumerate(self.owner.pages) if p.uid==self.page.uid),0)

    def update_navigation(self):
        if not hasattr(self,'nav_previous'):return
        visible=bool(self.owner.pages)
        self.nav_previous.setVisible(visible);self.nav_next.setVisible(visible)
        if not self.nav_scrubbing and self.nav_target_uid is None:self.nav_display_index=self.current_index()
        unit='항목' if any(p.is_document_card for p in self.owner.pages) else '장'
        self.nav_label.set_count(len(self.owner.pages),self.current_index(),unit)
        if self.page.is_document_card:
            self.nav_label.setText(self.nav_label.text()+f' · PDF {self.page.document_pages:,}쪽');self.nav_label.place()
        self.nav_previous.update();self.nav_next.update()
        self.end_overlay.sync()
        self.position_controls()

    def request_navigation(self,index,scrub=False,select=True):
        if self.closed or not self.owner.pages:return
        modal=QApplication.activeModalWidget()
        if modal is not None and modal is not self:return
        index=int(index)
        if index<0:self.first_page_hint_uid=self.owner.pages[0].uid
        elif index>0:self.first_page_hint_uid=None
        index=max(0,min(len(self.owner.pages)-1,index))
        self.nav_target_uid=self.owner.pages[index].uid;self.nav_display_index=index;self.nav_select=select
        self.end_overlay.sync()
        self.position_controls();self.view.viewport().update()
        # A fast repeat must not continuously restart (and starve) a single-shot timer.
        if not self.nav_timer.isActive():self.nav_timer.start()

    def perform_navigation(self):
        if self.closed or self.nav_target_uid is None or self.busy or self.paste_queue or self.after_image is not None:return
        modal=QApplication.activeModalWidget()
        if modal is not None and modal is not self:self.nav_timer.start();return
        if any(abs(v)>0.0001 for v in self.queued_nudge):return
        if self.has_pending_move():self.commit_move();return
        if self.nav_scrubbing and self.view.item is None:
            # Let the current uncached page appear before advancing again. Keep only
            # the latest requested target; large originals cannot build a render queue.
            engine=self.image_backend if is_image_source(self.page.path) else self.backend
            pending=([engine.active] if engine.active else [])+engine.jobs
            if any(job.get('op')=='preview' and job.get('token')==self.token for job in pending):
                self.nav_timer.start();return
        page=self.owner.by_id.get(self.nav_target_uid);self.nav_target_uid=None
        if page is not None:
            self.sync_page(page)
            if getattr(self,'nav_select',True):
                self.owner.canvas.selected={page.uid};self.owner.canvas.anchor=page.uid
                self.owner.ensure_page_visible(page.uid)
            self.owner.canvas.viewport().update()

    def copy_selected_image(self,cut=False):
        modal=QApplication.activeModalWidget()
        if modal is not None and modal is not self:return
        focus=QApplication.focusWidget()
        if isinstance(focus,(QLineEdit,QPlainTextEdit)):
            focus.cut() if cut else focus.copy();return
        if self.mode!='edit' or not self.selected_image or not self.ready():return
        if self.has_pending_move():
            self.after_image=lambda:self.copy_selected_image(cut=cut)
            self.commit_move();return
        try:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            try:data,size=copy_pdf_image_png(self.page.path,self.page.number,self.selected_image)
            finally:QApplication.restoreOverrideCursor()
            picture=QImage.fromData(data,'PNG')
            if picture.isNull():raise ValueError('그림을 클립보드로 복사하지 못했습니다.')
            mime=QMimeData();mime.setImageData(picture)
            mime.setData('image/png',data)
            mime.setData(IMAGE_CLIPBOARD_MIME,json.dumps(size).encode('utf-8'))
            QApplication.clipboard().setMimeData(mime)
            if QApplication.clipboard().image().isNull():raise ValueError('클립보드에 그림을 저장하지 못했습니다.')
            if cut:self.delete_image()
            else:QToolTip.showText(QCursor.pos(),'그림 복사 완료 · '+self.owner.keys.describe('paste')+'로 붙여넣기',self.view)
        except Exception as exc:QMessageBox.warning(self,'그림 잘라내기' if cut else '그림 복사',str(exc))

    def paste_clipboard(self):
        modal=QApplication.activeModalWidget()
        if modal is not None and modal is not self:return
        try:
            payloads=clipboard_edit_payloads(self.owner.session)
            if payloads:self.enqueue_paste(payloads)
            else:QToolTip.showText(QCursor.pos(),'붙여넣을 그림 또는 문자가 없습니다',self.view)
        except Exception as exc:QMessageBox.warning(self,'붙여넣기',str(exc))

    def enqueue_paste(self,payloads,page_uid=None):
        target=page_uid or self.page.uid
        page=self.owner.by_id.get(target)
        if page is not None and page.is_document_card:
            self.document_card_notice();return
        self.paste_queue.extend({**p,'page_uid':target} for p in payloads)
        self.drain_paste_queue()

    def drain_paste_queue(self):
        if self.closed or self.busy or not self.paste_queue:return
        if self.has_pending_move():self.commit_move();return
        payload=self.paste_queue[0];target=self.owner.by_id.get(payload['page_uid'])
        if target is None:
            self.paste_queue.pop(0);QTimer.singleShot(0,self.drain_paste_queue);return
        if target.is_document_card:
            self.paste_queue.pop(0);self.document_card_notice();QTimer.singleShot(0,self.drain_paste_queue);return
        if self.page.uid!=target.uid:
            self.mode='edit';self.sync_page(target);return
        if self.mode!='edit':self.set_mode('edit')
        if not self.ready():return
        if not self.info.get('images_ready'):self.request_info();return
        self.paste_queue.pop(0);self.cancel_move();self.paste_serial+=1
        pw,ph=self.info['width'],self.info['height']
        if payload['kind']=='image':
            if 'pdf_size' in payload:
                width,height=payload['pdf_size'];scale=min(1,pw/width,ph/height)
                width,height=width*scale,height*scale
            else:
                scale=min(0.75,pw*0.62/payload['width'],ph*0.62/payload['height'])
                width,height=payload['width']*scale,payload['height']*scale
        else:
            width=pw*0.65;height=min(ph*0.7,max(40,len(payload['text'].splitlines())*17+12))
        offset=((self.paste_serial-1)%8)*8
        x=max(0,min(pw-width,(pw-width)/2+offset));y=max(0,min(ph-height,(ph-height)/2+offset))
        rect=[x,y,x+width,y+height]
        self.selected_text=self.selected_image=None;self.image_target=None;self.move_panel.hide()
        if payload['kind']=='image':
            self.restore_image=rect
            operation={'kind':'image_add','rect':rect,'filename':payload['filename']}
        else:
            self.restore_selection={'text':payload['text'].splitlines()[0],'rect':rect}
            operation={'kind':'text','rect':rect,'text':payload['text'],'size':11,'color':'#111111'}
        self.submit_edit(operation)

    def delete_selected(self):
        if not self.ready():return
        if self.selected_image:self.delete_image();return
        if self.selected_text:
            selected=self.selected_text;self.cancel_move();self.restore_selection=None
            self.submit_edit({'kind':'text_delete','rect':selected['rect'],'text':selected['text']})

    def pick_image_file(self):
        filename,_ = QFileDialog.getOpenFileName(self,'그림 파일 선택','',
            '그림 (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;모든 파일 (*)')
        return filename

    def choose_image(self):
        if self.busy: return
        filename = self.pick_image_file()
        if filename:
            pix = QPixmap(filename)
            if pix.isNull():
                QMessageBox.warning(self,'그림 파일','열 수 없는 그림입니다. PNG 또는 JPG 파일을 선택하세요.'); return
            self.enqueue_paste([{'kind':'image','filename':filename,'width':pix.width(),'height':pix.height()}])

    def select_image(self, element):
        if self.busy: return
        if self.has_pending_move():
            # 방향키 입력 직후 클릭해도 아직 저장 중인 위치를 버리지 않는다.
            self.commit_move(); return
        self.selected_text=None;self.move_offset=[0.0,0.0];self.move_panel.hide()
        self.selected_image = element
        self.image_target = list(element['rect']) if element else None
        self.view.viewport().update()

    def drag_image(self, start, end, handle, modifiers):
        if self.busy or not self.selected_image or not self.image_drag_base: return
        r = self.image_drag_base
        dx,dy = end[0]-start[0],end[1]-start[1]
        page_w,page_h = self.info['width'],self.info['height']
        if handle is None:
            if modifiers & Qt.KeyboardModifier.ShiftModifier:
                if abs(dx)>=abs(dy): dy=0
                else: dx=0
            dx=max(-r[0],min(page_w-r[2],dx)); dy=max(-r[1],min(page_h-r[3],dy))
            target=[r[0]+dx,r[1]+dy,r[2]+dx,r[3]+dy]
        else:
            sx = -1 if handle in (0,3) else 1
            sy = -1 if handle in (0,1) else 1
            ax = r[2] if sx<0 else r[0]; ay = r[3] if sy<0 else r[1]
            width=max(2,r[2]-r[0]+sx*dx); height=max(2,r[3]-r[1]+sy*dy)
            max_w=ax if sx<0 else page_w-ax; max_h=ay if sy<0 else page_h-ay
            if not modifiers & Qt.KeyboardModifier.ShiftModifier:
                ratio=(r[2]-r[0])/(r[3]-r[1])
                if abs(dx)/(r[2]-r[0]) >= abs(dy)/(r[3]-r[1]): height=width/ratio
                else: width=height*ratio
                factor=min(1,max_w/width,max_h/height); width*=factor; height*=factor
            else:
                width=min(width,max_w); height=min(height,max_h)
            bx=ax+sx*width; by=ay+sy*height
            target=[min(ax,bx),min(ay,by),max(ax,bx),max(ay,by)]
        self.image_target=target; self.view.viewport().update()

    def nudge_image(self, dx, dy):
        if self.busy or self.loading_info:
            if self.restore_image:
                self.queued_nudge[0]+=dx; self.queued_nudge[1]+=dy
            return
        if not self.selected_image or not self.image_target: return
        self.image_drag_base=list(self.image_target)
        self.drag_image([0,0],[dx,dy],None,Qt.KeyboardModifier.NoModifier)
        self.move_timer.start()

    def submit_image_edit(self, kind, **extra):
        if not self.ready() or not self.selected_image: return
        self.move_timer.stop()
        self.submit_edit({'kind':kind,'rect':self.selected_image['rect'],
                          'image_id':self.selected_image['id'],**extra})

    def image_geometry(self):
        if not self.ready() or not self.selected_image: return
        self.move_timer.stop()
        dialog = ImageGeometryDialog(self,self.image_target)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.image_target=dialog.rectangle()
            if dialog.replacement_path:
                filename=dialog.replacement_path
                if self.has_pending_move():self.after_image=lambda:self.replace_image_file(filename);self.commit_move()
                else:self.replace_image_file(filename)
            else:self.commit_move()
        elif self.has_pending_move():
            self.move_timer.start()

    def replace_image(self):
        if not self.ready() or not self.selected_image: return
        if self.has_pending_move():
            self.after_image=self.replace_image; self.commit_move(); return
        filename=self.pick_image_file()
        if filename:self.replace_image_file(filename)

    def replace_image_file(self,filename):
        if not self.ready() or not self.selected_image:return
        self.restore_image=list(self.selected_image['rect']);self.submit_image_edit('image_replace',filename=filename)

    def delete_image(self):
        if not self.ready() or not self.selected_image: return
        self.cancel_move(); self.restore_image=None
        self.submit_image_edit('image_delete')


class DragCancelGuard(QObject):
    """앱 안의 우클릭과 Windows OLE 드래그 중 우클릭을 모두 감시한다."""
    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas
        self.cancelled = False
        self.cancel_api = QDrag.cancel
        self.key_state = None
        if sys.platform == 'win32':
            import ctypes
            self.key_state = ctypes.windll.user32.GetAsyncKeyState
            self.key_state.argtypes = [ctypes.c_int]
            self.key_state.restype = ctypes.c_short
        self.timer = QTimer(self)
        self.timer.setInterval(15)
        self.timer.timeout.connect(self.poll)

    def start(self):
        QApplication.instance().installEventFilter(self)
        self.timer.start()

    def stop(self):
        self.timer.stop()
        QApplication.instance().removeEventFilter(self)

    def cancel(self):
        if not self.cancelled:
            self.cancelled = True
            self.canvas.cancelled_drag = True
            self.canvas.suppress_context_until = time.monotonic()+0.5
            self.canvas.slot = None
            self.canvas.pointer = None
            self.canvas.layout_pages()
            self.cancel_api()

    def poll(self):
        if self.key_state is not None and self.key_state(0x02) & 0x8000:
            self.cancel()

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.NonClientAreaMouseButtonPress):
            if event.button() == Qt.MouseButton.RightButton:
                self.cancel(); return True
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.cancel(); return True
        return False


class PageCanvas(QAbstractScrollArea):
    selectionChanged = Signal()

    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.setFrameShape(QAbstractScrollArea.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.viewport().setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet('QScrollBar:vertical{width:9px;background:transparent;} QScrollBar::handle:vertical{background:#52596c;border-radius:4px;min-height:30px;} QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}')
        self.selected = set()
        self.anchor = None
        self.positions, self.velocities = {}, {}
        self.targets = {}
        self.cells = []
        self.slot = None
        self.gap_point = None
        self.gap_points = []
        self.gap_count = 0
        self.dragging = set()
        self.pointer = None
        self.external_hover = False
        self.press_pos = None
        self.pressed_uid = None
        self.defer_click = False
        self.toggle_on_release = None
        self.internal_drop = False
        self.cancelled_drag = False
        self.cancel_guard = None
        self.suppress_context_until = 0
        self.angle = 0.0
        self.wheel_remainder = 0.0
        self.wheel_precise = None
        self.page_count=PageCountLabel(self.viewport())
        self.selectionChanged.connect(self.viewport().update)
        self.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

    def dimensions(self):
        width = max(200, self.viewport().width())
        self.card_w = min(self.owner.card_size, max(100, width-40))
        self.card_h = self.card_w * 1.36
        self.gap = 28
        self.columns = max(1, int((width-32+self.gap)/(self.card_w+self.gap)))
        self.margin = max(16, (width-self.columns*self.card_w-(self.columns-1)*self.gap)/2)

    def point_for(self, index):
        return QPointF(self.margin+(index % self.columns)*(self.card_w+self.gap),
                       44+(index//self.columns)*(self.card_h+self.gap))

    def layout_pages(self):
        self.dimensions()
        pages = self.owner.pages
        # 선택한 묶음을 제외한 목록을 기준으로 삽입할 빈칸을 계산한다.
        gap_at = None
        others = pages
        if self.slot is not None:
            others = [p for p in pages if p.uid not in self.dragging]
            self.slot = max(0, min(self.slot, len(others)))
            gap_at = self.slot
        self.gap_count = max(1, len(self.dragging)) if gap_at is not None else 0
        self.targets = {}
        self.cells = []
        for index, page in enumerate(others):
            visual_index = index + (self.gap_count if gap_at is not None and index >= gap_at else 0)
            point = self.point_for(visual_index)
            self.targets[page.uid] = point
            self.cells.append((page.uid, point))
            if page.uid not in self.positions:
                self.positions[page.uid] = point + QPointF(0, 24 if self.owner.animate else 0)
                self.velocities[page.uid] = QPointF(0, 0)
        self.gap_point = self.point_for(gap_at) if gap_at is not None else None
        self.gap_points = [self.point_for(gap_at+i) for i in range(self.gap_count)] if gap_at is not None else []
        total = len(others)+self.gap_count
        rows=math.ceil(total/self.columns)
        height = 62 + rows*self.card_h+max(0,rows-1)*self.gap
        self.verticalScrollBar().setRange(0, max(0, int(height-self.viewport().height())))
        self.verticalScrollBar().setPageStep(self.viewport().height())
        self.page_count.set_count(len(pages),unit='항목' if any(p.is_document_card for p in pages) else '장')
        self.viewport().update()

    def on_scroll(self):
        self.viewport().update()
        self.owner.prioritize_thumbnails()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.layout_pages()
        self.owner.place_actions()
        self.owner.prioritize_thumbnails()

    def wheelEvent(self,event):
        precise=bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
        if self.wheel_precise != precise:
            self.wheel_remainder=0.0;self.wheel_precise=precise
        pixel=event.pixelDelta().y();angle=event.angleDelta().y()
        if pixel:
            movement=-pixel*(0.25 if precise else 2.5)
        else:
            step=24 if precise else max(120,min(self.viewport().height()*0.8,self.card_h+self.gap))
            movement=-angle/120*step
        if movement*self.wheel_remainder<0:self.wheel_remainder=0.0
        self.wheel_remainder+=movement
        amount=math.trunc(self.wheel_remainder);self.wheel_remainder-=amount
        bar=self.verticalScrollBar();before=bar.value();bar.setValue(before+amount)
        if bar.value()!=before+amount:self.wheel_remainder=0.0
        event.accept()

    def tick(self):
        if not self.isVisible():
            return
        self.angle = (self.angle + 1.5) % 360
        moving = False
        for uid, target in self.targets.items():
            repel = QPointF(0, 0)
            if self.pointer is not None and self.owner.animate:
                delta = target+QPointF(self.card_w/2, self.card_h/2)-self.pointer
                distance = math.hypot(delta.x(), delta.y())
                radius = self.card_w*1.2
                if 0 < distance < radius:
                    repel = delta * ((1-distance/radius)*self.owner.repulsion/ max(distance,1))
            goal = target+repel
            pos = self.positions.get(uid, target)
            velocity = self.velocities.get(uid, QPointF(0,0))
            if self.owner.animate:
                velocity = (velocity + (goal-pos)*0.14)*0.72
                pos += velocity
                if abs(pos.x()-goal.x())+abs(pos.y()-goal.y()) < 0.15 and math.hypot(velocity.x(),velocity.y()) < 0.15:
                    pos, velocity = goal, QPointF(0,0)
                else:
                    moving = True
            else:
                pos, velocity = goal, QPointF(0,0)
            self.positions[uid], self.velocities[uid] = pos, velocity
        if self.pointer is not None:
            vy = self.pointer.y()-self.verticalScrollBar().value()
            shift = -18 if vy < 55 else (18 if vy > self.viewport().height()-55 else 0)
            if shift:
                before = self.verticalScrollBar().value()
                self.verticalScrollBar().setValue(before+shift)
                self.pointer.setY(self.pointer.y()+self.verticalScrollBar().value()-before)
                slot = self.insertion_at(self.pointer-QPointF(0,self.verticalScrollBar().value()))
                if slot != self.slot:
                    self.slot = slot
                    self.layout_pages()
        if moving or (self.selected and self.owner.animate) or self.pointer is not None or self.owner.pending_import:
            self.viewport().update()

    def card_rect(self, uid):
        point = self.positions.get(uid, self.targets.get(uid, QPointF()))
        return QRectF(point.x(), point.y()-self.verticalScrollBar().value(), self.card_w, self.card_h)

    def paintEvent(self, event):
        p = QPainter(self.viewport())
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = self.owner.dark
        p.fillRect(self.viewport().rect(), QColor('#181b24' if dark else '#edf0f5'))
        if not self.owner.pages:
            p.fillRect(self.viewport().rect(),QColor('#151821' if dark else '#e4e8ef'))
        moving_pages = [page for page in self.owner.pages if page.uid in self.dragging]
        for index, point in enumerate(self.gap_points):
            r = QRectF(point.x(),point.y()-self.verticalScrollBar().value(),self.card_w,self.card_h)
            if r.bottom() < -40 or r.top() > self.viewport().height()+40:
                continue
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor('#552531' if dark else '#ffd5dc'))
            p.drawRoundedRect(r,7,7)
            if index < len(moving_pages):
                page = moving_pages[index]
                pix = self.owner.thumbs.get((page.path,page.number))
                if pix is not None and not pix.isNull():
                    inside = r.adjusted(7,7,-7,-7)
                    size = pix.size().scaled(inside.size().toSize(),Qt.AspectRatioMode.KeepAspectRatio)
                    draw = QRectF(inside.center().x()-size.width()/2,inside.center().y()-size.height()/2,size.width(),size.height())
                    p.save();p.setOpacity(0.60);p.drawPixmap(draw,pix,QRectF(pix.rect()));p.restore()
            else:
                p.setPen(QPen(QColor('#ff7a90'),4,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
                p.drawLine(r.center()+QPointF(-16,0),r.center()+QPointF(16,0))
                p.drawLine(r.center()+QPointF(0,-16),r.center()+QPointF(0,16))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(QColor('#ff2d50'),4,Qt.PenStyle.DashLine))
            p.drawRoundedRect(r,7,7)
            if moving_pages:
                badge = QRectF(r.center().x()-29,r.center().y()-15,58,30)
                p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#de173a'))
                p.drawRoundedRect(badge,15,15)
                p.setPen(QColor('white'));p.setFont(QFont('Arial',11,QFont.Weight.Bold))
                p.drawText(badge,Qt.AlignmentFlag.AlignCenter,f'{index+1}/{len(moving_pages)}')
            if index == 0:
                p.setPen(QPen(QColor('#ff4060'),5,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
                x = r.left()-11
                p.drawLine(QPointF(x,r.top()+4),QPointF(x,r.bottom()-4))
                p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#ff4060'))
                p.drawEllipse(QPointF(x,r.top()),5,5);p.drawEllipse(QPointF(x,r.bottom()),5,5)
        for page in self.owner.pages:
            if page.uid not in self.targets:
                continue
            r = self.card_rect(page.uid)
            if r.bottom() < -40 or r.top() > self.viewport().height()+40:
                continue
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(0,0,0,65 if dark else 25))
            p.drawRoundedRect(r.translated(0,5).adjusted(-2,-2,2,2),7,7)
            if page.document_pages>1:
                for offset in (8,4):
                    p.setPen(QPen(QColor('#b24c5c' if dark else '#df8190'),1.4))
                    p.setBrush(QColor('#f5dce1' if offset==8 else '#fff0f3'))
                    p.drawRoundedRect(r.translated(offset,-offset),5,5)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor('#ffffff'))
            p.drawRoundedRect(r,5,5)
            key = (page.path,page.number)
            pix = self.owner.thumbs.get(key)
            if pix and not pix.isNull():
                inside = r.adjusted(5,5,-5,-5)
                size = pix.size().scaled(inside.size().toSize(),Qt.AspectRatioMode.KeepAspectRatio)
                draw = QRectF(inside.center().x()-size.width()/2, inside.center().y()-size.height()/2,size.width(),size.height())
                p.drawPixmap(draw,pix,QRectF(pix.rect()))
            else:
                p.setPen(QPen(QColor('#adb3c0' if key not in self.owner.thumb_errors else '#e52f48'),2))
                if key in self.owner.thumb_errors:
                    c=r.center();p.drawLine(c+QPointF(-10,-10),c+QPointF(10,10));p.drawLine(c+QPointF(-10,10),c+QPointF(10,-10))
                else:p.drawArc(QRectF(r.center().x()-13,r.center().y()-13,26,26),int(self.angle*16),220*16)
            p.setPen(QPen(page_border_brush(page,r),2));p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(r,5,5)
            if page.uid in self.selected:
                p.setPen(QPen(QColor(35,176,205,70) if page_is_picture(page) else QColor(242,39,66,60),11))
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.drawRoundedRect(r.adjusted(-2,-2,2,2),7,7)
                p.setPen(QPen(page_border_brush(page,r,True,self.angle if self.owner.animate else 0),4))
                p.drawRoundedRect(r.adjusted(-2,-2,2,2),7,7)
            if page.is_document_card:
                text=f'PDF · {page.document_pages:,}쪽'
                p.setFont(QFont('Malgun Gothic',9,QFont.Weight.DemiBold))
                width=min(r.width()-12,p.fontMetrics().horizontalAdvance(text)+16)
                badge=QRectF(r.left()+6,r.bottom()-28,width,22)
                p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor(163,20,46,230));p.drawRoundedRect(badge,5,5)
                p.setPen(QColor('white'));p.drawText(badge,Qt.AlignmentFlag.AlignCenter,text)
            elif self.owner.show_numbers:
                p.setBrush(QColor(20,25,35,180));p.setPen(Qt.PenStyle.NoPen)
                br = QRectF(r.right()-37,r.bottom()-24,32,19)
                p.drawRoundedRect(br,5,5);p.setPen(QColor('white'))
                p.setFont(QFont('Arial',9))
                p.drawText(br,Qt.AlignmentFlag.AlignCenter,str(page.label_number+1))
        if self.owner.pending_import:
            p.setPen(QPen(QColor('#ff4059'),3))
            p.drawArc(QRectF(14,14,20,20),int(self.angle*16),250*16)
        p.end()

    def uid_at(self, point):
        for page in reversed(self.owner.pages):
            if page.uid in self.targets and self.card_rect(page.uid).contains(point):
                return page.uid
        return None

    def selected_pages(self):
        return [p for p in self.owner.pages if p.uid in self.selected]

    def contextMenuEvent(self, event):
        if self.dragging or self.cancel_guard is not None or time.monotonic() < self.suppress_context_until:
            event.accept(); return
        uid = self.uid_at(event.pos())
        if uid is not None and uid not in self.selected:
            self.selected = {uid}; self.anchor = uid; self.selectionChanged.emit()
        self.setFocus()
        menu = QMenu(self)
        page=self.owner.by_id.get(uid)
        if page is not None and page.is_document_card:
            menu.addAction(f'PDF 전체 열기 · {page.document_pages:,}쪽',
                           lambda:self.owner.open_document_card(page))
            menu.addSeparator()
        menu.addAction('오른쪽에 빈 PDF 페이지 만들기', lambda: self.owner.insert_blank_page(uid))
        menu.addSeparator()
        copy = menu.addAction('페이지 복사   '+self.owner.keys.describe('copy'), self.owner.copy_pages); copy.setEnabled(bool(self.selected))
        menu.addAction('오른쪽에 붙여넣기   '+self.owner.keys.describe('paste'), lambda: self.owner.paste_pages(uid))
        menu.exec(event.globalPos()); event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton and self.cancel_guard is not None:
            self.cancel_guard.cancel(); return
        if event.button() != Qt.MouseButton.LeftButton:
            return
        self.setFocus()
        point = event.position()
        uid = self.uid_at(point)
        self.press_pos, self.pressed_uid = point.toPoint(), uid
        self.defer_click = False
        self.toggle_on_release = None
        mods = event.modifiers()
        ids = [p.uid for p in self.owner.pages]
        if uid is None:
            if not (mods & Qt.KeyboardModifier.ControlModifier):
                self.selected.clear()
        elif mods & Qt.KeyboardModifier.ShiftModifier and self.anchor in ids:
            a,b = sorted((ids.index(self.anchor),ids.index(uid)))
            if not (mods & Qt.KeyboardModifier.ControlModifier):
                self.selected.clear()
            self.selected.update(ids[a:b+1])
        elif mods & Qt.KeyboardModifier.ControlModifier:
            if uid in self.selected:
                # Ctrl을 누른 채 선택 묶음을 잡아도 드래그 직전에 선택이 풀리지 않는다.
                self.toggle_on_release = uid
            else:
                self.selected.add(uid)
            self.anchor = uid
        elif uid in self.selected:
            self.defer_click = True
        else:
            self.selected = {uid}
            self.anchor = uid
        self.selectionChanged.emit()

    def mouseReleaseEvent(self, event):
        if self.toggle_on_release is not None:
            self.selected.discard(self.toggle_on_release)
            self.selectionChanged.emit()
        elif self.defer_click and self.pressed_uid:
            self.selected = {self.pressed_uid}
            self.anchor = self.pressed_uid
            self.selectionChanged.emit()
        self.press_pos = None
        self.defer_click = False
        self.toggle_on_release = None

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.press_pos is not None:
            if (event.position().toPoint()-self.press_pos).manhattanLength() >= QApplication.startDragDistance():
                self.press_pos = None
                self.defer_click = False
                self.toggle_on_release = None
                if self.pressed_uid in self.selected:
                    self.begin_drag()
            return
        uid = self.uid_at(event.position())
        page = self.owner.by_id.get(uid)
        if page:
            tip=(f'{Path(page.label_path).name}  ·  {page.document_pages:,}쪽\n더블클릭으로 PDF 전체 열기' if page.is_document_card
                 else f'{Path(page.label_path).name}  ·  {page.label_number+1}쪽')
            error=self.owner.thumb_errors.get((page.path,page.number))
            if error:tip+='\n'+error
            QToolTip.showText(event.globalPosition().toPoint(),tip,self)
        else:
            QToolTip.hideText()

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        self.press_pos = None
        self.defer_click = False
        self.toggle_on_release = None
        page = self.owner.by_id.get(self.uid_at(event.position()))
        if page is not None:
            event.accept()
            if page.is_document_card:self.owner.open_document_card(page)
            else:self.owner.open_preview(page)
        elif not self.owner.pages:
            self.owner.open_files()

    def begin_drag(self):
        pages = self.selected_pages()
        if not pages:
            return
        QToolTip.hideText()
        # 표준 파일 URL 드래그라 탐색기가 실제 파일 사본을 받는다.
        directory = TEMP_ROOT / uuid.uuid4().hex
        try:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            paths = export_pages(pages,directory,'PDF_사본_'+uuid.uuid4().hex[:10],self.owner.separate)
        except ExportCancelled:return
        except Exception as exc:
            QMessageBox.warning(self,'PDF 사본 생성 실패',str(exc))
            return
        finally:
            QApplication.restoreOverrideCursor()
        mime = QMimeData()
        mime.setData(MIME,json.dumps({'session':self.owner.session,'ids':[p.uid for p in pages]}).encode())
        mime.setUrls([QUrl.fromLocalFile(str(p)) for p in paths])
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.setPixmap(pdf_badge(total_page_count(pages)))
        drag.setHotSpot(QPoint(22,20))
        self.dragging = {p.uid for p in pages}
        self.internal_drop = False
        self.cancelled_drag = False
        first = next(i for i,p in enumerate(self.owner.pages) if p.uid in self.dragging)
        self.slot = sum(p.uid not in self.dragging for p in self.owner.pages[:first])
        self.layout_pages()
        self.cancel_guard = DragCancelGuard(self)
        self.cancel_guard.start()
        target = ExplorerTarget()
        monitor = QTimer(self)
        monitor.timeout.connect(target.sample)
        monitor.start(180)
        try:
            result = drag.exec(Qt.DropAction.CopyAction,Qt.DropAction.CopyAction)
            target.sample()
        finally:
            monitor.stop();monitor.deleteLater()
            self.cancel_guard.stop();self.cancel_guard.deleteLater();self.cancel_guard = None
        internal = self.internal_drop
        if not self.cancelled_drag and not internal and result == Qt.DropAction.CopyAction:
            self.owner.mark_exported(pages)
        self.dragging.clear(); self.slot = None; self.pointer = None
        self.layout_pages()
        self.pointer = None;self.external_hover = False
        if not self.cancelled_drag and not internal and result == Qt.DropAction.CopyAction and self.owner.rename_after:
            QTimer.singleShot(100,lambda: self.owner.rename_copies(paths,target,pages))
        elif internal or result == Qt.DropAction.IgnoreAction:
            for path in paths:
                path.unlink(missing_ok=True)
            try: directory.rmdir()
            except OSError: pass
        drag.deleteLater()

    def is_internal(self, mime):
        try:
            return json.loads(bytes(mime.data(MIME))).get('session') == self.owner.session
        except (ValueError,TypeError):
            return False

    def pdf_paths(self, mime):
        return [u.toLocalFile() for u in mime.urls() if u.isLocalFile() and supported_input(u.toLocalFile())]

    def insertion_at(self, pos):
        # 현재 미리보기 격자 -> 선택 묶음을 제외한 목록의 삽입 경계.
        # 묶음의 반투명 영역 위에서는 같은 경계를 유지해 흔들림을 막는다.
        y = pos.y()+self.verticalScrollBar().value()
        for point in self.gap_points:
            if QRectF(point.x()-5,point.y()-5,self.card_w+10,self.card_h+10).contains(QPointF(pos.x(),y)):
                return self.slot
        row = max(0,int((y-34)/(self.card_h+self.gap)))
        x = pos.x()-self.margin
        col = max(0,min(self.columns-1,int(x/(self.card_w+self.gap))))
        idx = row*self.columns+col
        if x-col*(self.card_w+self.gap) > self.card_w/2:
            idx += 1
        if self.slot is not None and idx > self.slot:
            idx = max(self.slot,idx-self.gap_count)
        remaining = sum(p.uid not in self.dragging for p in self.owner.pages)
        return max(0,min(idx,remaining))

    def dragEnterEvent(self, event):
        if self.owner.clear_pending or event.buttons() & Qt.MouseButton.RightButton:
            event.ignore();return
        if self.cancel_guard is not None and self.cancelled_drag:
            event.ignore();return
        if self.is_internal(event.mimeData()) or self.pdf_paths(event.mimeData()):
            if self.is_internal(event.mimeData()):
                data = json.loads(bytes(event.mimeData().data(MIME)))
                self.dragging = set(data['ids']) & set(self.owner.by_id)
            else:
                self.dragging.clear()
            if self.cancel_guard is None:
                self.cancelled_drag = False
            self.slot = self.insertion_at(event.position())
            self.layout_pages()
            event.setDropAction(Qt.DropAction.CopyAction);event.accept()
            self.external_hover = True
            self.viewport().update()

    def dragMoveEvent(self, event):
        if self.owner.clear_pending or self.cancelled_drag or event.buttons() & Qt.MouseButton.RightButton:
            if self.cancel_guard is not None:self.cancel_guard.cancel()
            event.ignore();return
        if not (self.is_internal(event.mimeData()) or self.pdf_paths(event.mimeData())):
            event.ignore();return
        event.setDropAction(Qt.DropAction.CopyAction);event.accept()
        self.pointer = event.position()+QPointF(0,self.verticalScrollBar().value())
        slot = self.insertion_at(event.position())
        if slot != self.slot:
            self.slot = slot
            self.layout_pages()

    def dragLeaveEvent(self, event):
        self.pointer = None;self.slot = None;self.external_hover = False
        self.layout_pages();event.accept()

    def dropEvent(self, event):
        if self.owner.clear_pending or self.cancelled_drag or event.buttons() & Qt.MouseButton.RightButton:
            if self.cancel_guard is not None:self.cancel_guard.cancel()
            event.ignore();return
        slot = self.slot if self.slot is not None else self.insertion_at(event.position())
        if self.is_internal(event.mimeData()):
            data = json.loads(bytes(event.mimeData().data(MIME)))
            moved = [p for p in self.owner.pages if p.uid in set(data['ids'])]
            for page, point in zip(moved,self.gap_points):
                self.positions[page.uid] = QPointF(point)
                self.velocities[page.uid] = QPointF(0,0)
            self.slot = None;self.dragging.clear()
            self.owner.reorder(data['ids'],slot)
            self.internal_drop = True
        else:
            paths = self.pdf_paths(event.mimeData())
            if not paths:
                event.ignore();return
            self.owner.add_files(paths,slot)
            QTimer.singleShot(0,self.owner.focus_after_file_drop)
        self.slot = None;self.pointer = None;self.external_hover = False
        self.layout_pages()
        event.setDropAction(Qt.DropAction.CopyAction);event.accept()

    def keyPressEvent(self, event):
        if self.owner.handle_file_key(event):return
        if event.key() == Qt.Key.Key_Escape:
            self.selected.clear();self.selectionChanged.emit()
        else:
            super().keyPressEvent(event)


def hangul_saved_options(settings,mode='unified'):
    defaults=HANGUL_DEFAULTS['unified'];values={}
    typography={'body_size','table_size','body_ratio','letter_spacing','line_spacing','paragraph_gap',
                'join','gap_weight','indent_weight','font_weight','space_gap','join_words'}
    for key,default in defaults.items():
        fallback=settings.value(f'hangul/v290/editable/{key}',default,type=type(default)) if key in typography else default
        values[key]=settings.value(f'hangul/v300/{key}',fallback,type=type(default))
    return hangul_options('unified',values)


def hangul_saved_font(settings):
    fallback=settings.value('hangul/v291/editable/font',settings.value('hangul/font','함초롬바탕',type=str),type=str)
    return settings.value('hangul/v300/font',fallback,type=str)


class HangulModeSettings(QWidget):
    def __init__(self,owner,mode='unified'):
        super().__init__();self.owner=owner;self.controls={};self.mode='unified'
        layout=QVBoxLayout(self);layout.setContentsMargins(4,4,4,4)
        note=QLabel('본문은 문단으로 편집하고, 머리말·표·쪽 테두리는 양식으로 보존합니다.');note.setWordWrap(True);layout.addWidget(note)
        self.tabs=QTabWidget();layout.addWidget(self.tabs);values=hangul_saved_options(owner.settings)
        def pane(label):
            widget=QWidget();inner=QVBoxLayout(widget);inner.setContentsMargins(12,12,12,12)
            scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setWidget(widget);self.tabs.addTab(scroll,label)
            return inner
        form_page=pane('양식·쪽')
        for key,title in [('keep_pages','원본 쪽 나눔 유지'),('keep_headers','머리말·꼬리말 보존'),
            ('keep_page_borders','쪽 테두리 보존'),('keep_title_frames','제목 테두리를 편집 가능한 표로 복원'),
            ('keep_margins','원본 여백과 표지 배치 반영'),('fit_spacing','쪽 넘침 예상 시 문서 전체 간격 조정'),
            ('write_report','변환 파일 옆에 검사표 저장')]:
            check=QCheckBox(title);check.setChecked(values[key]);self.controls[key]=check;form_page.addWidget(check)
            check.toggled.connect(lambda value,k=key:self.persist(k,value))
        hint=QLabel('쪽 나눔을 끄면 본문이 연속으로 흐릅니다. 자동 조정은 문서 전체의 줄·문단 간격에 동일하게 적용되며, 페이지마다 글자 크기를 바꾸지 않습니다.')
        hint.setWordWrap(True);hint.setStyleSheet('color:#777;font-size:11px');form_page.addWidget(hint);form_page.addStretch()
        type_page=pane('본문 서식');form=QFormLayout();type_page.addLayout(form)
        self.font=QLineEdit(hangul_saved_font(owner.settings));self.font.textChanged.connect(lambda v:owner.settings.setValue('hangul/v300/font',v.strip() or '함초롬바탕'))
        form.addRow('문서 글꼴',self.font)
        for key,title,lo,hi,suffix in [('body_size','본문',8,24,' pt'),('table_size','표 글자',8,24,' pt'),
            ('header_size','머리말·꼬리말',8,16,' pt'),('body_ratio','장평',80,120,' %'),
            ('letter_spacing','자간',-10,20,' %'),('line_spacing','줄 간격',100,220,' %'),('paragraph_gap','문단 뒤 간격',0,20,' pt')]:
            spin=QSpinBox();spin.setRange(lo,hi);spin.setSuffix(suffix);spin.setValue(values[key]);self.controls[key]=spin
            spin.valueChanged.connect(lambda value,k=key:self.persist(k,value));form.addRow(title,spin)
        hint=QLabel('문단을 합친 뒤 전체 서식을 통일합니다. 제목의 크기·굵기는 단계별로 구분합니다.');hint.setWordWrap(True);type_page.addWidget(hint);type_page.addStretch()
        analysis=pane('분석');form=QFormLayout();analysis.addLayout(form)
        for key,title in [('join','문단 연결 강도'),('gap_weight','줄 간격 판단 비중'),('indent_weight','들여쓰기 판단 비중'),('font_weight','원본 글꼴·크기 판단 비중'),('space_gap','단어 공백 기준')]:
            row=QWidget();hl=QHBoxLayout(row);hl.setContentsMargins(0,0,0,0);slider=QSlider(Qt.Orientation.Horizontal)
            slider.setRange(5 if key=='space_gap' else 0,45 if key=='space_gap' else 100);slider.setValue(values[key])
            number=QLabel(str(values[key]));number.setFixedWidth(30);hl.addWidget(slider);hl.addWidget(number);form.addRow(title,row);self.controls[key]=slider
            slider.valueChanged.connect(lambda value,k=key,n=number:(n.setText(str(value)),self.persist(k,value)))
        for key,title in [('soft_breaks','문단 안에서 원본 줄바꿈 유지'),('cross_page','쪽 경계에서 이어지는 문단 연결'),('join_words','줄 끝에서 끊긴 낱말 이어붙이기')]:
            check=QCheckBox(title);check.setChecked(values[key]);self.controls[key]=check;analysis.addWidget(check)
            check.toggled.connect(lambda value,k=key:self.persist(k,value))
        analysis.addStretch();self.controls['keep_pages'].toggled.connect(self.update_cross);self.update_cross()
        reset=QPushButton('변환 기본값 복원');reset.clicked.connect(self.reset);layout.addWidget(reset)

    def persist(self,key,value):self.owner.settings.setValue(f'hangul/v300/{key}',value)
    def update_cross(self):self.controls['cross_page'].setEnabled(not self.controls['keep_pages'].isChecked())
    def reset(self):
        self.font.setText('함초롬바탕')
        for key,value in HANGUL_DEFAULTS['unified'].items():
            c=self.controls.get(key)
            if c is None:continue
            if isinstance(c,QCheckBox):c.setChecked(value)
            else:c.setValue(value)


class HangulSettings(QWidget):
    def __init__(self,owner,dialog):
        super().__init__();layout=QVBoxLayout(self);form=QFormLayout();layout.addLayout(form)
        self.format=QComboBox();self.format.addItems(['HWPX (.hwpx)','HWP (.hwp)']);self.format.setCurrentIndex(int(owner.settings.value('hangul/format',0)))
        self.dpi=QComboBox();self.dpi.addItems(['200','300','450','600']);self.dpi.setCurrentText(str(owner.settings.value('hangul/dpi','300')))
        self.format.currentIndexChanged.connect(lambda v:owner.settings.setValue('hangul/format',v));self.dpi.currentTextChanged.connect(lambda v:owner.settings.setValue('hangul/dpi',v))
        form.addRow('저장 형식',self.format);form.addRow('부분 그림 해상도',self.dpi)
        self.editor=HangulModeSettings(owner);layout.addWidget(self.editor)
        hint=QLabel('문자·서식 검사는 변환 후 표시됩니다. 예상 높이와 실제 한컴 배치는 차이가 있을 수 있습니다.');hint.setWordWrap(True);hint.setStyleSheet('color:#777;font-size:11px');layout.addWidget(hint)
        row=QHBoxLayout();layout.addLayout(row);run=QPushButton('한글로 변환');run.setIcon(corner_icon('hangul'));run.setEnabled(bool(owner.pages))
        run.clicked.connect(lambda:(dialog.accept(),QTimer.singleShot(0,owner.choose_hangul)));row.addWidget(run)
        recent=QPushButton('진행 / 최근 검사');recent.clicked.connect(owner.show_hangul_status);row.addWidget(recent)
        check=QPushButton('모듈 확인');check.setObjectName('hangul_module_check')
        check.clicked.connect(lambda _checked=False:owner.check_hangul_module(dialog));row.addWidget(check)


class HangulChoiceDialog(QDialog):
    def __init__(self,owner,parent=None):
        super().__init__(parent or owner);self.owner=owner;self.chosen=None;self.setWindowTitle('한글 통합 변환');self.setWindowIcon(corner_icon('hangul'));self.resize(430,300)
        layout=QVBoxLayout(self);title=QLabel('편집 가능한 문단 + 원본 양식');title.setStyleSheet('font-size:16px;font-weight:600');layout.addWidget(title)
        note=QLabel('본문은 문단으로 연결하고 머리말·제목 틀·쪽 테두리를 복원합니다. 변환 후 쪽별 검사 결과를 표시합니다.');note.setWordWrap(True);layout.addWidget(note)
        form=QFormLayout();layout.addLayout(form);self.format=QComboBox();self.format.addItems(['HWPX (.hwpx)','HWP (.hwp)']);self.format.setCurrentIndex(int(owner.settings.value('hangul/format',0)))
        self.scope=QComboBox();self.scope.addItems(['현재 전체 페이지','선택한 페이지만']);form.addRow('저장 형식',self.format);form.addRow('변환 범위',self.scope)
        self.keep_pages=QCheckBox('원본 쪽 나눔 유지');self.keep_pages.setChecked(hangul_saved_options(owner.settings)['keep_pages']);layout.addWidget(self.keep_pages)
        run=QPushButton('한글로 변환');run.setIcon(corner_icon('hangul'));run.setMinimumHeight(48)
        run.setStyleSheet('QPushButton{background:#293d62;color:white;border:1px solid #6986b8;border-radius:9px;font-size:14px;padding:8px}QPushButton:hover{background:#3b5480}')
        run.clicked.connect(self.choose);layout.addWidget(run);self.run_button=run;self.mode_buttons={'unified':run}
        row=QHBoxLayout();layout.addLayout(row);settings=QPushButton('변환 설정');settings.clicked.connect(self.open_settings);row.addWidget(settings)
        cancel=QPushButton('취소');cancel.clicked.connect(self.reject);row.addWidget(cancel)
    def choose(self,checked=False):
        settings=self.owner.settings;settings.setValue('hangul/format',self.format.currentIndex());settings.setValue('hangul/v300/keep_pages',self.keep_pages.isChecked())
        self.chosen=dict(mode='unified',format='hwpx' if self.format.currentIndex()==0 else 'hwp',selected=self.scope.currentIndex()==1,
                         dpi=int(settings.value('hangul/dpi',300)),font=hangul_saved_font(settings),options=hangul_saved_options(settings))
        self.accept()
    def open_settings(self):self.reject();QTimer.singleShot(0,lambda:self.owner.show_settings(tab='hangul'))


class HangulExportDialog(QDialog):
    """Keeps conversion in a child process; closing the panel only hides it."""
    def __init__(self, owner, job):
        super().__init__(owner);self.owner=owner;self.busy=True;self.conversion_result=None;self.error=''
        self.buffer=b'';self.errors=b'';self.ended=False
        self.setWindowTitle('한글 통합 변환 · 검사');self.resize(820,520)
        layout=QVBoxLayout(self);self.label=QLabel('한글 변환 준비 중');layout.addWidget(self.label)
        self.bar=QProgressBar();self.bar.setRange(0,len(job['pages']));layout.addWidget(self.bar)
        self.tabs=QTabWidget();layout.addWidget(self.tabs)
        self.checks=QTableWidget(0,7);self.checks.setHorizontalHeaderLabels(['원본 쪽','문단','문자·순서','본문 서식','보존 양식','높이 추정','확인 사항'])
        self.checks.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents);self.checks.horizontalHeader().setStretchLastSection(True)
        self.checks.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers);self.tabs.addTab(self.checks,'쪽별 검사')
        self.log=QPlainTextEdit();self.log.setReadOnly(True);self.tabs.addTab(self.log,'진행 기록');self.tabs.setCurrentIndex(1)
        mode='통합 · 편집 가능한 문단 + 원본 양식'
        self.log.setPlainText(f'{len(job["pages"])}쪽 · {mode}\n저장 예정: {job["output"]}')
        row=QHBoxLayout();layout.addLayout(row)
        self.open_button=QPushButton('한글 파일 열기');self.open_button.setEnabled(False)
        self.open_button.clicked.connect(self.open_result);row.addWidget(self.open_button)
        self.report_button=QPushButton('검사표 열기');self.report_button.setEnabled(False);self.report_button.clicked.connect(self.open_report);row.addWidget(self.report_button)
        close=QPushButton('닫기');close.clicked.connect(self.hide);row.addWidget(close)
        work=TEMP_ROOT/owner.session/'hangul'/uuid.uuid4().hex;work.mkdir(parents=True,exist_ok=True)
        self.job_path=work/'job.json';self.job_path.write_text(json.dumps(job,ensure_ascii=False),encoding='utf-8')
        self.process=QProcess(self);self.process.setProcessChannelMode(QProcess.ProcessChannelMode.SeparateChannels)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_errors)
        self.process.finished.connect(self.on_process_finished)
        self.process.errorOccurred.connect(self.process_error)
        executable,args=worker_launch();args=args[:-1]+['--hangul-worker',str(self.job_path)]
        self.process.start(executable,args)

    def read_output(self):
        self.buffer+=bytes(self.process.readAllStandardOutput())
        while b'\n' in self.buffer:
            line,self.buffer=self.buffer.split(b'\n',1)
            try:data=json.loads(line)
            except (ValueError,UnicodeDecodeError):continue
            if 'result' in data:self.conversion_result=data['result']
            elif 'error' in data:self.error=data['error']
            else:
                self.label.setText(data.get('message','변환 중'))
                self.bar.setValue(data.get('progress',0))

    def read_errors(self):
        self.errors=(self.errors+bytes(self.process.readAllStandardError()))[-6000:]

    def process_error(self, error):
        if error==QProcess.ProcessError.FailedToStart:
            self.error=self.process.errorString();self.on_process_finished(-1)

    def on_process_finished(self, code, status=None):
        if self.ended:return
        self.ended=True;self.read_output();self.read_errors();self.busy=False
        if self.conversion_result:
            self.bar.setValue(self.bar.maximum());self.label.setText('한글 파일 저장 완료')
            self.log.appendPlainText('\n저장 완료: '+self.conversion_result['output'])
            r=self.conversion_result
            self.log.appendPlainText(f'머리말 포함 문단 {r["paragraphs"]:,}개 · 본문 표 {r["tables"]}개 · 부분 그림 {r["figures"]}개')
            self.log.appendPlainText(f'이어 붙인 줄 {r["joined_lines"]:,}개 · 낱말 연결 {r["word_joins"]}개 · 앞뒤 쪽 문단 연결 {r["cross_page_joins"]}개')
            n=r['normalization']
            self.log.appendPlainText(f'전체 서식 통일: 본문 {n["body_size"]}pt · 장평 {n["body_ratio"]}% · 자간 {n["letter_spacing"]}% · 줄 간격 {n["line_spacing"]}%')
            self.log.appendPlainText(f'본문 글상자 0개 · 머리말 표 {r["header_tables"]}개 · 제목 틀 {r["title_tables"]}개 · 쪽 테두리 {r["page_borders"]}개')
            if r.get('spacing_adjustment'):self.log.appendPlainText(r['spacing_adjustment'])
            from PySide6.QtWidgets import QTableWidgetItem
            self.checks.setRowCount(len(r['page_checks']))
            for i,p in enumerate(r['page_checks']):
                values=[f'{p["index"]} ({p["source_page"]}쪽)',str(p['paragraphs']),'통과' if p['content_ok'] else '실패',
                    '통과' if p['style_ok'] else '실패',f'머리말 {p["headers"]} / 제목 {p["title_frames"]} / 테두리 {p["page_borders"]}',
                    f'{p["estimated_height_pt"]:.0f} / {p["available_height_pt"]:.0f} pt',' · '.join(p['warnings']) or '실제 화면 확인 전']
                for j,value in enumerate(values):
                    item=QTableWidgetItem(value);item.setToolTip(p['source'])
                    if p['warnings']:item.setBackground(QColor('#6b4b23'));item.setForeground(QColor('#ffffff'))
                    self.checks.setItem(i,j,item)
            self.tabs.setCurrentIndex(0)
            review=sum(bool(p['warnings']) for p in r['page_checks'])
            self.label.setText(f'저장 완료 · 문자/순서 {len(r["page_checks"])}/{r["pages"]} · 서식 통과 · 별도 검토 {review}쪽')
            self.report_button.setEnabled(bool(r.get('report')))
            for warning in r['warnings']:self.log.appendPlainText(warning)
            self.log.appendPlainText('한컴오피스에서 열어 글꼴과 배치를 확인하세요.')
            self.open_button.setEnabled(True)
        else:
            self.label.setText('한글 변환 실패')
            self.log.appendPlainText('\n'+(self.error or self.errors.decode('utf-8',errors='replace') or f'변환 프로세스 종료: {code}'))
        try:self.job_path.unlink(missing_ok=True);self.job_path.parent.rmdir()
        except OSError:pass

    def open_report(self):
        if self.conversion_result and self.conversion_result.get('report'):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.conversion_result['report']))

    def open_result(self):
        if self.conversion_result:QDesktopServices.openUrl(QUrl.fromLocalFile(self.conversion_result['output']))


class ImageExportDialog(QDialog):
    """Keep the final filename absent until a complete PDF is ready to publish."""
    def __init__(self,parent,target,pages=(),inputs=()):
        super().__init__(parent);self.setWindowTitle('JPG to PDF');self.resize(470,160)
        self.target=Path(target);self.stage=self.target.parent/('.pdfmagnet-'+uuid.uuid4().hex+'.tmp.pdf')
        self.result_path=None;self.error='';self.buffer=b'';self.ready=False;self.busy=False;self.cancelled=False;self.ended=False;self.owns_stage=False
        layout=QVBoxLayout(self);self.label=QLabel('변환 준비 중');layout.addWidget(self.label)
        self.bar=QProgressBar();self.bar.setRange(0,0);layout.addWidget(self.bar)
        self.cancel_button=QPushButton('취소');self.cancel_button.clicked.connect(self.reject);layout.addWidget(self.cancel_button)
        self.proc=QProcess(self);self.proc.readyReadStandardOutput.connect(self.read_output)
        self.proc.readyReadStandardError.connect(lambda:self.proc.readAllStandardError())
        self.proc.finished.connect(self.on_process_finished);self.proc.errorOccurred.connect(self.failed)
        self.job={'stage':str(self.stage),'pages':[(p.path,p.number) for p in pages],'inputs':list(inputs)}
        self.proc.started.connect(lambda:self.proc.write((json.dumps(self.job,ensure_ascii=True)+'\n').encode('ascii')))
        QTimer.singleShot(0,self.start)

    def start(self):
        if self.cancelled:return
        try:
            if self.target.exists():raise FileExistsError('같은 이름의 파일이 있습니다. 다른 이름으로 저장하세요.')
            with self.stage.open('xb'):pass
            self.owns_stage=True
            self.busy=True;program,args=worker_launch('--image-export-worker');self.proc.start(program,args)
        except Exception as exc:self.error=str(exc);self.on_process_finished()

    def read_output(self):
        self.buffer+=bytes(self.proc.readAllStandardOutput())
        while b'\n' in self.buffer:
            line,self.buffer=self.buffer.split(b'\n',1)
            try:data=json.loads(line)
            except ValueError:continue
            if 'catalog' in data:
                catalog=data['catalog'];self.label.setText(f'목록 확인 · {catalog.get("done",catalog.get("found",0)):,}개')
            elif 'total' in data:
                done,total=data['done'],max(1,data['total']);self.bar.setRange(0,total);self.bar.setValue(done)
                self.label.setText(f'{int(done*100/total)}% · {done:,}/{total:,}쪽'+(' · PDF 기록 중' if data['phase']=='write' else ' 변환'))
            if data.get('ready'):self.ready=True
            if data.get('error'):self.error=data['error']

    def failed(self,_error):
        if self.proc.state()==QProcess.ProcessState.NotRunning:
            if not self.cancelled:self.error=self.error or 'PDF 변환 프로세스를 실행하지 못했습니다.'
            self.on_process_finished()

    def on_process_finished(self,code=0,_status=None):
        if self.ended:return
        self.ended=True
        if self.proc.isOpen():self.read_output()
        self.busy=False
        try:
            if self.ready and not self.cancelled and code==0 and not self.error:
                if sys.platform=='win32':os.rename(self.stage,self.target)
                else:os.link(self.stage,self.target)
                self.result_path=str(self.target)
            elif not self.cancelled and not self.error:self.error='변환 프로세스가 중단되었습니다.'
        except Exception as exc:self.error=str(exc)
        finally:
            try:
                if self.owns_stage:self.stage.unlink(missing_ok=True)
            except OSError:pass
        if self.result_path:self.accept()
        else:super().reject()

    def reject(self):
        self.cancelled=True
        if self.busy:
            self.cancel_button.setEnabled(False);self.label.setText('변환 중단 중…')
            if self.proc.state()==QProcess.ProcessState.NotRunning:self.on_process_finished(self.proc.exitCode())
            else:self.proc.kill()
        else:super().reject()

    def closeEvent(self,event):
        if self.busy:self.reject();event.ignore()
        else:super().closeEvent(event)


class ImportProgress(QWidget):
    cancelled=Signal()

    def __init__(self,parent):
        super().__init__(parent)
        self.setObjectName('import_progress')
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True)
        self.setStyleSheet('QWidget#import_progress{background:#232734;border:1px solid #714052;border-radius:10px;}'
            'QLabel{color:#f1eef2;background:transparent;border:0;font-size:12px;}'
            'QPushButton{color:#fff;background:#8f2942;border:0;border-radius:5px;padding:6px 13px;}'
            'QPushButton:hover{background:#bd3553;} QPushButton:disabled{color:#b3a8ae;background:#50333f;}'
            'QProgressBar{background:#3e3541;border:0;border-radius:3px;height:6px;}'
            'QProgressBar::chunk{background:#f14665;border-radius:3px;}')
        layout=QVBoxLayout(self);layout.setContentsMargins(14,9,12,10);layout.setSpacing(5)
        row=QHBoxLayout();self.title=QLabel();self.title.setMinimumWidth(0)
        self.cancel=QPushButton('취소');self.cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel.clicked.connect(self.cancelled);row.addWidget(self.title,1);row.addWidget(self.cancel)
        layout.addLayout(row);self.detail=QLabel();layout.addWidget(self.detail)
        self.bar=QProgressBar();self.bar.setTextVisible(False);self.bar.setFixedHeight(6);layout.addWidget(self.bar)
        self.hide_timer=QTimer(self);self.hide_timer.setSingleShot(True);self.hide_timer.timeout.connect(self.hide)
        self.label='';self.data={};self.hide()

    def place(self):
        parent=self.parentWidget();width=max(160,min(640,parent.width()-24))
        self.setGeometry(max(0,(parent.width()-width)//2),max(0,parent.height()-139),width,97)
        self.title.setText(self.title.fontMetrics().elidedText(self.label,Qt.TextElideMode.ElideMiddle,max(60,width-105)))
        self.raise_()

    def hideEvent(self,event):
        super().hideEvent(event)
        editor=getattr(self.window(),'preview_dialog',None)
        if editor is not None and not editor.closed:editor.position_controls()

    def begin(self,path,index,total):
        self.hide_timer.stop();self.cancel.show();self.cancel.setEnabled(True)
        self.label=f'{Path(path).name}'+(f' · 입력 {index}/{total}' if total>1 else '')
        self.setToolTip(str(path));self.update_progress({'phase':'scan','found':0},0)
        self.show();self.place()

    def update_progress(self,data,pages,unit='쪽'):
        self.data=dict(data)
        if data.get('phase')=='scan':
            self.bar.setRange(0,0);self.detail.setText(f'목록 확인 중 · {data.get("found",0):,}개 발견')
        else:
            total=max(0,int(data.get('total',0)));done=max(0,int(data.get('done',0)))
            percent=min(100,max(0,100*(done+data.get('fraction',0))/total)) if total else 0
            self.bar.setRange(0,1000);self.bar.setValue(int(percent*10))
            action='목록' if data.get('phase')=='catalog' else '처리'
            detail=f'{int(percent)}%  ·  {action} {done:,}/{total:,}파일  ·  {pages:,}{unit}'
            if data.get('frames',0)>1:detail+=f'  ·  TIFF {data["frame"]}/{data["frames"]}쪽'
            if data.get('errors'):detail+=f'  ·  오류 {data["errors"]}'
            self.detail.setText(detail)
        if data.get('name'):self.setToolTip(data['name'])

    def stopping(self):
        self.cancel.setEnabled(False);self.detail.setText('읽기 중단 중 · 임시파일 확인')

    def finish(self,pages,cancelled=False,errors=0,unit='쪽'):
        self.cancel.hide();self.bar.setRange(0,1000)
        if not cancelled and not errors:self.bar.setValue(1000)
        self.detail.setText((f'읽기 취소 · {pages:,}{unit} 유지' if cancelled else
                            (f'목록 확인 종료 · {pages:,}{unit}' if errors else f'100% · 목록 확인 완료 · {pages:,}{unit}'))+
                            (f' · 오류 {errors:,}개' if errors else ''))
        self.hide_timer.start(4500)


class Window(QMainWindow):
    translationChanged=Signal()

    def __init__(self, startup_pdf_count=0):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(application_icon())
        self.resize(1280,850)
        self.single_file_layout=False
        fit_document_window(self,False)
        self.settings = QSettings('KRS','PDFMagnet')
        self.keys=ShortcutBindings(self,self.settings)
        self.card_size = int(self.settings.value('size',180))
        self.repulsion = int(self.settings.value('repulsion',27))
        self.animate = self.settings.value('animate',True,type=bool)
        self.dark = self.settings.value('dark',True,type=bool)
        self.separate = self.settings.value('separate',False,type=bool)
        self.rename_after = self.settings.value('rename',True,type=bool)
        self.show_numbers = self.settings.value('numbers',False,type=bool)
        self.auto_preview = True
        self.image_engine=self.settings.value('image_engine','auto',type=str)
        if self.image_engine not in ('auto','qt','vips','pillow'):self.image_engine='auto'
        self.auto_preview_opened = False
        self.session = uuid.uuid4().hex
        self.pages = []
        self.browse_path=None;self.browse_containers=False;self.closing=False
        self.browse_books=None
        self.original_path=None
        self.revision_directory=None
        self.last_saved_path=None
        self.last_save_error=''
        self.last_save_error_path=None
        self.deepl_api_key=load_deepl_key(self.settings)
        self.translation_directory=self.settings.value('deepl/directory','',type=str)
        self.deepl_usage_text='API 사용량: 연결 확인 전'
        self.usage_thread=None
        self.translation_thread=None
        self.translation_busy=False
        self.translation_job=None
        self.translation_status='번역 대기'
        self.translation_log=[]
        self.translation_dialog=None
        self.translation_windows=[]
        self.translation_waiting=False
        self.hangul_dialog=None
        self.hangul_waiting=False
        self.by_id = {}
        self.thumbs = OrderedDict()
        self.thumb_errors = {}
        self.requested = set()
        self.large_thumbs_requested=set()
        self.history = []
        self.future = []
        self.exported_revisions = set()
        self.clean_page_orders = {()}
        self.pristine_pages = set()
        self.clear_pending = False
        self.replacement_paths=None
        self.replacement_navigation_mode=None
        self.replacement_books=None
        self.navigation_token=0;self.navigation_request=None
        self.neighbor_serial=0;self.neighbor_request=None;self.neighbor_key=None
        self.neighbor_ready=False;self.neighbor_paths={};self.neighbor_error=''
        self.clear_timer = QTimer(self);self.clear_timer.setSingleShot(True);self.clear_timer.setInterval(120)
        self.clear_timer.timeout.connect(self.continue_clear)
        self.clipboard_pages = []
        self.clipboard_token = ''
        self.preview_dialog = None
        self.imports = []
        self.pending_import = None
        self.import_token = 0
        self.import_cancelling=False;self.cancelled_directory=None;self.close_after_import=False
        self.import_directory=None;self.cleanup_failures=[];self.last_import_errors=0
        self.backend = PdfBackend(self,lazy=True)
        self.backend.metadata.connect(self.got_metadata)
        self.backend.thumbnail.connect(self.got_thumbnail)
        self.backend.released.connect(self.cleanup_working_files)
        self.navigation_backend=PdfBackend(self,lazy=True)
        self.navigation_backend.siblingReady.connect(self.got_sibling)
        self.navigation_backend.neighborsReady.connect(self.got_neighbor_names)
        self.image_backend=ImageBackend(self);self.image_backend.thumbnail.connect(self.got_thumbnail)
        self.preview_image_backend=ImageBackend(self);self.preview_request_serial=0
        self.input_backend=InputBackend(self)
        self.input_backend.itemReady.connect(self.got_input_item)
        self.input_backend.completed.connect(self.got_input_done)
        self.input_backend.progress.connect(self.got_input_progress)
        self.input_backend.cancelled.connect(self.import_cancelled)
        self.canvas = PageCanvas(self)
        self.canvas.setMinimumWidth(200);self.canvas.setEnabled(False)
        self.canvas.setToolTip('파일 드롭: 이 위치에 추가 · 드래그: 페이지 순서 변경 · 단축키 변경: 정 → 단축키')
        self.empty_preview=EmptyPreview(self)
        self.thumbnails_collapsed=False
        self.preview_split_sizes=[int(self.width()*.65),int(self.width()*.35)]
        self.content=QWidget(self)
        content_layout=QHBoxLayout(self.content);content_layout.setContentsMargins(0,0,0,0);content_layout.setSpacing(0)
        self.splitter=QSplitter(Qt.Orientation.Horizontal,self.content)
        self.splitter.setChildrenCollapsible(False);self.splitter.setHandleWidth(5)
        self.splitter.setStyleSheet('QSplitter::handle{background:#363d4f;} QSplitter::handle:hover{background:#dc425e;}')
        self.splitter.addWidget(self.empty_preview);self.splitter.addWidget(self.canvas)
        self.splitter.setSizes(self.preview_split_sizes)
        content_layout.addWidget(self.splitter)
        self.thumbnail_rail=ThumbnailRail(self,self.content);content_layout.addWidget(self.thumbnail_rail)
        self.setCentralWidget(self.content)
        self.canvas.selectionChanged.connect(self.follow_thumbnail_selection)
        self.setAcceptDrops(True)
        self.actions=CornerActions(self.content,self,self.save_revision,self.translate_current,self.choose_hangul,self.show_settings,self.clear,
                                   right_inset=self.thumbnail_rail.width())
        self.import_progress=ImportProgress(self.content);self.import_progress.cancelled.connect(self.cancel_import)
        self.clear_button=self.actions.clear_button;self.clear_button.setEnabled(False)
        self.save_button=self.actions.save_button;self.options_button=self.actions.options_button
        self.translate_button=self.actions.translate_button;self.translate_button.setEnabled(False)
        self.hangul_button=self.actions.hangul_button;self.hangul_button.setEnabled(False)
        self.save_button.setEnabled(False)
        QApplication.instance().installEventFilter(self.keys)
        self.place_actions()

    def place_actions(self):
        if hasattr(self,'actions'):self.actions.place()
        if hasattr(self,'import_progress'):self.import_progress.place()

    def resizeEvent(self,event):
        super().resizeEvent(event)
        # 접힌 썸네일에는 resizeEvent가 오지 않으므로 주 창에서도 위치를 갱신한다.
        self.place_actions()

    def remember_preview_split(self):
        sizes=self.splitter.sizes()
        if not self.thumbnails_collapsed and len(sizes)==2 and all(sizes):
            self.preview_split_sizes=sizes

    def focus_content(self):
        if not self.thumbnails_collapsed and self.canvas.isEnabled():self.canvas.setFocus();return
        editor=self.preview_dialog
        if editor is not None and not editor.closed:editor.view.setFocus()
        else:self.empty_preview.setFocus()

    def focus_after_file_drop(self):
        # Windows 외부 드롭은 창을 활성화하지 않을 수 있다. setFocus만으로는
        # 탐색기에 남은 키 입력을 가져오지 못하므로 드롭 처리가 끝난 직후 한 번 활성화한다.
        # 읽기/렌더링 완료 시에는 호출하지 않아, 사용자가 옮겨 간 다른 창을 방해하지 않는다.
        if self.closing or not self.isVisible():return
        if QApplication.activeModalWidget() is not None or QApplication.activePopupWidget() is not None:return
        self.activateWindow();self.focus_content()

    def toggle_thumbnail_panel(self):
        # 위젯을 그대로 숨긴다. 페이지/선택/편집기/실행 취소 기록은 건드리지 않는다.
        focus=QApplication.focusWidget()
        canvas_had_focus=focus is self.canvas or (focus is not None and self.canvas.isAncestorOf(focus))
        scroll=self.canvas.verticalScrollBar().value()
        if self.thumbnails_collapsed:
            self.thumbnails_collapsed=False
            self.canvas.show();self.splitter.setSizes(self.preview_split_sizes)
            self.canvas.layout_pages();self.canvas.verticalScrollBar().setValue(scroll)
        else:
            self.remember_preview_split();self.thumbnails_collapsed=True
            self.canvas.hide()
            if canvas_had_focus:self.focus_content()
        self.thumbnail_rail.sync();self.place_actions();self.prioritize_thumbnails()

    def update_action_states(self):
        if hasattr(self,'canvas'):self.canvas.setEnabled(bool(self.pages) and not self.clear_pending)
        if hasattr(self,'save_button'):
            loading=bool(self.pending_import or self.imports or self.import_cancelling)
            can_clear=bool(self.pages or self.history or loading) and not self.clear_pending
            self.clear_button.setEnabled(can_clear)
            self.save_button.setEnabled(bool(self.pages) and not loading)
            tip='전체 PDF 저장 · '+self.keys.describe('save')
            if self.last_saved_path:
                tip+=f'\n최근 저장 완료:\n{self.last_saved_path}'
            self.save_button.setToolTip(tip)
            editor=self.preview_dialog
            if editor is not None and not editor.closed:
                editor.actions.clear_button.setEnabled(can_clear)
                editor.actions.save_button.setEnabled(bool(self.pages) and not loading)
                editor.actions.save_button.setToolTip(tip)
            enabled=bool(self.pages) and not loading
            translation_tip=self.translation_status if self.translation_busy else '현재 전체 PDF 번역 · '+self.keys.describe('translate')
            self.hangul_button.setEnabled(enabled)
            if editor is not None and not editor.closed:editor.actions.hangul_button.setEnabled(enabled)
            self.translate_button.setEnabled(enabled or self.translation_busy)
            self.translate_button.setToolTip(translation_tip)
            if editor is not None and not editor.closed:
                editor.actions.translate_button.setEnabled(enabled or self.translation_busy)
                editor.actions.translate_button.setToolTip(translation_tip)
                editor.end_overlay.sync()

    def snapshot(self):
        self.history.append(PageState(self.pages,self.original_path))
        self.history = self.history[-30:]
        self.future.clear()

    def refresh(self):
        self.update_action_states()
        self.canvas.setEnabled(bool(self.pages) and not self.clear_pending)
        self.by_id = {p.uid:p for p in self.pages}
        self.canvas.selected.intersection_update(self.by_id)
        self.canvas.positions = {k:v for k,v in self.canvas.positions.items() if k in self.by_id}
        self.canvas.velocities = {k:v for k,v in self.canvas.velocities.items() if k in self.by_id}
        self.canvas.layout_pages()
        self.prioritize_thumbnails()
        if self.preview_dialog is not None and not self.preview_dialog.closed:
            page = self.by_id.get(self.preview_dialog.page.uid)
            if page is None and self.preview_dialog.embedded and self.pages:
                page=self.pages[min(self.preview_dialog.nav_display_index,len(self.pages)-1)]
            if page is None:
                self.preview_dialog.close()
            else:
                self.preview_dialog.sync_page(page)
                self.preview_dialog.update_navigation()
        if self.pages and (self.preview_dialog is None or self.preview_dialog.closed):
            QTimer.singleShot(0,self.open_combined_view)
        if not self.pages:
            self.restore_empty_preview()
            self.setWindowTitle(APP_NAME+(f' · {Path(self.browse_path).name}' if self.browse_path else ''))

    def replace_page(self, old, path):
        if old.is_document_card:
            raise ValueError('PDF 대표 카드는 전체 문서를 연 뒤 편집하세요.')
        self.snapshot()
        self.pages = [PageRef(path, 0, p.uid, p.label_path, p.label_number,p.input_path) if p.uid == old.uid else p
                      for p in self.pages]
        self.refresh()

    def after_selection(self, uid=None):
        if uid in self.by_id:
            return next(i+1 for i,p in enumerate(self.pages) if p.uid == uid)
        indexes = [i for i,p in enumerate(self.pages) if p.uid in self.canvas.selected]
        return max(indexes)+1 if indexes else len(self.pages)

    def insert_page_refs(self, pages, slot):
        if not pages:
            return
        self.snapshot(); self.pages[slot:slot] = pages
        self.canvas.selected = {p.uid for p in pages}; self.canvas.anchor = pages[-1].uid
        self.refresh()
        point = self.canvas.targets.get(pages[0].uid)
        if point is not None:
            bar = self.canvas.verticalScrollBar()
            if point.y() < bar.value() or point.y()+self.canvas.card_h > bar.value()+self.canvas.viewport().height():
                bar.setValue(int(max(0,point.y()-20)))

    def copy_pages(self):
        pages = self.canvas.selected_pages()
        if not pages:
            return
        try:
            directory = TEMP_ROOT / self.session / 'clipboard' / uuid.uuid4().hex
            exported = export_pages(pages, directory, 'PDF_복사본', False)
            token = uuid.uuid4().hex
            mime = QMimeData()
            mime.setData(CLIPBOARD_MIME, json.dumps({'session':self.session,'token':token}).encode())
            mime.setUrls([QUrl.fromLocalFile(str(p)) for p in exported])
            mime.setData('application/x-qt-windows-mime;value="Preferred DropEffect"', b'\x01\x00\x00\x00')
            QApplication.clipboard().setMimeData(mime)
            self.clipboard_pages = list(pages); self.clipboard_token = token
        except ExportCancelled:return
        except Exception as exc:
            QMessageBox.warning(self, '페이지 복사', str(exc))

    def paste_pages(self, uid=None):
        mime = QApplication.clipboard().mimeData()
        if mime is None:
            return
        try:
            payloads=clipboard_edit_payloads(self.session)
            if payloads:
                self.paste_into_page(payloads,uid);return
        except Exception as exc:
            QMessageBox.warning(self,'붙여넣기',str(exc));return
        slot = self.after_selection(uid)
        try:
            data = json.loads(bytes(mime.data(CLIPBOARD_MIME))) if mime.hasFormat(CLIPBOARD_MIME) else {}
        except (ValueError, UnicodeError):
            data = {}
        if data.get('session') == self.session and data.get('token') == self.clipboard_token:
            copies = [PageRef(p.path,p.number,source_path=p.source_path,source_number=p.source_number,
                              input_path=p.input_path,document_pages=p.document_pages) for p in self.clipboard_pages]
            self.insert_page_refs(copies, slot)
        else:
            paths = self.canvas.pdf_paths(mime)
            self.add_files(paths, slot, select=True)

    def paste_into_page(self,payloads,uid=None):
        if not self.pages:self.insert_blank_page()
        if not self.pages:return
        if uid not in self.by_id:
            uid=self.canvas.anchor if self.canvas.anchor in self.canvas.selected else None
        page=self.by_id.get(uid) or next((p for p in self.pages if p.uid in self.canvas.selected),self.pages[0])
        dialog=self.open_preview(page)
        dialog.enqueue_paste(payloads,page.uid)

    def insert_blank_page(self, uid=None):
        import pymupdf
        slot = self.after_selection(uid)
        reference = self.pages[slot-1] if slot else None
        try:
            width, height = 595.276, 841.89
            if reference is not None:
                with editable_copy(reference.path,reference.number) as source:
                    size = source[0].rect; width,height = size.width,size.height
            folder = TEMP_ROOT / self.session / 'blank' / uuid.uuid4().hex
            folder.mkdir(parents=True, exist_ok=True); path = folder / '빈페이지.pdf'
            with pymupdf.open() as doc:
                doc.new_page(width=width,height=height)
                with path.open('xb') as stream:
                    stream.write(doc.tobytes(deflate=True))
            page = PageRef(str(path),0,source_path=str(path),source_number=0,input_path=reference.input_path if reference else '')
            self.insert_page_refs([page], slot)
        except Exception as exc:
            QMessageBox.warning(self, '빈 페이지 만들기', str(exc))

    def reorder(self, ids, slot):
        selected = set(ids)
        moving = [p for p in self.pages if p.uid in selected]
        others = [p for p in self.pages if p.uid not in selected]
        at = max(0, min(slot, len(others)))
        result = others[:at]+moving+others[at:]
        if result != self.pages:
            self.snapshot();self.pages = result
        self.refresh()

    def remove_selected(self):
        if self.canvas.selected:
            self.snapshot();self.pages = [p for p in self.pages if p.uid not in self.canvas.selected]
            self.refresh()

    def undo(self):
        if self.preview_dialog is not None and self.preview_dialog.busy:
            return
        if self.history:
            self.future.append(PageState(self.pages,self.original_path))
            state=self.history.pop();self.pages=list(state);self.original_path=state.original_path;self.refresh()

    def redo(self):
        if self.preview_dialog is not None and self.preview_dialog.busy:
            return
        if self.future:
            self.history.append(PageState(self.pages,self.original_path))
            state=self.future.pop();self.pages=list(state);self.original_path=state.original_path;self.refresh()

    def open_files(self):
        paths,_ = QFileDialog.getOpenFileNames(self,'PDF · 그림 · 압축파일 추가','',
            '지원 파일 (*.pdf *.jpg *.jpeg *.png *.webp *.tif *.tiff *.bmp *.zip *.cbz);;PDF (*.pdf);;그림 (*.jpg *.jpeg *.png *.webp *.tif *.tiff *.bmp);;그림 압축 (*.zip *.cbz)')
        self.add_files(paths,len(self.pages))

    def open_folder(self):
        path=QFileDialog.getExistingDirectory(self,'그림/PDF 폴더 추가 · 하위 폴더 포함')
        if path:self.add_files([path],len(self.pages))

    def open_new_files(self):
        paths,_=QFileDialog.getOpenFileNames(self,'PDF · 그림 · 압축파일 새로 열기','',
            '지원 파일 (*.pdf *.jpg *.jpeg *.png *.webp *.tif *.tiff *.bmp *.zip *.cbz)')
        if paths:self.replace_inputs(paths)

    def accepts_open_drop(self,event):
        return (not self.clear_pending and not event.buttons() & Qt.MouseButton.RightButton and
                not self.canvas.is_internal(event.mimeData()) and bool(self.canvas.pdf_paths(event.mimeData())))

    def dragEnterEvent(self,event):
        if self.accepts_open_drop(event):event.setDropAction(Qt.DropAction.CopyAction);event.accept()
        else:event.ignore()

    def dropEvent(self,event):
        # 확대/빈 화면은 새로 열기, 썸네일 영역만 삽입 위치를 정해 추가한다.
        if self.accepts_open_drop(event) and self.replace_inputs(self.canvas.pdf_paths(event.mimeData())):
            event.setDropAction(Qt.DropAction.CopyAction);event.accept()
            QTimer.singleShot(0,self.focus_after_file_drop)
        else:event.ignore()

    def replace_inputs(self,paths,navigation_mode=None,navigation_books=None):
        if self.clear_pending:return False
        paths=sorted(dict.fromkeys(str(Path(p).resolve()) for p in paths if supported_input(p)),
                     key=lambda p:(natural_path_key(p),p))
        if not paths:return False
        self.replacement_paths=paths;self.replacement_navigation_mode=navigation_mode
        self.replacement_books=navigation_books
        self.clear(replacing=True);return True

    def navigation_origin(self):
        editor=self.preview_dialog
        page=editor.page if editor is not None and not editor.closed else next(
            (p for p in self.pages if p.uid in self.canvas.selected),self.pages[0] if self.pages else None)
        if page is not None:
            if page.input_path:return page.input_path
            if is_image_source(page.path):return image_source_info(page.path)['file']
            return page.label_path
        return self.pending_import[1] if self.pending_import else self.browse_path

    def navigation_context(self):
        origin=self.navigation_origin();library=self.browse_books
        if library and origin and any(os.path.normcase(path)==os.path.normcase(origin) for path in library.get('paths',[])):
            return origin,True,library
        return origin,self.browse_containers,None

    def navigation_context_key(self):
        origin,containers,library=self.navigation_context()
        return origin,containers,library['root'] if library else ''

    def invalidate_neighbor_names(self):
        self.neighbor_serial+=1;self.neighbor_request=None;self.neighbor_key=None
        self.neighbor_ready=False;self.neighbor_paths={};self.neighbor_error=''
        self.navigation_backend.jobs=[job for job in self.navigation_backend.jobs if job['op']!='neighbors']

    def request_neighbor_names(self):
        if self.closing or self.clear_pending:return
        origin,containers,library=self.navigation_context();key=self.navigation_context_key()
        if not origin:return
        if self.neighbor_key==key and (self.neighbor_ready or self.neighbor_request is not None):return
        self.invalidate_neighbor_names();self.neighbor_key=key
        self.neighbor_request=(self.neighbor_serial,key)
        self.navigation_backend.request('neighbors',origin,token=self.neighbor_serial,
                                        payload={'include_containers':containers,'book_library':library})

    def got_neighbor_names(self,token,paths,error):
        pending=self.neighbor_request
        if pending is None or token!=pending[0]:return
        self.neighbor_request=None
        if self.closing or self.clear_pending or pending[1]!=self.navigation_context_key():return
        self.neighbor_paths=dict(paths);self.neighbor_error=error;self.neighbor_ready=True
        editor=self.preview_dialog
        if editor is not None and not editor.closed:editor.end_overlay.sync()

    def handle_file_key(self,event):
        return self.keys.handle(event,QApplication.focusWidget())

    def keyPressEvent(self,event):
        if self.handle_file_key(event):return
        super().keyPressEvent(event)

    def navigate_sibling(self,direction):
        if self.closing or self.clear_pending or self.navigation_request is not None:return
        origin,containers,library=self.navigation_context()
        if not origin:return
        if self.neighbor_ready and not self.neighbor_error and self.neighbor_key==self.navigation_context_key():
            path=self.neighbor_paths.get('previous' if direction<0 else 'next','')
            if path:self.replace_inputs([path],navigation_mode=containers,navigation_books=library);return
            QToolTip.showText(self.mapToGlobal(QPoint(24,48)),
                              '같은 폴더의 첫 항목입니다.' if direction<0 else '같은 폴더의 마지막 항목입니다.',self);return
        self.navigation_token+=1;self.navigation_request=(self.navigation_token,origin,direction,containers,library)
        self.update_action_states()
        self.navigation_backend.request('sibling',origin,token=self.navigation_token,
                                        payload={'direction':direction,'include_containers':containers,'book_library':library})

    def got_sibling(self,token,path,error):
        pending=self.navigation_request
        if pending is None or token!=pending[0]:return
        self.navigation_request=None
        self.update_action_states()
        if self.closing or self.clear_pending or self.navigation_origin()!=pending[1]:return
        if path and not error:self.replace_inputs([path],navigation_mode=pending[3],navigation_books=pending[4]);return
        text=error or ('같은 폴더의 첫 항목입니다.' if pending[2]<0 else '같은 폴더의 마지막 항목입니다.')
        QToolTip.showText(self.mapToGlobal(QPoint(24,48)),text,self)

    def ensure_page_visible(self,uid):
        point=self.canvas.targets.get(uid)
        if point is not None:
            bar=self.canvas.verticalScrollBar()
            if point.y()<bar.value() or point.y()+self.canvas.card_h>bar.value()+self.canvas.viewport().height():
                bar.setValue(int(max(0,point.y()-24)))

    def follow_thumbnail_selection(self):
        editor=self.preview_dialog
        if editor is None or editor.closed or not editor.embedded:return
        if len(self.canvas.selected)!=1:
            # A delayed single click must not override a following Ctrl/Shift selection.
            if not getattr(editor,'nav_select',True):editor.nav_target_uid=None;editor.nav_timer.stop()
            return
        uid=next(iter(self.canvas.selected))
        if uid==editor.page.uid:return
        index=next((i for i,p in enumerate(self.pages) if p.uid==uid),None)
        if index is not None:editor.request_navigation(index,select=False)

    def open_combined_view(self):
        if self.closing or not self.pages or self.clear_pending:return
        editor=self.preview_dialog
        if editor is not None and not editor.closed and editor.embedded:return
        page=next((p for p in self.pages if p.uid in self.canvas.selected),self.pages[0])
        self.single_file_layout=False
        self.remember_preview_split()
        if editor is None or editor.closed:
            editor=self.make_preview(page,embedded=True)
        else:
            editor.hide();editor.embedded=True
            editor.setParent(self.splitter,Qt.WindowType.Widget)
            editor.setMinimumSize(200,240);editor.actions.hide()
            for shortcut in editor.actions.shortcuts:shortcut.setEnabled(False)
        self.empty_preview.hide();self.empty_preview.setParent(self.content)
        self.splitter.insertWidget(0,editor)
        editor.show();self.canvas.setVisible(not self.thumbnails_collapsed)
        if not self.thumbnails_collapsed:self.splitter.setSizes(self.preview_split_sizes)
        self.canvas.setEnabled(True);self.auto_preview_opened=True
        if not self.canvas.selected:self.canvas.selected={page.uid};self.canvas.anchor=page.uid
        self.canvas.layout_pages();self.place_actions();self.focus_content()

    def restore_empty_preview(self):
        if self.preview_dialog is not None and not self.preview_dialog.closed:return
        if self.splitter.indexOf(self.empty_preview)<0:
            self.splitter.insertWidget(0,self.empty_preview)
            if not self.thumbnails_collapsed:self.splitter.setSizes(self.preview_split_sizes)
        self.empty_preview.show();self.empty_preview.update()

    def make_preview(self,page,embedded=False):
        dialog=PreviewDialog(self,page,embedded=embedded);self.preview_dialog=dialog
        def released():
            if self.preview_dialog is dialog:self.preview_dialog=None
        dialog.destroyed.connect(released)
        return dialog

    def next_preview_token(self):
        # 파일 교체 전후에 같은 번호가 다시 사용되어 이전 결과가 표시되지 않도록 한다.
        self.preview_request_serial+=1
        return self.preview_request_serial

    def open_document_card(self,page):
        current=self.by_id.get(page.uid)
        if current is None or not current.is_document_card:return False
        if not Path(current.path).is_file():
            QMessageBox.warning(self,'PDF 전체 열기','원본 PDF를 찾을 수 없습니다. 폴더를 다시 열어주세요.');return False
        QToolTip.hideText()
        return self.replace_inputs([current.path])

    def open_preview(self, page):
        QToolTip.hideText()
        if self.preview_dialog is None or self.preview_dialog.closed:self.open_combined_view()
        if self.preview_dialog is not None and not self.preview_dialog.closed:
            dialog=self.preview_dialog
            dialog.request_navigation(next(i for i,p in enumerate(self.pages) if p.uid==page.uid));dialog.perform_navigation()
            dialog.show();dialog.view.setFocus()
            if dialog.page.uid==page.uid and not dialog.busy:dialog.request_image()
            return dialog

    def add_files(self,paths,slot=None,select=False,navigation_mode=None,navigation_books=None):
        if not paths or self.clear_pending:return
        paths=sorted(dict.fromkeys(str(Path(p).resolve()) for p in paths if supported_input(p)),
                     key=lambda p:(natural_path_key(p),p))
        if not paths:return
        initial=not self.pages and not self.pending_import and not self.imports
        if initial:
            self.browse_path=paths[0]
            self.browse_books=navigation_books
            self.browse_containers=(bool(navigation_mode) if navigation_mode is not None else
                                    any(Path(p).suffix.lower() in ARCHIVE_EXTENSIONS or Path(p).is_dir() for p in paths))
        slot = len(self.pages) if slot is None else max(0,min(slot,len(self.pages)))
        before = self.pages[slot].uid if slot < len(self.pages) else None
        self.imports.append({'paths':paths, 'before':before, 'index':0, 'saved':False,
                             'select':select, 'selected_ids':[], 'initial':initial, 'opened_order':[], 'errors':[]})
        self.next_import()

    def next_import(self):
        if self.pending_import or self.import_cancelling:return
        while self.imports:
            batch = self.imports[0]
            if batch['index'] >= len(batch['paths']):
                if batch.get('initial'):self.clean_page_orders.add(tuple(batch['opened_order']))
                self.imports.pop(0)
                self.last_import_errors+=len(batch.get('errors',[]))
                if batch.get('errors'):
                    errors=list(batch['errors'])
                    QTimer.singleShot(0,lambda errors=errors:self.show_import_errors(errors))
                continue
            self.import_token += 1
            path = batch['paths'][batch['index']]
            if not self.pages:
                self.browse_path=path;self.setWindowTitle(f'{APP_NAME} · {Path(path).name}')
            self.pending_import = (self.import_token,path,batch)
            self.import_progress.begin(path,batch['index']+1,len(batch['paths']))
            if Path(path).suffix.lower()=='.pdf' and not Path(path).is_dir():
                self.import_directory=None
                self.backend.request('inspect',path,token=self.import_token,priority=True)
            else:
                self.import_directory=None
                self.input_backend.start(self.import_token,path,'')
            break
        if not self.imports:
            self.import_progress.finish(len(self.pages),errors=self.last_import_errors,
                                        unit='항목' if any(p.is_document_card for p in self.pages) else '쪽')
            self.last_import_errors=0
        self.canvas.viewport().update()
        self.update_action_states()

    def got_metadata(self,token,path,count,error):
        if not self.pending_import or token != self.pending_import[0]:return
        batch = self.pending_import[2]
        self.pending_import = None
        if error:batch['errors'].append(f'{Path(path).name}\n{error}')
        elif count:self.append_imported_pages(batch,path,[PageRef(path,i) for i in range(count)])
        batch['index'] += 1
        QTimer.singleShot(0,self.next_import)

    def append_imported_pages(self,batch,origin,added):
        if not added:return
        for page in added:page.input_path=str(Path(origin).resolve())
        if not batch['saved']:self.snapshot();batch['saved']=True
        if self.original_path is None:self.original_path=input_origin(origin)
        index=next((i for i,p in enumerate(self.pages) if p.uid==batch['before']),len(self.pages))
        batch['opened_order'].extend(self.page_order(added));self.pages[index:index]=added
        self.pristine_pages.update(self.page_order(added))
        if batch.get('select'):
            batch['selected_ids'].extend(p.uid for p in added)
            self.canvas.selected=set(batch['selected_ids']);self.canvas.anchor=added[-1].uid
        self.refresh()

    def got_input_item(self,token,data):
        if not self.pending_import or token!=self.pending_import[0]:return
        _token,origin,batch=self.pending_import
        if data.get('book_library'):
            self.browse_books=data['book_library'];self.invalidate_neighbor_names()
            if batch.get('initial'):
                self.browse_path=data['book_path'];self.browse_containers=True
        origin=data.get('book_path') or origin
        added=[]
        for item in data.get('items',[data]):
            added.extend(PageRef(item['path'],i,source_path=item.get('source_path',''),
                         source_number=i if item.get('image') else item.get('source_number',-1),
                         document_pages=item.get('document_pages',0)) for i in range(item['count']))
            if item.get('thumbnail'):
                pix=QPixmap();pix.loadFromData(base64.b64decode(item['thumbnail']))
                if not pix.isNull():self.thumbs[(item['path'],0)]=pix
        self.append_imported_pages(batch,origin,added)

    def got_input_done(self,token,result):
        if not self.pending_import or token!=self.pending_import[0]:return
        batch=self.pending_import[2];self.pending_import=None
        finished_directory=self.import_directory;self.import_directory=None
        batch['errors'].extend(result.get('errors',[]));batch['index']+=1
        if finished_directory:self.cleanup_working_files(scopes=[finished_directory])
        QTimer.singleShot(0,self.next_import)

    def got_input_progress(self,token,data):
        if not self.pending_import or token!=self.pending_import[0]:return
        self.import_progress.update_progress(data,len(self.pages),
                                             unit='항목' if any(p.is_document_card for p in self.pages) else '쪽')

    def cancel_import(self):
        if self.import_cancelling:return
        if not self.pending_import and not self.imports:return
        token=self.pending_import[0] if self.pending_import else self.import_token
        for batch in self.imports:
            if batch.get('initial'):self.clean_page_orders.add(tuple(batch['opened_order']))
        self.import_cancelling=True;self.cancelled_directory=self.import_directory
        self.imports.clear();self.pending_import=None;self.import_directory=None;self.import_token+=1
        self.backend.jobs=[j for j in self.backend.jobs if j['op']!='inspect']
        self.import_progress.stopping();self.update_action_states();self.canvas.viewport().update()
        if self.input_backend.active is not None:self.input_backend.cancel(token)
        else:QTimer.singleShot(0,lambda:self.import_cancelled(token))

    def import_cancelled(self,_token):
        if not self.import_cancelling:return
        directory=self.cancelled_directory;self.cancelled_directory=None
        if directory:self.cleanup_working_files(scopes=[directory])
        self.import_cancelling=False;self.last_import_errors=0
        self.import_progress.finish(len(self.pages),cancelled=True,
                                    unit='항목' if any(p.is_document_card for p in self.pages) else '쪽')
        if self.cleanup_failures:self.import_progress.detail.setText(self.import_progress.detail.text()+
            f' · 임시파일 {len(self.cleanup_failures)}개 정리 보류')
        self.update_action_states()
        if self.close_after_import:
            self.close_after_import=False;QTimer.singleShot(0,self.close)
        elif self.clear_pending:QTimer.singleShot(0,self.continue_clear)
        elif self.imports:QTimer.singleShot(0,self.next_import)

    def cleanup_working_files(self,scopes=None,closing=False):
        references=[];protected=[];root=TEMP_ROOT/self.session
        if not closing:
            refs=list(self.pages)+self.clipboard_pages
            for state in self.history+self.future:refs.extend(state)
            references.extend(p.path for p in refs)
            if self.import_directory:protected.append(self.import_directory)
            if self.cancelled_directory and self.input_backend.cancelling is not None:
                protected.append(self.cancelled_directory)
            for job in ([self.backend.active] if self.backend.active else [])+self.backend.jobs:
                if job.get('path'):references.append(job['path'])
            editor=self.preview_dialog
            if editor is not None and not editor.closed:
                references.append(editor.page.path)
                protected.extend([root/'edits',root/'paste'])
                if editor.backend.active and editor.backend.active.get('path'):
                    references.append(editor.backend.active['path'])
            # A HWP conversion reads original page refs independently of the UI.
            if self.hangul_dialog is not None and self.hangul_dialog.busy:
                try:
                    job=json.loads(self.hangul_dialog.job_path.read_text(encoding='utf-8'))
                    references.extend(p[0] for p in job['pages'])
                except (OSError,ValueError,KeyError):return
        self.cleanup_failures=prune_working_files(root,references,protected,scopes)

    def open_temp_folder(self):
        TEMP_ROOT.mkdir(parents=True,exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(TEMP_ROOT)))

    def jpg_to_pdf(self):
        if self.pending_import or self.imports or self.import_cancelling:
            QMessageBox.information(self,'JPG to PDF','목록 확인을 마치거나 취소한 뒤 변환하세요.');return
        picture=lambda p:is_image_source(p.path) or Path(p.source_path).suffix.lower() in IMAGE_EXTENSIONS
        all_pictures=[p for p in self.pages if picture(p)]
        selected=[p for p in all_pictures if p.uid in self.canvas.selected]
        chooser=QDialog(self);chooser.setWindowTitle('JPG to PDF');chooser.resize(390,210)
        layout=QVBoxLayout(chooser);layout.addWidget(QLabel('그림을 화면 순서대로 한 PDF에 저장'))
        mode=QComboBox();mode.addItem(f'현재 그림 전체 · {len(all_pictures):,}쪽','all')
        mode.addItem(f'선택한 그림 · {len(selected):,}쪽','selected');layout.addWidget(mode)
        start=QPushButton('현재 그림 변환');layout.addWidget(start)
        start.setStyleSheet('background:#b82b47;color:white;padding:9px;border-radius:5px;')
        start.setEnabled(bool(all_pictures));inputs=[];pages=[]
        def current():
            pages.extend(selected if mode.currentData()=='selected' else all_pictures)
            if pages:chooser.accept()
        start.clicked.connect(current)
        mode.currentIndexChanged.connect(lambda:start.setEnabled(bool(selected if mode.currentData()=='selected' else all_pictures)))
        def choose_files():
            paths,_=QFileDialog.getOpenFileNames(chooser,'그림 또는 그림 압축파일','',
                '그림 (*.jpg *.jpeg *.png *.webp *.tif *.tiff *.bmp *.zip *.cbz)')
            if paths:inputs.extend(sorted(paths,key=natural_path_key));chooser.accept()
        def choose_folder():
            folder=QFileDialog.getExistingDirectory(chooser,'그림 폴더 · 하위 폴더 포함')
            if folder:inputs.append(folder);chooser.accept()
        for text,callback in [('파일 선택',choose_files),('폴더 선택',choose_folder)]:
            button=QPushButton(text);button.clicked.connect(callback);layout.addWidget(button)
        accepted=chooser.exec()==QDialog.DialogCode.Accepted;chooser.deleteLater()
        if not accepted:return
        origin=Path(input_origin(inputs[0]) if inputs else self.original_path or '그림.pdf')
        target,_=QFileDialog.getSaveFileName(self,'JPG to PDF 저장',str(origin.with_name(origin.stem+'-(그림).pdf')),
            'PDF (*.pdf)',options=QFileDialog.Option.DontConfirmOverwrite)
        if not target:return
        if Path(target).suffix.lower()!='.pdf':target+='.pdf'
        dialog=ImageExportDialog(self,target,pages,inputs);dialog.exec()
        if dialog.error:QMessageBox.warning(self,'JPG to PDF',dialog.error)
        elif dialog.result_path:QMessageBox.information(self,'JPG to PDF',f'저장 완료\n{dialog.result_path}')
        dialog.deleteLater()

    def show_import_errors(self,errors):
        box=QMessageBox(self);box.setWindowTitle('일부 파일을 읽지 못했습니다')
        box.setIcon(QMessageBox.Icon.Warning);box.setText(f'읽지 못한 항목 {len(errors)}개')
        box.setInformativeText('\n'.join(errors[:3]));box.setDetailedText('\n\n'.join(errors))
        box.exec();box.deleteLater()

    def got_thumbnail(self,path,number,pix,error):
        key = (path,number)
        if not any((p.path,p.number)==key for p in self.pages):return
        if error:self.thumb_errors[key] = error
        else:
            self.thumbs[key] = pix;self.thumbs.move_to_end(key)
            editor=self.preview_dialog
            if editor is not None:editor.show_thumbnail(path,number,pix)
            total=sum(p.width()*p.height()*4 for p in self.thumbs.values())
            while total>64*1024*1024 and len(self.thumbs)>1:
                visible=getattr(self,'visible_thumb_keys',set())
                old=next((k for k in self.thumbs if k not in visible),next(iter(self.thumbs)))
                bitmap=self.thumbs.pop(old);total-=bitmap.width()*bitmap.height()*4
                self.requested.discard(old);self.large_thumbs_requested.discard(old)
        self.canvas.viewport().update()

    def prioritize_thumbnails(self):
        if not hasattr(self,'canvas'):return
        keys = []
        for page in (() if self.thumbnails_collapsed else self.pages):
            if page.uid in self.canvas.targets:
                r = self.canvas.card_rect(page.uid)
                if r.bottom() > -self.canvas.card_h and r.top() < self.canvas.viewport().height()+self.canvas.card_h:
                    keys.append((page.path,page.number))
        needed=set(keys)
        self.visible_thumb_keys=needed
        for engine in (self.backend,self.image_backend):
            removed=[j for j in engine.jobs if j['op']=='render' and (j['path'],j['page']) not in needed]
            for job in removed:self.requested.discard((job['path'],job['page']))
            engine.jobs=[j for j in engine.jobs if j not in removed]
        large=self.single_file_layout and len(self.pages)==1
        for path,number in keys:
            key=(path,number)
            if key in self.thumb_errors:continue
            if key in self.thumbs:self.thumbs.move_to_end(key)
            if large and key in self.thumbs and key not in self.large_thumbs_requested:self.requested.discard(key)
            if key in self.requested or (key in self.thumbs and (not large or key in self.large_thumbs_requested)):continue
            self.requested.add(key)
            if large:self.large_thumbs_requested.add(key)
            engine=self.image_backend if is_image_source(path) else self.backend
            engine.request('render',path,number,payload={'thumb_side':1600 if large else 370})
        self.backend.set_thumbnail_order(keys);self.image_backend.set_thumbnail_order(keys)

    def page_order(self,pages=None):
        return tuple(p.state_key for p in (self.pages if pages is None else pages))

    def has_unsaved_changes(self):
        # Order, additions/deletions and immutable edited page paths all count.
        return bool(self.pages) and self.page_order() not in self.clean_page_orders

    def cancel_clear(self):
        self.replacement_paths=None;self.replacement_navigation_mode=None
        self.replacement_books=None
        self.clear_pending=False;self.clear_timer.stop();self.update_action_states()

    def clear(self,*,replacing=False):
        if self.clear_pending:return
        if not replacing:self.replacement_paths=None;self.replacement_navigation_mode=None;self.replacement_books=None
        self.navigation_token+=1;self.navigation_request=None;self.navigation_backend.jobs.clear()
        self.invalidate_neighbor_names()
        editor=self.preview_dialog
        if editor is not None and not editor.closed:
            editor.nav_target_uid=None;editor.nav_timer.stop()
            editor.nav_previous.stop_drag();editor.nav_next.stop_drag()
        self.clear_pending=True;self.cancel_import();self.update_action_states();self.continue_clear()

    def continue_clear(self):
        if not self.clear_pending:return
        # Stop reading first, but finish accepted edits before offering Save.
        if self.import_cancelling or self.translation_waiting or self.hangul_waiting:
            self.clear_timer.start();return
        if self.pending_import or self.imports:
            self.cancel_import();self.clear_timer.start();return
        editor=self.preview_dialog
        if editor is not None and not editor.closed:
            if editor.busy or editor.loading_info or editor.paste_queue or editor.after_image is not None or editor.after_move is not None or any(abs(v)>.0001 for v in editor.queued_nudge):
                self.clear_timer.start();return
            if editor.has_pending_move():
                editor.commit_move()
                if self.clear_pending:self.clear_timer.start()
                return
        self.clear_timer.stop()
        if self.has_unsaved_changes():
            box=QMessageBox(editor if editor is not None and not editor.closed else self)
            replacing=bool(self.replacement_paths)
            box.setWindowTitle('새로 열기' if replacing else '전체 비우기');box.setIcon(QMessageBox.Icon.Question)
            box.setText('저장하지 않은 수정 내용이 있습니다.\n'+(
                '현재 순서의 전체 PDF를 저장한 뒤 새 파일을 열까요?' if replacing else '현재 순서의 전체 PDF를 저장한 뒤 비울까요?'))
            save=box.addButton('저장 후 열기' if replacing else '저장 후 비우기',QMessageBox.ButtonRole.AcceptRole)
            discard=box.addButton('저장하지 않고 열기' if replacing else '저장하지 않고 비우기',QMessageBox.ButtonRole.DestructiveRole)
            cancel=box.addButton('취소',QMessageBox.ButtonRole.RejectRole)
            box.setDefaultButton(save);box.setEscapeButton(cancel);box.exec()
            chosen=box.clickedButton();box.deleteLater()
            if chosen is save:
                if not self.save_revision():self.cancel_clear();return
            elif chosen is not discard:self.cancel_clear();return
        replacement=self.replacement_paths;navigation_mode=self.replacement_navigation_mode;books=self.replacement_books
        self.replacement_paths=None;self.replacement_navigation_mode=None;self.replacement_books=None
        if editor is not None and not editor.closed:
            editor.shutdown();editor.close()
        self.preview_dialog=None
        self.auto_preview_opened=False
        self.pages.clear();self.imports.clear();self.pending_import=None;self.import_token+=1
        self.original_path=None;self.revision_directory=None;self.last_saved_path=None;self.browse_path=None;self.browse_containers=False
        self.browse_books=None
        self.last_save_error='';self.last_save_error_path=None
        self.history.clear();self.future.clear();self.clean_page_orders={()};self.exported_revisions.clear()
        self.pristine_pages.clear()
        self.canvas.selected.clear();self.canvas.anchor=None;self.canvas.dragging.clear()
        self.canvas.slot=self.canvas.pointer=self.canvas.press_pos=self.canvas.pressed_uid=None
        self.canvas.external_hover=False;self.canvas.defer_click=False;self.canvas.toggle_on_release=None
        self.canvas.wheel_remainder=0;self.canvas.wheel_precise=None
        self.large_thumbs_requested.clear()
        self.backend.jobs.clear();self.requested.clear();self.thumbs.clear();self.thumb_errors.clear()
        self.image_backend.cancel_pending(release=True)
        self.clear_pending=False
        self.import_progress.hide_timer.stop();self.import_progress.hide()
        self.refresh()
        self.canvas.verticalScrollBar().setValue(0);self.focus_content()
        # Close cached Windows PDF handles before unlinking working files.
        if self.backend.proc.state()==QProcess.ProcessState.Running:
            self.backend.request('release','',priority=True)
        else:self.cleanup_working_files()
        if replacement:self.add_files(replacement,navigation_mode=navigation_mode,navigation_books=books)

    def ask_name(self,default):
        while True:
            text,ok = QInputDialog.getText(self,'사본 이름','파일 이름',QLineEdit.EchoMode.Normal,default)
            if not ok:return None
            try:return clean_name(text)
            except ValueError as exc:QMessageBox.information(self,'파일 이름 확인',str(exc))

    def rename_copies(self,sources,target,pages):
        # 표준 드롭이 끝난 다음, 실제 복사된 파일만 검증해서 이름 변경.
        default = Path(pages[0].label_path).stem+'_선택'+str(total_page_count(pages))+'쪽'
        name = self.ask_name(default)
        if name is None:return
        copies = target.find_copies(sources)
        if not copies:
            # Explorer 탭/특수 폴더/다른 앱 등 대상 경로를 확정하지 못하면 추측해서 변경하지 않는다.
            directory = QFileDialog.getExistingDirectory(self,'방금 PDF를 놓은 폴더 선택')
            if not directory:return
            copies = [Path(directory)/p.name for p in sources]
        try:
            for src,dst in zip(sources,copies):
                if not dst.is_file() or hashlib.sha256(dst.read_bytes()).digest() != hashlib.sha256(src.read_bytes()).digest():
                    raise ValueError('방금 만든 사본을 해당 폴더에서 확인하지 못했습니다. 원래 사본 이름으로 남겨두었습니다.')
            names = [p.with_name(f'{name}_{i+1:03d}.pdf' if len(copies)>1 else f'{name}.pdf') for i,p in enumerate(copies)]
            if any(p.exists() and p != old for p,old in zip(names,copies)):
                raise FileExistsError('같은 이름의 파일이 이미 있습니다. 파일을 덮어쓰지 않았습니다.')
            renamed = []
            try:
                for old,new in zip(copies,names):
                    if old != new:
                        if not QFile.rename(str(old),str(new)):
                            raise OSError(f'이름 변경 실패: {old.name}')
                        renamed.append((old,new))
            except Exception:
                for old,new in reversed(renamed):QFile.rename(str(new),str(old))
                raise
        except Exception as exc:
            QMessageBox.warning(self,'사본 이름 변경',str(exc))

    def save_selected(self):
        pages = self.canvas.selected_pages()
        if not pages:return
        name = self.ask_name('선택페이지')
        if name is None:return
        folder = QFileDialog.getExistingDirectory(self,'사본 저장 폴더')
        if not folder:return
        try:
            export_pages(pages,folder,name,self.separate)
            self.mark_exported(pages)
        except ExportCancelled:return
        except Exception as exc:QMessageBox.warning(self,'저장 실패',str(exc))

    def report_save_error(self, exc, original, directory):
        """실패 원문과 실행 환경을 표시. 진단 기록 자체가 저장 오류를 가리지 않는다."""
        import traceback
        from importlib.metadata import version, PackageNotFoundError
        try:
            pdf_version=version('PyMuPDF')
        except PackageNotFoundError:
            pdf_version='설치 확인 필요'
        sources='\n'.join(dict.fromkeys(p.label_path for p in self.pages))
        details=(f'{APP_NAME} {APP_VERSION}\n'
                 f'시각: {time.strftime("%Y-%m-%d %H:%M:%S %z")}\n'
                 f'Python: {sys.version}\nPyMuPDF: {pdf_version}\n'
                 f'실행 파일: {Path(__file__).resolve()}\n'
                 f'처음 연 PDF: {original}\n저장 폴더: {directory}\n'
                 f'페이지 수: {total_page_count(self.pages)} (화면 항목 {len(self.pages)})\n페이지 원본/작업 사본:\n{sources}\n\n'
                 + ''.join(traceback.format_exception(type(exc),exc,exc.__traceback__)))
        self.last_save_error=details
        self.last_save_error_path=None
        try:
            log_directory=TEMP_ROOT/'save_errors'
            log_directory.mkdir(parents=True,exist_ok=True)
            log_path=log_directory/(time.strftime('save-%Y%m%d-%H%M%S-')+uuid.uuid4().hex[:8]+'.txt')
            with log_path.open('x',encoding='utf-8') as stream:
                stream.write(details)
            self.last_save_error_path=str(log_path)
        except OSError:
            pass
        parent=self.preview_dialog if self.preview_dialog is not None and not self.preview_dialog.closed else self
        box=QMessageBox(parent)
        box.setWindowTitle('PDF 저장 실패')
        box.setIcon(QMessageBox.Icon.Warning)
        box.setTextFormat(Qt.TextFormat.PlainText)
        box.setText('PDF를 저장하지 못했습니다.')
        message=f'{type(exc).__name__}: {exc}\n\n저장 폴더: {directory}'
        if self.last_save_error_path:
            message+=f'\n\n오류 기록: {self.last_save_error_path}'
        box.setInformativeText(message)
        box.setDetailedText(details)
        box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        retry=box.addButton('다른 폴더 선택',QMessageBox.ButtonRole.AcceptRole) if isinstance(exc,OSError) else None
        copy=box.addButton('오류 내용 복사',QMessageBox.ButtonRole.ActionRole)
        copy.clicked.connect(lambda:QApplication.clipboard().setText(details))
        close=box.addButton('닫기',QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(close);box.setEscapeButton(close)
        box.exec()
        return retry is not None and box.clickedButton() is retry

    def save_revision(self):
        """선택 여부와 무관하게 현재 순서 전체를 원본 폴더의 다음 번호로 저장."""
        if not self.pages:return False
        if self.pending_import or self.imports or self.import_cancelling:
            QToolTip.showText(self.save_button.mapToGlobal(QPoint(0,30)),'파일을 모두 불러온 뒤 저장하세요',self.save_button)
            return False
        editor=self.preview_dialog
        if editor is not None and not editor.closed:
            if editor.paste_queue:
                QTimer.singleShot(120,self.save_revision);return False
            if editor.busy:
                editor.after_move=self.save_revision
                return False
            if editor.has_pending_move():
                editor.after_move=self.save_revision;editor.commit_move();return False
            if any(abs(v)>0.0001 for v in editor.queued_nudge):
                QTimer.singleShot(120,self.save_revision);return False
        original=self.original_path
        if original is None:
            if not self.revision_directory:
                self.revision_directory=QFileDialog.getExistingDirectory(self,'PDF 저장 폴더') or None
                if not self.revision_directory:return False
            original=str(Path(self.revision_directory)/'빈페이지.pdf')
        while True:
            try:
                target=export_numbered_copy(list(self.pages),original,self.revision_directory)
                break
            except ExportCancelled:return False
            except Exception as exc:
                directory=self.revision_directory or str(Path(original).parent)
                if not self.report_save_error(exc,original,directory):return False
                folder=QFileDialog.getExistingDirectory(self,'다른 저장 폴더 선택',str(directory))
                if not folder:return False
                self.revision_directory=folder
        self.last_saved_path=str(target)
        self.mark_exported(self.pages,document=True)
        self.update_action_states()
        button=editor.actions.save_button if editor is not None and not editor.closed else self.save_button
        QToolTip.showText(button.mapToGlobal(QPoint(0,32)),f'저장 완료\n{target}',button,button.rect(),6000)
        return True

    def mark_exported(self, pages,document=False):
        self.exported_revisions.update(p.state_key for p in pages if p.source_path)
        if document and self.page_order(pages)==self.page_order():self.clean_page_orders.add(self.page_order())

    def save_copy_dialog(self, pages, stem):
        while True:
            path, _ = QFileDialog.getSaveFileName(self, 'PDF 사본 저장', stem+'.pdf', 'PDF (*.pdf)',
                                                  options=QFileDialog.Option.DontConfirmOverwrite)
            if not path:
                return False
            target = Path(path)
            try:
                export_pages(pages, target.parent, target.name, False)
                self.mark_exported(pages,document=True)
                return True
            except ExportCancelled:return False
            except Exception as exc:
                QMessageBox.warning(self, '사본 저장', str(exc))

    def translation_message(self, message):
        self.translation_status=message
        self.translation_log.append(time.strftime('%H:%M:%S')+'  '+message)
        self.translation_log=self.translation_log[-100:]
        self.translationChanged.emit();self.update_action_states()

    def show_translation_status(self):
        if self.translation_dialog is None:self.translation_dialog=TranslationStatusDialog(self)
        self.translation_dialog.refresh();self.translation_dialog.show()
        self.translation_dialog.raise_();self.translation_dialog.activateWindow()

    def check_deepl_usage(self):
        if self.usage_thread is not None:return
        self.deepl_usage_text='DeepL 연결 확인 중…'
        worker=DeepLWorker(self.deepl_api_key,parent=self);self.usage_thread=worker
        def success(data):
            self.deepl_usage_text=(f'DeepL 계정 사용량: {data["count"]:,} / {data["limit"]:,}자'
                                   if data['valid'] else 'DeepL 연결 성공 · 문자 사용량은 이 계정에서 확인되지 않음')
            self.translationChanged.emit()
        def failure(data):
            self.deepl_usage_text='연결 확인 실패\n'+data['message'];self.translationChanged.emit()
        def finished():
            self.usage_thread=None;self.translationChanged.emit();worker.deleteLater()
        worker.result.connect(success);worker.failed.connect(failure);worker.finished.connect(finished)
        self.translationChanged.emit();worker.start()

    def confirm_translation(self, count, target):
        parent=self.preview_dialog if self.preview_dialog is not None and not self.preview_dialog.closed else self
        box=QMessageBox(parent);box.setWindowTitle('PDF 번역');box.setIcon(QMessageBox.Icon.Question)
        box.setTextFormat(Qt.TextFormat.PlainText)
        box.setText(f'현재 전체 {count}쪽을 한국어로 번역할까요?')
        box.setInformativeText(f'저장: {target}\n\n현재 순서와 편집 내용이 반영된 PDF가 DeepL로 전송됩니다.\n'
                               'PDF 1건당 최소 50,000자가 API 사용량에 산정됩니다.')
        yes=box.addButton('번역',QMessageBox.ButtonRole.AcceptRole)
        no=box.addButton('취소',QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(no);box.setEscapeButton(no);box.exec()
        return box.clickedButton() is yes

    def translate_current(self):
        if self.translation_busy:
            self.show_translation_status();return
        if not self.pages or self.translation_waiting:return
        if self.pending_import or self.imports or self.import_cancelling:
            QToolTip.showText(self.translate_button.mapToGlobal(QPoint(0,30)),'PDF를 모두 불러온 뒤 번역하세요',self.translate_button);return
        editor=self.preview_dialog
        if editor is not None and not editor.closed:
            if editor.paste_queue or any(abs(v)>0.0001 for v in editor.queued_nudge):
                self.translation_waiting=True
                def resume():
                    self.translation_waiting=False;self.translate_current()
                QTimer.singleShot(120,resume);return
            if editor.busy:
                editor.after_move=self.translate_current;return
            if editor.has_pending_move():
                editor.after_move=self.translate_current;editor.commit_move();return
        if not self.deepl_api_key:
            self.show_settings(tab='translation');return
        try:
            import deepl
        except ImportError:
            QMessageBox.warning(self,'번역 모듈 설치','CMD에서 한 번 설치하세요.\n\npy -m pip install -U deepl');return
        previous=self.translation_job or {}
        if previous and not previous.get('published') and not previous.get('terminal_error') and (previous.get('handle') or previous.get('downloaded')):
            self.show_translation_status();return
        original=self.original_path or '문서.pdf'
        directory=self.translation_directory or self.revision_directory or (str(Path(original).parent) if self.original_path else '')
        if not directory:
            directory=QFileDialog.getExistingDirectory(self,'번역 PDF 저장 폴더')
            if not directory:return
        try:
            stem=translation_stem(original)
            target=next_translation_path(directory,stem)
        except Exception as exc:
            QMessageBox.warning(self,'번역 파일명',str(exc));return
        count=total_page_count(self.pages)
        if not self.confirm_translation(count,target):return
        try:
            folder=Path(directory);folder.mkdir(parents=True,exist_ok=True)
            # 비용이 발생하는 업로드 전에 쓰기 가능한 폴더인지 확인한다.
            with tempfile.TemporaryFile(dir=folder):pass
            work=TEMP_ROOT/self.session/'translation'/uuid.uuid4().hex;work.mkdir(parents=True,exist_ok=True)
            source=export_pages(list(self.pages),work,'input',False)[0]
        except ExportCancelled:return
        except Exception as exc:
            QMessageBox.warning(self,'번역 준비 실패',str(exc));return
        self.translation_job={'input':str(source),'download':str(work/'translated.pdf.part'),
                              'directory':str(folder),'stem':stem,'pages':count}
        self.translation_log=[]
        self.translation_message(f'전체 {count}쪽 → 한국어 · {target.name}')
        self.start_translation_worker()

    def start_translation_worker(self):
        if self.translation_busy:return
        self.translation_busy=True
        worker=DeepLWorker(self.deepl_api_key,self.translation_job,self);self.translation_thread=worker
        worker.stage.connect(self.translation_message)
        worker.result.connect(self.translation_received)
        worker.failed.connect(self.translation_failed)
        def finished():
            self.translation_busy=False;self.translation_thread=None
            self.translationChanged.emit();self.update_action_states();worker.deleteLater()
        worker.finished.connect(finished)
        self.show_translation_status();self.update_action_states();worker.start()

    def translation_received(self, data):
        self.translation_job=data['job']
        count=self.translation_job.get('billed_characters')
        if count is not None:self.translation_message(f'DeepL이 반환한 이번 문서 사용량: {count:,}자')
        self.finish_translation_save()

    def translation_failed(self, data):
        self.translation_job=data['job']
        self.translation_message('번역 중 오류\n'+data['message'])
        job=self.translation_job or {}
        if job.get('handle') and not job.get('terminal_error'):
            self.translation_message('같은 요청의 결과를 이어받을 수 있습니다. 이어받기는 PDF를 새로 업로드하지 않습니다.')

    def finish_translation_save(self):
        import pymupdf
        job=self.translation_job
        if not job or job.get('published'):return
        try:
            with pymupdf.open(job['download']) as doc:
                if not doc.is_pdf or doc.needs_pass or len(doc)==0:
                    raise ValueError('DeepL 응답을 읽을 수 있는 PDF로 확인하지 못했습니다.')
        except Exception as exc:
            job['terminal_error']=True;self.translation_message('번역 PDF 확인 실패\n'+str(exc));return
        try:
            target=publish_translation(job['download'],job['directory'],job['stem'])
        except Exception as exc:
            self.translation_message('번역 완료 · 결과 저장 실패\n'+str(exc))
            self.translation_message('다운로드한 PDF는 보관 중입니다. 저장 다시 시도로 다른 폴더에 저장하세요.');return
        job['published']=str(target)
        self.translation_message('번역 저장 완료\n'+str(target))
        # 성공한 요청의 임시 입력/다운로드만 정리한다.
        for key in ('input','download'):
            try:Path(job[key]).unlink(missing_ok=True)
            except OSError:pass
        try:Path(job['input']).parent.rmdir()
        except OSError:pass
        job.pop('handle',None)

    def resume_translation(self):
        if self.translation_busy:return
        job=self.translation_job or {}
        if job.get('published') or job.get('terminal_error'):return
        if job.get('downloaded'):
            folder=QFileDialog.getExistingDirectory(self,'번역 PDF를 저장할 폴더',job['directory'])
            if folder:
                job['directory']=folder;self.finish_translation_save()
        elif job.get('handle'):
            if not self.deepl_api_key:
                self.show_settings(tab='translation');return
            self.start_translation_worker()

    def open_translation(self):
        path=(self.translation_job or {}).get('published')
        if not path or not Path(path).is_file():return
        window=Window(startup_pdf_count=1);self.translation_windows.append(window)
        window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        window.destroyed.connect(lambda:self.translation_windows.remove(window) if window in self.translation_windows else None)
        window.show();window.add_files([path])

    def choose_hangul(self):
        if self.hangul_dialog is not None and self.hangul_dialog.busy:
            self.show_hangul_status();return
        if not self.pages:return
        editor=self.preview_dialog
        parent=editor if editor is not None and not editor.closed else self
        dialog=HangulChoiceDialog(self,parent)
        if dialog.exec()==QDialog.DialogCode.Accepted and dialog.chosen:
            self.export_hangul(dialog.chosen)
        dialog.deleteLater()

    def show_hangul_status(self):
        if self.hangul_dialog is not None:
            self.hangul_dialog.show();self.hangul_dialog.raise_();self.hangul_dialog.activateWindow()

    def show_hangul_module_error(self,error,parent=None):
        if not isinstance(error,HangulDependencyError):
            error=HangulDependencyError('한글 모듈을 확인하는 과정에서 오류가 발생했습니다.',cause=error)
        box=QMessageBox(parent or self);box.setWindowTitle('한글 변환 모듈 확인')
        box.setIcon(QMessageBox.Icon.Warning);box.setTextFormat(Qt.TextFormat.PlainText)
        box.setText(error.message)
        hint=('이 뷰어가 사용하는 Python:\n'+sys.executable+
              '\n\n설치 명령 복사: 위 실행 환경에 설치하는 명령입니다.') if error.install_command else (
              '현재 실행 중인 EXE:\n'+sys.executable+
              '\n\nEXE 내부 모듈·배포 정보는 실행 파일에 포함되어야 합니다.')
        box.setInformativeText(hint);box.setDetailedText(error.details)
        box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        copy=box.addButton('진단 정보 복사',QMessageBox.ButtonRole.ActionRole)
        copy.clicked.connect(lambda:QApplication.clipboard().setText(error.details))
        if error.install_command:
            install=box.addButton('설치 명령 복사',QMessageBox.ButtonRole.ActionRole)
            install.clicked.connect(lambda:QApplication.clipboard().setText(error.install_command))
        close=box.addButton('확인',QMessageBox.ButtonRole.AcceptRole)
        box.setDefaultButton(close);box.setEscapeButton(close);box.exec();box.deleteLater()

    def check_hangul_module(self,parent=None):
        try:_,ver=hangul_dependencies()
        except Exception as exc:self.show_hangul_module_error(exc,parent);return
        module=sys.modules.get('hwpx');details=hangul_environment_report(ver,getattr(module,'__file__',''))
        box=QMessageBox(parent or self);box.setWindowTitle('한글 변환 모듈 확인')
        box.setIcon(QMessageBox.Icon.Information);box.setTextFormat(Qt.TextFormat.PlainText)
        box.setText('현재 뷰어에서 python-hwpx 6.6.0을 정상적으로 불러왔습니다.')
        box.setInformativeText('실행 파일:\n'+sys.executable);box.setDetailedText(details)
        copy=box.addButton('진단 정보 복사',QMessageBox.ButtonRole.ActionRole)
        copy.clicked.connect(lambda:QApplication.clipboard().setText(details))
        close=box.addButton('확인',QMessageBox.ButtonRole.AcceptRole)
        box.setDefaultButton(close);box.setEscapeButton(close);box.exec();box.deleteLater()

    def export_hangul(self, prefs):
        if self.hangul_dialog is not None and self.hangul_dialog.busy:
            self.show_hangul_status();return
        if not self.pages or self.hangul_waiting:return
        if self.pending_import or self.imports or self.import_cancelling:
            QMessageBox.information(self,'한글 변환','PDF를 모두 불러온 뒤 변환하세요.');return
        editor=self.preview_dialog
        if editor is not None and not editor.closed:
            if editor.paste_queue or any(abs(v)>.0001 for v in editor.queued_nudge):
                self.hangul_waiting=True
                def resume():
                    self.hangul_waiting=False;self.export_hangul(prefs)
                QTimer.singleShot(120,resume);return
            if editor.busy:
                editor.after_move=lambda:self.export_hangul(prefs);return
            if editor.has_pending_move():
                editor.after_move=lambda:self.export_hangul(prefs);editor.commit_move();return
        pages=self.canvas.selected_pages() if prefs.get('selected') else list(self.pages)
        if not pages:
            QMessageBox.information(self,'한글 변환','변환할 페이지를 먼저 선택하세요.');return
        try:hangul_dependencies()
        except Exception as exc:
            self.show_hangul_module_error(exc,editor if editor is not None and not editor.closed else self);return
        original=Path(self.original_path or '문서.pdf')
        folder=self.revision_directory or str(original.parent)
        tag='통합'
        extension=prefs['format']
        default=str(Path(folder)/(original.stem+f'-(한글-{tag}).'+extension))
        target,_=QFileDialog.getSaveFileName(self,'한글 파일 저장 · 중복 이름에는 번호를 붙입니다',default,
                 f'한글 문서 (*.{extension})',options=QFileDialog.Option.DontConfirmOverwrite)
        if not target:return
        if Path(target).suffix.lower()!='.'+extension:target+='.'+extension
        try:
            job={'pages':[(p.path,p.number) for p in expanded_page_refs(pages)],'output':str(Path(target).resolve()),
                 'mode':prefs['mode'],'dpi':prefs['dpi'],'font':prefs['font'],'options':prefs.get('options')}
            old=self.hangul_dialog
            self.hangul_dialog=HangulExportDialog(self,job)
            if old is not None:old.deleteLater()
            self.show_hangul_status()
        except Exception as exc:QMessageBox.warning(self,'한글 변환 준비 실패',str(exc))

    def set_image_engine(self,mode):
        if mode not in ('auto','qt','vips','pillow') or mode==self.image_engine:return
        self.image_engine=mode;self.settings.setValue('image_engine',mode)
        self.image_backend.engine_mode=mode;self.image_backend.reset()
        self.preview_image_backend.engine_mode=mode;self.preview_image_backend.reset()
        for key in list(self.thumbs):
            if is_image_source(key[0]):self.thumbs.pop(key)
        self.requested={k for k in self.requested if not is_image_source(k[0])}
        self.large_thumbs_requested={k for k in self.large_thumbs_requested if not is_image_source(k[0])}
        self.thumb_errors={k:v for k,v in self.thumb_errors.items() if not is_image_source(k[0])}
        self.prioritize_thumbnails();self.canvas.viewport().update()
        editor=self.preview_dialog
        if editor is not None and not editor.closed:
            if is_image_source(editor.page.path):
                editor.token=self.next_preview_token();editor.requested_side=0;editor.request_image()

    def show_donation(self, parent=None):
        """제공받은 QR 원본을 내장해 별도 파일 없이 표시한다."""
        source=QPixmap()
        if not source.loadFromData(base64.b64decode(_DONATION_QR_PNG_BASE64),'PNG'):
            QMessageBox.warning(self,'도네이션','후원 QR 이미지를 읽지 못했습니다.');return
        dialog=QDialog(parent if isinstance(parent,QWidget) else self)
        dialog.setObjectName('donation_dialog');dialog.setWindowTitle('도네이션')
        dialog.setWindowIcon(application_icon());dialog.resize(455,550)
        layout=QVBoxLayout(dialog);layout.setContentsMargins(24,20,24,20);layout.setSpacing(14)
        title=QLabel(APP_NAME);title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet('font-size:16px;font-weight:600;');layout.addWidget(title)
        qr=QLabel();qr.setObjectName('donation_qr');qr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # QR 원본을 정수 배율로 확대하고, 보간으로 경계가 흐려지지 않게 한다.
        qr.setPixmap(source.scaled(source.size()*3,Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.FastTransformation))
        qr.setStyleSheet('background:#fff;border-radius:12px;padding:16px;')
        layout.addWidget(qr,0,Qt.AlignmentFlag.AlignCenter)
        note=QLabel('휴대폰으로 QR을 스캔해 주세요.')
        note.setObjectName('donation_status');note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setWordWrap(True);note.setStyleSheet('color:#888;font-size:12px;');layout.addWidget(note)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.button(QDialogButtonBox.StandardButton.Close).setText('닫기')
        buttons.rejected.connect(dialog.accept);layout.addWidget(buttons)
        dialog.exec();dialog.deleteLater()

    def github_repository_url(self):
        try:return normalize_github_repository(self.settings.value('github_repository_url',PROJECT_GITHUB_URL,type=str))
        except ValueError:return ''

    def show_settings(self, parent=None, tab='general'):
        dialog = QDialog(parent if isinstance(parent,QWidget) else self);dialog.setWindowTitle('옵션');dialog.resize(760,690)
        dialog.setWindowIcon(corner_icon('options'))
        outer=QVBoxLayout(dialog);tabs=QTabWidget();tabs.setObjectName('settings_tabs');outer.addWidget(tabs)
        general=QWidget();layout=QVBoxLayout(general);form=QFormLayout();layout.addLayout(form)
        scroller=QScrollArea();scroller.setWidgetResizable(True);scroller.setWidget(general);tabs.addTab(scroller,'기본')
        size = QSlider(Qt.Orientation.Horizontal);size.setRange(110,320);size.setValue(self.card_size)
        force = QSlider(Qt.Orientation.Horizontal);force.setRange(0,65);force.setValue(self.repulsion)
        animation = QCheckBox();animation.setChecked(self.animate)
        dark = QCheckBox();dark.setChecked(self.dark)
        numbers = QCheckBox();numbers.setChecked(self.show_numbers)
        rename = QCheckBox();rename.setChecked(self.rename_after)
        mode = QComboBox();mode.addItems(['선택 페이지를 한 PDF로','페이지별 PDF로']);mode.setCurrentIndex(int(self.separate))
        form.addRow('썸네일 크기',size);form.addRow('자석 반발 강도',force)
        form.addRow('움직임 / 선택 테두리 애니메이션',animation)
        form.addRow('어두운 배경',dark);form.addRow('쪽수 표시',numbers)
        form.addRow('밖으로 복사한 뒤 이름 입력',rename);form.addRow('사본 구성',mode)
        reader_mode=QComboBox();reader_mode.setObjectName('image_engine')
        for label,value in [('자동 (형식별 선택)','auto'),('Qt 우선','qt'),('libvips 우선','vips'),('Pillow 호환','pillow')]:
            reader_mode.addItem(label,value)
        reader_mode.setCurrentIndex(reader_mode.findData(self.image_engine))
        reader_mode.currentIndexChanged.connect(lambda:self.set_image_engine(reader_mode.currentData()))
        form.addRow('그림 읽기 엔진',reader_mode)
        reader_note=QLabel('자동: JPG·WebP·BMP → Qt / PNG·TIFF → libvips\n'
            'libvips 미설치·읽기 실패 시 다른 엔진으로 읽습니다.\n'
            'libvips 설치: python -m pip install "pyvips[binary]"')
        reader_note.setWordWrap(True);reader_note.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        reader_note.setStyleSheet('color:#888;font-size:11px;');layout.addWidget(reader_note)
        engines=[self.image_backend]
        if self.preview_dialog is not None:engines.append(self.preview_dialog.image_backend)
        recent=next((e for e in reversed(engines) if e.last_engine),None)
        if recent is not None:
            state=QLabel('최근 그림 읽기: '+{'qt':'Qt QImageReader','vips':'libvips','pillow':'Pillow'}[recent.last_engine]+
                         (' · 대체 엔진 사용' if recent.last_note else ''))
            state.setStyleSheet('color:#888;font-size:11px;');state.setToolTip(recent.last_note);layout.addWidget(state)
        jpg_button=QPushButton('JPG to PDF');jpg_button.setObjectName('jpg_to_pdf')
        jpg_button.setStyleSheet('QPushButton{background:#b82b47;color:white;border:0;border-radius:6px;padding:9px;font-weight:bold;} QPushButton:hover{background:#d53755;}')
        jpg_button.setToolTip('현재 그림·선택한 그림 또는 파일/폴더를 한 PDF로 변환')
        jpg_button.clicked.connect(lambda:(dialog.accept(),QTimer.singleShot(0,self.jpg_to_pdf)));layout.addWidget(jpg_button)
        for label,callback in [('PDF · 그림 · ZIP/CBZ 추가',self.open_files),('폴더 추가 (하위 폴더 포함)',self.open_folder),('선택 페이지 저장',self.save_selected),('되돌리기',self.undo),('다시 실행',self.redo),('목록 비우기',self.clear)]:
            button = QPushButton(label)
            button.clicked.connect(lambda _checked=False,cb=callback:(dialog.accept(),cb()))
            layout.addWidget(button)
        desktop=QPushButton('바탕화면 아이콘 만들기');desktop.setIcon(application_icon())
        desktop.setEnabled(sys.platform=='win32');desktop.clicked.connect(self.create_desktop_icon);layout.addWidget(desktop)
        register = QPushButton('Windows PDF 연결 등록 / 기본 앱 설정')
        register.setEnabled(sys.platform == 'win32'); register.clicked.connect(self.register_pdf_handler)
        layout.addWidget(register)
        temp_button=QPushButton('임시파일 폴더 열기');temp_button.clicked.connect(self.open_temp_folder);layout.addWidget(temp_button)
        temp_note=QLabel('읽기 취소: 이미 표시한 쪽은 유지합니다.\n'
            '작업 임시파일은 미사용 상태에서 정리합니다. 복사·드래그 전달용 사본은 남습니다.\n'
            f'이전 버전·비정상 종료의 잔여 파일을 수동 삭제할 때는 외부 붙여넣기를 마치고 모든 {APP_NAME} 창을 닫으세요.')
        temp_note.setWordWrap(True);temp_note.setStyleSheet('color:#777;font-size:11px;');layout.addWidget(temp_note)
        if self.cleanup_failures:
            pending=QLabel(f'정리하지 못한 작업 임시파일: {len(self.cleanup_failures)}개 · 종료 시 재시도');layout.addWidget(pending)
        hint = QLabel('기본: 크게 보기 + 썸네일\n오른쪽 테두리: 썸네일 접기 / +로 펼치기\n폴더 PDF: 첫 장 + 전체 쪽수 · 더블클릭으로 전체 열기\nPDF 카드 저장·복사·변환: 뒷장 포함\nPDF 테두리: 붉은색 · 그림: 파랑~초록\n확대 화면 드롭: 새로 열기 · 썸네일 드롭: 위치에 추가\n, / . 또는 [ / ]: 같은 폴더의 이전 / 다음 파일\n일반 PDF·그림 시작: PDF·그림만 이동\n폴더·ZIP 직접 열기 시작: 폴더·압축파일도 이동\n다음 쪽: → / Space / PgDown · 이전 쪽: ← / Backspace / PgUp\n아래 키는 기본값이며 단축키 탭에서 변경 가능\nCtrl+S: 전체 PDF를 원본 이름-정(번호)로 저장\nCtrl+T: 전체 PDF 번역 · Ctrl+H: 한글 변환 · Ctrl+O: 옵션\nCtrl+Shift+O: 파일 추가\nCtrl 누르기: 저장(S) / 번역(T) / 한글(H) / 옵션(O) 표시\n목록 휠: 빠르게 · Ctrl+휠: 조금씩\nCtrl/Shift: 선택 · Ctrl+C/V: 페이지 복사 / 붙여넣기\n우클릭: 빈 페이지 · Ctrl+Z/Y: 되돌리기 / 다시 실행\n더블클릭: 크게 보기 · 확대창 우클릭: 글/그림 편집\n확대창 Ctrl+V: 그림/문자 붙여넣기 · 선택 후 Del: 삭제\n양쪽 화살표: 한 장 이동 · 잡고 위/아래: 연속 탐색\n약 2cm 안: 한 장씩 · 더 당기기: 가속 (주황→붉은 테두리)\n드래그 위치 유지: 계속 이동 · 시작 위치로 당기기: 정지\n확대창 휠: 크기 조절 · 드래그 중 우클릭/Esc: 취소\n하단: 현재 쪽/전체 장수 항상 표시\nDelete: 작업목록에서 제외 (원본 유지)')
        hint.setStyleSheet('color:#777;font-size:11px;');layout.addWidget(hint)
        layout.addStretch()
        translation=TranslationSettings(self,dialog);tabs.addTab(translation,'번역')
        hangul=HangulSettings(self,dialog);tabs.addTab(hangul,'한글 변환')
        keyboard=ShortcutSettings(self);tabs.addTab(keyboard,'단축키')
        community=CommunitySettings(self);tabs.addTab(community,'소식')
        tabs.setCurrentIndex({'translation':1,'hangul':2,'shortcuts':3,'community':4}.get(tab,0))
        # 탭의 스크롤 영역 밖에 두어 어느 탭에서도 최하단에 고정된다.
        footer=QHBoxLayout();footer.setSpacing(6)
        version=QLabel(f'v{APP_VERSION}');version.setObjectName('app_version')
        version.setStyleSheet('color:#888;font-size:11px;');version.setToolTip(APP_NAME)
        footer.addWidget(version);footer.addStretch()
        for label,name,callback in [
                ('블로그','blog_button',lambda:QDesktopServices.openUrl(QUrl(BLOG_URL))),
                ('GitHub','github_button',lambda:QDesktopServices.openUrl(QUrl(self.github_repository_url()))
                 if self.github_repository_url() else tabs.setCurrentWidget(community))]:
            link=QPushButton(label);link.setObjectName(name)
            link.setStyleSheet('QPushButton{color:#80848b;background:transparent;border:1px solid #aeb2b9;border-radius:5px;padding:5px 9px;font-size:11px;} QPushButton:hover{color:#646970;background:rgba(128,132,139,15);}')
            link.clicked.connect(lambda _checked=False,cb=callback:cb());footer.addWidget(link)
        donation=QPushButton('도네이션');donation.setObjectName('donation_button')
        donation.setToolTip('후원 QR 보기')
        donation.setStyleSheet('QPushButton{color:#80848b;background:transparent;border:1px solid #aeb2b9;'
            'border-radius:5px;padding:5px 11px;font-size:11px;}'
            'QPushButton:hover{color:#646970;border-color:#858b94;background:rgba(128,132,139,15);}'
            'QPushButton:pressed{background:rgba(128,132,139,30);}'
            'QPushButton:focus{border-color:#858b94;}')
        donation.clicked.connect(lambda _checked=False:self.show_donation(dialog));footer.addWidget(donation)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.button(QDialogButtonBox.StandardButton.Close).setText('닫기')
        buttons.rejected.connect(dialog.accept);footer.addWidget(buttons);outer.addLayout(footer)
        def apply():
            self.card_size = size.value();self.repulsion = force.value();self.animate = animation.isChecked()
            self.dark = dark.isChecked();self.show_numbers = numbers.isChecked()
            self.rename_after = rename.isChecked();self.separate = bool(mode.currentIndex())
            self.canvas.layout_pages();self.empty_preview.update();self.thumbnail_rail.sync()
            if self.preview_dialog is not None and not self.preview_dialog.closed:
                self.preview_dialog.view.setBackgroundBrush(QColor('#181b24' if self.dark else '#edf0f5'))
        for control in (size,force):control.valueChanged.connect(apply)
        for control in (animation,dark,numbers,rename):control.toggled.connect(apply)
        mode.currentIndexChanged.connect(apply)
        dialog.exec();self.save_settings();dialog.deleteLater()

    def register_pdf_handler(self):
        if sys.platform != 'win32':
            return
        try:
            import winreg
            import ctypes
            launcher=install_windows_launcher()
            for key,name,value in windows_registration_values(launcher['command'],str(launcher['icon'])):
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER,key) as handle:
                    winreg.SetValueEx(handle,name,0,winreg.REG_SZ,value)
            ctypes.windll.shell32.SHChangeNotify(0x08000000,0,None,None)
            QMessageBox.information(self,'PDF 연결 등록',
                f'{APP_NAME}을 열기 후보로 등록했습니다.\n\nWindows 설정 → 앱 → 기본 앱 → .pdf 검색 → {APP_NAME} 선택\n\n'
                '프로그램 업데이트 후 이 버튼을 다시 누르면 등록된 사본도 갱신됩니다.\n실행에 사용한 Python 환경은 유지해주세요.')
            os.startfile('ms-settings:defaultapps')
        except Exception as exc:
            QMessageBox.warning(self,'Windows PDF 연결',str(exc))

    def create_desktop_icon(self):
        if sys.platform!='win32':return
        try:
            launcher=install_windows_launcher()
            path=create_windows_shortcut(launcher)
            QMessageBox.information(self,'바탕화면 아이콘',
                f'{APP_NAME} 실행 바로가기를 만들었습니다.\n\n{path}\n\n'
                '이 바로가기로 실행하세요. 업데이트한 파일에서 이 버튼을 다시 누르면 실행 사본과 아이콘도 갱신됩니다.')
        except Exception as exc:
            QMessageBox.warning(self,'바탕화면 아이콘',str(exc))

    def save_settings(self):
        for key,value in {'size':self.card_size,'repulsion':self.repulsion,'animate':self.animate,'dark':self.dark,'numbers':self.show_numbers,'rename':self.rename_after,'separate':self.separate,'auto_preview':self.auto_preview,'image_engine':self.image_engine}.items():
            self.settings.setValue(key,value)

    def closeEvent(self,event):
        if self.hangul_dialog is not None and self.hangul_dialog.busy:
            self.show_hangul_status();event.ignore();return
        if self.translation_busy or (self.usage_thread is not None and self.usage_thread.isRunning()):
            QMessageBox.information(self,'DeepL 작업 중','진행 중인 DeepL 작업을 마친 뒤 프로그램을 종료하세요.')
            event.ignore();return
        if self.pending_import or self.imports or self.import_cancelling:
            self.cancel_clear();self.close_after_import=True;self.cancel_import();event.ignore();return
        if self.preview_dialog is not None and self.preview_dialog.paste_queue:
            QTimer.singleShot(120,self.close);event.ignore();return
        if self.preview_dialog is not None and self.preview_dialog.has_pending_move():
            self.preview_dialog.after_move = self.close; self.preview_dialog.commit_move(); event.ignore(); return
        if self.preview_dialog is not None and self.preview_dialog.busy:
            event.ignore(); return
        if self.has_unsaved_changes():
            choice = QMessageBox.question(self, '수정본 저장', '내보내지 않은 수정 내용이 있습니다.\n현재 순서의 전체 페이지를 사본으로 저장할까요?',
                                          QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                                          QMessageBox.StandardButton.Save)
            if choice == QMessageBox.StandardButton.Cancel:
                event.ignore(); return
            if choice == QMessageBox.StandardButton.Save and not self.save_revision():
                event.ignore(); return
        self.closing=True;self.replacement_paths=None;self.navigation_request=None
        if self.preview_dialog is not None:
            self.preview_dialog.close()
        self.clear_timer.stop();self.clear_pending=False
        self.save_settings();self.input_backend.stop();self.backend.stop();self.image_backend.stop();self.preview_image_backend.stop();self.navigation_backend.stop()
        self.cleanup_working_files(closing=True)
        super().closeEvent(event)


def main():
    set_windows_app_identity()
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME);app.setApplicationDisplayName(APP_NAME);app.setApplicationVersion(APP_VERSION)
    app.setStyle('Fusion')
    app.setWindowIcon(application_icon())
    paths = [p for p in sys.argv[1:] if supported_input(p)]
    window = Window(startup_pdf_count=len(paths));window.show()
    if paths:QTimer.singleShot(0,lambda:window.add_files(paths))
    return app.exec()


if __name__ == '__main__':
    raise SystemExit(main())
