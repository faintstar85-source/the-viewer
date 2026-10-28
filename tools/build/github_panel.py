"""Tk GitHub tab integrated into the single-file Viewer builder."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import tempfile
import threading
import time
import traceback
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from build_common import BuildError, Cancelled, atomic_json, inspect_source, read_json
from github_release import (DEFAULT_REPO, OFFICIAL_LINKS, GitHubClient, default_notes, find_gh,
                            normalize_repo, prepare_release, load_prepared_release, changes_from_notes)


def settings_root() -> Path:
    return Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'TVBuild'


def spec_fingerprint(spec: dict) -> str:
    return hashlib.sha256(json.dumps(spec,ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest()


class GitHubPanel:
    def __init__(self,app,parent):
        self.app=app; self.parent=parent; self.busy=False; self.events=queue.Queue()
        self.client=None; self.cancel_event=threading.Event(); self.plan=None; self.plan_fingerprint=''
        self.linked_build=None; self.last_url=''; self.poll_job=None; self.closed=False; self.controls=[]
        self.settings_file=settings_root()/'github_single_settings.json'
        try: saved=read_json(self.settings_file)
        except (OSError,ValueError): saved={}
        if not isinstance(saved,dict): saved={}
        self.repo=tk.StringVar(value=saved.get('repo') or DEFAULT_REPO)
        self.gh=tk.StringVar(value=saved.get('gh') or find_gh())
        self.source=tk.StringVar(value=saved.get('py') or app.source.get())
        self.zip=tk.StringVar(value=saved.get('zip',''))
        self.installer=tk.StringVar(value=saved.get('installer',''))
        self.output=tk.StringVar(value=saved.get('output') or str(settings_root()/'GitHub_Uploads'))
        self.tag=tk.StringVar(value=saved.get('tag') or 'v3.13.38')
        self.title=tk.StringVar(value=saved.get('title') or 'The Viewer 3.13.38')
        self.publish=tk.BooleanVar(value=saved.get('publish',True)); self.prerelease=tk.BooleanVar(value=saved.get('prerelease',False))
        self.status=tk.StringVar(value='ZIP·PY 선택 → 버전 안내 준비 → GitHub 업로드')
        self.version=tk.StringVar(value='뷰어 버전: 확인 전')
        self.setup(saved.get('changes') or default_notes('3.13.38'))
        self.poll_job=app.root.after(100,self.poll)

    def setup(self,changes):
        outer=ttk.Frame(self.parent,padding=18); outer.pack(fill='both',expand=True)
        ttk.Label(outer,text='The Viewer  /  GitHub 업로드',style='Title.TLabel').pack(anchor='w')
        ttk.Label(outer,text='설치 EXE + ZIP + 뷰어 PY + 버전 안내를 같은 릴리스에 올립니다.',style='Small.TLabel').pack(anchor='w',pady=(3,10))
        form=ttk.Frame(outer); form.pack(fill='x'); form.columnconfigure(1,weight=1)
        self.row(form,0,'저장소',self.repo,lambda:self.open_repo(),'저장소 열기')
        self.row(form,1,'GitHub CLI gh.exe',self.gh,self.choose_gh,'gh.exe 선택')
        actions=ttk.Frame(outer); actions.pack(fill='x',pady=(5,8))
        for text,callback in [('CLI 설치 안내',lambda:webbrowser.open(OFFICIAL_LINKS['CLI 설치'])),
                              ('브라우저 로그인',self.login),('연결 확인',self.check_connection)]:
            button=ttk.Button(actions,text=text,command=callback); button.pack(side='left',padx=(0,6)); self.controls.append(button)
        ttk.Label(actions,textvariable=self.version,style='Small.TLabel').pack(side='right')
        files=ttk.Frame(outer); files.pack(fill='x'); files.columnconfigure(1,weight=1)
        self.row(files,0,'올릴 ZIP',self.zip,self.choose_zip,'ZIP 선택')
        self.row(files,1,'올릴 뷰어 PY',self.source,self.choose_source,'PY 선택')
        self.row(files,2,'올릴 설치 EXE (선택)',self.installer,self.choose_installer,'설치 EXE 선택')
        self.row(files,3,'업로드 준비 폴더',self.output,self.choose_output,'폴더 선택')
        release=ttk.Frame(outer); release.pack(fill='x',pady=(6,4)); release.columnconfigure(1,weight=1); release.columnconfigure(3,weight=2)
        ttk.Label(release,text='버전 태그').grid(row=0,column=0,padx=(0,8))
        entry=ttk.Entry(release,textvariable=self.tag,width=18); entry.grid(row=0,column=1,sticky='ew'); self.controls.append(entry)
        ttk.Label(release,text='릴리스 제목').grid(row=0,column=2,padx=(15,8))
        entry=ttk.Entry(release,textvariable=self.title); entry.grid(row=0,column=3,sticky='ew'); self.controls.append(entry)
        flags=ttk.Frame(outer); flags.pack(fill='x',pady=4)
        for text,var in [('첨부파일 확인 후 공개',self.publish),('시험 배포 표시',self.prerelease)]:
            button=ttk.Checkbutton(flags,text=text,variable=var); button.pack(side='left',padx=(0,15)); self.controls.append(button)
        ttk.Label(outer,text='버전 수정 내역 (직접 수정 가능)',font=('맑은 고딕',10,'bold')).pack(anchor='w',pady=(8,4))
        self.notes=ScrolledText(outer,height=7,font=('맑은 고딕',10),wrap='word'); self.notes.pack(fill='x')
        self.notes.insert('1.0',changes)
        actions=ttk.Frame(outer); actions.pack(fill='x',pady=9)
        self.prepare_button=ttk.Button(actions,text='1. 안내·파일 준비',command=self.prepare); self.prepare_button.pack(side='left'); self.controls.append(self.prepare_button)
        self.resume_button=ttk.Button(actions,text='준비 폴더 불러오기',command=self.load_prepared)
        self.resume_button.pack(side='left',padx=(6,0));self.controls.append(self.resume_button)
        self.upload_button=ttk.Button(actions,text='2. 설치 EXE + ZIP + PY 올리기',command=self.upload,state='disabled'); self.upload_button.pack(side='left',padx=6)
        self.cancel_button=ttk.Button(actions,text='중지',command=self.cancel,state='disabled'); self.cancel_button.pack(side='left',padx=6)
        ttk.Button(actions,text='준비 폴더',command=self.open_folder).pack(side='right')
        ttk.Button(actions,text='릴리스 열기',command=self.open_release).pack(side='right',padx=6)
        ttk.Label(outer,textvariable=self.status,font=('맑은 고딕',10,'bold'),wraplength=970).pack(anchor='w',pady=(0,6))
        self.log=ScrolledText(outer,height=7,font=('Consolas',9),wrap='word',bg='#101c2a',fg='#deebf7')
        self.log.pack(fill='both',expand=True); self.log.configure(state='disabled')

    def row(self,parent,row,label,var,callback,caption):
        ttk.Label(parent,text=label).grid(row=row,column=0,sticky='w',pady=4,padx=(0,10))
        entry=ttk.Entry(parent,textvariable=var); entry.grid(row=row,column=1,sticky='ew',pady=4)
        button=ttk.Button(parent,text=caption,command=callback); button.grid(row=row,column=2,padx=(8,0),pady=4,sticky='ew')
        self.controls.extend((entry,button))

    def snapshot(self):
        return {'repo':self.repo.get(),'gh':self.gh.get(),'py':self.source.get(),'zip':self.zip.get(),'installer':self.installer.get(),
                'output':self.output.get(),'tag':self.tag.get(),'title':self.title.get(),
                'publish':self.publish.get(),'prerelease':self.prerelease.get(),
                'changes':self.notes.get('1.0','end-1c'),'build_result':self.linked_build}

    def locked(self,value):
        self.busy=value
        for control in self.controls: control.configure(state='disabled' if value else 'normal')
        self.notes.configure(state='disabled' if value else 'normal')
        self.upload_button.configure(state='normal' if not value and self.plan else 'disabled')
        self.cancel_button.configure(state='normal' if value else 'disabled')
        self.app.start_button.configure(state='disabled' if value or self.app.busy else 'normal')

    def task(self,kind,worker):
        if self.busy or self.app.busy:
            messagebox.showinfo('작업 중','현재 작업이 끝난 뒤 실행하세요.'); return
        spec=self.snapshot(); self.cancel_event=threading.Event(); self.locked(True)
        self.status.set({'prepare':'ZIP·PY 확인 및 버전 안내 작성 중…','upload':'GitHub에 업로드하고 첨부파일을 확인합니다…',
                         'resume':'기존 준비 파일·안내·SHA-256 확인 중…',
                         'check':'GitHub 연결 확인 중…','source':'뷰어 PY 확인 중…','login':'로그인 창을 엽니다…'}.get(kind,'작업 중…'))
        def run():
            folder=None
            try:
                settings={key:value for key,value in spec.items() if key!='build_result'}
                atomic_json(self.settings_file,settings)
                if kind in ('upload','check'):
                    folder=(Path(self.plan['folder']) if kind=='upload' else Path(spec['output'])/('Connection_'+str(time.time_ns())))
                    self.client=GitHubClient(spec['gh'],folder,emit=lambda line:self.events.put(('log',line)),cancel=self.cancel_event)
                value=worker(spec)
                self.events.put(('done',(kind,value,spec)))
            except BaseException as exc:
                detail=traceback.format_exc()
                if folder:
                    try: (folder/'GitHub_Failure.txt').write_text(detail,encoding='utf-8-sig')
                    except OSError: pass
                self.events.put(('error',(str(exc),detail)))
            finally: self.client=None
        threading.Thread(target=run,daemon=True).start()

    def choose_gh(self):
        value=filedialog.askopenfilename(title='GitHub CLI의 gh.exe 선택',filetypes=[('GitHub CLI','gh.exe'),('실행파일','*.exe')])
        if value: self.gh.set(value)
    def choose_zip(self):
        value=filedialog.askopenfilename(title='업로드할 ZIP 선택',filetypes=[('ZIP','*.zip')])
        if value: self.zip.set(value); self.linked_build=None; self.plan=None; self.upload_button.configure(state='disabled')
    def choose_source(self):
        value=filedialog.askopenfilename(title='업로드할 The_Viewer.py 선택',filetypes=[('Python','*.py')])
        if value:
            self.source.set(value); self.linked_build=None; self.plan=None
            self.task('source',lambda spec:inspect_source(Path(spec['py'])))
    def choose_installer(self):
        value=filedialog.askopenfilename(title='배포할 The Viewer 설치 EXE 선택',filetypes=[('Windows installer','*.exe')])
        if value:self.installer.set(value);self.plan=None;self.upload_button.configure(state='disabled')
    def choose_output(self):
        value=filedialog.askdirectory(title='업로드 준비 파일을 저장할 폴더')
        if value: self.output.set(value)
    def login(self):
        def start(spec):
            path=Path(spec['gh']).expanduser().resolve()
            if not path.is_file() or path.name.lower()!='gh.exe': raise BuildError('GitHub CLI의 gh.exe를 먼저 선택하세요.')
            if os.name!='nt': raise BuildError('이 로그인 버튼은 Windows용입니다.')
            process=subprocess.Popen([str(path),'auth','login','--hostname','github.com','--git-protocol','https','--web'],
                creationflags=getattr(subprocess,'CREATE_NEW_CONSOLE',0))
            return process.pid
        self.task('login',start)
    def check_connection(self):
        def check(spec):
            self.client.command(['--version'])
            self.client.command(['auth','status','--hostname','github.com'])
            user=self.client.api('user'); repository=self.client.api('repos/'+normalize_repo(spec['repo']))
            return {'login':user['login'],'repo':repository['full_name'],'push':bool(repository.get('permissions',{}).get('push'))}
        self.task('check',check)
    def prepare(self):
        if self.busy or self.app.busy: return
        self.plan=None; self.upload_button.configure(state='disabled')
        self.task('prepare',lambda spec:prepare_release(spec,check=self.cancel_check,emit=lambda line:self.events.put(('log',line))))
    def load_prepared(self):
        if self.busy or self.app.busy:return
        folder=filedialog.askdirectory(title='실패했던 업로드 준비 폴더 선택 (Upload_Plan.json 포함)',
                                       initialdir=self.output.get())
        if not folder:return
        self.plan=None;self.upload_button.configure(state='disabled')
        self.task('resume',lambda spec:load_prepared_release(Path(folder),check=self.cancel_check,
                                        emit=lambda line:self.events.put(('log',line))))

    def restore_prepared(self,plan):
        self.plan=plan;self.linked_build=None;self.last_url=''
        self.repo.set(plan['repo']);self.tag.set(plan['tag']);self.title.set(plan['title'])
        self.publish.set(plan['publish']);self.prerelease.set(plan['prerelease'])
        self.output.set(str(Path(plan['folder']).parent))
        self.source.set(next(a['path'] for a in plan['assets'] if a['name'].lower().endswith('.py')))
        self.zip.set(next(a['path'] for a in plan['assets'] if a['name'].lower().endswith('.zip')))
        self.installer.set(next((a['path'] for a in plan['assets'] if a['name'].lower().endswith('.exe')),''))
        self.version.set('뷰어 버전: '+plan['viewer_version'])
        self.notes.configure(state='normal');self.notes.delete('1.0','end')
        self.notes.insert('1.0',changes_from_notes(plan['notes']))
        self.plan_fingerprint=spec_fingerprint(self.snapshot())
        self.status.set('기존 준비 폴더 복원 완료. 공개 설정을 확인하고 [2. 설치 EXE + ZIP + PY 올리기]를 누르세요.')
        self.write('준비 폴더: '+plan['folder'])
    def upload(self):
        if not self.plan:
            messagebox.showinfo('안내 준비','먼저 [1. 안내·파일 준비]로 ZIP/PY와 버전 안내를 확인하세요.'); return
        if self.plan_fingerprint!=spec_fingerprint(self.snapshot()):
            self.plan=None; self.upload_button.configure(state='disabled')
            messagebox.showinfo('입력 변경','파일이나 버전 안내가 바뀌었습니다. [1. 안내·파일 준비]를 다시 실행하세요.'); return
        self.task('upload',lambda spec:self.client.publish(self.plan))
    def cancel_check(self):
        if self.cancel_event.is_set(): raise Cancelled('업로드 준비 중지를 요청했습니다.')
    def cancel(self):
        if self.busy:
            self.cancel_event.set(); self.status.set('작업 중지 요청 중… 생성된 파일과 초안은 보존합니다.')
            self.cancel_button.configure(state='disabled')

    def set_build_result(self,result):
        if self.busy: return
        self.linked_build=result; self.plan=None
        self.source.set(result['release_py']['path']); self.zip.set(result['zip']['path'])
        self.installer.set(result['installer']['path'] if result.get('installer') else '')
        version=result['viewer_version']; self.tag.set('v'+version); self.title.set('The Viewer '+version)
        self.version.set('뷰어 버전: '+version)
        self.notes.delete('1.0','end'); self.notes.insert('1.0',default_notes(version))
        self.upload_button.configure(state='disabled')
        self.status.set('완료한 설치 EXE·ZIP·PY가 연결됐습니다. 버전 안내를 확인하고 [1. 안내·파일 준비]를 누르세요.')
    def write(self,text):
        self.log.configure(state='normal'); self.log.insert('end',str(text)+'\n')
        lines=int(self.log.index('end-1c').split('.')[0])
        if lines>2200: self.log.delete('1.0',f'{lines-2000}.0')
        self.log.see('end'); self.log.configure(state='disabled')
    def poll(self):
        if self.closed: return
        self.poll_job=None; started=time.monotonic()
        try:
            for _ in range(100):
                if time.monotonic()-started>.02: break
                kind,value=self.events.get_nowait()
                if kind=='log': self.write(value)
                elif kind=='error':
                    message,detail=value; self.locked(False); self.status.set('작업 중단: '+message[:160]); self.write(detail)
                    messagebox.showerror('GitHub 작업 중단',message[:2000])
                elif kind=='done':
                    task,result,spec=value
                    if task=='prepare':
                        self.plan=result; self.plan_fingerprint=spec_fingerprint(spec)
                        self.status.set('ZIP·PY·버전 안내 준비 완료. 확인 후 [2. ZIP + PY 올리기]를 누르세요.')
                        self.write(result['notes']); self.write('준비 폴더: '+result['folder'])
                        for item in result['assets']: self.write(f"{item['name']} / {item['bytes']} bytes / SHA-256 {item['sha256']}")
                    elif task=='resume':self.restore_prepared(result)
                    elif task=='upload':
                        self.last_url=result['url']; self.status.set(('초안 저장' if result['draft'] else '공개 완료')+' · 첨부파일 해시 확인 통과')
                        self.write(self.last_url); webbrowser.open(self.last_url)
                    elif task=='source':
                        version=result['version']; self.version.set('뷰어 버전: '+version)
                        self.tag.set('v'+version); self.title.set('The Viewer '+version)
                        self.notes.configure(state='normal')
                        self.notes.delete('1.0','end'); self.notes.insert('1.0',default_notes(version))
                        self.status.set('PY 확인 완료. ZIP과 버전 안내를 준비하세요.')
                    elif task=='check':
                        self.status.set(f"로그인: {result['login']} / 저장소: {result['repo']} / 업로드 권한: {'확인' if result['push'] else '없음'}")
                    elif task=='login': self.status.set('로그인 창에서 브라우저 인증을 완료한 뒤 [연결 확인]을 누르세요.')
                    self.locked(False)
        except queue.Empty: pass
        self.poll_job=self.app.root.after(100,self.poll)
    def open_repo(self):
        try: webbrowser.open('https://github.com/'+normalize_repo(self.repo.get()))
        except BuildError as exc: messagebox.showerror('저장소',str(exc))
    def open_release(self):
        if self.last_url: webbrowser.open(self.last_url)
        else:
            try: webbrowser.open('https://github.com/'+normalize_repo(self.repo.get())+'/releases')
            except BuildError as exc: messagebox.showerror('릴리스',str(exc))
    def open_folder(self):
        path=Path(self.plan['folder']) if self.plan else Path(self.output.get()).expanduser()
        try:
            if os.name=='nt': os.startfile(str(path))
            else: subprocess.Popen(['xdg-open',str(path)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except OSError as exc: messagebox.showerror('준비 폴더',str(exc))
    def close(self):
        self.closed=True
        if self.poll_job:
            try: self.app.root.after_cancel(self.poll_job)
            except tk.TclError: pass
            self.poll_job=None
