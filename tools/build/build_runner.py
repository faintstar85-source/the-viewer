"""Isolated build runner. Windows-only builds; library functions can be unit-tested elsewhere.
Source, engines, Windows DLLs and the user's installed Python packages are never modified.
"""
from __future__ import annotations
import argparse
import codecs
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import uuid
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

from build_common import (VERSION, CONTROL_PREFIX, REQUIRED_ENGINES, BINARY_PACKAGES,
    BuildError, Cancelled, atomic_json, read_json, sha256, files_in, inspect_source,
    verify_bundle, clean_environment, probe_python, kill_tree, tail_text, WorkspaceLock,
    stage_viewer_icon, embed_staged_icon, inspect_ico)
from installer_build import inspect_iscc, build_installer
import license_gate

class Runner:
    def __init__(self, job: dict):
        self.job=job
        self.run=Path(job['run_dir']).resolve()
        self.run.mkdir(parents=True,exist_ok=True)
        self.logs=self.run/'logs'; self.logs.mkdir(exist_ok=True)
        self.cancel_file=self.run/'CANCEL_REQUESTED'
        self.log_file=(self.run/'build.log').open('a',encoding='utf-8',buffering=1)
        self.step=0
        self.current=None

    def close(self): self.log_file.close()

    def emit(self,message):
        message=str(message)
        self.log_file.write(message+'\n'); self.log_file.flush()
        print(message,flush=True)

    def phase(self,message,progress):
        self.emit(message)
        print(CONTROL_PREFIX+json.dumps({'kind':'phase','message':message,'progress':progress},ensure_ascii=True),flush=True)

    def check(self):
        if self.cancel_file.exists(): raise Cancelled('사용자가 작업 중지를 요청했습니다.')

    def command(self,args,*,label,cwd=None,timeout=1800,env=None,allow_failure=False,log_path=None,report=None):
        """File-backed output avoids an unread-PIPE deadlock. UI runs in another process."""
        self.check(); self.step+=1
        path=Path(log_path) if log_path else self.logs/f'{self.step:02d}_{label}.log'
        args=list(map(str,args))
        self.emit('[실행] '+subprocess.list2cmdline(args))
        start=last=time.monotonic(); offset=0
        process=None
        decoder=codecs.getincrementaldecoder('utf-8')('replace')
        pending=''; flushed=False
        def show(text,final=False):
            nonlocal pending
            pending+=text.replace('\r','\n')
            while '\n' in pending:
                line,pending=pending.split('\n',1)
                if line.strip(): self.emit(line[:4000])
            while len(pending)>4000:
                self.emit(pending[:4000]); pending=pending[4000:]
            if final and pending:
                self.emit(pending); pending=''
        def drain():
            nonlocal offset
            try:
                with path.open('rb') as f:
                    f.seek(offset); raw=f.read(128*1024); offset=f.tell()
                if raw:
                    show(decoder.decode(raw))
                return bool(raw)
            except OSError:
                return False
        try:
            with path.open('wb') as output:
                process=subprocess.Popen(args,cwd=str(cwd or self.run),env=env or clean_environment(),
                    stdin=subprocess.DEVNULL,stdout=output,stderr=subprocess.STDOUT,
                    creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                self.current=process
                self.emit(f'[프로세스] PID {process.pid} / 로그: {path.name}')
                while process.poll() is None:
                    self.check(); drain()
                    now=time.monotonic()
                    if now-start > timeout:
                        raise BuildError(f'{label}: 실행 제한시간 {timeout}초 초과. 로그: {path}')
                    if now-last >= 12:
                        detail=''
                        if report and Path(report).is_file():
                            try:
                                state=read_json(Path(report)); detail=f" / {len(state.get('checks',[]))}/{state.get('required_check_count','?')} / {state.get('active_check') or '결과 확인 중'}"
                            except (OSError,ValueError): pass
                        self.emit(f'[실행 대기] {label} / {now-start:.0f}초 / PID {process.pid}{detail}')
                        last=now
                    time.sleep(.15)
                code=process.wait()
            while drain(): pass
            show(decoder.decode(b'',final=True),final=True); flushed=True
            self.emit(f'[종료] {label}: {code} (0x{code & 0xffffffff:08X})')
            if code and not allow_failure:
                raise BuildError(f'{label} 실패 / 종료 코드 {code}\n로그: {path}\n\n마지막 출력:\n'+tail_text(path))
            return code,path
        finally:
            if process is not None and process.poll() is None: kill_tree(process)
            if not flushed:
                while drain(): pass
                show(decoder.decode(b'',final=True),final=True)
            self.current=None


def pip_arguments(python:Path,detail:Path,packages:list[str],*,upgrade=False,requirements:Path|None=None):
    args=[str(python),'-I','-m','pip','--isolated','--require-virtualenv',
          '--disable-pip-version-check','--log',str(detail),'install',
          '--index-url','https://pypi.org/simple','--timeout','60','--retries','3',
          '--progress-bar','off','--prefer-binary','--only-binary',BINARY_PACKAGES]
    if upgrade: args.append('--upgrade')
    args+=packages
    if requirements: args+=['-r',str(requirements)]
    return args


def scoped_env(job:dict) -> dict:
    env=clean_environment()
    temp=Path(job['stage'])/'temp'; temp.mkdir(parents=True,exist_ok=True)
    env.update(TMP=str(temp),TEMP=str(temp))
    return env


def copy_tree_checked(src:Path,dest:Path,r:Runner) -> dict:
    source_files=files_in(src,r.check)
    dest.mkdir(parents=True,exist_ok=False)
    mapping={}; last=0.0
    for i,p in enumerate(source_files,1):
        r.check(); rel=p.relative_to(src); target=dest/rel; target.parent.mkdir(parents=True,exist_ok=True)
        h=hashlib.sha256(); size=0
        with p.open('rb') as a,target.open('xb') as b:
            while True:
                r.check(); block=a.read(1024*1024)
                if not block: break
                b.write(block); h.update(block); size+=len(block)
        if sha256(target,r.check)!=h.hexdigest(): raise BuildError('완료 폴더 복사 검증 실패: '+str(rel))
        mapping[rel.as_posix()]={'bytes':size,'sha256':h.hexdigest()}
        if time.monotonic()-last>1 or i==len(source_files):
            r.emit(f'[완료 폴더 복사] {i}/{len(source_files)} / {rel}'); last=time.monotonic()
    return mapping


def make_zip(source:Path,target:Path,mapping:dict,r:Runner) -> dict:
    """Only called after EXE checks pass. Read every member and compare SHA-256, not just CRC."""
    temp=target.with_suffix('.partial')
    last=0.0
    try:
        with zipfile.ZipFile(temp,'x',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
            for i,(rel,expected) in enumerate(mapping.items(),1):
                r.check(); path=source/rel
                if time.monotonic()-last>1 or i==len(mapping):
                    r.emit(f'[ZIP 생성] {i}/{len(mapping)} / {rel}'); last=time.monotonic()
                # ZipFile.write can spend a long time on a large file. Stream with cancellation.
                zi=zipfile.ZipInfo.from_file(path,source.name+'/'+rel)
                zi.compress_type=zipfile.ZIP_DEFLATED
                zi._compresslevel=1  # ZipInfo streaming uses this field on Python 3.10-3.13.
                with path.open('rb') as a,z.open(zi,'w',force_zip64=True) as b:
                    while True:
                        r.check(); block=a.read(1024*1024)
                        if not block: break
                        b.write(block)
        r.emit('[ZIP 검사] 전체 항목 SHA-256과 크기를 확인합니다.')
        with zipfile.ZipFile(temp) as z:
            entries=z.infolist()
            if len(entries)!=len(mapping): raise BuildError('ZIP 파일 개수 불일치')
            expected_names={source.name+'/'+rel for rel in mapping}
            if {i.filename for i in entries}!=expected_names: raise BuildError('ZIP 경로 목록 불일치')
            last=0.0
            for i,entry in enumerate(entries,1):
                r.check(); rel=entry.filename[len(source.name)+1:]; h=hashlib.sha256(); size=0
                with z.open(entry) as stream:
                    while True:
                        r.check(); block=stream.read(1024*1024)
                        if not block: break
                        h.update(block); size+=len(block)
                if h.hexdigest()!=mapping[rel]['sha256'] or size!=mapping[rel]['bytes']:
                    raise BuildError('ZIP 파일 내용 불일치: '+rel)
                if time.monotonic()-last>1 or i==len(entries):
                    r.emit(f'[ZIP 검사] {i}/{len(entries)} / {rel}'); last=time.monotonic()
        os.replace(temp,target)
        return {'path':str(target),'bytes':target.stat().st_size,'sha256':sha256(target,r.check),
                'contents_sha256_verified':True,'extracted_zip_executed':False}
    except BaseException:
        temp.unlink(missing_ok=True)
        raise


def strict_report(path:Path,nonce:str,frozen:bool,code:int,expected=None,required_count=22) -> dict:
    import viewer_build_support as support
    value=support.verify_viewer_report(path,nonce,frozen,code,expected)
    if value.get('required_check_count')!=required_count or len(value.get('checks',[]))!=required_count:
        raise BuildError(f'이 뷰어는 {required_count}개 검사를 모두 수행해야 합니다. 검사 축소는 허용하지 않습니다.')
    if value.get('platform')!='win32' or value.get('completed') is not True:
        raise BuildError('Windows 검사 완료 기록이 아닙니다.')
    if frozen:
        for row in value['checks']:
            if row.get('status')=='passed':continue
            optional_office=(row.get('name')=='Office 동봉 상태·변환 결과·제외 엔진 부재'
                and row.get('status')=='not_applicable' and value.get('office_bundle_included') is False
                and row.get('details',{}).get('excluded_engines_absent') is True)
            if not optional_office:
                raise BuildError('완성 EXE 필수 검사에서는 건너뛴 항목을 허용하지 않습니다.')
    return value


def probe_viewer(r:Runner,command:list[str],report:Path,cwd:Path,*,frozen:bool,expected=None,required_count=22):
    import viewer_build_support as support
    nonce=uuid.uuid4().hex
    report.unlink(missing_ok=True)
    env=support.viewer_probe_environment(frozen,Path(command[0])); env.update(TEMP=str(Path(r.job['stage'])/'temp'),TMP=str(Path(r.job['stage'])/'temp'))
    code,_=r.command(command+[str(report),nonce],label=report.stem,cwd=cwd,timeout=900,env=env,
                     allow_failure=True,log_path=report.with_suffix('.log'),report=report)
    result=strict_report(report,nonce,frozen,code,expected,required_count)
    for row in result['checks']:
        r.emit(f"[검사 {row['status']}] {row['name']}")
        if row['name'].startswith('Type3 '):
            r.emit('[Type3 검증] '+json.dumps(row.get('details',{}),ensure_ascii=False,sort_keys=True))
        if row['name']=='짧은 숫자 선택·입력·원본 굵기':
            r.emit('[숫자·굵기 검증] '+json.dumps(row.get('details',{}),ensure_ascii=False,sort_keys=True))
    return result


def assert_environment(path:Path, expected:dict):
    actual=probe_python(str(path))
    if actual['prefix']==actual['base_prefix'] or Path(actual['prefix']).resolve()!=path.parent.parent.resolve():
        raise BuildError('격리된 전용 가상환경이 아닙니다. 전역 Python에는 패키지를 설치하지 않습니다.')
    if actual['version']!=expected['version']:
        raise BuildError('가상환경 Python 버전과 선택한 Python 버전이 다릅니다.')
    return actual


def environment_paths(requested:Path, *, required=False) -> tuple[Path,Path]:
    """Find the physical venv via its configuration, including Store redirection.

    Python's Store package can redirect AppData writes into LocalCache. Resolving
    a path before it exists does not discover the location subsequently created
    by venv. Resolve the existing pyvenv.cfg instead, then use its sibling Scripts
    interpreter. Do not resolve an interpreter link into the global Python.
    """
    requested=Path(requested)
    config=requested/'pyvenv.cfg'
    if config.is_file():
        root=config.resolve(strict=True).parent
    elif required:
        raise BuildError('가상환경 생성 후 pyvenv.cfg를 찾지 못했습니다: '+str(config))
    else:
        root=requested
    python=root/'Scripts'/'python.exe'
    if required and not python.is_file():
        raise BuildError('가상환경 Python 파일을 찾지 못했습니다: '+str(python))
    return root,python


def prepare_build_environment(r:Runner,workspace:Path,base:dict,requirements:Path,env:dict):
    identity=hashlib.sha256((str(base['base'])+repr(base['version'])+sha256(requirements)).encode()).hexdigest()[:12]
    requested=workspace/'envs'/f"cp{base['version'][0]}{base['version'][1]}_{identity}"
    venv,python=environment_paths(requested)
    marker=venv/'tvbuild_environment.json'
    if not marker.is_file():
        if venv.exists():
            # Preserve failed environments, including the one left by 1.5.0.
            stale=venv.with_name(venv.name+'_incomplete_'+uuid.uuid4().hex[:6]); venv.rename(stale)
            r.emit('[미완성 가상환경 보존] '+str(stale))
        r.command([sys.executable,'-I','-m','venv',str(venv)],label='venv_create',timeout=300,env=env)
        venv,python=environment_paths(venv,required=True)
        marker=venv/'tvbuild_environment.json'
        r.emit('[가상환경 실제 경로] '+str(venv))
        actual=assert_environment(python,base)
        r.command(pip_arguments(python,r.logs/'pip_bootstrap_detail.log',['pip>=25.2','setuptools>=70','wheel'],upgrade=True),
                  label='pip_bootstrap',timeout=1800,env=env)
        # A failed bootstrap must not be mistaken for a complete environment.
        atomic_json(marker,{'tool':VERSION,'base':base,'requirements_sha256':sha256(requirements)})
    else:
        recorded=read_json(marker)
        if recorded.get('base',{}).get('base')!=base['base'] or recorded.get('requirements_sha256')!=sha256(requirements):
            raise BuildError('전용 가상환경 기록이 다릅니다. 가상환경을 자동으로 덮어쓰지 않습니다.')
        venv,python=environment_paths(venv,required=True)
        r.emit('[가상환경 실제 경로] '+str(venv))
        actual=assert_environment(python,base)
    return venv,python,actual


def prepare_icon_for_build(main:Path,record:dict) -> dict:
    icon=Path(record['staged_path'])
    if sha256(icon)!=record['sha256']: raise BuildError('검사한 ICO와 임시 ICO가 다릅니다.')
    if not record['has_png']:
        # The viewer reads PNG frames for its Qt icon; normalize classic DIB ICOs.
        import io
        from PIL import Image
        with Image.open(icon) as image:
            image.load(); normalized=image.convert('RGBA'); data=io.BytesIO()
            sizes=[(s,s) for s in (16,20,24,32,40,48,64,128,256)
                   if s<=min(normalized.size)]
            normalized.save(data,format='ICO',sizes=sizes or [normalized.size],bitmap_format='png')
        icon.write_bytes(data.getvalue())
    info=inspect_ico(icon.read_bytes())
    if not info['has_png']: raise BuildError('Qt 뷰어용 ICO 변환 실패')
    embed_staged_icon(main,icon)
    return dict(record,built_sha256=info['sha256'],built_frames=info['frames'])


def prepare(r:Runner,job:dict):
    if os.name!='nt': raise BuildError('Windows 빌드는 Windows PC에서 실행해야 합니다.')
    if job.get('make_installer'):
        from github_release import normalize_repo
        job['iscc']=str(inspect_iscc(job.get('iscc','')))
        job['release_repo']=normalize_repo(job.get('release_repo','faintstar85-source/the-viewer'))
    base=probe_python(sys.executable)
    r.phase('1/8 · PDFium 소스·선택 Office·라이선스 자료를 검사합니다.',5)
    source=Path(job['source']).resolve(); inspection=inspect_source(source)
    atomic_json(r.run/'Source_Inspection.json',inspection)
    stage=Path(job['stage']); stage.mkdir(parents=True,exist_ok=False)
    stage=stage.resolve(strict=True); job['stage']=str(stage)
    (stage/'temp').mkdir()
    staged_source=stage/'source'; staged_source.mkdir()
    snapshot=staged_source/'The_Viewer.py'; shutil.copy2(source,snapshot)
    if sha256(snapshot)!=inspection['sha256']: raise BuildError('소스 복사 중 원본이 변경되었습니다.')
    job['inspection']=inspection
    job['icon']=stage_viewer_icon(snapshot,stage/'app.ico',job.get('icon_path',''))
    atomic_json(r.run/'Icon_Inspection.json',job['icon'])
    engines=(Path(job['engines_root']).expanduser().resolve() if job.get('engines_root') else source.parent/'engines')
    job['engines_root']=str(engines)
    r.emit('[동봉 엔진 폴더] '+str(engines))
    checks=[]
    job['included_engines']=[]
    if not job.get('include_office',False):r.emit('[Office 미동봉] 사용자 PC에 설치된 변환 프로그램을 사용합니다.')
    for engine in (REQUIRED_ENGINES if job.get('include_office',False) else ()):
        if not (engines/engine).exists():
            r.emit('[Office 미동봉] Office 문서는 설치된 변환 프로그램이 필요합니다.')
            continue
        license_gate.verify_optional_office_source(engines/engine)
        checks.append(verify_bundle(engines/engine,engine,destination=stage/'engines'/engine,
                                    check=r.check,emit=r.emit))
        job['included_engines'].append(engine)
    atomic_json(r.run/'Engine_Inspection.json',checks)
    job['backend_modules']=license_gate.stage_backend_modules(snapshot,staged_source)
    package=Path(job['builder_root']) if job.get('builder_root') else None
    job['license_evidence']=license_gate.prepare_license_materials(
        source,stage/'licenses',HERE,builder_root=package,
        selected=job.get('compliance_root',''),engines_root=job.get('engines_root',''))
    r.emit('[라이선스 자료 폴더] '+job['license_evidence']['origin'])
    atomic_json(r.run/'License_Inspection.json',job['license_evidence'])
    workspace=Path(job['workspace']); workspace.mkdir(parents=True,exist_ok=True)
    workspace=workspace.resolve(strict=True); job['workspace']=str(workspace)
    requirements=HERE/'requirements_build.txt'
    r.phase('2/8 · 전용 가상환경을 준비합니다. 전역 Python은 변경하지 않습니다.',12)
    env=scoped_env(job)
    venv,python,actual=prepare_build_environment(r,workspace,base,requirements,env)
    job['venv_python']=str(python); job['venv']=str(venv)
    atomic_json(r.run/'Environment.json',{'base':base,'venv':actual,'requirements_sha256':sha256(requirements),
                'index':'https://pypi.org/simple','global_packages_modified':False})
    r.phase('3/8 · 전용 가상환경에 PySide6 및 빌드 의존성을 설치합니다.',20)
    # Qt-only first: makes this user's failure directly attributable in a separate log.
    r.command(pip_arguments(python,r.logs/'pip_Qt_detail.log',['PySide6==6.11.1']),label='pip_Qt',timeout=1800,env=env)
    r.command(pip_arguments(python,r.logs/'pip_requirements_detail.log',[],requirements=requirements),
              label='pip_requirements',timeout=2400,env=env)
    r.command([python,'-I','-m','pip','--isolated','--require-virtualenv','check'],label='pip_check',timeout=120,
              env=env,log_path=r.run/'pip_check.txt')
    r.command([python,'-I','-m','pip','--isolated','list','--format=freeze'],label='installed_versions',timeout=120,
              env=env,log_path=r.run/'installed_versions.txt')
    # Capture actual build-tool version as part of the reproducibility record.
    r.command([python,'-I','-m','PyInstaller','--version'],label='pyinstaller_version',timeout=60,env=env)
    atomic_json(r.run/'worker_job.json',job)
    r.command([python,'-u',str(HERE/'build_runner.py'),'--inside',str(r.run/'worker_job.json')],
              label='build_worker',cwd=HERE,timeout=7200,env=env)
    result=read_json(r.run/'Build_Result.json')
    if result.get('status')!='passed' or result.get('windows_exe_checks_passed') is not True:
        raise BuildError('빌드 작업이 끝났지만 완료 검사 기록이 없습니다.')
    r.phase('8/8 · EXE 기능 검사와 ZIP 무결성 검사 완료',100)


def build_inside(r:Runner,job:dict):
    import viewer_build_support as support
    if os.name!='nt' or sys.prefix==sys.base_prefix or Path(sys.executable).resolve()!=Path(job['venv_python']).resolve():
        raise BuildError('Windows 전용 가상환경에서만 빌드 작업을 수행합니다.')
    stage=Path(job['stage']); staged_source=stage/'source'; main=staged_source/'The_Viewer.py'
    info=job['inspection']; env=scoped_env(job)
    if sha256(main)!=info['sha256']: raise BuildError('검사한 소스와 임시 소스가 다릅니다.')
    icon=Path(job['icon']['staged_path'])
    icon_record=prepare_icon_for_build(main,job['icon'])
    atomic_json(r.run/'Icon_Inspection.json',icon_record)
    # Export the single viewer PY before adding the private frozen-check launcher.
    release_py=r.run/f"The_Viewer_v{info['version']}.py"
    release_py.write_text(main.read_text(encoding='utf-8-sig'),encoding='utf-8-sig')
    release_record={'path':str(release_py),'bytes':release_py.stat().st_size,'sha256':sha256(release_py)}
    if inspect_source(release_py)['version']!=info['version']: raise BuildError('업로드용 PY 버전 불일치')
    helper=support.prepare_viewer_check(main)
    r.phase('4/8 · 소스의 PDF·그림·한글·작업 프로세스를 검사합니다.',32)
    before=probe_viewer(r,[sys.executable,str(helper),str(main)],r.run/'뷰어_사전검사.json',stage,frozen=False,required_count=info['required_check_count'])
    hwpx=support.hwpx_build_requirement(['hwpx'])
    wheel_licenses=license_gate.collect_installed_notices(stage/'licenses')
    atomic_json(r.run/'Runtime_License_Inspection.json',wheel_licenses)
    hook=stage/'viewer_runtime_hook.py'; hook.write_text(support.VIEWER_RUNTIME_HOOK_SOURCE,encoding='utf-8')
    options=support.viewer_collection_options()+[('--runtime-hook',str(hook))]
    options.append(('--add-data',str(stage/'licenses')+os.pathsep+'licenses'))
    for engine in job['included_engines']:
        options.append(('--add-data',str(stage/'engines'/engine)+os.pathsep+'engines/'+engine))
    wrapper=stage/'pyinstaller_runner.py'
    license_gate.write_pyinstaller_wrapper(wrapper,r.run/'Excluded_Collection.json')
    args=['--noconfirm','--onedir','--windowed','--noupx','--clean','--contents-directory','_internal',
          '--name','The_Viewer','--distpath',str(stage/'dist'),'--workpath',str(stage/'work'),
          '--specpath',str(stage/'spec'),'--paths',str(staged_source),'--paths',str(HERE),'--log-level','INFO',
          '--icon',str(icon)]
    for flag,value in dict.fromkeys(options): args += [flag,value]
    for module in ('tensorflow','torch','torchvision','torchaudio','jax','jaxlib','paddle','paddleocr'):
        if module not in info['imports']: args += ['--exclude-module',module]
    for module in license_gate.EXCLUDED_MODULES:args += ['--exclude-module',module]
    args.append(str(main))
    r.phase('5/8 · PyInstaller 폴더형 EXE를 만듭니다.',48)
    try:
        r.command([sys.executable,str(wrapper),*args],label='pyinstaller_build',cwd=HERE,timeout=5400,env=env)
    finally:
        # Retain warnings even when PyInstaller fails before producing an EXE.
        warnings=list((stage/'work').rglob('warn-*.txt'))
        for i,p in enumerate(warnings):
            try: shutil.copy2(p,r.logs/f'PyInstaller_warnings_{i}.txt')
            except OSError as exc: r.emit('[경고 로그 보존 실패] '+str(exc))
    product=stage/'dist'/'The_Viewer'; exe=product/'The_Viewer.exe'; internal=product/'_internal'
    if not exe.is_file() or not internal.is_dir() or not list(internal.glob('python*.dll')):
        raise BuildError('EXE 또는 _internal/Python DLL이 누락됐습니다.')
    r.phase('6/8 · 동봉 엔진·한글 템플릿과 완성 EXE를 검사합니다.',70)
    deliveries=[]
    for engine in job['included_engines']:
        delivery=verify_bundle(internal/'engines'/engine,engine,check=r.check,emit=r.emit)
        original=next(x for x in read_json(r.run/'Engine_Inspection.json') if x['engine']==engine)
        if delivery['manifest_sha256']!=original['manifest_sha256']:
            raise BuildError('패키징 전후 엔진 검사 목록이 다릅니다: '+engine)
        deliveries.append(delivery)
    atomic_json(r.run/'Engine_Delivery.json',deliveries)
    support.validate_hwpx_bundle(product,'onedir',hwpx)
    license_audit=license_gate.audit_product(product)
    atomic_json(r.run/'License_Delivery.json',license_audit)
    probe_cwd=stage/'probe_work'; probe_cwd.mkdir()
    after=probe_viewer(r,[str(exe),support.VIEWER_CHECK_FLAG],r.run/'뷰어_배포검사.json',probe_cwd,
                       frozen=True,expected=before['versions'],required_count=info['required_check_count'])
    r.phase('7/8 · 최종 위치에 복사하고 다시 실행해 검사합니다.',83)
    final=r.run/'완료파일'/'The_Viewer'
    final.parent.mkdir(exist_ok=True)
    mapping=copy_tree_checked(product,final,r)
    final_probe=r.run/'probe_cwd'; final_probe.mkdir()
    final_check=probe_viewer(r,[str(final/'The_Viewer.exe'),support.VIEWER_CHECK_FLAG],
                     r.run/'뷰어_최종위치검사.json',final_probe,frozen=True,expected=before['versions'],required_count=info['required_check_count'])
    # EXE must not mutate the shipped tree during its offline test.
    current={p.relative_to(final).as_posix() for p in files_in(final,r.check)}
    if current!=set(mapping): raise BuildError('EXE 검사 중 배포 폴더 파일 목록이 변경됐습니다.')
    r.phase('8/8 · 전달 ZIP을 만들고 모든 파일 해시를 확인합니다.',94)
    zip_path=r.run/f"The_Viewer_v{info['version']}_windows_x64.zip"
    zip_info=make_zip(final,zip_path,mapping,r)
    installer=None
    if job.get('make_installer'):
        r.phase('설치 EXE 생성 · 현재 사용자 설치와 업데이트를 준비합니다.',97)
        installer=build_installer(r,final,icon,info['version'],Path(job['iscc']),job['release_repo'])
    result={'tool_version':VERSION,'status':'passed','viewer_version':info['version'],'source':info['source'],
            'source_sha256':info['sha256'],'icon':icon_record,'release_py':release_record,'venv':job['venv'],'run_dir':str(r.run),'exe':str(final/'The_Viewer.exe'),
            'zip':zip_info,'installer':installer,'engine_profile':info['engine_profile'],
            'license_file_audit':license_audit,'included_engines':job['included_engines'],'source_checks':len(before['checks']),'exe_checks':len(after['checks']),
            'final_location_checks':len(final_check['checks']),'windows_exe_checks_passed':True,
            'tested_platform':sys.platform,'python':sys.version.split()[0],
            'different_clean_pc_tested':False,'actual_printer_tested':False,'DeepL_API_tested':False,
            'layout_accuracy_fully_verified':False,'public_redistribution_approval':False,
            'completed_at':time.strftime('%Y-%m-%dT%H:%M:%S%z')}
    atomic_json(r.run/'Build_Result.json',result)
    r.emit('[완료] '+str(zip_path))
    # Remove only this tool's owned per-run staging; output/logs/venv stay available.
    if job.get('cleanup_stage',True):
        try: shutil.rmtree(stage)
        except OSError as exc: r.emit('[임시공간 정리 주의] '+str(exc))


def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument('job',nargs='?'); p.add_argument('--inside'); a=p.parse_args(argv)
    path=Path(a.inside or a.job or '')
    if not path.is_file(): p.error('job JSON 파일을 지정하세요.')
    job=read_json(path); r=Runner(job)
    try:
        if a.inside: build_inside(r,job)
        else:
            atomic_json(r.run/'Build_Result.json',{'tool_version':VERSION,'status':'running',
                'windows_exe_checks_passed':False,'public_redistribution_approval':False})
            with WorkspaceLock(Path(job['workspace'])/'build.lock'): prepare(r,job)
        return 0
    except BaseException as exc:
        if isinstance(exc,(KeyboardInterrupt,Cancelled)): state='cancelled'
        else: state='failed'
        detail=''.join(traceback.format_exception(type(exc),exc,exc.__traceback__))
        r.emit('[중단] '+str(exc))
        # Keep the inner worker's more specific failure instead of replacing it with exit status.
        existing={}
        try: existing=read_json(r.run/'Build_Result.json')
        except (OSError,ValueError): pass
        if existing.get('status') not in ('failed','cancelled') or a.inside:
            atomic_json(r.run/'Build_Result.json',{'tool_version':VERSION,'status':state,
                'error':str(exc),'traceback':detail,'windows_exe_checks_passed':False,
                'public_redistribution_approval':False,'run_dir':str(r.run)})
            (r.run/'Failure_Summary.txt').write_text(detail,encoding='utf-8')
        return 2 if state=='cancelled' else 1
    finally: r.close()

if __name__=='__main__': raise SystemExit(main())
