"""Release preparation and GitHub CLI backend; standard library only, no startup I/O."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import threading
import time
from urllib.parse import urlparse
import uuid
import zipfile

from build_common import VERSION, BuildError, Cancelled, atomic_json, read_json, inspect_source, sha256, clean_environment, kill_tree

DEFAULT_REPO = 'faintstar85-source/the-viewer'
OFFICIAL_LINKS = {
    'CLI 설치': 'https://cli.github.com/',
    '로그인': 'https://cli.github.com/manual/gh_auth_login',
    '릴리스 생성': 'https://cli.github.com/manual/gh_release_create',
    '파일 업로드': 'https://cli.github.com/manual/gh_release_upload',
    '릴리스 공개': 'https://cli.github.com/manual/gh_release_edit',
    '첨부파일 검증': 'https://docs.github.com/en/rest/releases/assets',
}

KNOWN_NOTES = {
    '3.12.2': (
        '- 서로 다른 캡처 여백과 높이를 맞추려고 그림을 세로로 늘리던 정렬 문제를 수정했습니다.\n'
        '- 후보를 묶을 때 이미 합쳐진 사각형의 빈 공간까지 다시 연결하던 문제를 수정했습니다. 실제로 인접한 원래 영역끼리 묶습니다.\n'
        '- 선화·종이 스캔에서 제한된 선 주변 재샘플링 흔적을 구분해 JPEG·축소·이동으로 생기는 오탐을 줄였습니다.\n'
        '- 정렬 뒤 겹치지 않는 밝은 무채색 종이 여백은 별도 기록합니다. 실제 그림·문자가 잘린 가장자리는 보류를 유지합니다.\n'
        '- PDF 문자 정렬 좌표도 같은 비율 기준으로 처리하며, 추출 문자와 서식 변경의 직접 비교를 유지합니다.\n'
        '- 좌우 듀얼 보기·오른쪽 파일 드롭·붉은 클립·동시 이동·원형 후보·변환 검토뷰·짧고 굵은 [+]를 유지합니다.\n\n'
        '첨부된 두 흑백 그림: 육안으로 확인한 10곳에 대응하는 후보 10곳을 양쪽에 표시했습니다.\n'
        '파일 순서 반전, 비교 그림의 75% 축소, JPEG 품질 85 재압축에서도 해당 10곳을 표시했습니다.\n'
        '동일 그림의 재압축·시작 위치/여백 변경은 후보 0개, 실제 내용 잘림은 보류였습니다.\n'
        '첨부 사례 검사 26개, 좌우 보기·정렬 44개, 드롭 39개, 변환 검토 43개가 통과했습니다(합계 152개).\n'
        '한글 PDF 및 캡처의 오타, 위치만 달라진 같은 PDF도 별도 검사했습니다.\n'
        '위 결과는 검사한 사례의 결과입니다. 공통 특징 점수는 전체 내용의 동일성 확률이 아닙니다.\n'
        '검출 한계: 기존 OMORI 원본 예시는 7곳 중 6곳, 제어 예시의 단독 1×1픽셀 변경은 미검출입니다.\n'
        'Qt offscreen 환경과 실제 작업 프로세스를 사용했습니다. Windows 탐색기 드래그·EXE 실행은 여기서 검사하지 않았습니다.\n'
        '번역 완료 검사는 로컬 PDF 결과를 사용했으며 DeepL 실서버와 실제 GitHub 공개는 실행하지 않았습니다.\n'
        'HWP/HWPX는 간편 읽기 화면이며 실제 한컴 출력과 배치가 다를 수 있습니다.\n'
    ),
    '3.12.1': (
        '- 오른쪽 듀얼 화면, 파일명 줄, 썸네일 머리글에 파일을 끌어 넣어 오른쪽 비교 대상을 바꿀 수 있습니다.\n'
        '- 왼쪽의 현재 페이지·편집 상태·확대 배율·선택을 유지하며 오른쪽에서 새 파일을 읽습니다.\n'
        '- 여러 파일을 함께 넣으면 오른쪽에서 한 묶음으로 넘겨 볼 수 있습니다. 반복 드롭도 오른쪽 쪽 수를 중복시키지 않습니다.\n'
        '- 읽는 동안 동시 이동·분석을 잠시 멈추고, 완료 후 현재 동시 이동 설정에 맞춰 다시 연결합니다.\n'
        '- 취소·읽기 실패·창 닫기·연속 드롭을 처리하며, 연속 드롭에서는 마지막 비교 대상이 표시됩니다.\n'
        '- 빈 화면과 문서 변환 화면의 [+]를 팔이 짧고 두께가 굵은 채워진 십자로 바꿨습니다.\n'
        '- 진행률이 아래부터 차오르고 완료 시 십자가 네모로 커지는 표시를 유지합니다. 오른쪽 변환 표시는 완료 때도 오른쪽에 남습니다.\n'
        '- 오른쪽 새 화면의 초기 맞춤이 왼쪽 확대 배율까지 바꾸던 문제를 수정했습니다.\n'
        '- 좌우 듀얼 보기·가운데 펼침 버튼·휠 표시·OpenCV 정렬·원형 차이 후보·보류 판정·변환 후 검토뷰를 유지합니다.\n\n'
        'Qt offscreen 환경에서 실제 읽기·변환 작업 프로세스와 드래그 이벤트를 검사했습니다.\n'
        '오른쪽 드롭 39개, 좌우 비교·정렬 44개, 변환 검토 43개 항목이 통과했습니다(합계 126개).\n'
        'Windows 탐색기에서의 실제 마우스 드롭 및 Windows EXE 빌드·실행은 여기서 검사하지 않았습니다.\n'
        '번역 완료 검사는 준비된 PDF 결과를 사용했으며 DeepL 실서버와 실제 GitHub 공개는 실행하지 않았습니다.\n'
        '차이 표시는 검토 후보이며 모든 오타·차이 검출을 보장하지 않습니다. HWP/HWPX는 간편 읽기 화면입니다.\n'
    ),
    '3.12.0': (
        '- 썸네일 위의 듀얼 보기 버튼에서 오른쪽 비교 화면이 아래로 펼쳐집니다.\n'
        '- 원본과 비교 쪽을 왼쪽·오른쪽에 표시하고, 가운데 구분선이 넓어지며 버튼이 나타납니다.\n'
        '- 동시 이동을 켜면 양쪽 붉은 클립이 잠기고 페이지·확대·스크롤이 양방향으로 연결됩니다.\n'
        '- 연결 상태에서는 움직이는 마우스 휠 표시가 나타납니다. 클립을 풀면 동시 이동도 풀립니다.\n'
        '- 자동 정렬은 차이 비교를 켜지 않아도 실행되며, 검증된 정렬을 실제 화면 위치에 적용합니다.\n'
        '- 위치가 달라 겹치지 않는 가장자리가 있으면 정렬 위치를 보여 주면서도 전체 판정은 보류합니다.\n'
        '- 차이 후보는 양쪽에 커졌다 작아지는 원형으로 표시합니다.\n'
        '- 오른쪽 썸네일 버튼에서 비교 파일을 바꾸고, 접으면 원래 썸네일 화면을 복구합니다.\n'
        '- 번역 PDF 및 HWP/HWPX 저장 후 원본·결과 검토뷰 자동 열기를 유지합니다.\n\n'
        '기본 휠: 페이지 이동. 기본 ↑/↓: 확대·축소. 단축키 설정에서 휠 동작을 바꿀 수 있습니다.\n'
        'Qt/OpenCV 실제 작업 프로세스로 좌우 보기·연동·정렬 44개 및 변환 검토 43개 항목을 검사했습니다.\n'
        '번역 완료 처리 검사는 준비된 PDF 결과를 사용했으며 DeepL 실서버는 호출하지 않았습니다.\n'
        'Windows EXE 빌드·실행 및 실제 GitHub 공개는 여기서 실행하지 않았습니다.\n'
        '차이 후보 없음은 문서 전체의 동일성 확정이 아닙니다. HWP/HWPX는 간편 읽기 화면입니다.\n'
    ),
    '3.11.2': (
        '- 번역 PDF와 HWP/HWPX 결과를 저장하면 별도 검토뷰를 자동으로 엽니다.\n'
        '- 위에는 변환 당시 원본, 아래에는 실제 저장한 결과를 표시합니다.\n'
        '- 쪽 수가 같으면 붉은 클립과 페이지·확대·스크롤 연동을 켭니다.\n'
        '- 쪽 수가 다르면 추가 결과 쪽을 볼 수 있도록 독립 이동합니다.\n'
        '- 완료 안내에서 검토뷰를 다시 열 수 있습니다.\n'
        '- 기존 OpenCV 자동 정렬과 커졌다 작아지는 원형 차이 후보 표시를 유지합니다.\n\n'
        'HWP/HWPX 화면은 간편 읽기 결과이며 한컴의 실제 출력과 배치가 다를 수 있습니다.\n'
        '차이 표시는 검토 후보입니다. 모든 오타·차이 검출을 보장하지 않습니다.\n'
    )
}



KNOWN_NOTES['3.12.3'] = (
    '- Windows 설치 EXE 생성을 추가했습니다. 현재 사용자 설치·바탕화면/시작 메뉴 바로가기·제거 항목을 제공합니다.\n'
    '- 정 → 소식과 설정 하단에서 업데이트를 확인할 수 있습니다. 시작 시 하루 한 번 확인은 끌 수 있습니다.\n'
    '- GitHub 정식 릴리스의 설치 파일을 SHA-256과 크기로 확인한 뒤, 저장 확인·뷰어 종료·설치 순서로 연결합니다.\n'
    '- 패키징 도구 1.4.0은 설치 EXE·ZIP·PY·버전 안내를 한 릴리스에 올리고 첨부파일을 검사합니다.\n'
    '- 설치 방식이 달라도 기존 사용자 설정은 유지합니다. 더 낮은 버전의 설치를 차단합니다.\n'
    '- 실제 Windows 설치/제거·여러 PC 업데이트·GitHub 공개는 이 환경에서 실행하지 않았습니다. 첫 배포는 Windows PC에서 확인하세요.\n'
) + KNOWN_NOTES['3.12.2']

def default_notes(version: str) -> str:
    if version == '3.13.38':
        return '- PDF 읽기 작업 프로세스가 GUI·편집 모듈보다 먼저 시작하도록 구성되어 있습니다.\n- 일반 PDF는 PDFium에서 읽으며, 양식 페이지와 편집 요청은 PY에 포함된 호환 코드로 처리합니다.\n- PDF 문자 검색, 검색 결과 위치 표시와 검색 전 위치로 돌아가기를 지원합니다.\n- 패키징 검사 요청을 v3.13.38의 render/preview/search/editinfo 형식에 맞췄습니다.\n- GitHub 매니저가 _viewer_fast_pdf_worker를 인식하고 pypdfium2==5.14.0을 기록하도록 수정했습니다.\n'
    if version == '3.13.3':
        return ('- 글자 이동/삭제 시 페이지 전체를 다시 생성하지 않고 선택한 원본 글자 연산만 분리합니다. 원래 글꼴·간격과 주변 배치를 검증합니다.\n'
                '- 사진 위 비율 유지 버튼은 정사각형/직사각형으로 전환됩니다. 8개 핸들로 가로·세로를 따로 조절할 수 있습니다.\n'
                '- 사진·추가 글자·흰색 도형에 맨 앞/맨 뒤와 한 단계 위/아래 Z 순서 버튼을 추가했습니다.\n'
                '- 흰색 덮기는 다시 선택·이동·크기 변경·삭제할 수 있는 벡터 사각형입니다.\n'
                '- 추가 문장은 한 개체로 선택하며, 글자 선택 시 좌표 대신 글꼴·크기·굵게·색상과 실제 PDF 미리보기를 표시합니다. 적용은 실행 취소 한 단계로 확정됩니다.\n'
                '- 원본 페이지 내용은 배경 한 레이어로 유지합니다. 공유 Form/불완전한 글자 선택/복잡한 클리핑은 안전하게 편집을 중단할 수 있습니다.\n'
                '- 기존 설정 정리·PDF/JPG/JPEG 통합 등록·클립 없는 동시 이동·비교·변환 검토를 유지합니다.\n'
                '- 제작 도구 1.5.5를 사용해 Windows EXE/설치 파일을 다시 빌드해야 합니다. 이번 제공물은 소스 PY와 제작 ZIP입니다.\n')
    if version == '3.13.2':
        return ('- 설정의 문서 읽기 탭과 AI/EPS 설정 진입을 제거했습니다. Office 문서는 설치된 LibreOffice를 자동 검색합니다.\n'
                '- 기본 설정에서 JPG to PDF·파일/폴더 추가·선택 저장·되돌리기/다시 실행·목록 비우기·연결 설정·임시폴더 버튼을 제거했습니다.\n'
                '- 차이 비교 아래 콤보박스를 가운데 정렬하고 차이 후보 이동 화살표 글자를 24px로 키웠습니다.\n'
                '- GitHub 주소를 faintstar85-source/the-viewer로 고정하고 주소 저장 버튼과 입력란을 제거했습니다.\n'
                '- 설치 옵션 하나로 PDF·JPG·JPEG 열기 등록을 함께 수행합니다. Windows 기본 앱 변경은 시스템 설정에서 사용자가 선택합니다.\n'
                '- python-hwpx 6.6.0의 Apache-2.0 LICENSE·NOTICE를 유지하고 라이선스 화면에 안내했습니다.\n'
                '- 클립 제거·동시 이동·자동 정렬·차이 후보·변환 결과 검토 기능을 유지합니다. 비교 알고리즘은 변경하지 않았습니다.\n'
                '- Windows 제작 도구 1.5.4로 실제 EXE·설치 파일을 다시 빌드하고 Windows에서 확인하세요.\n')
    if version == '3.13.1':
        return ('- 듀얼 보기 상단 클립 버튼과 클립 잠금에 따른 파일 이동 차단을 제거했습니다.\n'
                '- 동시 이동 버튼으로 페이지·확대·스크롤 연결을 켜고 끕니다. 현재 쪽 간격을 유지합니다.\n'
                '- 다른 문서 선택 시 비교 상대의 현재 쪽을 유지하고 새 쪽 간격을 기준으로 연결합니다.\n'
                '- 오른쪽 파일 드롭과 변환 결과 검토 화면을 클립 없이 사용할 수 있습니다.\n'
                '- 정 → 문서 읽기에는 LibreOffice 선택만 유지합니다. Office 문서는 설치된 LibreOffice가 필요합니다.\n'
                '- Ghostscript·LibreDWG와 DWG·AI·EPS·PS 읽기는 제외한 구성을 유지합니다.\n'
                '- Windows 제작 도구 1.5.3에 이번 변경 내역을 반영했습니다.\n'
                '- Windows EXE·설치 파일은 제작 PC에서 다시 빌드하고 확인하세요.\n')
    if version == '3.13.0':
        return ('- PDF 표시·텍스트 추출 엔진을 PDFium/pypdfium2로 교체했습니다.\n'
                '- PDF 페이지 저장은 pypdf, 새 PDF 생성은 ReportLab을 사용합니다.\n'
                '- PyMuPDF/MuPDF, Ghostscript, LibreDWG, libvips와 Qt Virtual Keyboard 동봉을 제외했습니다.\n'
                '- DWG·AI·EPS·PS는 지원 목록에서 제외했습니다.\n'
                '- Qt 기본 UI는 LGPLv3 경로로 배포하고 대응 소스·라이선스 고지를 동봉합니다.\n'
                '- Office 변환 엔진은 선택 사항이며 미동봉 시 설치된 외부 프로그램이 필요합니다.\n'
                '- 비교 결과는 검토 후보이며 모든 오타·차이 검출을 보장하지 않습니다.\n'
                '- 검증 범위와 Windows 빌드 결과는 첨부 버전 안내·검사 기록을 확인하세요.\n')
    if version == '3.12.4':
        return ('- 설치 시 PDF/JPG 열기 등록 선택과 Windows 기본 앱 설정 연결을 추가했습니다.\n'
                '- 정 메뉴에 업데이트 탭을 추가하고 인터넷에서 새 버전을 확인할 수 있습니다.\n'
                '- 업데이트 설치를 누르면 다운로드·크기/SHA-256 검사·저장 확인·설치로 이어집니다.\n'
                '- 다운로드 취소와 창 닫기는 자동 설치 연결을 취소합니다.\n'
                '- 비교 도움말 버튼과 설정의 긴 사용법 문단을 제거했습니다.\n'
                '- 비교 알고리즘의 검출 정확도를 변경한 버전은 아닙니다.\n')
    return KNOWN_NOTES.get(version, '수정 내역을 이곳에 입력하세요.\n')


def normalize_repo(value: str) -> str:
    value = value.strip().rstrip('/')
    if '://' in value:
        parsed = urlparse(value)
        if parsed.scheme != 'https' or parsed.netloc.lower() != 'github.com' or parsed.query or parsed.fragment:
            raise BuildError('저장소는 github.com 주소 또는 소유자/저장소 형식으로 입력하세요.')
        parts = parsed.path.strip('/').split('/')
        if len(parts) == 3 and parts[2] == 'releases': parts.pop()
        if len(parts) != 2: raise BuildError('저장소 주소를 확인하세요.')
        value = '/'.join(parts)
    if value.endswith('.git'): value = value[:-4]
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9_.-]{1,100}', value):
        raise BuildError('저장소는 소유자/저장소 형식으로 입력하세요.')
    if value.split('/')[1] in ('.', '..'): raise BuildError('저장소 이름을 확인하세요.')
    return value


def valid_tag(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}', value) or '..' in value or value.endswith(('.', '.lock')):
        raise BuildError('버전 태그는 v3.11.2처럼 영문·숫자·점·밑줄·하이픈으로 입력하세요.')
    return value


def find_gh() -> str:
    found = shutil.which('gh')
    if found: return str(Path(found).resolve())
    for parent in (os.environ.get('ProgramFiles', ''), os.environ.get('LOCALAPPDATA', '')):
        if parent:
            path = Path(parent) / 'GitHub CLI' / 'gh.exe'
            if path.is_file(): return str(path.resolve())
    return ''


def github_environment() -> dict:
    env=clean_environment()
    env.pop('GH_DEBUG',None); env.pop('GH_FORCE_TTY',None)
    env.update(GH_HOST='github.com',GH_PROMPT_DISABLED='1',GH_PAGER='cat',NO_COLOR='1')
    return env


def same_notes(actual: str, expected: str) -> bool:
    return actual.replace('\r\n','\n').strip()==expected.replace('\r\n','\n').strip()


def inspect_zip(path: Path, check=lambda: None, emit=lambda value: None) -> dict:
    if not path.is_file() or path.suffix.lower() != '.zip': raise BuildError('업로드할 ZIP을 선택하세요.')
    before = path.stat(); count = 0; total = 0; names = set()
    with zipfile.ZipFile(path) as archive:
        for entry in archive.infolist():
            check(); count += 1
            name = entry.filename
            if name in names: raise BuildError('ZIP에 중복된 파일명이 있습니다: ' + name)
            names.add(name)
            if name.startswith(('/', '\\')) or '\\' in name or ':' in name or '..' in name.split('/'):
                raise BuildError('ZIP에 안전하지 않은 경로가 있습니다: ' + name)
            if entry.flag_bits & 1: raise BuildError('암호화된 ZIP은 사용할 수 없습니다.')
            if entry.is_dir(): continue
            with archive.open(entry) as item:
                while True:
                    check(); block = item.read(1024*1024)
                    if not block: break
                    total += len(block)
            if count % 100 == 0: emit(f'[ZIP 원본 확인] {count}개 / {total // 1024**2} MB')
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise BuildError('확인 중 ZIP이 변경되었습니다.')
    return {'files': count, 'bytes_uncompressed': total, 'sha256': sha256(path, check), 'bytes': after.st_size}


def release_notes(version: str, tag: str, py_name: str, zip_name: str, changes: str, *, build_verified=False, installer_name='') -> str:
    if not changes.strip(): raise BuildError('버전 수정 내역을 입력하세요.')
    check_text = ('현재 PC의 빌드 기록에서 소스·완성 EXE·최종 위치 검사 통과와 ZIP 해시를 확인했습니다.'
                  if build_verified else '선택한 ZIP/PY 파일을 확인했습니다. 이 업로드 과정에서 Windows EXE 기능 검사는 실행하지 않았습니다.')
    return (f'# The Viewer {version}\n\n버전 태그: `{tag}`\n\n'
            '## 제공 파일\n\n' + (f'- `{installer_name}`: Windows 설치 파일. Python을 따로 설치하지 않고 사용합니다.\n' if installer_name else '') +
            f'- `{zip_name}`: ZIP 배포 파일. `Release_Notes` 폴더에 버전 안내가 들어 있습니다.\n'
            f'- `{py_name}`: 단독 뷰어 Python 소스. 필요한 라이브러리와 파일 변환 엔진이 있어야 실행할 수 있습니다.\n'
            '- `VERSION_GUIDE.txt`: 버전·사용 안내.\n- `RELEASE_NOTES.md`: 수정 내역.\n'
            '- `SHA256SUMS.txt`: 첨부파일 SHA-256 확인값.\n\n'
            f'## 수정 내역\n\n{changes.strip()}\n\n'
            '## 사용 방법\n\n' + ('설치 EXE에서 PDF/JPG 열기 등록을 선택하고 Windows 기본 앱 화면에서 연결합니다. 이후에는 정 → 업데이트 → 인터넷 업데이트 확인에서 새 버전을 확인하고 설치합니다.\n' if installer_name else '') +
            'ZIP을 압축 해제한 뒤, EXE 배포본이면 The_Viewer.exe를 실행합니다. '
            '_internal 폴더 등 동봉 파일을 함께 유지하세요.\n'
            'PY는 Python과 뷰어 의존성을 설치한 환경에서 실행합니다.\n\n'
            f'## 확인 내역\n\n{check_text}\n')


def version_guide(version: str, tag: str, notes: str) -> str:
    return (f'The Viewer {version}\n버전 태그: {tag}\n패키징·업로드 도구: {VERSION}\n\n'
            'ZIP과 PY는 GitHub Releases의 첨부파일로 제공합니다.\n'
            'ZIP 내부의 Release_Notes 폴더와 릴리스 본문에서 같은 수정 내역을 볼 수 있습니다.\n\n'
            + notes + '\n공식 GitHub CLI 안내\n'
            + '\n'.join(f'{label}: {url}' for label, url in OFFICIAL_LINKS.items()) + '\n')


def copy_checked(source: Path, target: Path, check=lambda: None, emit=lambda value: None) -> dict:
    before = source.stat(); digest = hashlib.sha256(); size = 0; last = time.monotonic()
    with source.open('rb') as src, target.open('xb') as dst:
        while True:
            check(); data = src.read(1024*1024)
            if not data: break
            dst.write(data); digest.update(data); size += len(data)
            if time.monotonic()-last > 2:
                emit(f'[업로드 파일 준비] {source.name} / {size // 1024**2} MB'); last=time.monotonic()
    after = source.stat()
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns) or sha256(target,check)!=digest.hexdigest():
        raise BuildError('복사 중 파일이 변경되었습니다: '+source.name)
    return {'name':target.name,'path':str(target),'bytes':size,'sha256':digest.hexdigest()}


def validate_build_link(link: dict | None, py: Path, zip_info: dict, source_info: dict) -> bool:
    if not link: return False
    if link.get('status') != 'passed' or link.get('windows_exe_checks_passed') is not True:
        raise BuildError('연결된 빌드에 EXE 검사 성공 기록이 없습니다.')
    if link.get('zip',{}).get('sha256') != zip_info['sha256'] or link.get('viewer_version') != source_info['version']:
        raise BuildError('연결된 빌드 ZIP/버전과 선택한 파일이 다릅니다.')
    record=link.get('release_py',{})
    if record.get('sha256') != source_info['sha256']:
        raise BuildError('연결된 빌드의 단독 뷰어 PY와 선택한 PY가 다릅니다.')
    required=source_info['required_check_count']
    if any(link.get(key) != required for key in ('source_checks','exe_checks','final_location_checks')):
        raise BuildError('연결된 빌드에 전체 기능 검사 통과 기록이 없습니다.')
    return True


def prepare_release(spec: dict, *, check=lambda: None, emit=lambda value: None) -> dict:
    repo=normalize_repo(spec['repo']); tag=valid_tag(spec['tag'])
    py=Path(spec['py']).expanduser().resolve(); chosen_zip=Path(spec['zip']).expanduser().resolve()
    source=inspect_source(py); zip_info=inspect_zip(chosen_zip,check,emit)
    verified=validate_build_link(spec.get('build_result'),py,zip_info,source)
    installer_path=Path(spec['installer']).expanduser().resolve() if spec.get('installer','').strip() else None
    if installer_path:
        from build_common import pe_machine
        expected_name='The_Viewer_Setup_'+source['version']+'_x64.exe'
        if tag!='v'+source['version']:
            raise BuildError('자동 업데이트용 설치 파일은 뷰어 버전과 같은 정식 태그(v'+source['version']+')로 배포하세요.')
        if not installer_path.is_file() or installer_path.name!=expected_name or pe_machine(installer_path) not in (0x14c,0x8664):
            raise BuildError('뷰어 버전과 같은 The_Viewer_Setup_'+source['version']+'_x64.exe를 선택하세요.')
    root=Path(spec['output']).expanduser().resolve(); root.mkdir(parents=True,exist_ok=True)
    folder=root/('TheViewer_Upload_'+tag+'_'+time.strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:6])
    folder.mkdir(exist_ok=False)
    py_name=f"The_Viewer_v{source['version']}.py"
    zip_name=f"The_Viewer_v{source['version']}_windows_x64.zip" if verified else chosen_zip.name
    if '#' in zip_name or zip_name.startswith('-'): zip_name=f"The_Viewer_v{source['version']}.zip"
    title=spec.get('title','').strip() or 'The Viewer '+source['version']
    notes=release_notes(source['version'],tag,py_name,zip_name,spec['changes'],build_verified=verified,
                        installer_name=installer_path.name if installer_path else '')
    guide=version_guide(source['version'],tag,notes)
    doc_bytes={'Release_Notes/VERSION_GUIDE.txt':guide.encode('utf-8-sig'),
               'Release_Notes/RELEASE_NOTES.md':notes.encode('utf-8')}
    staged_py=folder/py_name; py_record=copy_checked(py,staged_py,check,emit)
    staged_zip=folder/zip_name; original_record=copy_checked(chosen_zip,staged_zip,check,emit)
    if py_record['sha256']!=source['sha256'] or original_record['sha256']!=zip_info['sha256']:
        raise BuildError('안내 준비 중 원본 ZIP/PY가 변경되었습니다.')
    additions={}
    with zipfile.ZipFile(staged_zip,'r') as archive:
        for name, data in doc_bytes.items():
            if name in archive.namelist():
                if archive.read(name)!=data:
                    raise BuildError('ZIP의 기존 버전 안내와 입력한 안내가 다릅니다. 원래 빌드 ZIP을 선택하세요.')
            else: additions[name]=data
    if additions:
        with zipfile.ZipFile(staged_zip,'a',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
            for name,data in additions.items():
                check(); entry=zipfile.ZipInfo(name,(2020,1,1,0,0,0)); entry.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(entry,data)
    checked=inspect_zip(staged_zip,check,emit)
    assets=[dict(py_record), {'name':zip_name,'path':str(staged_zip),'bytes':checked['bytes'],'sha256':checked['sha256']}]
    installer_verified=False
    if installer_path:
        record=copy_checked(installer_path,folder/installer_path.name,check,emit)
        assets.append(record)
        linked=(spec.get('build_result') or {}).get('installer') or {}
        installer_verified=bool(verified and linked.get('sha256')==record['sha256'] and linked.get('bytes')==record['bytes']
                                and linked.get('compiled') is True and linked.get('version')==source['version'] and linked.get('repo')==repo)
    for name,data in [('VERSION_GUIDE.txt',guide.encode('utf-8-sig')),('RELEASE_NOTES.md',notes.encode('utf-8'))]:
        path=folder/name; path.write_bytes(data)
        assets.append({'name':name,'path':str(path),'bytes':len(data),'sha256':sha256(path,check)})
    sums=''.join(f"{a['sha256']}  {a['name']}\n" for a in assets)
    path=folder/'SHA256SUMS.txt'; path.write_text(sums,encoding='utf-8')
    assets.append({'name':path.name,'path':str(path),'bytes':path.stat().st_size,'sha256':sha256(path,check)})
    plan={'schema':1,'tool_version':VERSION,'repo':repo,'tag':tag,'title':title,'viewer_version':source['version'],
          'publish':bool(spec.get('publish',True)),'prerelease':bool(spec.get('prerelease',False)),
          'folder':str(folder),'notes':notes,'notes_path':str(folder/'RELEASE_NOTES.md'),
          'build_checks_verified':verified,'installer_build_verified':installer_verified,
          'zip_original_sha256':zip_info['sha256'],'assets':assets}
    atomic_json(folder/'Upload_Plan.json',plan)
    emit('[안내 준비 완료] '+str(folder))
    return plan


def verify_plan_files(plan: dict, check=lambda: None) -> None:
    normalize_repo(plan['repo']); valid_tag(plan['tag'])
    if len(plan['assets']) not in (5,6) or not {'VERSION_GUIDE.txt','RELEASE_NOTES.md','SHA256SUMS.txt'}<=set(a['name'] for a in plan['assets']):
        raise BuildError('ZIP·PY·버전 안내 업로드 목록이 누락됐습니다.')
    if sum(a['name'].lower().endswith('.zip') for a in plan['assets'])!=1 or sum(a['name'].lower().endswith('.py') for a in plan['assets'])!=1:
        raise BuildError('ZIP과 PY를 각각 하나씩 준비해야 합니다.')
    installers=[a for a in plan['assets'] if a['name'].lower().endswith('.exe')]
    if len(installers)!=len(plan['assets'])-5 or (installers and (installers[0]['name']!='The_Viewer_Setup_'+plan['viewer_version']+'_x64.exe' or plan['tag']!='v'+plan['viewer_version'])):
        raise BuildError('설치 파일명·버전 태그와 업로드 목록이 다릅니다.')
    names=set()
    for record in plan['assets']:
        check(); path=Path(record['path'])
        if record['name']!=path.name or record['name'] in names: raise BuildError('업로드 파일명 목록이 잘못되었습니다.')
        names.add(record['name'])
        if not path.is_file() or path.stat().st_size!=record['bytes'] or sha256(path,check)!=record['sha256']:
            raise BuildError('안내 준비 후 파일이 변경되었습니다. 안내를 다시 준비하세요: '+record['name'])
    if Path(plan['notes_path']).read_text(encoding='utf-8-sig')!=plan['notes']:
        raise BuildError('릴리스 안내가 변경되었습니다. 안내를 다시 준비하세요.')


def load_prepared_release(folder: Path, *, check=lambda: None, emit=lambda value: None) -> dict:
    """Resume checked, staged files, including plans written by tool 1.5.9."""
    folder=Path(folder).expanduser().resolve()
    try:
        plan=read_json(folder/'Upload_Plan.json')
        if not isinstance(plan,dict) or plan.get('schema')!=1:
            raise ValueError('지원하지 않는 준비 파일 형식입니다.')
        for key in ('repo','tag','title','viewer_version','notes'):
            if not isinstance(plan.get(key),str) or not plan[key].strip():
                raise ValueError('준비 파일에 필요한 정보가 없습니다: '+key)
        if type(plan.get('publish')) is not bool or type(plan.get('prerelease')) is not bool:
            raise ValueError('공개/시험 배포 설정을 확인할 수 없습니다.')
        if not isinstance(plan.get('assets'),list):
            raise ValueError('준비한 첨부파일 목록이 없습니다.')
        # Files may have been moved together. Use only basenames beneath the
        # chosen directory, then recheck their stored sizes/hashes and notes.
        for record in plan['assets']:
            name=record.get('name') if isinstance(record,dict) else None
            if not isinstance(name,str) or name in ('','.','..') or any(c in name for c in ('/','\\',':','\x00')):
                raise ValueError('준비 파일의 첨부파일명이 잘못되었습니다.')
            record['path']=str(folder/name)
        plan['folder']=str(folder);plan['notes_path']=str(folder/'RELEASE_NOTES.md')
        verify_plan_files(plan,check)
    except Cancelled:
        raise
    except (OSError,ValueError,KeyError,TypeError) as exc:
        raise BuildError('업로드 준비 폴더를 불러오지 못했습니다. Upload_Plan.json과 첨부파일이 함께 있어야 합니다.\n'+str(exc)) from exc
    emit('[준비 폴더 복원 완료] '+str(folder)+' / '+plan['tag'])
    return plan


def changes_from_notes(notes: str) -> str:
    before,separator,rest=notes.partition('## 수정 내역\n\n')
    if separator and '\n\n## 사용 방법\n\n' in rest:
        return rest.rsplit('\n\n## 사용 방법\n\n',1)[0]
    return notes


class GitHubClient:
    def __init__(self, gh: str, folder: Path, *, emit=lambda value: None, cancel=None):
        path=Path(gh).expanduser().resolve()
        if not path.is_file() or (os.name=='nt' and path.name.lower()!='gh.exe'):
            raise BuildError('GitHub CLI의 gh.exe 파일을 선택하세요.')
        self.gh=str(path); self.folder=Path(folder); self.folder.mkdir(parents=True,exist_ok=True)
        self.emit=emit; self.cancel=cancel or threading.Event(); self.current=None
        steps=[int(match.group(1)) for item in self.folder.iterdir()
               if (match:=re.fullmatch(r'gh_(\d+)\.(?:out|log)',item.name))]
        self.step=max(steps,default=0)
    def check(self):
        if self.cancel.is_set(): raise Cancelled('GitHub 작업 중지를 요청했습니다. 생성된 초안과 로컬 파일은 보존됩니다.')
    def command(self,args,*,timeout=180,allow_failure=False):
        self.check(); self.step+=1
        stem='gh_'+str(self.step).zfill(2); out=self.folder/(stem+'.out'); err=self.folder/(stem+'.log')
        env=github_environment()
        command=[self.gh,*map(str,args)]
        self.emit('[GitHub 실행] '+subprocess.list2cmdline(command))
        start=last=time.monotonic(); process=None
        try:
            with out.open('wb') as stdout, err.open('wb') as stderr:
                process=subprocess.Popen(command,cwd=str(self.folder),env=env,stdin=subprocess.DEVNULL,
                    stdout=stdout,stderr=stderr,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                self.current=process
                while process.poll() is None:
                    self.check()
                    if time.monotonic()-start>timeout: raise BuildError('GitHub 실행 제한시간 초과. 로그: '+str(err))
                    if time.monotonic()-last>5:
                        self.emit(f'[GitHub 실행 중] {args[0]} / {time.monotonic()-start:.0f}초'); last=time.monotonic()
                    time.sleep(.1)
                code=process.wait()
            text=out.read_text(encoding='utf-8-sig',errors='replace'); error=err.read_text(encoding='utf-8-sig',errors='replace')
            if error.strip(): self.emit(error[-6000:])
            if code and not allow_failure: raise BuildError(f'GitHub 명령 실패 ({code})\n'+(error or text)[-10000:])
            return code,text,error
        finally:
            if process is not None and process.poll() is None: kill_tree(process)
            self.current=None
    def api(self,endpoint,*,method='GET',payload=None):
        args=['api',endpoint,'--hostname','github.com','--method',method,
              '-H','Accept: application/vnd.github+json']
        if payload is not None:
            request=self.folder/('gh_request_'+uuid.uuid4().hex+'.json')
            atomic_json(request,payload);args.extend(['--input',str(request)])
        _,text,_=self.command(args)
        try:return json.loads(text)
        except ValueError as exc:
            raise BuildError('GitHub JSON 응답을 읽지 못했습니다. 준비 폴더의 gh_*.out/gh_*.log를 확인하세요.') from exc

    def validate_release(self,release,repo,tag,*,release_id=None):
        if not isinstance(release,dict) or type(release.get('id')) is not int or release['id']<=0 or type(release.get('draft')) is not bool:
            raise BuildError('릴리스 ID/초안 상태 응답이 잘못되었습니다.')
        if release.get('tag_name')!=tag:
            raise BuildError('GitHub 응답의 버전 태그가 다릅니다. 기존 릴리스와 첨부파일을 보존했습니다.')
        if release_id is not None and release['id']!=release_id:
            raise BuildError('작업 중 릴리스 ID가 변경되었습니다. 공개를 진행하지 않았습니다.')
        self.emit('[릴리스 확인] '+tag+' / ID '+str(release['id'])+' / '+('초안' if release['draft'] else '공개'))
        return release

    def remember_release(self,repo,tag,release):
        atomic_json(self.folder/'Release_State.json',{'schema':1,'repo':repo,'tag':tag,
            'create_started':True,'release_id':release['id']})

    def view_release(self,repo,tag,*,release_id=None):
        # The tag endpoint is documented for published releases. The authenticated
        # list endpoint includes drafts for users with push access; scan every page
        # so retrying an upload reuses the existing draft instead of creating one.
        normalize_repo(repo); valid_tag(tag)
        if release_id is not None:
            if type(release_id) is not int or release_id<=0:
                raise BuildError('저장된 릴리스 ID가 잘못되었습니다.')
            # Once its ID is known, do not depend on the listing to find a draft
            # or to confirm it after publishing. Retry reads only, never writes.
            for attempt,delay in enumerate((0,.3,1.0)):
                if delay and self.cancel.wait(delay):self.check()
                try:
                    release=self.api(f'repos/{repo}/releases/{release_id}')
                except Cancelled:raise
                except BuildError as exc:
                    if attempt==2:
                        raise BuildError('저장한 릴리스 ID '+str(release_id)+' 조회 실패. 같은 준비 폴더에서 다시 시도할 수 있습니다.\n'+str(exc)) from exc
                    continue
                return self.validate_release(release,repo,tag,release_id=release_id)
        matches=[]; page=1
        while True:
            self.check()
            try:
                batch=self.api(f'repos/{repo}/releases?per_page=100&page={page}')
            except Cancelled:
                raise
            except (BuildError,ValueError) as exc:
                raise BuildError('기존 릴리스 확인 실패. 권한/네트워크 오류를 새 릴리스 없음으로 처리하지 않습니다.\n'+str(exc)) from exc
            if not isinstance(batch,list) or len(batch)>100 or any(not isinstance(item,dict) for item in batch):
                raise BuildError('릴리스 목록 응답 형식이 잘못되었습니다. 초안을 새로 만들지 않았습니다.')
            matches.extend(item for item in batch if item.get('tag_name')==tag)
            if len(batch)<100:
                break
            page+=1
        if len(matches)>1:
            raise BuildError('같은 태그의 릴리스가 여러 개입니다. GitHub에서 '+tag+'의 초안을 확인하세요. 기존 파일은 보존했습니다.')
        if not matches:
            # Also resolve a pending tag directly; an empty REST listing alone
            # must not decide that no existing draft can be resumed.
            owner,name=repo.split('/')
            query=('query ViewerRelease($owner:String!,$name:String!,$tag:String!) {'
                   ' repository(owner:$owner,name:$name) {'
                   ' release(tagName:$tag) { databaseId tagName isDraft } } }')
            data=self.api('graphql',method='POST',payload={'query':query,
                'variables':{'owner':owner,'name':name,'tag':tag}})
            if not isinstance(data,dict) or data.get('errors'):
                raise BuildError('태그 직접 조회에 실패했습니다. 새 초안을 만들지 않았습니다.')
            repository=(data.get('data') or {}).get('repository')
            if not isinstance(repository,dict) or 'release' not in repository:
                raise BuildError('태그 직접 조회의 저장소 응답이 잘못되었습니다. 새 초안을 만들지 않았습니다.')
            node=repository['release']
            if node is None:return None
            if (not isinstance(node,dict) or node.get('tagName')!=tag or
                    type(node.get('databaseId')) is not int or node['databaseId']<=0 or
                    type(node.get('isDraft')) is not bool):
                raise BuildError('태그 직접 조회의 릴리스 정보가 잘못되었습니다.')
            return self.view_release(repo,tag,release_id=node['databaseId'])
        return self.validate_release(matches[0],repo,tag)

    def recover_release(self,repo,tag):
        for delay in (0,.3,1.0):
            if delay and self.cancel.wait(delay):self.check()
            release=self.view_release(repo,tag)
            if release is not None:
                self.remember_release(repo,tag,release);return release
        return None

    def create_draft(self,plan):
        repo=normalize_repo(plan['repo']);tag=valid_tag(plan['tag'])
        # Record the attempt before sending a write. A timeout can happen after
        # GitHub committed it; restarting must not blindly create another draft.
        atomic_json(self.folder/'Release_State.json',{'schema':1,'repo':repo,'tag':tag,
            'create_started':True,'release_id':None})
        try:
            release=self.api(f'repos/{repo}/releases',method='POST',payload={
                'tag_name':tag,'name':plan['title'],'body':plan['notes'],
                'draft':True,'prerelease':plan['prerelease']})
        except Cancelled:raise
        except BuildError as exc:
            release=self.recover_release(repo,tag)
            if release is not None:return release
            raise BuildError('초안 생성 결과를 확정하지 못했습니다. 중복 생성을 막기 위해 다시 만들지 않았습니다.\n'
                             '준비 폴더의 gh_*.out/gh_*.log를 확인하세요.\n'+str(exc)) from exc
        release=self.validate_release(release,repo,tag)
        self.remember_release(repo,tag,release)
        if not release['draft']:
            raise BuildError('초안 생성 응답이 공개 상태입니다. 자동 업로드를 중단했습니다.')
        self.emit('[초안 생성 완료] 응답 ID '+str(release['id'])+' 사용')
        return release

    def resume_or_find_release(self,repo,tag):
        state_path=self.folder/'Release_State.json'
        if not state_path.exists():return self.view_release(repo,tag)
        try:state=read_json(state_path)
        except (OSError,ValueError) as exc:
            raise BuildError('릴리스 재개 기록을 읽지 못했습니다. 준비 폴더를 보존하고 기록을 확인하세요.') from exc
        if (not isinstance(state,dict) or state.get('schema')!=1 or state.get('repo')!=repo or
                state.get('tag')!=tag or state.get('create_started') is not True):
            raise BuildError('릴리스 재개 기록의 저장소/태그가 다릅니다. 자동 생성을 중단했습니다.')
        if state.get('release_id') is not None:
            return self.view_release(repo,tag,release_id=state['release_id'])
        release=self.recover_release(repo,tag)
        if release is None:
            raise BuildError('이 준비 폴더에 초안 생성 요청 기록이 있지만 GitHub 결과를 확인하지 못했습니다. '
                             '중복 생성을 막기 위해 새 초안을 만들지 않았습니다. 준비 폴더의 gh_*.out/gh_*.log를 확인하세요.')
        return release
    def assets(self,repo,release_id):
        records=[]; page=1
        while True:
            self.check(); batch=self.api(f'repos/{repo}/releases/{release_id}/assets?per_page=100&page={page}')
            if not isinstance(batch,list): raise BuildError('첨부파일 목록 응답 형식이 잘못되었습니다.')
            records.extend(batch)
            if len(batch)<100: return records
            page+=1
    def verify_asset(self,repo,asset,record):
        if asset.get('state')!='uploaded' or asset.get('size')!=record['bytes']:
            raise BuildError('GitHub 첨부파일 상태/크기가 다릅니다: '+record['name'])
        digest=asset.get('digest')
        if digest:
            if digest.lower()!='sha256:'+record['sha256']: raise BuildError('GitHub 첨부파일 SHA-256이 다릅니다: '+record['name'])
        else:
            # Older assets may lack digest. Download from the authenticated asset API and hash.
            self.check(); self.step+=1; target=self.folder/f"verify_asset_{asset['id']}.bin"
            error_path=target.with_suffix('.log'); process=None
            try:
                with target.open('wb') as output,error_path.open('wb') as error:
                    env=github_environment()
                    process=subprocess.Popen([self.gh,'api',f"repos/{repo}/releases/assets/{asset['id']}",
                        '-H','Accept: application/octet-stream'],stdout=output,stderr=error,stdin=subprocess.DEVNULL,
                        env=env,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                    self.current=process; started=time.monotonic()
                    while process.poll() is None:
                        self.check()
                        if time.monotonic()-started>3600: raise BuildError('첨부파일 재다운로드 검증 제한시간 초과')
                        time.sleep(.1)
                    if process.wait(): raise BuildError('첨부파일 재다운로드 검증 실패: '+error_path.read_text(encoding='utf-8',errors='replace'))
                if target.stat().st_size!=record['bytes'] or sha256(target,self.check)!=record['sha256']:
                    raise BuildError('재다운로드한 첨부파일 해시가 다릅니다: '+record['name'])
            finally:
                if process is not None and process.poll() is None: kill_tree(process)
                self.current=None; target.unlink(missing_ok=True)
        self.emit('[첨부파일 SHA-256 확인] '+record['name'])
    def publish(self,plan):
        verify_plan_files(plan,self.check); repo=plan['repo']; tag=plan['tag']
        self.command(['auth','status','--hostname','github.com'])
        repository=self.api('repos/'+repo)
        if not repository.get('permissions',{}).get('push'):
            raise BuildError('로그인 계정에 이 저장소의 업로드 권한이 없습니다.')
        release=self.resume_or_find_release(repo,tag)
        if release is None:
            release=self.create_draft(plan)
        self.remember_release(repo,tag,release)
        if release.get('tag_name')!=tag: raise BuildError('GitHub 응답의 버전 태그가 다릅니다.')
        remote=self.assets(repo,release['id']); by_name={a['name']:a for a in remote}
        # Check all name conflicts before uploading anything. Never delete existing assets.
        missing=[]
        for record in plan['assets']:
            if record['name'] in by_name: self.verify_asset(repo,by_name[record['name']],record)
            else: missing.append(record)
        if not release.get('draft'):
            if missing or not same_notes(release.get('body') or '',plan['notes']):
                raise BuildError('이미 공개된 태그입니다. 기존 파일을 보존했습니다. 새 태그(예: '+tag+'-r2)를 입력하세요.')
        else:
            self.command(['release','edit',tag,'--repo',repo,'--title',plan['title'],'--notes-file',plan['notes_path'],
                          '--prerelease='+str(plan['prerelease']).lower()])
            for record in missing:
                self.check(); verify_plan_files(plan,self.check)
                self.command(['release','upload',tag,record['path'],'--repo',repo],timeout=3600)
            remote=self.assets(repo,release['id']); by_name={a['name']:a for a in remote}
            for record in plan['assets']:
                if record['name'] not in by_name: raise BuildError('업로드한 첨부파일이 없습니다: '+record['name'])
                self.verify_asset(repo,by_name[record['name']],record)
            if plan['publish']:
                verify_plan_files(plan,self.check)
                draft=self.view_release(repo,tag,release_id=release['id'])
                if draft is None or not draft.get('draft') or not same_notes(draft.get('body') or '',plan['notes']):
                    raise BuildError('공개 전 버전 안내 확인 실패. 릴리스는 초안으로 보존됩니다.')
                self.command(['release','edit',tag,'--repo',repo,'--draft=false'])
        final=self.view_release(repo,tag,release_id=release['id'])
        if final is None or not same_notes(final.get('body') or '',plan['notes']):
            raise BuildError('업로드 후 버전 안내 확인 실패')
        if plan['publish'] and final.get('draft'): raise BuildError('공개 완료 상태가 아닙니다.')
        if final.get('name')!=plan['title'] or bool(final.get('prerelease'))!=plan['prerelease']:
            raise BuildError('업로드 후 릴리스 제목/시험 배포 표시가 다릅니다.')
        final_assets={a['name']:a for a in self.assets(repo,final['id'])}
        for record in plan['assets']:
            if record['name'] not in final_assets: raise BuildError('최종 릴리스 첨부파일 누락: '+record['name'])
            self.verify_asset(repo,final_assets[record['name']],record)
        result={'status':'passed','repo':repo,'tag':tag,'url':final['html_url'],'draft':bool(final.get('draft')),
                'asset_count':len(plan['assets']),'all_assets_sha256_verified':True}
        atomic_json(self.folder/'Upload_Result.json',result)
        return result
