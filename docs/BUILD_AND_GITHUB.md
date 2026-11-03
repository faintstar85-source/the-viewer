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

같은 버전의 기존 파일을 다른 내용으로 덮어쓰지 않습니다. 공개된 태그는 빌드·업로드·수정 없이 보존하며, 실행 요약에 `Already public`을 기록합니다. 이 경로는 새 빌드 검증이나 새 공개를 수행했다는 뜻이 아닙니다.

새 버전은 `publish: false`로 먼저 빌드하여 초안을 준비할 수 있습니다. 공개할 때는 같은 main에서 **Run workflow → publish: true**로 실행하거나, **release.json의 publish만 true로 바꾸어** 반영합니다. 원래 Windows 빌드의 산출물 ID를 찾아 재사용하므로 EXE·ZIP을 다시 만들지 않습니다. `Re-run failed jobs`는 이전 성공 빌드의 ID를 그대로 사용하고, `Re-run all jobs`는 같은 입력의 보존된 산출물을 다시 선택합니다. 현재 재실행 번호로 산출물 이름을 추측하지 않습니다.

- 입력 식별값은 모든 Git 추적 파일의 내용·파일 모드를 포함합니다. 소스, 두 의존성 명세, 빌드 도구, 워크플로, 라이선스 자료, 안내가 포함되며 `release.json.publish`만 제외합니다. 문서만 바뀌어도 재사용을 거절하는 보수적인 정책입니다. 체크아웃의 바이트가 커밋과 다른 경우에도 중단합니다.
- 원본 커밋의 입력 식별값, 같은 저장소/main/release 워크플로에서 만든 산출물인지, **원본 실행 attempt**의 validate·windows-build 성공 여부를 확인합니다. release 작업 실패는 재사용을 막지 않습니다.
- Actions ZIP 전체 SHA-256, 내부 첨부파일 크기·SHA-256, 소스·EXE·최종 위치 검사 횟수, 설치 파일 검증을 다시 확인합니다. 원본 소스와 아이콘·BOM·줄바꿈을 처리한 배포 PY는 각각의 해시를 보존합니다. 실제 설치 패키지 목록, Python/runner 정보, Inno 컴파일러 파일 해시도 보존합니다. 재시도에서 의존성을 다시 설치하지 않습니다.
- 입력이 일치하는 산출물이 여럿이면 자동 선택하지 않습니다. 최초 빌드의 Actions 실행 ID를 **reuse_run_id**에 지정합니다. 지정해도 기존 초안 파일의 해시 비교는 생략되지 않습니다.
- 산출물 보존기간은 요청값 90일이며 저장소 정책의 제한을 받습니다. 만료·삭제·검증 기록 누락, 입력 변경 또는 다른 파일과의 충돌이면 초안을 보존한 채 중단합니다. 재빌드 결과를 기존 버전에 맞추려면 강제 진행하지 말고 새 버전을 사용합니다.
- 패치 이전 산출물에는 새 입력·출처 검증 기록이 없으므로 자동 승격하지 않습니다. 이미 공개된 v3.13.41은 보존합니다. 최초 적용은 새 버전으로 진행합니다.
- 새 릴리스의 태그 대상은 검증한 커밋 SHA에 고정합니다. 이미 있는 태그가 다른 입력을 가리키면 중단하며 태그를 이동하거나 삭제하지 않습니다.

초안에 같은 파일이 일부만 올라간 경우에는 모든 기존 파일을 먼저 검사하고 누락 파일만 올립니다. 다른 크기·해시, 추가 첨부파일, 다른 안내가 있으면 공개하지 않습니다. 자동화끼리는 main 동시 실행을 직렬화합니다. 검사와 GitHub 쓰기는 원자적 트랜잭션이 아니므로 진행 중인 초안을 다른 도구나 브라우저에서 동시에 수정하지 마세요.

소스와 실행 환경은 전용 빌드 공간에 준비합니다. GitHub의 배포 권한은 검사에 성공한 `main` 배포 작업에만 전달합니다. Pull Request 검사는 릴리스를 만들지 않습니다.

## 사용자 프로그램 업데이트

기존 **정 → 업데이트**를 사용합니다. 공개된 새 버전의 설치 파일을 내려받아 확인한 뒤 작업 저장·종료·설치로 연결됩니다. 기존 사용자가 GitHub Actions나 제작 도구를 조작할 필요는 없습니다.

## 로컬 검사

```sh
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

Windows 빌드 검사는 GitHub Actions 기록으로 확인합니다. 현장 PC 전체 동작, 실제 프린터 출력, DeepL 실서버 결과를 모두 확인했다는 의미는 아닙니다.

## 패치 적용 후 GitHub/Windows 확인

1. 새 버전을 초안으로 빌드하고 설치 EXE·ZIP 및 `BUILD_VERIFICATION.json`, 실제 의존성·컴파일러 기록이 보존되는지 확인합니다.
2. 같은 입력에서 publish만 바꾸어 실행합니다. Windows 빌드가 skipped이고 원래 artifact ID/원래 attempt의 성공 검사로 공개되는지, EXE·ZIP 해시가 초안과 같은지 확인합니다.
3. 별도 시험 버전의 부분 업로드 실패 후 실패 작업만 재실행하고, 전체 재실행도 검사합니다. 새 빌드나 기존 첨부파일 교체가 없어야 합니다.
4. 입력 변경, 다른 산출물, 만료된 산출물은 공개 전에 실패해야 합니다. 공개된 버전은 빌드·업로드 없이 보존되어야 합니다. 회귀시험에는 운영 v3.13.41의 첨부파일·태그를 변경하지 않습니다.

## 참고

- [GitHub Python 빌드](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [Windows 2022 실행 환경](https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md)
- [GitHub 릴리스 API](https://docs.github.com/en/rest/releases/releases)
- [Actions 산출물 API와 SHA-256 digest](https://docs.github.com/en/rest/actions/artifacts)
- [upload-artifact v4: 불변 산출물과 artifact-id](https://github.com/actions/upload-artifact/tree/v4)
