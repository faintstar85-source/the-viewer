# The Viewer (정)

PDF와 그림을 크게 보기·썸네일 화면에서 확인하고 편집하는 Windows용 Python 프로그램입니다.

## 다운로드 · 소식

- [최신 배포 및 수정사항](https://github.com/faintstar85-source/the-viewer/releases)
- [오류 제보 · 기능 요청](https://github.com/faintstar85-source/the-viewer/issues)
- [개발자 블로그](https://blog.naver.com/faintstar)
- 새 버전 알림: 이 저장소에서 **Watch → Custom → Releases**를 선택하세요.

## 주요 기능

- PDF·JPG·PNG·WebP·TIFF·BMP, 그림 폴더 및 ZIP·CBZ 보기
- 페이지 순서 변경, 분리 복사, 그림 삽입, PDF 글자·그림 편집
- PDF를 문단·표 중심의 HWPX로 변환 (문서 구조에 따라 결과가 다를 수 있음)
- 사용자 DeepL API 키를 이용한 한국어 PDF 번역
- 파일·쪽 이동 단축키 사용자 설정

## Python으로 실행

```console
py -m pip install -r requirements.txt
py pdf_page_dragger.py
```

선택 기능:

```console
py -m pip install "pyvips[binary]"
py -m pip install "python-hwpx==6.6.0"
```

DeepL 키는 프로그램의 [정] → 번역에서 개인별로 등록합니다.
기본 단축키: 다음 쪽 → / Space, 이전 쪽 ← / Backspace, 이웃 파일 , . [ ].
일반 PDF·그림으로 시작하면 같은 폴더의 PDF·그림만 이동합니다.
후원 QR 및 블로그·GitHub 링크는 [정]에서 열 수 있습니다.

## 라이선스

이 도우미는 LICENSE를 자동으로 지정하지 않습니다. 권리자가 선택한 LICENSE 파일을 추가해 적용 범위를 명시하세요.
사용하는 외부 라이브러리는 각 배포자의 라이선스를 따릅니다.
[GitHub 라이선스 안내](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
