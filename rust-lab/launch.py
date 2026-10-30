"""Run the existing UI with the experimental Rust PDF reader and isolated settings."""
import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
import bridge


def isolate_settings(viewer, directory):
    """The explicit org/app Qt constructor ignores setDefaultFormat on Linux.

    Give the experiment an explicit INI filename on every platform, including
    Windows where NativeFormat would otherwise use the real application registry.
    """
    from PySide6.QtCore import QSettings
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    class ExperimentalSettings(QSettings):
        def __init__(self, *args, **kwargs):
            if args[:2] == ("KRS", "PDFMagnet"):
                super().__init__(str(directory / "viewer-rust-lab.ini"), QSettings.Format.IniFormat)
                self.setFallbacksEnabled(False)
            else:
                super().__init__(*args, **kwargs)
    viewer.QSettings = ExperimentalSettings


def main():
    parser = argparse.ArgumentParser(description="The Viewer Rust PDF reader experiment (hybrid)")
    parser.add_argument("--rust", type=Path, default=ROOT / "target/release" / ("viewer-rust-worker.exe" if os.name == "nt" else "viewer-rust-worker"))
    parser.add_argument("--settings", type=Path, default=Path.home() / ".the-viewer-rust-lab")
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()
    import pdf_page_dragger as viewer
    from PySide6.QtWidgets import QMessageBox
    bridge.install(viewer, args.rust)
    isolate_settings(viewer, args.settings)
    viewer.APP_NAME = "The Viewer (정) · Rust 처리 시험본"
    viewer.APP_USER_MODEL_ID = "TheViewer.RustLab.Experimental"
    def no_release_update(self, *unused, **kwargs):
        QMessageBox.information(self, "Rust 처리 시험본", "이 시험본은 기존 배포 업데이트와 별도로 실행합니다.")
    viewer.Window.check_for_updates = no_release_update
    viewer.Window.check_startup_update = lambda self: None
    viewer.tv_update_mutex_open = lambda: None
    viewer.tv_update_mutex_close = lambda mutex: None
    sys.argv = [str(Path(viewer.__file__).resolve()), *args.files]
    viewer.main()


if __name__ == "__main__":
    main()
