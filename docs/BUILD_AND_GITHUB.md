# 패키징과 GitHub 업데이트 — v3.13.39

[사용 안내](PROGRAM_GUIDE.md) · [업로드 순서](../UPLOAD_GUIDE.md)

## Windows 빌드

보완된 제작 묶음은 `TheViewer_v3.13.39_Build_Complete.zip`입니다. 전체 압축을 풀고 `START_BUILD.py`를 실행하면 뷰어 소스와 동봉된 compliance 경로를 지정해 패키징 v1.5.9를 엽니다.

1. 선택된 소스가 `The_Viewer_v3.13.39.py`인지 확인합니다.
2. 아이콘을 바꾸려면 빌드 전에 ICO 파일을 지정합니다.
3. 설치 파일이 필요하면 **설치 EXE도 만들기**와 Inno Setup의 **ISCC.exe**를 지정합니다.
4. **패키징 시작**을 누르고 결과와 진단 로그를 확인합니다.

compliance에는 Qt/PySide6 6.11.1과 certifi의 라이선스·대응 소스가 들어 있습니다. PY만 따로 옮기거나 자료를 누락하면 자료 검사에서 중단될 수 있습니다. MD 문서 ZIP은 이 빌드 자료를 대신하지 않습니다.

설치 EXE의 기본 파일명은 `The_Viewer_Setup_3.13.39_x64.exe`입니다. 설치 EXE 제작을 선택하지 않은 빌드에는 이 파일이 생성되지 않습니다.

## 문서·소스·릴리스 업로드

`The_Viewer_GitHub_Manager_v2.1.2.py`를 실행합니다.

1. **로그인 · 설정**에서 필요한 도구와 GitHub 로그인을 확인합니다.
2. 저장소가 `faintstar85-source/the-viewer`인지 확인합니다.
3. **간편 업로드**에 다음 세 파일을 선택합니다.
   - `TheViewer_GitHub_Markdown_v3.13.39.zip`
   - `The_Viewer_Setup_3.13.39_x64.exe`
   - 빌드에 사용한 `The_Viewer_v3.13.39.py`
4. **릴리스 설명 확인**으로 본문과 버전을 확인합니다.
5. **업로드 시작 · 릴리스 공개**를 누릅니다.

MD ZIP은 풀지 않고 선택합니다. README.md, CHANGELOG.md, UPLOAD_GUIDE.md, docs/, releases/의 문서가 저장소에 반영됩니다. 뷰어 PY는 `pdf_page_dragger.py`로 준비하며 원본 파일을 보존합니다. 설치 EXE·MD ZIP·뷰어 PY를 릴리스에 첨부합니다.

매니저 v2.1.2의 같은 폴더 자동 선택은 v3.13.38을 기준으로 합니다. 이번 파일들은 직접 선택하세요. 선택한 PY의 실제 버전과 v3.13.39 릴리스 문서가 일치하면 입력 검사 대상이 됩니다.

## 입력 검사

```bat
py The_Viewer_GitHub_Manager_v2.1.2.py --check-inputs "The_Viewer_v3.13.39.py" "TheViewer_GitHub_Markdown_v3.13.39.zip"
```

이 명령은 PY 문법, 소스 버전, MD ZIP 구성과 해당 버전 릴리스 문서를 검사합니다. GitHub 로그인·업로드는 하지 않으며 설치 EXE의 실행 검사를 대신하지 않습니다.

## 확인 범위

v3.13.39의 빌드 완료는 제작자가 전달했습니다. 이 문서 묶음을 준비하면서 Windows 설치·실행·탐색기 드래그를 새로 검사하거나 GitHub에 공개하지는 않았습니다. 해당 PC의 빌드 결과는 `Build_Result.json`과 로그로 확인합니다.

기준 자료: `The_Viewer_GitHub_Manager_v2.1.2.py`의 `check_local_inputs`, `quick_project`, `quick_publish`, `markdown_bundle` 및 [뷰어 소스](../pdf_page_dragger.py).
