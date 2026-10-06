# 패키징과 GitHub 업데이트

[사용 안내](PROGRAM_GUIDE.md) · [업로드 파일 배치](../UPLOAD_GUIDE.md)

## 설치 EXE 만들기

제작 도구는 **TheViewer_Build_Standalone_v1.5.7.py**입니다. 빌더 보조 코드가 포함된 단일 PY이며, 패키징과 GitHub 업로드 탭을 제공합니다.

1. 제작 PC에서 패키징 PY를 실행합니다.
2. 뷰어 소스로 **The_Viewer_v3.13.30.py**를 선택합니다.
3. 필요하면 ICO를 선택합니다. 비워두면 뷰어 내장 아이콘을 사용합니다.
4. 기존 제작·배포 자료의 **compliance 폴더 전체**를 선택합니다. 빌더는 원래 빌더·뷰어·엔진 옆에서도 자동 탐색합니다.
5. 설치 EXE가 필요한 경우 Inno Setup의 **ISCC.exe**를 선택합니다.
6. **패키징 시작**을 누르고 빌드 및 완성 파일 검사를 확인합니다.

제작 PC는 Windows x64의 지원 Python 환경을 사용합니다. 빌더가 전용 가상환경에 의존성을 준비하며 첫 빌드에는 인터넷 연결이 필요합니다. 설치 EXE 제작에는 빌더에서 지원하는 Inno Setup 6.4 이상 또는 7이 필요합니다.

v3.13.30의 설치 파일명은 `The_Viewer_Setup_3.13.30_x64.exe` 형태입니다. 이 문서는 파일명 규칙을 안내하며 완성 EXE를 포함하지 않습니다.

## compliance

compliance에는 Qt/PySide6와 certifi 등의 라이선스·대응 소스가 들어 있습니다. 단독 빌더 PY에는 이 폴더가 내장되어 있지 않으므로 기존 배포 자료의 폴더 구조와 아카이브를 함께 유지합니다.

기본 빌드는 Office 엔진을 동봉하지 않습니다. LibreOffice 동봉을 선택하면 해당 엔진의 정확한 버전 정보와 대응 소스 자료도 필요합니다.

## GitHub 전용 업데이트 PY

파일: **The_Viewer_GitHub_Manager_v2.1.0.py**

1. **로그인 · 설정**에서 Git·GitHub CLI와 gh.exe를 확인하고 브라우저로 로그인합니다.
2. 저장소를 `faintstar85-source/the-viewer`로 지정합니다.
3. **간편 업로드**에서 다음 세 파일을 선택합니다.
   - `TheViewer_GitHub_Markdown_v3.13.30.zip`
   - `The_Viewer_v3.13.30.py`
   - 빌드가 완료된 `The_Viewer_Setup_3.13.30_x64.exe`
4. 버전과 파일 목록을 확인하고 **업로드 시작 · 릴리스 공개**를 누릅니다.

매니저는 뷰어 PY를 저장소의 `pdf_page_dragger.py`로 준비하고, Markdown의 폴더 구조·본문을 그대로 반영합니다. 해당 버전의 릴리스 설명을 본문으로 사용하며 EXE·문서 ZIP·뷰어 PY를 릴리스에 첨부합니다. 파일 선택만으로 공개하지 않습니다.

소스 실행 의존성 안내도 PDFium 계열에 맞춰 준비합니다. 원본 PY는 유지하고 업로드용 작업 사본을 만듭니다.

## 확인 범위

이번 전달 과정에서 v3.13.30 소스의 빌더 인식, 내장 보조 코드 검사, GitHub 매니저의 문서·소스 준비를 확인합니다. Windows에서의 실제 EXE 빌드와 원격 GitHub 업로드는 제작 PC에서 수행합니다.

근거: 제공된 패키징 PY, GitHub 업데이트 PY와 [뷰어 소스](../pdf_page_dragger.py).
