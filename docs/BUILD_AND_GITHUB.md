# 패키징과 GitHub 업데이트 — v3.13.38

[사용 안내](PROGRAM_GUIDE.md) · [업로드 순서](../UPLOAD_GUIDE.md)

## 1. Windows 설치 EXE 만들기

파일: **TheViewer_Build_Standalone_v1.5.9.py**

1. 패키징 PY를 실행하고 첨부받은 `The_Viewer_v3.13.38(2).py`를 선택합니다. `(2)`가 붙어 있어도 내부 버전을 읽으므로 이름을 바꿀 필요가 없습니다.
2. 아이콘을 바꿀 경우 **ICO 선택**에서 지정합니다. 비워두면 선택한 뷰어의 내장 아이콘을 사용합니다.
3. 기존 패키징 자료의 **compliance 폴더 전체**를 지정합니다. 이 폴더는 단독 PY 안에 포함되어 있지 않습니다.
4. 설치 파일을 만들 경우 **설치 EXE도 만들기**를 켜고 Inno Setup의 **ISCC.exe**를 선택합니다.
5. **패키징 시작**을 누릅니다. 소스·EXE·최종 폴더 실행 검사를 통과하면 결과가 생성됩니다.

제작 PC는 x64 CPython 3.11~3.13과 tkinter를 사용하는 Windows 환경입니다. 의존성은 전용 가상환경에 설치하며 첫 준비에는 인터넷이 필요합니다. 설치 EXE 제작은 Inno Setup 6.4 이상 또는 7을 사용하는 기존 빌드 경로를 유지합니다.

결과: `The_Viewer_Setup_3.13.38_x64.exe`, `The_Viewer_v3.13.38_windows_x64.zip`, `The_Viewer_v3.13.38.py`. 설치 EXE를 선택하지 않으면 앞의 설치 파일은 생성하지 않습니다.

compliance는 기존과 동일하게 Qt/PySide6 6.11.1 및 certifi 대응 소스·라이선스 자료를 검사합니다. 임의로 빈 폴더를 만들면 통과하지 않습니다. Office 엔진은 기본 미동봉이며, LibreOffice 동봉을 선택한 경우 해당 엔진 자료도 필요합니다.

## 2. 저장소 문서·소스·릴리스 업데이트

파일: **The_Viewer_GitHub_Manager_v2.1.2.py**

1. **로그인 · 설정**에서 Git·GitHub CLI와 `gh.exe`를 확인하고 브라우저로 로그인합니다.
2. 저장소가 `faintstar85-source/the-viewer`인지 확인합니다.
3. **간편 업로드**에 아래 세 파일을 선택하거나 함께 드롭합니다.
   - `TheViewer_GitHub_Markdown_v3.13.38.zip`
   - 빌드한 `The_Viewer_Setup_3.13.38_x64.exe`
   - 이번 빌드에서 만든 `The_Viewer_v3.13.38.py`
4. **릴리스 설명 확인**으로 본문을 확인합니다.
5. **업로드 시작 · 릴리스 공개**를 누르면 선택 저장소의 문서·소스를 반영하고 첨부파일을 확인한 뒤 공개합니다.

MD ZIP에는 README.md, CHANGELOG.md, docs/, releases/가 들어 있습니다. 압축을 풀지 않고 매니저에 넣습니다. `TheViewer_GIT_Update_v3.13.38.md`는 릴리스 설명을 따로 읽거나 복사할 때 쓰는 단일 문서입니다.

매니저는 PY를 저장소의 `pdf_page_dragger.py`로 준비합니다. 원본을 수정하지 않고 업로드용 작업 사본에 저장소 주소를 반영합니다. 같은 폴더에 버전이 일치하는 뷰어 PY와 MD ZIP이 하나의 내용으로 확인되면 자동으로 선택합니다. 실행·선택만으로 업로드하지 않습니다.

패키징 PY 안의 **GitHub 업로드** 탭은 설치 EXE·실행 ZIP·PY 릴리스 첨부를 위한 기존 기능입니다. **README 등 저장소 문서까지 갱신할 때는 위 전용 매니저를 사용하세요.**

## 3. 입력만 확인하기

```bat
py TheViewer_Build_Standalone_v1.5.9.py --check-payload
py TheViewer_Build_Standalone_v1.5.9.py --check-source "The_Viewer_v3.13.38(2).py"
py The_Viewer_GitHub_Manager_v2.1.2.py --check-inputs "The_Viewer_v3.13.38(2).py" "TheViewer_GitHub_Markdown_v3.13.38.zip"
```

위 명령은 입력 검사이며 GitHub에 업로드하지 않습니다. 매니저 GUI에는 PySide6가 필요합니다. 설치되어 있지 않으면 `py -m pip install PySide6`로 준비합니다. 패키징 도구 자체 화면에는 PySide6가 필요하지 않습니다.

## 확인 범위와 근거

Windows 설치 EXE 빌드·설치와 원격 GitHub 업로드는 이 전달 과정에서 수행하지 않았습니다. 실제 Windows 검사는 제작 PC에서 생성되는 Build_Result.json 및 검사 로그로 확인합니다. 빌드 시 설치되는 라이브러리 버전은 requirements_build.txt의 기존 고정값을 유지합니다.

- [PyInstaller 공식 사용 안내](https://pyinstaller.org/en/stable/usage.html)
- [GitHub CLI 릴리스 생성](https://cli.github.com/manual/gh_release_create)
- [GitHub CLI 릴리스 공개](https://cli.github.com/manual/gh_release_edit)
- [뷰어 소스](../pdf_page_dragger.py)
