# The Viewer Rust 처리 시험본

기준: The Viewer v3.13.45, `b284c7e0f8d2e435667d0e736dd283d37aaf0903`.

**전체를 Rust로 다시 만든 프로그램이 아닙니다.** 원본 화면·기능 코드를 유지하고, 일반 PDF의 화면/썸네일 RGB 렌더링을 Rust 프로세스로 교체한 비교용 구현입니다. 기존 PDFium 라이브러리를 그대로 사용합니다. 소수점 좌표·CropBox·UserUnit을 보존하기 위해 메타데이터는 기존 pypdf로 읽으며, 검색·편집·양식·PNG 응답은 기존 Python worker에 위임합니다.

| 구간 | 시험본 구현 |
|---|---|
| PDF 열기/쪽수 확인 | Rust → PDFium |
| 일반 PDF RGB 렌더링·썸네일 | Rust → PDFium, 정밀 메타데이터는 Python |
| UI·확대·페이지 이동·공유 캐시·듀얼뷰 | 기존 Python/PySide6 코드 |
| PDF 검색·편집·페이지 일괄처리·양식 | 기존 Python 호환 worker |
| 사진·ZIP·텍스트·Office/HWP·비교분석·인쇄 | 기존 구현 유지. Rust 성능 측정 대상 아님 |

원본 `pdf_page_dragger.py`와 배포 설정은 수정하지 않습니다. 시험 실행 시 설정 저장 위치와 Windows AppUserModelID를 분리하며, 정식 배포 업데이트 확인은 끕니다. 원본 소스 해시가 달라지면 시험본 연결을 중단하고 먼저 재검토하도록 했습니다.

## 실행

공개 실험 브랜치는 **추가 소스·검증 스크립트·Windows CI 설정**을 포함합니다. 아래 명령으로 별도 폴더에 복제합니다. 실제 설치 프로그램 폴더에 덮어쓰지 않습니다. Windows 빌드 상태와 산출물은 해당 커밋의 `Rust reader experiment - no release` Actions 실행에서 확인합니다.

```powershell
git clone --branch experiment/rust-backend-20261030 https://github.com/faintstar85-source/the-viewer.git TheViewer-Rust-Lab
cd TheViewer-Rust-Lab
```

Windows workflow가 성공하면 **Rust PDF worker EXE**와 원본 UI 실행용 Python 소스를 포함한 artifact를 생성합니다. ZIP을 별도 폴더에 모두 풀어 사용합니다. 전체 앱의 단독 설치 EXE는 아닙니다. Python 3.13과 의존성이 필요합니다. 소스로 복제했다면 아래 직접 빌드를 먼저 수행합니다.

```powershell
python -m pip install -r rust-lab/requirements-benchmark.txt
python rust-lab/launch.py
```

`rust-lab/START_RUST_TRIAL.bat`를 더블클릭해도 됩니다. 사진·문서 변환·인쇄 등 원본의 추가 기능을 사용하려면 저장소의 `requirements.txt`와 각 변환 엔진 조건이 적용됩니다. 위 최소 의존성은 PDF 읽기/비교 시험용입니다.

직접 빌드:

```powershell
cargo build --manifest-path rust-lab/Cargo.toml --release --locked
python rust-lab/launch.py
```

비교 재실행:

```powershell
python rust-lab/test_protocol.py --rust rust-lab/target/release/viewer-rust-worker.exe --out rust-lab/results/my-protocol.json
python rust-lab/bench.py --rust rust-lab/target/release/viewer-rust-worker.exe --out rust-lab/results/my-benchmark.json --repetitions 7
```

Linux에서는 바이너리 이름의 `.exe`를 빼고 `QT_QPA_PLATFORM=offscreen`으로 GUI 검사를 수행합니다.

## 비교 기준

- baseline도 원래 UI가 사용하는 `worker_launch()`의 marshal 캐시 실행 경로를 사용합니다.
- 두 구현이 같은 PDFium 파일과 같은 합성 PDF를 사용합니다. 출력 크기와 RGB SHA-256 일치를 먼저 검사합니다.
- 프로세스 시작→첫 화면의 RGB 전체 수신, 다음 쪽, 재방문, 썸네일을 분리합니다. 전체 앱 실행 시간이나 사용자 화면에 실제 그려진 시간은 아닙니다.
- 실행 순서를 교대하며 반복 원자료·중앙값·p95를 남깁니다. OS 디스크 캐시를 초기화한 냉간 디스크 시험이 아닙니다.
- Rust가 Python에 위임한 결과는 `python-compat`로 기록합니다. 이를 순수 Rust 처리 성공/속도 향상으로 계산하지 않습니다.
- 메모리는 Rust의 Python 자식도 포함한 프로세스 트리 RSS의 20ms 표본 최대값입니다. 공유 페이지가 합산될 수 있고 실제 물리 메모리 독점량과 다릅니다.
- 이 작업의 Linux/Windows CI 결과와 사용자의 Windows PC 체감 성능은 별개입니다.

측정 원자료와 검사 결과는 각 Actions 실행의 artifact 안 `rust-lab/results/`에 저장합니다. 검증 화면 이미지는 업로드하지 않습니다. 공개 릴리스나 정식 자동 업데이트는 이 workflow에서 수행하지 않습니다.

## 정확성·구조 근거

- [기준 소스](https://github.com/faintstar85-source/the-viewer/blob/b284c7e0f8d2e435667d0e736dd283d37aaf0903/pdf_page_dragger.py)
- [기존 소수점 좌표 회귀 기록](https://github.com/faintstar85-source/the-viewer/blob/b284c7e0f8d2e435667d0e736dd283d37aaf0903/docs/READING_SPEED_v3.13.32.md)
- [기존 읽기·캐시 구조](https://github.com/faintstar85-source/the-viewer/blob/b284c7e0f8d2e435667d0e736dd283d37aaf0903/docs/READING_SPEED.md)
- [PDFium 공식 C API 및 단일 스레드 조건](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/public/fpdfview.h)

Rust 의존성 버전은 `Cargo.lock`으로 고정합니다. PDFium은 기존 pypdfium2 배포 파일을 읽습니다. 정식 패키징은 원본 프로젝트 및 각 라이브러리의 라이선스·고지 구성 검토가 필요하며 이 시험판은 정식 설치본을 대체하지 않습니다.
