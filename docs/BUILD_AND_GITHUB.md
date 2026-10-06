# 패키징과 GitHub 업로드

[사용 안내](PROGRAM_GUIDE.md) · [문서 배치 안내](../UPLOAD_GUIDE.md)

## 설치 EXE 만들기

확인한 제작 파일은 **TheViewer_Build_Standalone_v1.5.6.py**입니다. 설치 EXE 생성과 GitHub 업로드가 한 PY에 포함되어 있습니다.

제작 PC는 Windows x64, CPython 3.11~3.13과 tkinter를 사용합니다. 설치 EXE 생성에는 Inno Setup의 **ISCC.exe**가 필요합니다. 빌더 안내의 지원 범위는 Inno Setup 6.4 이상 또는 7입니다.

1. 제작용 배포 ZIP 전체를 압축 해제합니다.
2. 패키징할 최신 **The_Viewer_v3.13.15.py**를 준비합니다.
3. **compliance 폴더 전체**를 이 뷰어 PY와 같은 폴더에 둡니다.
4. 패키징 PY를 실행하고 뷰어 PY, 사용할 ICO, ISCC.exe를 선택합니다.
5. 패키징을 시작하고 빌드·검사 결과를 확인합니다.

아이콘 선택란을 비워 두면 뷰어에 내장된 아이콘을 사용합니다. 제작 도구는 전용 가상환경에 빌드 의존성을 설치합니다. 첫 빌드에는 인터넷 연결과 작업 공간이 필요합니다.

뷰어 버전이 3.13.15일 때 설치 파일명은 `The_Viewer_Setup_3.13.15_x64.exe` 형태입니다. 이는 빌더의 파일명 규칙이며, 해당 파일이 이미 공개되었다는 의미는 아닙니다.

## compliance 위치

확인한 **TheViewer_Build_GitHub_v1.5.6_Viewer3.13.7.zip**의 위치는 다음과 같습니다.

`TheViewer_3.13.7_Source_Build/compliance`

폴더 안에는 `QT_SOURCE_MANIFEST.json`, `CERTIFI_SOURCE_MANIFEST.json`, 안내문과 `OpenSource_Sources`의 소스 아카이브가 들어 있습니다. 폴더 구조와 아카이브를 함께 유지합니다.

이 자료의 Qt/PySide6 버전은 **6.11.1**, certifi 버전은 **2026.4.22**로 검토한 빌더의 고정 의존성과 일치합니다. 빌드 중 파일 크기와 해시를 검사합니다.

## 통합 PY의 GitHub 업로드 탭

패키징 도구의 **GitHub 업로드** 탭에서 gh.exe 확인 → 로그인 → 안내 준비 → 설치 EXE·ZIP·PY 업로드 순서로 진행합니다. 빌드가 성공하면 생성 파일이 이 탭에 연결됩니다.

## GitHub 전용 매니저

별도로 사용하는 파일은 **The_Viewer_GitHub_Manager.py v2.0.0**입니다. PySide6가 설치된 Python 환경에서 실행합니다.

1. **필요 도구 설치**에서 Git과 GitHub CLI 상태를 확인합니다.
2. **브라우저로 로그인**하고 계정을 확인합니다.
3. 저장소를 `faintstar85-source/the-viewer`로 지정합니다.
4. 최신 뷰어 PY와 버전, 소개, 수정사항을 입력합니다.
5. 배포할 ZIP·EXE를 선택합니다.
6. **전체 업로드 · 공개**를 누르고 문서·파일 목록을 검토한 뒤 실제 업로드를 진행합니다.

매니저는 README, 사용 안내, 수정 기록과 릴리스 설명을 자동 작성합니다. 원본 PY와 별도로 업로드용 사본을 준비합니다. 실제 공개는 프로그램에서 해당 버튼을 눌러 수행합니다.

## 이번 Markdown 파일 사용

이 묶음의 README·사용 안내·세부 문서는 저장소의 파일로 올립니다. 릴리스 본문에는 [v3.13.15 릴리스 설명](../releases/RELEASE_NOTES_v3.13.15.md)의 내용을 사용합니다.

전용 매니저의 **이번 버전 수정사항**에는 이 릴리스 설명 MD를 불러올 수 있습니다. 매니저가 자동 생성하는 README·사용 안내는 프로그램 입력값에 따라 다시 만들어지므로, 이번에 정리한 문서 파일은 자동 업로드 뒤에 최종 확인합니다.

## 소스 실행 의존성

v3.13.15는 PDFium 계열 소스입니다. 검토한 제작 도구는 `pypdfium2`, `pypdf`, `ReportLab`, PySide6와 기타 읽기·변환 의존성을 준비합니다.

2026-10-06에 확인한 저장소의 `requirements.txt`는 PyMuPDF를 포함한 이전 구성이고 `pypdfium2`가 없습니다. 소스 실행 안내를 최신 버전으로 맞출 때는 제작 패키지의 `requirements_build.txt`도 함께 확인합니다.

## 확인 자료

- TheViewer_Build_GitHub_v1.5.6_Viewer3.13.7.zip 안의 단독 빌더·설치 코드·빌드 의존성 목록
- The_Viewer_GitHub_Manager.py v2.0.0의 로그인·업로드·문서 생성 코드
- [GitHub 파일 올리기 공식 안내](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)
- [GitHub 릴리스 관리 공식 안내](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

