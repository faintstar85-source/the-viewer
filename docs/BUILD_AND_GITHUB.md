# GitHub에서 빌드·검사·배포

The Viewer는 `faintstar85-source/the-viewer` 저장소에서 관리합니다. 제작 PC에서 별도의 패키징·업로드 프로그램을 실행하는 절차를 GitHub Actions로 옮겼습니다.

## 다음 업데이트

1. 저장소의 `pdf_page_dragger.py`를 수정하고 `APP_VERSION`을 새 버전으로 올립니다.
2. `releases/RELEASE_NOTES_v새버전.md`에 변경 내용을 작성합니다.
3. `release.json`의 `version`, `notes`를 같은 버전으로 맞춥니다. `publish: true`이면 검사 후 공개하며, `false`이면 초안으로 준비합니다.
4. `main`에 반영합니다. Actions의 **Build and release The Viewer**가 처리합니다.

ChatGPT의 GitHub 연결로 이 파일들을 직접 수정할 수 있습니다. 사용자에게 PY를 내려받아 제작 PC에서 다시 빌드하도록 요구할 필요가 없습니다.

## 자동 처리 내용

- 소스 문법·버전 일치·내장 PDF 엔진 코드·배포 안전성 테스트.
- Windows Server 2022 / x64 Python 3.13 환경의 기존 빌더 1.5.10 실행.
- 기존 Qt/PySide6·certifi 대응 소스 기록과 크기·SHA-256 확인. 대응 소스는 기록된 공식 URL에서 자동으로 받습니다.
- 소스 실행 검사, 완성 EXE 검사, 최종 배포 위치 검사와 설치 EXE 생성.
- 설치 EXE·ZIP·PY·버전 안내·수정 내역·SHA256SUMS 준비.
- GitHub에 초안 생성 → 첨부파일 크기·SHA-256 확인 → `publish` 설정에 따라 공개.

Inno Setup은 Windows 실행 환경의 `ISCC.exe`를 자동 탐색합니다. 필수 자료나 검사가 빠지면 배포를 중단합니다. Office 엔진은 기존 기본값처럼 동봉하지 않으며, 사용자 PC에 설치된 LibreOffice를 사용합니다.

## 상태 확인과 재시도

[자동 배포 상태](https://github.com/faintstar85-source/the-viewer/actions/workflows/release.yml)에서 실행 결과와 실패 단계를 확인합니다. 실패 시 빌드·배포 진단 기록이 Actions 첨부자료로 남습니다.

같은 버전의 기존 파일을 다른 내용으로 덮어쓰지 않습니다. 이미 초안에 파일이 올라갔거나 공개가 끝난 뒤 새로 빌드하려면 버전을 올리세요. 초안의 기존 검증 파일을 그대로 공개하려면 Releases에서 해당 초안의 공개 버튼을 사용합니다.

소스와 실행 환경은 전용 빌드 공간에 준비합니다. GitHub의 배포 권한은 검사에 성공한 `main` 배포 작업에만 전달합니다. Pull Request 검사는 릴리스를 만들지 않습니다.

## 사용자 프로그램 업데이트

기존 **정 → 업데이트**를 사용합니다. 공개된 새 버전의 설치 파일을 내려받아 확인한 뒤 작업 저장·종료·설치로 연결됩니다. 기존 사용자가 GitHub Actions나 제작 도구를 조작할 필요는 없습니다.

## 로컬 검사

```sh
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

Windows 빌드 검사는 GitHub Actions 기록으로 확인합니다. 현장 PC 전체 동작, 실제 프린터 출력, DeepL 실서버 결과를 모두 확인했다는 의미는 아닙니다.

## 참고

- [GitHub Python 빌드](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [Windows 2022 실행 환경](https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md)
- [GitHub 릴리스 API](https://docs.github.com/en/rest/releases/releases)
