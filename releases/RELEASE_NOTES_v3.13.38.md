# The Viewer v3.13.38

첨부된 데스크톱 v3.13.38 소스에 맞춘 패키징·GitHub 업데이트 자료입니다.

## 반영 내용

- PDF 읽기 작업 프로세스가 GUI·편집 모듈보다 먼저 시작하도록 구성되어 있습니다.
- 일반 PDF는 PDFium에서 읽으며, 양식 페이지와 편집 요청은 PY에 포함된 호환 코드로 처리합니다.
- PDF 문자 검색, 검색 결과 위치 표시와 검색 전 위치로 돌아가기를 지원합니다.
- 패키징 검사 요청을 v3.13.38의 render/preview/search/editinfo 형식에 맞췄습니다.
- GitHub 매니저가 _viewer_fast_pdf_worker를 인식하고 pypdfium2==5.14.0을 기록하도록 수정했습니다.

## 사용

PDF를 연 뒤 **Ctrl+F**로 검색 패널을 열고 검색어를 입력합니다. 결과를 선택하면 해당 위치로 이동하며 **검색 전 위치**로 돌아갈 수 있습니다. 문자 정보가 없는 스캔 이미지는 이 문자 검색의 대상이 아닙니다.

설치 파일은 `The_Viewer_Setup_3.13.38_x64.exe`입니다. 제작자가 Windows에서 빌드를 완료한 뒤 배포하는 파일명입니다. 프로그램 내부에서는 **정 → 업데이트**에서 공개된 새 버전을 확인합니다.

이 데스크톱 소스에는 **DWG·AI·EPS·PS 읽기가 제외**되어 있습니다. Office 문서는 동봉하거나 PC에 설치한 LibreOffice로 변환합니다.

## 검증 범위

이번 도구는 소스·문서 준비와 해당 PDF 작업 프로토콜을 기준으로 점검합니다. Windows 설치 EXE 빌드·설치·인쇄 및 실제 GitHub 업로드 완료를 뜻하지 않습니다. Windows EXE는 패키징 도구의 사전 검사·배포 검사·최종 위치 검사를 통과해야 합니다.

이 버전의 속도 향상 배수나 밀리초 측정치는 새로 확인하지 않았으므로 제시하지 않습니다. 기존 v3.13.31·v3.13.32 수치를 v3.13.38의 측정 결과로 사용하지 않습니다.

제작 도구: **패키징 v1.5.9 / GitHub 매니저 v2.1.2**.

근거: [뷰어 저장소](https://github.com/faintstar85-source/the-viewer)의 `_viewer_fast_pdf_worker`, `worker_launch`, `PdfSearchPanel`, `REMOVED_INPUT_EXTENSIONS`. 전달받은 원본 PY SHA-256: `6fb31ed3cd9214db9e084843c6ba7680779152a5b2f64fc009e491deafef7a90`.
