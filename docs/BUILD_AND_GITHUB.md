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

## 소스 보존과 산출물 관리

혼자 작업할 때의 실수 방지 절차와 새 프로젝트용 항목은 [간단한 운영 체크리스트](SOLO_PROJECT_CHECKLIST.md)를 참고합니다.

ChatGPT와 계속 개발할 수 있도록 필수 소스, 런타임 자산, 템플릿, 폰트, 모델, 빌드 설정, 테스트, 라이선스 및 고지 자료는 보존합니다. 저장소 정리 시 재현 가능한 빌드 산출물만 별도로 관리하며, 파일 크기나 확장자만으로 개발·실행에 필요한 자료를 삭제하지 않습니다.

`release.yml`의 **Keep checked distribution**이 올리는 임시 `dist/` Actions artifact와 실패 진단 및 릴리즈 상태 artifact는 기존 14일 보관을 유지합니다. 배포 재시도·복구에 필요한 기간이 검증되지 않아 7일 단축은 적용하지 않습니다. 기존 artifact나 Releases 첨부파일도 삭제하지 않습니다.

Releases 첨부파일 삭제와 Actions artifact 저장공간 관리는 별개입니다. 보관기간 단축은 임시 artifact의 저장기간을 줄일 뿐, 워크플로 실행시간을 줄이거나 이미 사용한 실행시간을 돌려주지 않습니다. 기존 main 자동 빌드·배포 트리거, 작업 의존관계와 공개 조건은 그대로 유지합니다.

## 보관기간과 재시도 검토 (2026-11-16)

- 현행 main `cf19a380ac5d2cc133e749ae47b437ff8eb7e4a5`: 업로드·다운로드 이름에 `github.run_attempt`가 포함됩니다. 실패한 release job만 다시 실행하면 성공한 Windows job은 이전 산출물을 남긴 채 attempt가 증가하므로 이름이 달라질 위험이 있습니다. 이는 코드와 GitHub 재실행 규칙을 대조한 판단이며 실제 재실행으로 재현하지 않았습니다. 14일 보관만으로 재시도 성공을 보장하지 않습니다. 전체 재실행이나 새 수동 실행은 원본 산출물 재사용 대신 Windows 빌드를 다시 수행하는 구조입니다.
- 미병합 [draft PR #1](https://github.com/faintstar85-source/the-viewer/pull/1), head `7f75e9c8ff005ebdf2ef32bfe4ebb2206fb26729`: 원본 artifact ID·해시·원본 attempt의 성공 기록을 검증해 재사용하고, 보관 요청값을 90일로 늘리는 별도 제안입니다. 만료된 자료는 거부하고 기존 초안을 보존합니다. 현행 main에 적용된 기능이 아니며, 확인 시 병합 불가 상태였습니다. 기존 자료에는 새 출처 기록이 없어 자동 재사용할 수 없다는 제약도 있습니다.
- 14→7일 단축은 이후 산출물의 다운로드·조사·수동 복구 자료 확보 기간을 7일 줄입니다. PR #1 방식에서도 원본 artifact가 만료되면 재사용할 수 없으므로 짧은 보관기간은 복구 선택지를 줄입니다. GitHub의 재실행 가능 기간과 artifact 보관기간은 별개이며, 진단 자료만 남아 있어도 설치 파일을 대신할 수 없습니다. 현재 복구에 필요한 기간, 실제 실패 job 재실행, 원본 artifact 복원·초안 공개 전환은 검증하지 않았으므로 기존 14일을 유지합니다.

근거: [현행 workflow](https://github.com/faintstar85-source/the-viewer/blob/cf19a380ac5d2cc133e749ae47b437ff8eb7e4a5/.github/workflows/release.yml), [PR #1 재사용 코드](https://github.com/faintstar85-source/the-viewer/blob/7f75e9c8ff005ebdf2ef32bfe4ebb2206fb26729/scripts/release_artifact.py), [GitHub job 재실행 규칙](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs), [artifact 보관 설정](https://docs.github.com/en/actions/tutorials/store-and-share-data).

## 참고

- [GitHub Python 빌드](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [Windows 2022 실행 환경](https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md)
- [GitHub 릴리스 API](https://docs.github.com/en/rest/releases/releases)
