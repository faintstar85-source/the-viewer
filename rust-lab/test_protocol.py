#!/usr/bin/env python3
"""Integration checks against the compiled worker and unchanged baseline.

Run: python rust-lab/test_protocol.py --rust rust-lab/target/release/viewer-rust-worker
"""
from __future__ import annotations

import argparse
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

import bench


def small_pdf(path, label, pages=1):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(str(path), pagesize=(612, 792), invariant=1)
    for page in range(pages):
        c.setFont("Helvetica", 18)
        c.drawString(45, 730, f"{label} - page {page}")
        c.rect(40, 50, 500, 500)
        c.showPage()
    c.save()


class WorkerProtocolTests(unittest.TestCase):
    rust_path = None

    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="viewer_rust_protocol_")
        cls.root = Path(cls.temp.name)
        cls.unicode_root = cls.root / "검사 자료 [한글]"
        cls.unicode_root.mkdir()
        cls.fixture = cls.unicode_root / "한글 파일명.pdf"
        small_pdf(cls.fixture, "Original", 3)
        cls.original_hash = bench.sha256(cls.fixture)
        cls.commands = bench.commands(cls.rust_path)

    @classmethod
    def tearDownClass(cls):
        if bench.sha256(cls.fixture) != cls.original_hash:
            raise AssertionError("Read-only worker changed the original PDF")
        cls.temp.cleanup()

    def setUp(self):
        self.old = bench.Worker(self.commands["python"])
        self.new = bench.Worker(self.commands["rust"])

    def tearDown(self):
        self.new.close()
        self.old.close()

    def test_unicode_path_count_and_raw_rgb_exact(self):
        a, _, _ = self.old.request("inspect", path=str(self.fixture))
        b, _, _ = self.new.request("inspect", path=str(self.fixture))
        self.assertEqual(a["count"], 3)
        self.assertEqual(a["count"], b["count"])
        self.assertEqual(b.get("engine"), "rust-pdfium")
        for page in (0, 1, 2):
            a = bench.render(self.old, self.fixture, page)
            b = bench.render(self.new, self.fixture, page)
            self.assertEqual(bench.signature(a), bench.signature(b))
            self.assertEqual(b["engine"], "rust-pdfium")

    def test_release_then_reopen_keeps_pixels(self):
        before = bench.render(self.new, self.fixture)
        header, data, _ = self.new.request("release")
        self.assertTrue(header["ok"])
        self.assertEqual(data, b"")
        after = bench.render(self.new, self.fixture)
        self.assertEqual(bench.signature(before), bench.signature(after))

    def test_replace_same_path_invalidates_cache(self):
        destination = self.root / "replaced.pdf"
        shutil.copyfile(self.fixture, destination)
        original = bench.render(self.new, destination)
        replacement = self.root / "replacement.pdf"
        small_pdf(replacement, "Changed content", 1)
        # Windows disallows replacing an open PDF. Explicit release is the
        # application's normal edit path, so that contract is checked there.
        if os.name == "nt":
            self.new.request("release")
        os.replace(replacement, destination)
        changed = bench.render(self.new, destination)
        expected = bench.render(self.old, destination)
        self.assertNotEqual(original["sha256"], changed["sha256"])
        self.assertEqual(bench.signature(changed), bench.signature(expected))

    def test_errors_are_responses_and_stream_recovers(self):
        cases = [
            {"op": "inspect", "path": str(self.root / "missing.pdf")},
            {"op": "preview", "path": str(self.fixture), "page": 99999,
             "payload": {"raw_frame": True}, "max_side": 1800},
            {"op": "not_a_real_operation", "path": str(self.fixture)},
        ]
        for case in cases:
            header, body, _ = self.new.request(raw_request=case)
            self.assertFalse(header.get("ok"), case)
            self.assertEqual(body, b"")
            self.assertTrue(header.get("error"))
        good = bench.render(self.new, self.fixture)
        reference = bench.render(self.old, self.fixture)
        self.assertEqual(bench.signature(good), bench.signature(reference))

    def test_malformed_json_does_not_desynchronize_rgb_stream(self):
        self.new.proc.stdin.write(b"{malformed JSON}\n")
        self.new.proc.stdin.flush()
        reply = self.new.responses.get(timeout=self.new.timeout)
        if isinstance(reply, Exception):
            raise reply
        header, body = reply
        self.assertFalse(header.get("ok"))
        self.assertEqual(body, b"")
        actual = bench.render(self.new, self.fixture)
        expected = bench.render(self.old, self.fixture)
        self.assertEqual(bench.signature(actual), bench.signature(expected))

    def test_search_fallback_matches_original(self):
        request = {"path": str(self.fixture), "page": 0,
                   "payload": {"query": "Original", "limit": 10}}
        a, ab, _ = self.old.request("search", **request)
        b, bb, _ = self.new.request("search", **request)
        self.assertTrue(a["ok"])
        self.assertTrue(b["ok"])
        self.assertEqual(a["search"], b["search"])
        self.assertEqual(ab, bb)
        self.assertEqual(b.get("engine"), "python-compat")

    def test_png_fallback_matches_decoded_original(self):
        from PIL import Image
        import base64
        request = {"path": str(self.fixture), "page": 0, "max_side": 1000,
                   "payload": {"raw_frame": False}}
        a, _, _ = self.old.request("preview", **request)
        b, _, _ = self.new.request("preview", **request)
        self.assertTrue(a["ok"])
        self.assertTrue(b["ok"])
        with Image.open(io.BytesIO(base64.b64decode(a["png"]))) as left:
            with Image.open(io.BytesIO(base64.b64decode(b["png"]))) as right:
                self.assertEqual(left.size, right.size)
                self.assertEqual(left.convert("RGB").tobytes(), right.convert("RGB").tobytes())
        self.assertEqual(b.get("engine"), "python-compat")

    def test_geometry_forms_unchanged(self):
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import NameObject, FloatObject, NumberObject, RectangleObject
        source = PdfReader(self.fixture)
        output = PdfWriter()
        for rotation in (0, 90, 180, 270):
            page = output.add_page(source.pages[0])
            page.mediabox = RectangleObject((0, 0, 595.2756, 841.8898))
            page.cropbox = RectangleObject((3.12345, 7.98765, 589.65432, 833.24689))
            page[NameObject("/UserUnit")] = FloatObject(1.25)
            page[NameObject("/Rotate")] = NumberObject(rotation)
        path = self.root / "fractional_geometry.pdf"
        with path.open("wb") as stream:
            output.write(stream)
        source.stream.close()
        for page in range(4):
            for op, side in (("preview", 1800), ("render", 370)):
                a = bench.render(self.old, path, page, side, op)
                b = bench.render(self.new, path, page, side, op)
                self.assertEqual(bench.signature(a), bench.signature(b), (page, op))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rust", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    WorkerProtocolTests.rust_path = args.rust.resolve()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(WorkerProtocolTests))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({"tests_run": result.testsRun, "passed": result.wasSuccessful(),
                                       "failures": [(str(case), error) for case, error in result.failures],
                                       "errors": [(str(case), error) for case, error in result.errors],
                                       "platform": bench.platform.platform()}, indent=2), encoding="utf8")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
