# 설치와 업데이트

[사용 안내](PROGRAM_GUIDE.md) · [처음 화면](../README.md) · [릴리스 목록](https://github.com/faintstar85-source/the-viewer/releases)

## 설치 EXE 사용

1. [GitHub Releases](https://github.com/faintstar85-source/the-viewer/releases/latest)에서 설치 EXE가 첨부된 버전을 확인합니다.
2. 설치 EXE를 실행합니다.
3. PDF/JPG 열기 등록을 선택한 경우 Windows 기본 앱 설정에서 The Viewer를 선택합니다.
4. The Viewer를 실행하고 파일을 드래그해 넣거나 시작 화면의 [+]로 엽니다.

검토한 설치 빌더의 대상은 **Windows 10 2004 이상 또는 Windows 11, x64**입니다. 사용 PC에는 Python이나 Inno Setup을 별도로 설치할 필요가 없습니다.

## ZIP 배포본 사용

배포 ZIP 전체를 압축 해제하고 **The_Viewer.exe**를 실행합니다. 동봉된 **_internal** 폴더와 필요한 파일을 함께 유지하세요.

변환 기능은 설치된 구성요소와 배포본의 엔진 구성에 따라 달라집니다. Office 읽기는 설치된 LibreOffice를 사용할 수 있습니다.

## 프로그램에서 업데이트 확인

**정 → 설정 → 업데이트**에서 새 버전을 확인합니다. 새 설치 파일을 다운로드하고 검증한 뒤 작업 저장을 확인하고 뷰어를 종료해 설치합니다.

현재 소스의 프로그램 내부 업데이트는 **전체 설치 EXE를 내려받는 방식**입니다. 업데이트 다운로드 취소나 창 닫기 시 자동 설치 연결도 취소됩니다.

## 제작용 PY와 compliance

설치 EXE와 제작용 Python 소스는 사용 대상이 다릅니다. 소스에서 설치 파일을 만들려면 [패키징 안내](BUILD_AND_GITHUB.md)를 확인합니다.

**compliance**는 제작용 배포 패키지에 포함된 라이선스·대응 소스 자료 폴더입니다. 패키징할 뷰어 PY와 같은 폴더에 전체 자료를 둡니다. 일반 사용자가 설치 EXE로 실행할 때 직접 이 폴더를 준비하는 절차는 없습니다.

기능 기준: v3.13.38 [뷰어 소스](../pdf_page_dragger.py)와 TheViewer_Build_Standalone_v1.5.8의 설치 코드.

