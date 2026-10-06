# The Viewer v3.13.15

## 이번 버전: PDF 아이콘 개선

- 듀얼 보기를 나타내는 빨간 책 모양을 유지했습니다.
- 우측 아래 PDF 글자를 조금 키웠습니다.
- 짙은 빨간 테두리로 윤곽을 또렷하게 다듬었습니다.
- 16·20·24·32·40·48·64·128·256px 아이콘을 포함합니다.

v3.13.15의 코드 변경은 아이콘과 버전 표시입니다. 아래 항목은 앞선 3.13.x 편집 개선으로, 이 버전에 포함된 기능을 안내합니다.

## 최근 반영된 PDF 편집 기능

- 글자를 상자 안에서 바로 수정하고, 테두리·손잡이로 위치와 크기를 조절합니다.
- 글상자·선·그림·도형을 다른 페이지의 같은 X/Y 좌표에 붙여넣습니다.
- 빈 페이지에 붙여넣을 때 발생하던 `/Resources` 관련 오류를 수정했습니다.
- 우클릭 범위 선택과 Ctrl 선택 조절을 지원합니다.
- 글줄의 왼쪽·가운데 정렬, 가로·세로 빈 간격 조절을 개선했습니다.
- 여러 개체를 선택한 바깥 손잡이로 개체 크기를 유지하면서 간격을 조절합니다.
- **글상자 합치기**로 선택한 문자 조각을 하나의 상자로 수정합니다. 줄바꿈을 유지하고 첫 글자의 서식을 사용합니다.
- 방향키 이동 후 바로 입력 커서로 돌아가는 흐름을 줄이도록 이동 상태를 약 3.5초 유지합니다.
- 스포이드의 가리키는 색상을 색상 버튼과 미리보기에 표시합니다.
- 듀얼 보기와 1|2 전환 애니메이션은 기본 꺼짐이며 설정에서 켤 수 있습니다.
- 수정 후 종료 질문을 **예 / 아니오 / 취소**로 표시합니다.

## 사용 안내

- [PDF 편집 안내](https://github.com/faintstar85-source/the-viewer/blob/main/docs/PDF_EDITING.md)
- [듀얼 보기 안내](https://github.com/faintstar85-source/the-viewer/blob/main/docs/DUAL_VIEW.md)
- [설치·업데이트 안내](https://github.com/faintstar85-source/the-viewer/blob/main/docs/INSTALL_AND_UPDATE.md)

대상 페이지가 작아 원래 좌표의 개체가 페이지 밖으로 나가면 붙여넣기를 제한합니다. 글상자 합치기는 개별 글자의 서로 다른 서식을 모두 보존하지 않습니다.

**지원 형식:** PDF, 이미지, ZIP/CBZ 이미지, 일반 텍스트, HWP/HWPX, LibreOffice를 이용한 Office 읽기, DXF, PSD. DWG·AI·EPS·PS 직접 읽기는 이 소스에 포함되어 있지 않습니다.

[프로젝트](https://github.com/faintstar85-source/the-viewer) · [전체 수정 기록](https://github.com/faintstar85-source/the-viewer/blob/main/CHANGELOG.md) · [오류 제보](https://github.com/faintstar85-source/the-viewer/issues)

