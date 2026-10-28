#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Small standalone build UI. Does not import PySide6 or the old manager.
All discovery and build I/O is outside Tk callbacks. No startup installs or uploads.
"""
from __future__ import annotations
import hashlib
import json
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import uuid
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from build_common import (VERSION,CONTROL_PREFIX,BuildError,probe_python,python_candidates,
    clean_environment,kill_tree,atomic_json,read_json,diagnostic_zip,choose_build_workspace)
from github_panel import GitHubPanel
from installer_build import find_iscc, INNO_DOWNLOAD_URL
from license_gate import find_compliance_root

HERE=Path(__file__).resolve().parent


def desktop_path() -> Path:
    if os.name=='nt':
        try:
            import ctypes
            buf=ctypes.create_unicode_buffer(32768)
            if ctypes.windll.shell32.SHGetFolderPathW(None,0x10,None,0,buf)==0:
                return Path(buf.value)
        except (OSError,AttributeError): pass
    return Path.home()/'Desktop'


def workspace_path() -> Path:
    candidates=[Path(os.environ.get('LOCALAPPDATA',str(Path.home())))/'TVBuild']
    user=hashlib.sha256(str(Path.home()).encode()).hexdigest()[:8]
    if os.name=='nt': candidates.append(Path(os.environ.get('PUBLIC',r'C:\Users\Public'))/('TVBuild_'+user))
    candidates.append(Path(tempfile.gettempdir())/('TVBuild_'+user))
    for p in candidates:
        if str(p).isascii(): return p
    return candidates[0]


class BuilderUI:
    def __init__(self,root:tk.Tk,initial_source=''):
        self.root=root; self.root.title('The Viewer 설치 EXE + GitHub · '+VERSION)
        width=min(1080,max(860,self.root.winfo_screenwidth()-60))
        height=min(900,max(660,self.root.winfo_screenheight()-90))
        self.root.geometry(f'{width}x{height}'); self.root.minsize(860,660)
        self.events=queue.Queue(); self.process=None; self.busy=False; self.closing=False
        self.started=0.; self.last_line=0.; self.run_dir=None; self.choices=[]; self.choice_info={}
        self.auto_diagnostic=None
        self.scan_id=0; self.cancel_since=0.; self.kill_started=False
        self.source=tk.StringVar(value=initial_source)
        self.icon=tk.StringVar(value='')
        self.engines=tk.StringVar(value='')
        self.builder_root=Path(os.environ.get('THEVIEWER_BUILDER_ROOT',str(HERE))).resolve()
        self.compliance=tk.StringVar(value=os.environ.get('THEVIEWER_COMPLIANCE_DIR',''))
        self.discover_compliance()
        self.include_office=tk.BooleanVar(value=False)
        self.make_installer=tk.BooleanVar(value=True)
        self.iscc=tk.StringVar(value=find_iscc())
        self.python=tk.StringVar(); self.output=tk.StringVar(value=str(desktop_path()/'TheViewer_Builds'))
        self.workspace=tk.StringVar(value=str(workspace_path()))
        self.phase=tk.StringVar(value='The_Viewer.py 선택 → Python 확인 → 패키징 시작')
        self.health=tk.StringVar(value='빌더 화면에는 PySide6가 필요하지 않습니다.')
        self.progress=tk.DoubleVar(value=0)
        self.setup()
        self.root.protocol('WM_DELETE_WINDOW',self.close)
        self.poll_job=self.root.after(100,self.poll)
        self.scan()

    def setup(self):
        s=ttk.Style(); s.theme_use('clam')
        s.configure('TFrame',background='#f3f5f8')
        s.configure('TLabel',background='#f3f5f8',foreground='#1c2f44')
        s.configure('Title.TLabel',font=('맑은 고딕',18,'bold'))
        s.configure('Small.TLabel',font=('맑은 고딕',9),foreground='#536578')
        s.configure('Start.TButton',font=('맑은 고딕',11,'bold'),padding=(14,10))
        self.notebook=ttk.Notebook(self.root); self.notebook.pack(fill='both',expand=True)
        self.build_tab=ttk.Frame(self.notebook); self.github_tab=ttk.Frame(self.notebook)
        self.notebook.add(self.build_tab,text='  패키징  '); self.notebook.add(self.github_tab,text='  GitHub 업로드  ')
        outer=ttk.Frame(self.build_tab,padding=20); outer.pack(fill='both',expand=True)
        ttk.Label(outer,text='The Viewer  /  전용 패키징',style='Title.TLabel').pack(anchor='w')
        ttk.Label(outer,text='소스 선택 → EXE 검사 → 설치 EXE·ZIP → GitHub 배포',style='Small.TLabel').pack(anchor='w',pady=(5,15))
        form=ttk.Frame(outer); form.pack(fill='x'); form.columnconfigure(1,weight=1)
        self.lockable=[]
        self.row(form,0,'뷰어 소스 PY',self.source,self.choose_source,'파일 선택')
        ttk.Label(form,text='빌드용 Python').grid(row=1,column=0,sticky='w',padx=(0,10),pady=7)
        self.pybox=ttk.Combobox(form,textvariable=self.python,state='readonly')
        self.pybox.grid(row=1,column=1,sticky='ew',pady=7)
        pyactions=ttk.Frame(form); pyactions.grid(row=1,column=2,padx=(8,0))
        b=ttk.Button(pyactions,text='다시 찾기',command=self.scan); b.pack(side='left'); self.lockable.append(b)
        b=ttk.Button(pyactions,text='직접 선택',command=self.choose_python); b.pack(side='left',padx=(5,0)); self.lockable.append(b)
        self.row(form,2,'결과 저장 폴더',self.output,self.choose_output,'폴더 선택')
        self.row(form,3,'가상환경·임시공간',self.workspace,self.choose_workspace,'폴더 선택')
        self.row(form,4,'아이콘 ICO (선택)',self.icon,self.choose_icon,'ICO 선택')
        self.row(form,5,'Office 엔진 폴더 (선택)',self.engines,self.choose_engines,'폴더 선택')
        self.row(form,6,'설치 컴파일러 ISCC.exe',self.iscc,self.choose_iscc,'ISCC.exe 선택')
        self.row(form,7,'라이선스 compliance 폴더',self.compliance,self.choose_compliance,'폴더 선택')
        install_actions=ttk.Frame(outer);install_actions.pack(fill='x',pady=(7,2))
        install_option=ttk.Checkbutton(install_actions,text='설치 EXE도 만들기 · 사용하는 PC에는 Python 설치 불필요',variable=self.make_installer)
        install_option.pack(side='left');self.lockable.append(install_option)
        office_actions=ttk.Frame(outer);office_actions.pack(fill='x',pady=(2,2))
        office_option=ttk.Checkbutton(office_actions,text='LibreOffice 동봉 · 정확한 버전의 대응 소스를 준비한 경우에만',variable=self.include_office)
        office_option.pack(side='left');self.lockable.append(office_option)
        install_help=ttk.Button(install_actions,text='Inno Setup 설치 안내',command=self.open_inno_help)
        install_help.pack(side='right');self.lockable.append(install_help)
        ttk.Label(outer,text='기본은 Office 엔진을 동봉하지 않습니다. Office 변환은 사용자 PC에 설치된 프로그램을 사용합니다. DWG·AI·EPS는 제외합니다.',
                  style='Small.TLabel',wraplength=960).pack(anchor='w',pady=(10,3))
        ttk.Label(outer,text='compliance는 소스·빌더·엔진 옆에서 자동으로 찾습니다. 별도 위치라면 폴더 선택을 누르세요. ICO를 비워두면 기본 아이콘을 사용합니다.',
                  style='Small.TLabel',wraplength=960).pack(anchor='w',pady=(0,8))
        actions=ttk.Frame(outer); actions.pack(fill='x',pady=6)
        self.start_button=ttk.Button(actions,text='패키징 시작',style='Start.TButton',command=self.start)
        self.start_button.pack(side='left')
        self.cancel_button=ttk.Button(actions,text='중지',command=self.cancel,state='disabled'); self.cancel_button.pack(side='left',padx=8)
        self.folder_button=ttk.Button(actions,text='결과 폴더',command=self.open_result); self.folder_button.pack(side='right')
        self.diag_button=ttk.Button(actions,text='진단 ZIP 저장',command=self.export_diag,state='disabled'); self.diag_button.pack(side='right',padx=8)
        ttk.Label(outer,textvariable=self.phase,font=('맑은 고딕',10,'bold'),wraplength=940).pack(anchor='w',pady=(15,6))
        ttk.Progressbar(outer,variable=self.progress,maximum=100).pack(fill='x')
        ttk.Label(outer,textvariable=self.health,style='Small.TLabel').pack(anchor='w',pady=(5,9))
        self.log=ScrolledText(outer,font=('Consolas',10),height=10,wrap='word',bg='#101c2a',fg='#deebf7',insertbackground='white')
        self.log.pack(fill='both',expand=True); self.log.configure(state='disabled')
        ttk.Label(outer,text='완료 후 GitHub 탭에 설치 EXE·ZIP·PY 연결 / 새 릴리스 공개 후 뷰어에서 업데이트 안내',
                  style='Small.TLabel',wraplength=970).pack(anchor='w',pady=(9,0))
        self.github=GitHubPanel(self,self.github_tab)

    def row(self,parent,row,label,var,callback,button_text):
        ttk.Label(parent,text=label).grid(row=row,column=0,sticky='w',padx=(0,10),pady=7)
        e=ttk.Entry(parent,textvariable=var); e.grid(row=row,column=1,sticky='ew',pady=7)
        b=ttk.Button(parent,text=button_text,command=callback); b.grid(row=row,column=2,sticky='ew',padx=(8,0),pady=7)
        self.lockable += [e,b]

    def write(self,text):
        self.log.configure(state='normal'); self.log.insert('end',str(text)+'\n')
        lines=int(self.log.index('end-1c').split('.')[0])
        if lines>3500: self.log.delete('1.0',f'{lines-3000}.0')
        self.log.see('end'); self.log.configure(state='disabled')

    def choose_source(self):
        p=filedialog.askopenfilename(title='패키징할 The_Viewer.py 선택 (관리자 PY 제외)',filetypes=[('Python source','*.py')])
        if p:
            self.source.set(p);self.discover_compliance()

    def discover_compliance(self):
        if self.compliance.get().strip():return
        try:
            found=find_compliance_root(Path(self.source.get().strip() or str(self.builder_root/'The_Viewer.py')),
                                       HERE,builder_root=self.builder_root,engines_root=self.engines.get().strip())
            self.compliance.set(str(found))
        except BuildError:pass

    def choose_compliance(self):
        p=filedialog.askdirectory(title='QT_SOURCE_MANIFEST.json이 있는 compliance 폴더 선택',
                                  initialdir=self.compliance.get() or str(self.builder_root))
        if p:self.compliance.set(p)

    def choose_output(self):
        p=filedialog.askdirectory(title='결과를 저장할 폴더')
        if p: self.output.set(p)

    def choose_icon(self):
        p=filedialog.askopenfilename(title='EXE와 뷰어에 적용할 ICO 선택',filetypes=[('Windows icon','*.ico')])
        if p: self.icon.set(p)

    def choose_engines(self):
        p=filedialog.askdirectory(title='LibreOffice가 들어 있는 engines 폴더 선택 (선택)')
        if p:
            self.engines.set(p);self.discover_compliance()

    def choose_iscc(self):
        p=filedialog.askopenfilename(title='Inno Setup의 ISCC.exe 선택',filetypes=[('Inno Setup compiler','ISCC.exe')])
        if p:self.iscc.set(p)

    def open_inno_help(self):
        import webbrowser
        webbrowser.open(INNO_DOWNLOAD_URL)

    def choose_workspace(self):
        p=filedialog.askdirectory(title='가상환경·임시공간용 짧은 영문 경로')
        if p: self.workspace.set(str(Path(p)/'TVBuild'))

    def scan(self):
        if self.busy: return
        self.scan_id+=1; current=self.scan_id
        self.health.set('설치된 Python을 별도 프로세스로 확인하는 중입니다…')
        def worker():
            good=[]; bad=[]
            for path in python_candidates():
                try: good.append(probe_python(path))
                except Exception as exc: bad.append(f'{path}: {exc}')
            good.sort(key=lambda d:(d['store'],tuple(-x for x in d['version'])))
            unique=[]; seen=set()
            for info in good:
                key=info['executable'].casefold()
                if key not in seen: seen.add(key); unique.append(info)
            self.events.put(('pythons',(current,unique,bad)))
        threading.Thread(target=worker,daemon=True).start()

    def choose_python(self):
        p=filedialog.askopenfilename(title='빌드에 사용할 python.exe (x64 CPython 3.11~3.13)',filetypes=[('Python','python.exe'),('실행파일','*.exe')])
        if not p: return
        def worker():
            try: self.events.put(('python_add',probe_python(p)))
            except Exception as exc: self.events.put(('notice',str(exc)))
        threading.Thread(target=worker,daemon=True).start()

    def add_choice(self,info):
        label=f"Python {'.'.join(map(str,info['version']))} x64 {'[Store]' if info['store'] else '[일반]'} · {info['executable']}"
        if label not in self.choice_info:
            self.choice_info[label]=info; self.choices.append(label)
        self.pybox.configure(values=self.choices)
        return label

    def lock(self,value):
        self.busy=value
        for b in self.lockable: b.configure(state='disabled' if value else 'normal')
        self.pybox.configure(state='disabled' if value else 'readonly')
        self.start_button.configure(state='disabled' if value else 'normal')
        self.cancel_button.configure(state='normal' if value else 'disabled')
        self.diag_button.configure(state='normal' if not value and self.run_dir else 'disabled')

    def start(self):
        if self.busy: return
        if getattr(self,'github',None) and self.github.busy:
            messagebox.showinfo('GitHub 작업 중','GitHub 작업이 끝난 뒤 패키징을 시작하세요.'); return
        source=self.source.get().strip(); out=self.output.get().strip(); workspace=self.workspace.get().strip()
        icon=self.icon.get().strip()
        engines=self.engines.get().strip()
        compliance=self.compliance.get().strip()
        builder_root=str(self.builder_root)
        include_office=self.include_office.get()
        make_installer=self.make_installer.get();iscc=self.iscc.get().strip()
        release_repo=self.github.repo.get().strip()
        info=self.choice_info.get(self.python.get())
        if not source or not out or not workspace or not info:
            messagebox.showwarning('선택 확인','뷰어 소스, Python, 결과 폴더를 모두 선택하세요.'); return
        self.run_dir=None
        self.auto_diagnostic=None
        self.lock(True); self.started=self.last_line=time.monotonic(); self.cancel_since=0; self.kill_started=False
        self.progress.set(0); self.phase.set('작업 폴더와 실행 환경을 준비합니다.'); self.write('\n=== 새 패키징 시작 ===')
        def worker():
            process=None
            try:
                root=Path(out).expanduser().resolve(); root.mkdir(parents=True,exist_ok=True)
                cache=choose_build_workspace(Path(workspace),info,root,
                    emit=lambda message:self.events.put(('log',message)))
                self.events.put(('workspace',str(cache)))
                if os.name=='nt':
                    import shutil
                    for p in (cache,root):
                        if shutil.disk_usage(p).free<6*1024**3:
                            raise BuildError('이 빌더의 여유 공간 기준은 작업/출력 드라이브 각각 6GB 이상입니다: '+str(p))
                ident=time.strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:6]
                run=root/('TheViewer_Build_'+ident); run.mkdir(exist_ok=False)
                self.run_dir=run; self.events.put(('run',str(run)))
                job={'source':source,'icon_path':icon,'engines_root':engines,'run_dir':str(run),'workspace':str(cache),'stage':str(cache/'jobs'/ident),'cleanup_stage':True,
                     'make_installer':make_installer,'iscc':iscc,'release_repo':release_repo,'include_office':include_office,
                     'builder_root':builder_root,'compliance_root':compliance}
                atomic_json(run/'job.json',job)
                env=clean_environment()
                log=run/'launcher.log'
                with log.open('w',encoding='utf-8',buffering=1) as output:
                    cmd=[info['executable'],'-u',str(HERE/'build_runner.py'),str(run/'job.json')]
                    output.write('[실행] '+subprocess.list2cmdline(cmd)+'\n')
                    process=subprocess.Popen(cmd,cwd=str(HERE),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                        stdin=subprocess.DEVNULL,text=True,encoding='utf-8',errors='replace',bufsize=1,env=env,
                        creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                    self.process=process
                    self.events.put(('log',f'[빌드 실행] PID {process.pid}\n선택 Python: {info["executable"]}'))
                    for line in process.stdout:
                        output.write(line); output.flush()
                        self.events.put(('line',line.rstrip('\n')))
                    code=process.wait()
                if code:
                    try: self.events.put(('automatic_diagnostic',str(diagnostic_zip(run))))
                    except Exception as exc: self.events.put(('log','진단 ZIP 생성 실패: '+str(exc)))
                self.events.put(('finished',(code,run)))
            except Exception as exc:
                if process is not None and process.poll() is None: kill_tree(process)
                if self.run_dir:
                    try:
                        detail=traceback.format_exc()
                        (self.run_dir/'Failure_Summary.txt').write_text(detail,encoding='utf-8')
                        atomic_json(self.run_dir/'Build_Result.json',{'status':'failed','error':str(exc),
                            'traceback':detail,'windows_exe_checks_passed':False})
                        self.events.put(('automatic_diagnostic',str(diagnostic_zip(self.run_dir))))
                    except Exception: pass
                self.events.put(('start_error',str(exc)))
            finally: self.process=None
        threading.Thread(target=worker,daemon=True).start()

    def cancel(self):
        if not self.busy or self.cancel_since: return
        if not messagebox.askyesno('중지','현재 전용 빌드와 그 자식 프로세스를 중지할까요? 원본 소스는 변경하지 않습니다.'): return
        self.cancel_since=time.monotonic(); self.cancel_button.configure(state='disabled')
        self.phase.set('중지 요청 중… 로그와 실패 기록은 보존합니다.')
        if self.run_dir:
            def request():
                try: (self.run_dir/'CANCEL_REQUESTED').touch(exist_ok=True)
                except OSError as exc: self.events.put(('log','중지 요청 파일 작성 실패: '+str(exc)))
            threading.Thread(target=request,daemon=True).start()

    def open_result(self):
        p=self.run_dir
        if p is None:
            messagebox.showinfo('결과','아직 이번 빌드 결과 폴더가 없습니다.'); return
        try:
            if os.name=='nt': os.startfile(str(p))
            else: subprocess.Popen(['xdg-open',str(p)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except OSError as exc: messagebox.showerror('결과 폴더',str(exc))

    def export_diag(self):
        if self.busy or not self.run_dir: return
        self.diag_button.configure(state='disabled'); folder=self.run_dir
        def worker():
            try: self.events.put(('diagnostic',str(diagnostic_zip(folder))))
            except Exception as exc: self.events.put(('notice',str(exc)))
        threading.Thread(target=worker,daemon=True).start()

    def poll(self):
        if self.poll_job is not None:
            try: self.root.after_cancel(self.poll_job)
            except tk.TclError: pass
            self.poll_job=None
        if self.closing: return
        start=time.monotonic(); buffer=[]
        try:
            for _ in range(160):
                if time.monotonic()-start>.02: break
                kind,data=self.events.get_nowait()
                if kind in ('line','log'):
                    self.last_line=time.monotonic()
                    if kind=='line' and data.startswith(CONTROL_PREFIX):
                        try:
                            value=json.loads(data[len(CONTROL_PREFIX):]); self.phase.set(value['message']); self.progress.set(value['progress'])
                        except (ValueError,KeyError,TypeError): buffer.append(data)
                    else: buffer.append(str(data))
                elif kind=='pythons':
                    ident,good,bad=data
                    if ident!=self.scan_id or self.busy: continue
                    self.choices=[]; self.choice_info={}
                    for info in good: self.add_choice(info)
                    if self.choices: self.python.set(self.choices[0]); self.health.set('Python 선택 완료. 처음 빌드할 때 전용 가상환경을 생성합니다.')
                    else: self.python.set(''); self.health.set('사용 가능한 x64 Python 3.11~3.13을 찾지 못했습니다. 직접 선택을 사용하세요.')
                    for error in bad: buffer.append('[Python 후보 제외] '+error)
                elif kind=='python_add':
                    if not self.busy: self.python.set(self.add_choice(data))
                elif kind=='run': buffer.append('[결과 위치] '+str(data))
                elif kind=='workspace': self.workspace.set(str(data))
                elif kind=='start_error':
                    self.lock(False); self.phase.set('시작 실패 — 원본은 변경하지 않았습니다.'); buffer.append(str(data))
                    messagebox.showerror('시작 실패',str(data))
                elif kind=='finished':
                    code,run=data; self.lock(False)
                    try: result=read_json(run/'Build_Result.json')
                    except (OSError,ValueError): result={}
                    ok=code==0 and result.get('status')=='passed' and result.get('windows_exe_checks_passed') is True
                    if ok:
                        self.progress.set(100); self.phase.set('완료 — '+('설치 EXE·' if result.get('installer') else '')+'ZIP 준비 및 뷰어 검사 통과')
                        buffer.append('완료 ZIP: '+result.get('zip',{}).get('path',''))
                        if result.get('installer'):buffer.append('설치 EXE: '+result['installer']['path'])
                        if result.get('release_py') and getattr(self,'github',None): self.github.set_build_result(result)
                        self.open_result()
                    else:
                        self.phase.set('중단 — 실제 오류는 아래 로그와 Failure_Summary.txt를 확인하세요.')
                        buffer.append('[빌드 결과] '+str(result.get('error') or f'실행 종료 코드 {code}. launcher.log 확인'))
                        diagnostic_message=('전체 오류 로그를 담은 진단 ZIP:\n'+self.auto_diagnostic
                                            if self.auto_diagnostic else '[진단 ZIP 저장]을 눌러 전체 로그를 모을 수 있습니다.')
                        messagebox.showerror('패키징 중단','패키징이 중단됐습니다. '+diagnostic_message+
                            '\n\n[결과 폴더]에서 Failure_Summary.txt와 logs의 PyInstaller/pip 로그를 확인할 수 있습니다.')
                    self.health.set('작업 종료. 기존 소스·엔진·전역 Python 패키지는 변경하지 않았습니다.')
                elif kind=='automatic_diagnostic':
                    self.auto_diagnostic=str(data)
                    buffer.append('전체 빌드 로그를 포함한 진단 ZIP: '+str(data))
                elif kind=='diagnostic':
                    self.diag_button.configure(state='normal'); buffer.append('진단 ZIP: '+str(data))
                    messagebox.showinfo('진단 ZIP 저장','로컬 경로와 빌드 로그가 포함됩니다. 공유 전에 확인하세요.\n\n'+str(data))
                    self.open_result()
                elif kind=='notice':
                    self.diag_button.configure(state='normal' if self.run_dir and not self.busy else 'disabled')
                    messagebox.showerror('확인',str(data))
        except queue.Empty: pass
        if buffer: self.write('\n'.join(buffer))
        if self.busy:
            elapsed=time.monotonic()-self.started; quiet=time.monotonic()-self.last_line
            self.health.set(f'경과 {int(elapsed)//60:02d}:{int(elapsed)%60:02d} · 마지막 출력 {quiet:.0f}초 전 · 화면 응답 유지 / 빌드 완료와는 별도')
            if self.cancel_since and time.monotonic()-self.cancel_since>6 and not self.kill_started:
                self.kill_started=True; process=self.process
                if process is not None: threading.Thread(target=kill_tree,args=(process,),daemon=True).start()
        self.poll_job=self.root.after(100,self.poll)

    def close(self):
        if getattr(self,'github',None) and self.github.busy:
            self.github.cancel(); messagebox.showinfo('작업 종료 대기','GitHub 작업 중지 완료 후 창을 닫아주세요.'); return
        if self.busy:
            self.cancel(); messagebox.showinfo('작업 종료 대기','중지 완료 후 창을 닫아주세요. 실행 중인 빌드를 남기지 않도록 종료를 기다립니다.'); return
        self.closing=True
        if getattr(self,'github',None): self.github.close()
        if self.poll_job is not None:
            try: self.root.after_cancel(self.poll_job)
            except tk.TclError: pass
            self.poll_job=None
        self.root.destroy()


def main():
    if os.name!='nt':
        print('이 패키징 도구는 Windows 실행용입니다.',flush=True)
        return 1
    root=tk.Tk()
    initial=sys.argv[1] if len(sys.argv)>1 and sys.argv[1].lower().endswith('.py') else ''
    BuilderUI(root,initial); root.mainloop(); return 0

if __name__=='__main__': raise SystemExit(main())
