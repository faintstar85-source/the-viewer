"""Build-time license evidence and banned-engine gates. No user code license grant.

Artifacts remain folder based so compatible LGPL DLLs can be replaced. This gate
checks shipped evidence and version/source correspondence; it does not give a
legal opinion about the author's complete distribution obligations.
"""
from __future__ import annotations
import ast
import hashlib
import json
import re
import shutil
from importlib.metadata import distribution, distributions, PackageNotFoundError, version
from pathlib import Path
from build_common import BuildError, files_in, sha256, safe_relative

QT_MODULE_SOURCES = {
    'Core':'qtbase', 'Gui':'qtbase', 'Widgets':'qtbase', 'PrintSupport':'qtbase',
    'Network':'qtbase', 'OpenGL':'qtbase', 'OpenGLWidgets':'qtbase', 'DBus':'qtbase',
    'Xml':'qtbase', 'Svg':'qtsvg', 'SvgWidgets':'qtsvg',
}
QT_VERSION = '6.11.1'
EXCLUDED_MODULES = (
    'pymupdf','fitz','pyvips','_libvips','ezdxf.addons.drawing.pymupdf',
    'PySide6.QtPdf','PySide6.QtPdfWidgets','PySide6.QtQml','PySide6.QtQuick',
    'PySide6.QtQuickWidgets','PySide6.QtQuickControls2','PySide6.QtVirtualKeyboard',
    'PySide6.QtCharts','PySide6.QtGraphs','PySide6.QtGraphsWidgets','PySide6.QtDataVisualization',
    'PySide6.Qt3DCore','PySide6.Qt3DRender','PySide6.Qt3DInput','PySide6.Qt3DLogic',
    'PySide6.Qt3DExtras','PySide6.Qt3DAnimation','PySide6.QtQuick3D','PySide6.QtWebEngineCore',
    'PySide6.QtWebEngineWidgets','PySide6.QtWebEngineQuick','PySide6.QtMultimedia',
    'PySide6.QtMultimediaWidgets','PySide6.QtPositioning','PySide6.QtLocation',
)
BANNED_BINARY_MARKERS = ('pymupdf','mupdf','ghostscript','gsdll','gswin','libredwg','dwg2dxf',
                        'qtvirtualkeyboard','qt6virtualkeyboard','libvips','pyvips','ffmpeg')
DISTRIBUTIONS = ('PySide6','PySide6-Essentials','PySide6-Addons','shiboken6',
                 'pypdfium2','reportlab','pypdf','Pillow','deepl','python-hwpx',
                 'certifi','lxml','requests','psd-tools','ezdxf','psutil','numpy',
                 'opencv-python-headless','packaging','typing_extensions','charset-normalizer',
                 'idna','urllib3','fonttools','scipy','scikit-image','networkx',
                 'tifffile','imageio','lazy-loader','aggdraw','pywin32','cryptography','cffi','pycparser')
REQUIRED_DIST = {'PySide6','PySide6-Essentials','PySide6-Addons','shiboken6',
                 'pypdfium2','reportlab','pypdf','Pillow','deepl','python-hwpx',
                 'certifi','lxml','requests','psd-tools','ezdxf','psutil','numpy',
                 'opencv-python-headless','cryptography'}
PLUGIN_DIRECTORIES = {'imageformats','platforms','styles','iconengines','printsupport','tls',
                      'networkinformation'}


def stage_backend_modules(source: Path, destination: Path) -> list[str]:
    """Expose embedded Python sources to normal PyInstaller static analysis."""
    tree=ast.parse(source.read_text(encoding='utf-8-sig'))
    names={'_VIEWER_PDF_ENGINE_SOURCE':'viewer_pdf_engine.py','_VIEWER_PDF_EDIT_SOURCE':'viewer_pdf_edit.py'}
    found={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id in names:
                    try:value=ast.literal_eval(node.value)
                    except (ValueError,TypeError):continue
                    if not isinstance(value,str):continue
                    compile(value,names[target.id],'exec')
                    found[names[target.id]]=value
    if set(found)!=set(names.values()):
        raise BuildError('단독 PY에 PDFium 엔진/편집 소스가 모두 포함되어야 합니다.')
    for name,text in found.items():
        for n in ast.walk(ast.parse(text)):
            imports=[]
            if isinstance(n,ast.Import):imports=[a.name for a in n.names]
            elif isinstance(n,ast.ImportFrom) and n.module:imports=[n.module]
            if any(i.split('.')[0] in {'pymupdf','fitz','pyvips','_libvips'} for i in imports):
                raise BuildError('동봉 엔진 소스에 제외 대상 import가 남아 있습니다: '+name)
        (destination/name).write_text(text,encoding='utf-8')
    return sorted(found)


def find_compliance_root(source: Path, fallback: Path | None=None, *,
                         builder_root: Path | None=None, selected: str='',
                         engines_root: str='') -> Path:
    """Keep the original package location separate from the materialized tools."""
    if selected:
        chosen=Path(selected).expanduser().resolve()
        candidates=[chosen,chosen/'compliance']
    else:
        candidates=[Path(source).expanduser().resolve().parent/'compliance']
        if builder_root:
            package=Path(builder_root).expanduser().resolve()
            candidates.extend([package/'compliance',package.parent/'compliance'])
        if engines_root:
            engines=Path(engines_root).expanduser().resolve()
            candidates.extend([engines/'compliance',engines.parent/'compliance'])
        if fallback:
            candidates.extend([Path(fallback)/'compliance',Path(fallback).parent/'compliance'])
    seen=set()
    for candidate in candidates:
        candidate=candidate.resolve()
        if str(candidate) in seen:continue
        seen.add(str(candidate))
        if (candidate/'QT_SOURCE_MANIFEST.json').is_file():return candidate
    checked='\n'.join('  '+p for p in seen)
    raise BuildError('compliance/Qt 대응 소스·라이선스 폴더를 찾지 못했습니다.\n'
                     '패키징 화면의 [라이선스 compliance 폴더]에서 기존 배포 ZIP을 푼 compliance 폴더를 선택하세요.\n'
                     '확인한 위치:\n'+checked)


def prepare_license_materials(source: Path, destination: Path, fallback: Path | None=None, *,
                              builder_root: Path | None=None, selected: str='',
                              engines_root: str='') -> dict:
    origin=find_compliance_root(source,fallback,builder_root=builder_root,
                                selected=selected,engines_root=engines_root)
    for required in ('NOTICES_KO.txt','THIRD_PARTY_NOTICES.txt','QT_SOURCE_MANIFEST.json'):
        if not (origin/required).is_file():raise BuildError('라이선스 배포 자료 누락: '+required)
    manifest=json.loads((origin/'QT_SOURCE_MANIFEST.json').read_text(encoding='utf-8-sig'))
    if manifest.get('schema')!=1 or manifest.get('qt_version')!=QT_VERSION or manifest.get('pyside_version')!=QT_VERSION:
        raise BuildError('Qt/PySide 대응 소스 버전은 빌드한 6.11.1과 같아야 합니다.')
    modules=manifest.get('modules',{})
    for module in ('qtbase','qtsvg','qtimageformats','pyside'):
        record=modules.get(module,{})
        relative=safe_relative(record.get('path',''))
        path=origin/relative
        if not path.is_file() or path.stat().st_size!=record.get('bytes') or sha256(path)!=record.get('sha256'):
            raise BuildError('Qt 대응 소스 크기/해시 불일치: '+module)
    certifi_path=origin/'CERTIFI_SOURCE_MANIFEST.json'
    if not certifi_path.is_file():raise BuildError('certifi MPL 대응 소스 안내가 없습니다.')
    certifi=json.loads(certifi_path.read_text(encoding='utf-8-sig'))
    certifi_archive=origin/safe_relative(certifi.get('path',''))
    if certifi.get('version')!='2026.4.22' or not certifi_archive.is_file() or certifi_archive.stat().st_size!=certifi.get('bytes') or sha256(certifi_archive)!=certifi.get('sha256'):
        raise BuildError('certifi 대응 소스 버전/크기/해시 불일치')
    destination.mkdir(parents=True,exist_ok=False)
    for path in files_in(origin):
        dest=destination/path.relative_to(origin);dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,dest)
        if sha256(dest)!=sha256(path):raise BuildError('라이선스 자료 복사 검증 실패: '+str(path))
    return {'origin':str(origin),'qt_version':QT_VERSION,'source_archives':len(modules),
            'source_hashes_verified':True,'files':len(files_in(destination)),
            'app_license_assigned':False}



def verify_optional_office_source(engine: Path) -> dict:
    """Old binary-only bundles are not silently republished with this profile."""
    manifest_path=engine/'SOURCE_MANIFEST.json'
    if not manifest_path.is_file():
        raise BuildError('LibreOffice 동봉에는 정확한 버전의 SOURCE_MANIFEST.json과 대응 소스 아카이브가 필요합니다. LibreOffice 동봉 체크를 끄고 사용자 설치 LibreOffice를 사용할 수 있습니다.')
    bundle=json.loads((engine/'bundle.json').read_text(encoding='utf-8-sig'))
    manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    if manifest.get('schema')!=1 or manifest.get('engine_version')!=bundle.get('version'):
        raise BuildError('LibreOffice 대응 소스 버전/구조 불일치')
    archives=manifest.get('archives')
    if not isinstance(archives,list) or not archives:raise BuildError('LibreOffice 대응 소스 아카이브 목록이 없습니다.')
    for record in archives:
        relative=safe_relative(record.get('path',''));source=engine/relative
        if not str(record.get('source_url','')).startswith('https://'):
            raise BuildError('LibreOffice 공식 대응 소스 URL이 없습니다.')
        if not source.is_file() or source.stat().st_size!=record.get('bytes') or sha256(source)!=record.get('sha256'):
            raise BuildError('LibreOffice 대응 소스 크기/해시 불일치: '+relative)
    return {'version':manifest['engine_version'],'archives':len(archives),'source_hashes_verified':True,
            'scope':'source presence/version/hash evidence only; no legal opinion'}

def collect_installed_notices(destination: Path) -> dict:
    """Copy exact license/NOTICE files from every installed runtime wheel."""
    output=destination/'installed_wheel_notices';output.mkdir(parents=True,exist_ok=True)
    records=[]
    installed={d.metadata.get('Name') for d in distributions()}
    build_only={'pip','setuptools','wheel','pyinstaller','pyinstaller-hooks-contrib','altgraph','pefile','pywin32-ctypes'}
    normalized=lambda n:re.sub(r'[-_.]+','-',n).casefold()
    names={normalized(n):n for n in DISTRIBUTIONS}
    for n in installed:
        if n and normalized(n) not in build_only:names.setdefault(normalized(n),n)
    for name in sorted(names.values(),key=str.casefold):
        try:dist=distribution(name)
        except PackageNotFoundError:
            if name in REQUIRED_DIST:raise BuildError('빌드 의존성 메타데이터 누락: '+name)
            continue
        matching=[]
        for entry in dist.files or ():
            path=Path(entry);lower=path.as_posix().lower();base=path.name.lower()
            if 'license' in base or base.startswith(('copying','notice','copyright','authors')) or '/licenses/' in lower:
                original=Path(dist.locate_file(entry))
                if not original.is_file():continue
                if path.is_absolute() or '..' in path.parts:raise BuildError('라이선스 상대 경로 오류: '+name)
                dest=output/name/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,dest)
                matching.append({'path':dest.relative_to(destination).as_posix(),'bytes':dest.stat().st_size,'sha256':sha256(dest)})
        # Some projects put the license only in wheel METADATA. Keep it, and gate a missing notice.
        metadata=dist.read_text('METADATA') or ''
        meta_target=output/name/'METADATA.txt';meta_target.parent.mkdir(parents=True,exist_ok=True)
        meta_target.write_text(metadata,encoding='utf-8')
        if not matching and name in REQUIRED_DIST:
            raise BuildError('실제 설치 휠의 라이선스 파일이 없습니다: '+name)
        records.append({'distribution':name,'version':dist.version,'license_files':matching})
    if version('certifi')!='2026.4.22':raise BuildError('certifi 대응 소스와 실제 휠 버전 불일치')
    for name in ('PySide6','PySide6-Essentials','PySide6-Addons','shiboken6'):
        if version(name)!=QT_VERSION:raise BuildError('Qt 대응 소스와 실제 휠 버전 불일치: '+name)
    (destination/'INSTALLED_RUNTIME_LICENSES.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    dependencies={'python':__import__('sys').version,'platform':__import__('sys').platform,
        'runtime_wheels':{r['distribution']:r['version'] for r in records},
        'qt_sources_version':QT_VERSION,'custom_library_build':False}
    (destination/'BUILD_DEPENDENCIES.json').write_text(json.dumps(dependencies,ensure_ascii=False,indent=2),encoding='utf-8')
    configuration=destination/'BUILD_LIBRARY_CONFIGURATION';configuration.mkdir(exist_ok=True)
    config_records=[]
    for name in ('PySide6','PySide6-Essentials','PySide6-Addons','shiboken6'):
        dist=distribution(name)
        for entry in dist.files or ():
            path=Path(entry);base=path.name.lower()
            if base not in {'_config.py','qt.conf','qconfig.h','qconfig.cpp','configure.json','config.opt'} and path.suffix.lower() not in {'.pri','.prl'}:continue
            original=Path(dist.locate_file(entry))
            if not original.is_file():continue
            dest=configuration/name/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,dest)
            config_records.append({'distribution':name,'file':dest.relative_to(destination).as_posix(),'sha256':sha256(dest)})
    from PySide6.QtCore import QLibraryInfo
    qtbuild={'version':QLibraryInfo.version().toString(),'build':QLibraryInfo.build(),
        'debug':QLibraryInfo.isDebugBuild(),'configuration_files':config_records,
        'source':'official PyPI prebuilt wheels; no locally changed Qt/PySide library',
        'unavailable_build_details':'Flags not present in the upstream wheels are not invented.'}
    if qtbuild['version']!=QT_VERSION:raise BuildError('실제 Qt 공유 라이브러리 버전 불일치')
    (configuration/'QT_BUILD_INFORMATION.json').write_text(json.dumps(qtbuild,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'distribution_count':len(records),'license_files':sum(len(r['license_files']) for r in records),
            'versions':{r['distribution']:r['version'] for r in records}}


def excluded_toc_reason(entry) -> str | None:
    """Return removal reason only for expressly excluded runtime components."""
    dest=Path(str(entry[0]).replace('\\','/'));low=dest.as_posix().lower();base=dest.name.lower()
    if low.startswith('licenses/') or '/licenses/' in low:return None
    if any(marker in low for marker in BANNED_BINARY_MARKERS):return 'excluded_engine'
    match=re.fullmatch(r'qt6([a-z0-9]+)(?:d)?\.dll',base)
    if match and match.group(1) not in {m.lower() for m in QT_MODULE_SOURCES}:return 'unused_qt_module'
    if 'pyside6' in low:
        wrapper=re.fullmatch(r'qt([a-z0-9]+)(?:\.abi3)?\.(?:pyd|so)',base)
        if wrapper and wrapper.group(1) not in {m.lower() for m in QT_MODULE_SOURCES}:return 'unused_qt_python_module'
        if '/qml/' in low:return 'qml_not_used'
        if base in {'qpdf.dll','qtvirtualkeyboardplugin.dll'}:return 'excluded_qt_plugin'
        if '/plugins/' in low:
            directory=low.split('/plugins/',1)[1].split('/',1)[0]
            if directory not in PLUGIN_DIRECTORIES:return 'unused_qt_plugin_group'
    return None


def write_pyinstaller_wrapper(path: Path, audit_file: Path) -> None:
    """Filter unrequested hook collections before PYZ/COLLECT; never alter installed Qt."""
    code='''import json, sys
from pathlib import Path
sys.setrecursionlimit(10000)
from license_gate import excluded_toc_reason
from PyInstaller.building.build_main import Analysis
original_assemble=Analysis.assemble
def filtered_assemble(self):
    original_assemble(self)
    removed=[]
    for field in ('binaries','datas'):
        kept=[]
        for entry in getattr(self,field):
            reason=excluded_toc_reason(entry)
            if reason:removed.append({'field':field,'name':entry[0],'reason':reason})
            else:kept.append(entry)
        setattr(self,field,kept)
    Path(AUDIT_FILE).write_text(json.dumps(removed,ensure_ascii=False,indent=2),encoding='utf-8')
Analysis.assemble=filtered_assemble
from PyInstaller.__main__ import run
run(sys.argv[1:])
'''
    prefix='AUDIT_FILE = '+repr(str(audit_file))+'\nimport sys\nsys.path.insert(0,'+repr(str(Path(__file__).resolve().parent))+')\n'
    path.write_text(prefix+code,encoding='utf-8')


def audit_product(product: Path) -> dict:
    internal=product/'_internal';qt=[];pdfium=[];banned=[]
    for path in files_in(product):
        relative=path.relative_to(product).as_posix();low=relative.lower();base=path.name.lower()
        if '/licenses/' in low:continue
        if path.suffix.lower() in ('.dll','.exe','.pyd','.py','.pyc'):
            if any(marker in low for marker in BANNED_BINARY_MARKERS):banned.append(relative)
            if base=='qpdf.dll':banned.append(relative)
            wrapper=re.fullmatch(r'qt([a-z0-9]+)(?:\.abi3)?\.(?:pyd|so)',base)
            if 'pyside6' in low and wrapper and wrapper.group(1) not in {m.lower() for m in QT_MODULE_SOURCES}:banned.append(relative)
            match=re.fullmatch(r'qt6([a-z0-9]+)(?:d)?\.dll',base)
            if match:
                module=next((key for key in QT_MODULE_SOURCES if key.lower()==match.group(1)),None)
                if module is None:banned.append(relative)
                else:qt.append({'file':relative,'module':module,'source':QT_MODULE_SOURCES[module]})
            if base=='pdfium.dll':pdfium.append(relative)
        if '/pyside6/qt/qml/' in low:banned.append(relative)
        if '/engines/ghostscript/' in low or '/engines/libredwg/' in low:banned.append(relative)
    if banned:raise BuildError('제외 대상/대응 소스 없는 Qt 파일이 배포본에 포함됐습니다: '+', '.join(banned[:12]))
    if not pdfium:raise BuildError('pypdfium2의 pdfium.dll이 배포본에 없습니다.')
    if not (internal/'licenses'/'QT_SOURCE_MANIFEST.json').is_file():raise BuildError('배포본 Qt 대응 소스 안내 누락')
    result={'status':'passed','banned_components':[],'qt_libraries':qt,'pdfium_dlls':pdfium,
            'qt_source_version':QT_VERSION,'app_license_assigned':False,
            'scope':'file presence/version/hash evidence; no legal opinion or printer acceptance claim'}
    return result
