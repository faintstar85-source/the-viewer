# GitHub 문서 배치 안내

대상 저장소: [faintstar85-source/the-viewer](https://github.com/faintstar85-source/the-viewer)

이 묶음은 **v3.13.15 소스를 기준으로 작성한 Markdown 문서**입니다. 압축을 풀어 저장소 안에서 아래 경로를 유지합니다.

## 파일별 넣을 곳

| 파일 | 저장소 위치·용도 |
| --- | --- |
| `README.md` | 저장소 최상위의 프로그램 소개 |
| `CHANGELOG.md` | 저장소 최상위의 수정 기록. 기존 3.12.4·3.6.2·3.6.1 기록을 유지 |
| `docs/PROGRAM_GUIDE.md` | 사용 안내의 시작 페이지 |
| `docs/PDF_EDITING.md` | 글상자·그림·선·정렬·같은 좌표 붙여넣기 |
| `docs/DUAL_VIEW.md` | A\|A 검토·1\|2 두 장 보기·차이 후보 |
| `docs/FORMATS_AND_CONVERSION.md` | 지원 형식·번역·한글 변환·인쇄 |
| `docs/INSTALL_AND_UPDATE.md` | 설치·기본 앱·프로그램 업데이트 |
| `docs/BUILD_AND_GITHUB.md` | 패키징·compliance·GitHub 업로드 |
| `releases/RELEASE_NOTES_v3.13.15.md` | v3.13.15 릴리스 설명의 본문 |
| `UPLOAD_GUIDE.md` | 이 문서 배치 안내 |

README의 `assets/guide/01_viewer.png`부터 `06_update.png`는 현재 저장소에 있는 이미지 경로를 사용합니다. 이번 ZIP에 이미지를 다시 넣지는 않았습니다. 기존 `assets/guide` 폴더를 유지합니다.

## 웹에서 문서 파일 올리기

1. 저장소에서 **Add file → Upload files**를 선택합니다.
2. 압축을 푼 뒤 README·CHANGELOG·docs·releases 등 문서 파일과 폴더를 올립니다.
3. 파일 경로와 기존 파일 변경 내용을 확인합니다.
4. 변경 설명을 적고 새 브랜치 또는 현재 브랜치의 저장 방식을 선택해 커밋합니다.

README나 CHANGELOG 한 파일만 고칠 때는 파일의 편집 버튼으로 내용을 바꾸고 Preview에서 확인한 뒤 저장할 수도 있습니다.

근거: [GitHub 파일 추가 공식 안내](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository), [파일 편집 공식 안내](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files).

## 릴리스 설명에 넣기

릴리스 본문에는 **RELEASE_NOTES_v3.13.15.md의 내용을 붙여넣습니다.** Markdown 파일을 첨부만 하는 것과 릴리스 본문을 채우는 것은 별도 작업입니다.

GitHub 전용 매니저를 사용할 때는 이 MD를 **이번 버전 수정사항** 입력에 불러올 수 있습니다. 실제로 배포할 뷰어 PY·설치 EXE·ZIP을 선택하고, 생성된 설명과 파일 목록을 확인한 뒤 업로드합니다.

매니저 v2.0.0은 README·PROGRAM_GUIDE·CHANGELOG를 자체 생성합니다. 자동 생성 뒤에는 이번에 작성한 문서 파일과 링크가 유지되는지 확인하고, 최종 문서 파일을 반영합니다.

근거: The_Viewer_GitHub_Manager.py v2.0.0의 수정사항 불러오기·문서 생성 코드와 [GitHub 릴리스 관리 안내](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

## 소스와 문서 버전 맞추기

2026-10-06에 확인한 저장소 스냅샷에서는 README가 **3.12.4**를 안내하고, `pdf_page_dragger.py`의 `APP_VERSION`은 **3.6.2**입니다.

이번 문서를 반영할 때 저장소의 **pdf_page_dragger.py**도 최신 **The_Viewer_v3.13.15.py 내용**으로 함께 갱신합니다. 소스 원본 파일 이름은 로컬에서 유지하고, 저장소 경로를 맞춰 업로드하면 됩니다. GitHub 전용 매니저 v2.0.0은 선택한 뷰어 PY를 `pdf_page_dragger.py` 경로로 준비합니다.

검토한 저장소의 `requirements.txt`도 이전 구성입니다. 최신 소스 실행 안내에는 제작 패키지의 `requirements_build.txt`에 있는 PDFium 계열 의존성을 함께 반영해야 합니다.

확인한 스냅샷: 커밋 `c838231825cb8bc4efc9376a2f9b2738cacc35e2`의 [README](https://github.com/faintstar85-source/the-viewer/blob/c838231825cb8bc4efc9376a2f9b2738cacc35e2/README.md), [소스 버전](https://github.com/faintstar85-source/the-viewer/blob/c838231825cb8bc4efc9376a2f9b2738cacc35e2/pdf_page_dragger.py#L92), [의존성 목록](https://github.com/faintstar85-source/the-viewer/blob/c838231825cb8bc4efc9376a2f9b2738cacc35e2/requirements.txt).

