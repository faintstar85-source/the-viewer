"""Shared, standard-library-only helpers. No files are changed on import."""
from __future__ import annotations
import ast
import base64
import hashlib
import json
import os
import platform
import re
import shutil
import struct
import subprocess
import sys
import time
import zipfile
from pathlib import Path, PurePosixPath
from typing import Callable

VERSION = '1.5.10'
CONTROL_PREFIX = '@@TVBUILD '
REQUIRED_ENGINES = {
    'libreoffice': ['program/soffice.com', 'program/soffice.exe', 'program/soffice.bin',
                   'program/mergedlo.dll', 'program/bootstrap.ini', 'program/fundamental.ini',
                   'program/vcruntime140.dll', 'license.txt', 'SOURCE_INFO.txt',
                   'checks/word.docx', 'checks/excel.xlsx', 'checks/slides.pptx'],
}
# Exact fingerprint of the runtime that failed in this conversation. Not a version-wide blacklist.
KNOWN_FAILED_VCRUNTIME1 = '42b5f76f1f0ae03c93fc4c107adf83c5f14e86032474860032cfe672d0836546'
BINARY_PACKAGES = ('PySide6,PySide6-Essentials,PySide6-Addons,shiboken6,pypdfium2,'
                   'Pillow,numpy,scipy,lxml,pywin32,psutil,opencv-python-headless')

class BuildError(RuntimeError):
    pass

class Cancelled(BuildError):
    pass


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def atomic_json(path: Path, value) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temp, path)


def sha256(path: Path, check: Callable[[], None] = lambda: None) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while True:
            check()
            block = f.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def is_link(path: Path) -> bool:
    st = path.lstat()
    return path.is_symlink() or bool(getattr(st, 'st_file_attributes', 0) & 0x400)


def files_in(root: Path, check: Callable[[], None] = lambda: None) -> list[Path]:
    root = Path(root)
    if is_link(root):
        raise BuildError(f'링크 폴더는 사용하지 않습니다: {root}')
    files = []
    for base, dirs, names in os.walk(root, followlinks=False):
        check()
        for name in dirs + names:
            p = Path(base) / name
            if is_link(p):
                raise BuildError(f'링크/재분석 지점을 발견했습니다: {p}')
        files.extend(Path(base) / name for name in names)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix().casefold())


def safe_relative(value: str) -> str:
    if not isinstance(value, str) or not value or '\\' in value or ':' in value or '\x00' in value:
        raise BuildError(f'검사 목록의 경로가 잘못되었습니다: {value!r}')
    p = PurePosixPath(value)
    if p.is_absolute() or any(x in ('', '.', '..') or x.endswith((' ', '.')) for x in value.split('/')):
        raise BuildError(f'검사 목록의 경로가 잘못되었습니다: {value!r}')
    return value


def pe_machine(path: Path) -> int:
    with path.open('rb') as f:
        header = f.read(64)
        if len(header) != 64 or header[:2] != b'MZ':
            raise BuildError(f'Windows 실행파일 헤더가 아닙니다: {path}')
        offset = struct.unpack_from('<I', header, 60)[0]
        if offset > path.stat().st_size - 6:
            raise BuildError(f'Windows 실행파일 헤더 위치가 잘못되었습니다: {path}')
        f.seek(offset)
        pe = f.read(6)
        if len(pe) != 6 or pe[:4] != b'PE\0\0':
            raise BuildError(f'Windows PE 헤더가 아닙니다: {path}')
        return struct.unpack_from('<H', pe, 4)[0]


def inspect_source(path: Path) -> dict:
    path = Path(path).resolve()
    if not path.is_file() or path.suffix.lower() != '.py':
        raise BuildError('패키징할 The_Viewer.py 파일을 선택하세요.')
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    tree = ast.parse(text, filename=str(path))
    compile(tree, str(path), 'exec')
    constants = {}
    funcs = set()
    imports = set()
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            funcs.add(n.name)
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant):
            for target in n.targets:
                if isinstance(target, ast.Name):
                    constants[target.id] = n.value.value
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imports.update(a.name.split('.')[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            imports.add(n.module.split('.')[0])
    if constants.get('APP_NAME') != 'The Viewer (정)' or constants.get('APP_USER_MODEL_ID') != 'KRS.PDFMagnet':
        raise BuildError('뷰어 소스가 아닙니다. pkpk16 관리자 PY가 아닌 The_Viewer.py를 선택하세요.')
    if constants.get('ENGINE_PROFILE') != 'permissive-pdf':
        raise BuildError('이 도구는 PDFium 기반 permissive-pdf 뷰어만 빌드합니다. 3.12.4 이전 PY를 사용하지 마세요.')
    banned = {'pymupdf', 'fitz', 'pyvips', '_libvips'} & imports
    if banned:
        raise BuildError('제외 대상 엔진 import가 남아 있습니다: ' + ', '.join(sorted(banned)))
    required = {'bundled_engines_package_selftest', 'printing_package_selftest',
                'document_package_selftest', 'vector_package_selftest', 'worker_launch',
                'DirectImageReader', 'office_to_pdf'}
    if not required <= funcs:
        raise BuildError('지원하는 단일파일 뷰어의 검사 함수가 없습니다: ' + ', '.join(sorted(required-funcs)))
    version = str(constants.get('APP_VERSION', ''))
    if not re.fullmatch(r'[0-9A-Za-z._-]{1,40}', version):
        raise BuildError('APP_VERSION 값이 비어 있거나 파일명으로 사용할 수 없습니다.')
    return {'source': str(path), 'version': version, 'sha256': hashlib.sha256(raw).hexdigest(),
            'imports': sorted(imports), 'engine_profile': constants['ENGINE_PROFILE'],
            'required_check_count': 14 + int('printing_package_selftest' in funcs) + int('vector_package_selftest' in funcs) + 2*int('document_package_selftest' in funcs) + int('bundled_engines_package_selftest' in funcs) + int('text_package_selftest' in funcs) + int('compare_page_pair' in funcs) + int('editing_ui_package_selftest' in funcs) + int('type3_edit_package_selftest' in funcs)}


def inspect_ico(raw: bytes) -> dict:
    """Validate the ICO directory without importing Qt or executing viewer code."""
    if len(raw) < 6 or len(raw) > 16 * 1024 * 1024:
        raise BuildError('ICO 파일 크기가 잘못되었습니다.')
    reserved, kind, count = struct.unpack_from('<HHH', raw)
    if reserved or kind != 1 or not 1 <= count <= 256 or len(raw) < 6 + count * 16:
        raise BuildError('올바른 Windows ICO 파일이 아닙니다.')
    frames = []
    for i in range(count):
        w, h, colors, unused, planes, bits, size, offset = struct.unpack_from('<BBBBHHII', raw, 6 + i * 16)
        if unused or not size or offset < 6 + count * 16 or size > len(raw) - offset:
            raise BuildError('ICO 내부 이미지 위치/크기가 잘못되었습니다.')
        content = raw[offset:offset + size]
        png = content.startswith(b'\x89PNG\r\n\x1a\n')
        if png:
            if len(content) < 33 or content[12:16] != b'IHDR':
                raise BuildError('ICO 내부 PNG 헤더가 잘못되었습니다.')
            actual_w, actual_h = struct.unpack_from('>II', content, 16)
            if (actual_w, actual_h) != (w or 256, h or 256):
                raise BuildError('ICO 이미지 크기와 목록의 크기가 다릅니다.')
        elif len(content) < 40 or struct.unpack_from('<I', content)[0] not in (40, 108, 124):
            raise BuildError('지원하지 않는 ICO 내부 이미지 형식입니다.')
        frames.append({'width': w or 256, 'height': h or 256, 'png': png})
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'frames': frames, 'has_png': any(f['png'] for f in frames)}


def stage_viewer_icon(source: Path, target: Path, selected: str = '') -> dict:
    if selected:
        path = Path(selected).expanduser().resolve()
        if not path.is_file() or path.suffix.lower() != '.ico':
            raise BuildError('아이콘은 .ico 파일을 선택하세요.')
        raw = path.read_bytes()
        origin = str(path)
    else:
        tree = ast.parse(source.read_text(encoding='utf-8-sig'))
        value = next((n.value for n in tree.body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == '_APPLICATION_ICO_BASE64' for t in n.targets)), None)
        if value is None:
            raise BuildError('뷰어 기본 아이콘이 없습니다. 사용할 ICO를 선택하세요.')
        try:
            raw = base64.b64decode(ast.literal_eval(value), validate=True)
        except (ValueError, TypeError) as exc:
            raise BuildError('뷰어 기본 ICO 데이터를 읽을 수 없습니다.') from exc
        origin = 'viewer_embedded_icon'
    info = inspect_ico(raw)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    if sha256(target) != info['sha256']:
        raise BuildError('ICO 복사 검증 실패')
    return dict(info, origin=origin, staged_path=str(target))


def embed_staged_icon(source: Path, ico: Path) -> None:
    """Replace only the embedded icon constant in the temporary viewer copy."""
    text = source.read_text(encoding='utf-8-sig')
    tree = ast.parse(text)
    matches = [n for n in tree.body if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == '_APPLICATION_ICO_BASE64' for t in n.targets)]
    if len(matches) != 1:
        raise BuildError('뷰어 아이콘 상수가 하나가 아닙니다.')
    node = matches[0]
    if node.col_offset or node.end_lineno is None:
        raise BuildError('뷰어 아이콘 상수 위치를 확인할 수 없습니다.')
    encoded = base64.b64encode(ico.read_bytes()).decode('ascii')
    lines = text.splitlines(keepends=True)
    replacement = '_APPLICATION_ICO_BASE64 = (\n' + ''.join('    ' + repr(encoded[i:i+120]) + '\n'
                                                               for i in range(0, len(encoded), 120)) + ')\n'
    updated = ''.join(lines[:node.lineno-1]) + replacement + ''.join(lines[node.end_lineno:])
    compile(updated, str(source), 'exec')
    source.write_text(updated, encoding='utf-8')


def bundle_files(root: Path, engine: str, check=lambda: None) -> tuple[dict, dict, bytes]:
    if engine not in REQUIRED_ENGINES:
        raise BuildError('지원하지 않는 엔진입니다: ' + engine)
    if not root.is_dir():
        raise BuildError(f'소스 PY 옆에 engines/{engine} 폴더가 없습니다: {root}')
    manifest = root / 'bundle.json'
    if not manifest.is_file():
        raise BuildError('엔진 검사 목록이 없습니다: ' + str(manifest))
    raw = manifest.read_bytes()
    info = json.loads(raw.decode('utf-8-sig'))
    if info.get('platform') != 'windows-x86_64' or not info.get('version') or not info.get('license'):
        raise BuildError('엔진 버전/플랫폼/라이선스 표기를 확인하세요: ' + engine)
    records = info.get('files')
    if not isinstance(records, dict) or not records:
        raise BuildError('엔진 파일 목록이 비어 있습니다: ' + engine)
    lowered = set()
    for relative, record in records.items():
        safe_relative(relative)
        if relative.casefold() in lowered:
            raise BuildError('대소문자가 중복된 파일 경로: ' + relative)
        lowered.add(relative.casefold())
        if not isinstance(record, dict) or type(record.get('bytes')) is not int or record['bytes'] < 0:
            raise BuildError('파일 크기 기록이 잘못되었습니다: ' + relative)
        if not re.fullmatch(r'[0-9a-fA-F]{64}', str(record.get('sha256', ''))):
            raise BuildError('파일 해시 기록이 잘못되었습니다: ' + relative)
    if not set(REQUIRED_ENGINES[engine]) <= set(records):
        raise BuildError('엔진 필수 파일이 검사 목록에서 누락되었습니다: ' + engine)
    actual = {p.relative_to(root).as_posix() for p in files_in(root, check) if p != manifest}
    if actual != set(records):
        missing, extra = sorted(set(records)-actual), sorted(actual-set(records))
        raise BuildError(f'{engine} 파일 목록 불일치. 누락={missing[:5]}, 추가={extra[:5]}. bundle.json을 임의로 다시 쓰지 마세요.')
    exe = root / REQUIRED_ENGINES[engine][0]
    if pe_machine(exe) != 0x8664:
        raise BuildError('64비트 x64 엔진이 아닙니다: ' + str(exe))
    return info, records, raw


def verify_bundle(root: Path, engine: str, *, destination: Path | None = None,
                  check=lambda: None, emit=lambda s: None) -> dict:
    """Verify EVERY listed byte. Optionally make a verified copy; never rewrite source manifests."""
    info, records, manifest = bundle_files(root, engine, check)
    if destination is not None:
        destination.mkdir(parents=True, exist_ok=False)
    last = 0.0
    total_bytes = 0
    for i, (relative, expected) in enumerate(records.items(), 1):
        check()
        source = root / relative
        if time.monotonic()-last >= 1.0 or i == len(records):
            emit(f'[{engine}] {i}/{len(records)} 확인: {relative}')
            last = time.monotonic()
        size = 0
        h = hashlib.sha256()
        output = None
        try:
            if destination is not None:
                target = destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                output = target.open('xb')
            with source.open('rb') as f:
                while True:
                    check()
                    block = f.read(1024*1024)
                    if not block:
                        break
                    size += len(block)
                    h.update(block)
                    if output:
                        output.write(block)
        finally:
            if output:
                output.close()
        if size != expected['bytes'] or h.hexdigest() != expected['sha256'].lower():
            raise BuildError(f'엔진 파일 크기/해시 불일치: {engine}/{relative}. DLL 적용 결과를 확인하세요.')
        if engine == 'libreoffice' and relative.casefold() == 'program/vcruntime140_1.dll' and h.hexdigest() == KNOWN_FAILED_VCRUNTIME1:
            raise BuildError('이전에 충돌했던 정확히 같은 DLL이 아직 소스 엔진에 있습니다. Office_Source_Apply_Fix_v2 적용 완료 후 실행하세요.')
        total_bytes += size
    if (root/'bundle.json').read_bytes() != manifest:
        raise BuildError('검사 중 bundle.json이 변경되었습니다. 작업을 멈추고 다시 실행하세요.')
    actual = {p.relative_to(root).as_posix() for p in files_in(root, check) if p != root/'bundle.json'}
    if actual != set(records):
        raise BuildError('검사 중 엔진 파일 목록이 바뀌었습니다.')
    if destination is not None:
        (destination/'bundle.json').write_bytes(manifest)
    return {'engine': engine, 'files': len(records), 'bytes': total_bytes,
            'version': info['version'], 'manifest_sha256': hashlib.sha256(manifest).hexdigest(),
            'local_runtime_test': info.get('local_runtime_test'), 'status': 'passed'}


def clean_environment() -> dict:
    env = os.environ.copy()
    for name in list(env):
        if name.upper().startswith('PIP_') or name in ('PYTHONHOME','PYTHONPATH','QT_PLUGIN_PATH',
                'QT_QPA_PLATFORM_PLUGIN_PATH','QML2_IMPORT_PATH','QML_IMPORT_PATH','VIPS_PATH','GI_TYPELIB_PATH'):
            env.pop(name, None)
    env.update(PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONUNBUFFERED='1',
               PYTHONNOUSERSITE='1', PIP_CONFIG_FILE=os.devnull)
    return env


def probe_python(executable: str, timeout: float = 12.0) -> dict:
    code = ('import json,sys,struct,platform,sysconfig;print(json.dumps({'
            '"executable":sys.executable,"base":getattr(sys,"_base_executable",sys.executable),'
            '"version":list(sys.version_info[:3]),"bits":struct.calcsize("P")*8,'
            '"machine":platform.machine(),"implementation":platform.python_implementation(),'
            '"free_threaded":bool(sysconfig.get_config_var("Py_GIL_DISABLED")),'
            '"prefix":sys.prefix,"base_prefix":sys.base_prefix}))')
    p = subprocess.run([str(executable), '-I', '-c', code], text=True, encoding='utf-8', errors='replace',
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), env=clean_environment())
    if p.returncode:
        raise BuildError('Python 실행 확인 실패: ' + p.stderr.strip()[-1000:])
    info = json.loads(p.stdout.strip().splitlines()[-1])
    major, minor, *_ = info['version']
    if info['bits'] != 64 or info['implementation'] != 'CPython' or (major,minor) not in [(3,x) for x in (11,12,13)]:
        raise BuildError('이 빌더는 CPython 3.11~3.13 64비트를 대상으로 합니다.')
    if info.get('free_threaded') or info['machine'].lower() not in ('amd64','x86_64'):
        raise BuildError('일반 x64 CPython을 선택하세요. ARM64/실험적 free-threaded는 대상이 아닙니다.')
    info['store'] = ('windowsapps' in info['executable'].lower() or 'pythonsoftwarefoundation' in info['base'].lower())
    return info


def probe_workspace(executable:str,directory:Path,timeout:float=12.0) -> Path:
    """Check the physical writable directory in the selected Python's context.

    The UI and selected interpreter may belong to different Store packages or
    the UI may run under python.org Python. Resolving inside the UI alone cannot
    discover the selected interpreter's AppData write redirection.
    """
    code='''import json,os,sys,uuid
from pathlib import Path
root=Path(sys.argv[1]).expanduser()
root.mkdir(parents=True,exist_ok=True)
marker=root/('.tvbuild_path_'+uuid.uuid4().hex+'.tmp')
created=False
try:
    with marker.open('xb') as stream:
        created=True
        stream.write(b'TVBuild path probe')
    actual=Path(os.path.realpath(marker,strict=True)).parent
    print(json.dumps({'actual_directory':str(actual)},ensure_ascii=True))
finally:
    if created:
        marker.unlink()
'''
    try:
        p=subprocess.run([str(executable),'-I','-c',code,str(directory)],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                         encoding='utf-8',errors='replace',timeout=timeout,
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),env=clean_environment())
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise BuildError('선택한 Python의 작업 폴더 확인 실패: '+str(exc)) from exc
    if p.returncode:
        raise BuildError('선택한 Python의 작업 폴더 확인 실패: '+p.stderr.strip()[-1000:])
    try:
        value=json.loads(p.stdout.strip().splitlines()[-1])
        physical=Path(value['actual_directory'])
        if not physical.is_absolute(): raise ValueError('absolute path required')
    except (ValueError,KeyError,IndexError,TypeError) as exc:
        raise BuildError('선택한 Python의 작업 폴더 확인 결과가 잘못되었습니다.') from exc
    return physical


def choose_build_workspace(preferred:Path,python_info:dict,output_root:Path,emit:Callable[[str],None]=lambda _:None) -> Path:
    """Honor a valid selection; find a short physical path for Store Python."""
    preferred=Path(preferred).expanduser().absolute()
    candidates=[preferred]
    if python_info.get('store'):
        user=hashlib.sha256(str(Path.home()).encode('utf-8')).hexdigest()[:8]
        candidates.extend([Path(output_root)/'TVBuild',
                           Path(os.environ.get('PUBLIC',r'C:\Users\Public'))/('TVBuild_'+user)])
    errors=[]; seen=set()
    for candidate in candidates:
        key=str(candidate).casefold()
        if key in seen: continue
        seen.add(key)
        try:
            if not str(candidate).isascii() or len(str(candidate))>110:
                raise BuildError('작업 폴더는 110자 이하의 영문 경로가 필요합니다: '+str(candidate))
            physical=probe_workspace(python_info['executable'],candidate)
            if not str(physical).isascii() or len(str(physical))>110:
                raise BuildError('실제 작업 폴더가 경로 조건을 넘습니다: '+str(physical))
        except BuildError as exc:
            errors.append(str(exc))
            emit('[작업 폴더 확인] '+str(exc))
            continue
        if candidate!=preferred:
            emit('[작업 폴더 자동 변경] '+str(physical))
        else:
            emit('[작업 폴더 실제 경로] '+str(physical))
        return physical
    raise BuildError('작업 폴더를 준비하지 못했습니다. 가상환경·임시공간에 D:\\TVBuild 같은 짧은 영문 폴더를 선택하세요.\n'+'\n'.join(errors))


def python_candidates() -> list[str]:
    result = [getattr(sys, '_base_executable', sys.executable), sys.executable]
    if os.name == 'nt':
        try:
            import winreg
            for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
                    try:
                        with winreg.OpenKey(hive, r'SOFTWARE\Python\PythonCore', 0, winreg.KEY_READ|view) as k:
                            for i in range(winreg.QueryInfoKey(k)[0]):
                                name = winreg.EnumKey(k,i)
                                try:
                                    with winreg.OpenKey(k,name+r'\InstallPath') as ip:
                                        try: result.append(winreg.QueryValueEx(ip,'ExecutablePath')[0])
                                        except OSError: result.append(str(Path(winreg.QueryValueEx(ip,'')[0])/'python.exe'))
                                except OSError: pass
                    except OSError: pass
        except ImportError:
            pass
        launcher = shutil.which('py')
        if launcher:
            try:
                p = subprocess.run([launcher,'-0p'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding='utf-8', errors='replace', timeout=8,
                                   creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                for line in p.stdout.splitlines():
                    m = re.search(r'([A-Za-z]:[\\/].*?python(?:w)?\.exe)\s*$', line, re.I)
                    if m: result.append(m.group(1).strip())
            except (OSError,subprocess.TimeoutExpired): pass
        for base in (Path(os.environ.get('LOCALAPPDATA',''))/'Programs'/'Python', Path('C:/')):
            if base.is_dir():
                result.extend(str(p) for p in base.glob('Python3*/python.exe'))
    found = []
    seen = set()
    for value in result:
        p = Path(value)
        if p.name.lower() == 'pythonw.exe': p=p.with_name('python.exe')
        # Reject only the unversioned WindowsApps alias; a real Store interpreter is selectable.
        if p.parent.name.lower() == 'windowsapps': continue
        key = str(p).casefold()
        if key not in seen and p.is_file():
            seen.add(key); found.append(str(p))
    return found


def kill_tree(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    try:
        if os.name == 'nt':
            taskkill = Path(os.environ.get('SystemRoot',r'C:\Windows'))/'System32'/'taskkill.exe'
            subprocess.run([str(taskkill),'/PID',str(process.pid),'/T','/F'],
                           stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10,
                           creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        else:
            process.terminate()
        process.wait(timeout=5)
    except (OSError,subprocess.TimeoutExpired):
        try: process.kill(); process.wait(timeout=5)
        except (OSError,subprocess.TimeoutExpired): pass


def tail_text(path: Path, count: int = 12000) -> str:
    if not path.is_file(): return ''
    with path.open('rb') as f:
        offset=max(0, path.stat().st_size-count)
        f.seek(offset)
        raw=f.read()
        if offset:
            # A byte limit can start in the middle of a Korean UTF-8 character.
            while raw and 0x80 <= raw[0] <= 0xBF:
                raw=raw[1:]
        return raw.decode('utf-8','replace')


def redact(text: str) -> str:
    # Local originals remain intact. The optional shared diagnostic is redacted.
    text=re.sub(r'(https?://)[^\s/@:]+:[^\s/@]+@',r'\1[REDACTED]@',text, flags=re.I)
    return re.sub(r'([?&](?:token|key|password|secret|signature)=)[^&\s]+',r'\1[REDACTED]',text,flags=re.I)


def diagnostic_zip(run_dir: Path) -> Path:
    dest=run_dir.parent/(run_dir.name+'_diagnostic.zip')
    names=['Build_Result.json','Environment.json','Failure_Summary.txt','build.log','launcher.log',
           'Source_Inspection.json','Icon_Inspection.json','Engine_Inspection.json','Engine_Delivery.json',
           'License_Inspection.json','Runtime_License_Inspection.json','License_Delivery.json','Excluded_Collection.json',
           '뷰어_사전검사.json','뷰어_사전검사.log','뷰어_배포검사.json','뷰어_배포검사.log',
           '뷰어_최종위치검사.json','뷰어_최종위치검사.log','installed_versions.txt','pip_check.txt']
    candidates=[run_dir/n for n in names]
    logdir=run_dir/'logs'
    if logdir.is_dir(): candidates += [p for p in logdir.iterdir() if p.suffix in ('.log','.txt') and p.is_file()]
    temp=dest.with_suffix('.tmp')
    with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in candidates:
            if p.is_file() and not is_link(p):
                # Include the whole log, including the first failing build output.
                # Line streaming keeps large pip/PyInstaller logs out of memory.
                with p.open('r',encoding='utf-8-sig',errors='replace',newline='') as source:
                    with z.open(p.relative_to(run_dir).as_posix(),'w',force_zip64=True) as target:
                        for line in source:
                            target.write(redact(line).encode('utf-8'))
        z.writestr('PRIVACY.txt','Local paths and package/build logs are included. No viewer source, DLL, private document or environment dump is included. Inspect before sharing.\n')
    os.replace(temp,dest)
    return dest


class WorkspaceLock:
    def __init__(self,path:Path): self.path=path; self.f=None
    def __enter__(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.f=self.path.open('a+b'); self.f.seek(0)
        if self.path.stat().st_size==0: self.f.write(b'0'); self.f.flush()
        self.f.seek(0)
        try:
            if os.name=='nt':
                import msvcrt
                msvcrt.locking(self.f.fileno(),msvcrt.LK_NBLCK,1)
            else:
                import fcntl
                fcntl.flock(self.f.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as e:
            self.f.close(); self.f=None
            raise BuildError('다른 전용 빌더가 실행 중입니다. 기존 작업 종료 후 다시 실행하세요.') from e
        return self
    def __exit__(self,*args):
        if self.f:
            if os.name=='nt':
                import msvcrt
                self.f.seek(0); msvcrt.locking(self.f.fileno(),msvcrt.LK_UNLCK,1)
            else:
                import fcntl
                fcntl.flock(self.f.fileno(),fcntl.LOCK_UN)
            self.f.close()
