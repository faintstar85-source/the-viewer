# 업데이트 배포

이제 저장소에서 소스와 버전을 수정하면 GitHub가 빌드·검사·배포합니다.

1. `pdf_page_dragger.py`의 코드와 `APP_VERSION`을 수정합니다.
2. 새 버전의 `releases/RELEASE_NOTES_v버전.md`를 작성합니다.
3. `release.json`을 같은 버전으로 맞추고 `main`에 반영합니다.
4. [GitHub Actions](https://github.com/faintstar85-source/the-viewer/actions/workflows/release.yml)에서 결과를 확인합니다.

`publish: true`이면 설치 EXE·ZIP·PY·SHA-256 확인 후 공개합니다. `false`이면 초안으로 준비합니다. 같은 버전으로 이미 올라간 파일을 교체하지 않습니다.

기존 사용자는 프로그램의 **정 → 업데이트**에서 확인합니다. 제작 PC에서 별도 패키징·업로드 프로그램을 실행할 필요가 없습니다.

[자동 빌드·배포 자세히 보기](docs/BUILD_AND_GITHUB.md)
