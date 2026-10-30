#!/usr/bin/env python3
"""Compare the real Viewer PDF-worker protocol; this is not a GUI/EXE benchmark.

No user documents are needed. Inputs are deterministic synthetic PDFs. The
baseline uses worker_launch(), including its bytecode-cache startup path.
Timing includes IPC and reception of every RGB byte; hashing is outside timing.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import queue
import random
import statistics
import subprocess
import sys
import threading
import time
from collections import Counter

try:
    import psutil as _psutil
except ImportError:
    _psutil = None

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen" if os.name != "nt" else "windows")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pdfium_path():
    import pypdfium2_raw
    folder = Path(pypdfium2_raw.__file__).parent
    names = ("pdfium.dll", "libpdfium.so", "libpdfium.dylib")
    for name in names:
        candidate = folder / name
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(f"PDFium binary not found in {folder}")


def commands(rust, library=None):
    import pdf_page_dragger as viewer
    import bridge
    executable, arguments = viewer.worker_launch("--pdf-worker")
    baseline = [executable, *arguments]
    return {
        "python": baseline,
        "rust": [str(Path(rust).resolve()), "--pdfium", str(library or pdfium_path()),
                 "--fallback-json", json.dumps(bridge.compatibility_command(viewer), ensure_ascii=True)],
    }


class Worker:
    """One outstanding request, bounded header/frame reads, portable timeout."""
    def __init__(self, command, timeout=45):
        self.timeout = timeout
        self.serial = 0
        self.responses = queue.Queue()
        self.stderr = bytearray()
        self.peak_tree_rss = None
        self.memory_samples = 0
        self.memory_warning = None
        self.closed = threading.Event()
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, bufsize=0, cwd=ROOT)
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()
        self.error_reader = threading.Thread(target=self._read_stderr, daemon=True)
        self.error_reader.start()
        self.memory_reader = threading.Thread(target=self._sample_memory, daemon=True)
        self.memory_reader.start()

    def _read_exact(self, count):
        chunks = bytearray()
        while len(chunks) < count:
            part = self.proc.stdout.read(count - len(chunks))
            if not part:
                raise EOFError(f"Truncated RGB frame: {len(chunks)}/{count}")
            chunks.extend(part)
        return bytes(chunks)

    def _read(self):
        try:
            while True:
                line = self.proc.stdout.readline(2 * 1024 * 1024 + 1)
                if not line:
                    raise EOFError("Worker stdout closed")
                if not line.endswith(b"\n") or len(line) > 2 * 1024 * 1024:
                    raise ValueError("Invalid/oversized worker header")
                header = json.loads(line)
                if not isinstance(header, dict):
                    raise ValueError("Response header must be an object")
                count = header.get("nbytes", 0)
                if type(count) is not int or not 0 <= count <= 150_000_000:
                    raise ValueError("Invalid response byte count")
                data = self._read_exact(count)
                self.responses.put((header, data))
        except Exception as exc:
            self.responses.put(exc)

    def _read_stderr(self):
        while True:
            chunk = self.proc.stderr.read(4096)
            if not chunk:
                break
            self.stderr.extend(chunk)
            if len(self.stderr) > 65536:
                del self.stderr[:-65536]

    def _sample_memory(self):
        psutil = _psutil
        if psutil is None:
            self.memory_warning = "psutil is unavailable"
            return
        try:
            process = self._resolve_memory_process(psutil)
            while not self.closed.is_set():
                total = 0
                for item in [process, *process.children(recursive=True)]:
                    try:
                        total += item.memory_info().rss
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                self.peak_tree_rss = max(self.peak_tree_rss or 0, total)
                self.memory_samples += 1
                self.closed.wait(0.02)
        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError, RuntimeError) as exc:
            self.memory_warning = str(exc)
            return

    def _resolve_memory_process(self, psutil):
        # Some execution hosts use a child PID namespace while exposing the
        # host /proc mount. Popen.pid then points to an unrelated host process.
        # Match a DIRECT child of this Python host PID by its innermost NSpid;
        # never report arbitrary psutil.Process(Popen.pid) RSS in that case.
        if sys.platform == "linux":
            status = Path("/proc/self/status").read_text()
            host_self = int(next(line.split()[1] for line in status.splitlines() if line.startswith("Pid:")))
            if host_self != os.getpid():
                for candidate in psutil.Process(host_self).children():
                    try:
                        child_status = Path(f"/proc/{candidate.pid}/status").read_text()
                        namespace_ids = next(line.split()[1:] for line in child_status.splitlines() if line.startswith("NSpid:"))
                        if int(namespace_ids[-1]) == self.proc.pid and candidate.ppid() == host_self:
                            return candidate
                    except (OSError, StopIteration, psutil.NoSuchProcess):
                        continue
                raise RuntimeError("Cannot resolve worker PID namespace; memory unavailable")
        return psutil.Process(self.proc.pid)

    def request(self, operation=None, *, raw_request=None, **kwargs):
        self.serial += 1
        request = (dict(raw_request) if raw_request is not None else
                   {"op": operation, "path": None, "page": None, "payload": {}, **kwargs})
        request.setdefault("id", self.serial)
        data = (json.dumps(request, ensure_ascii=True) + "\n").encode("ascii")
        start = time.perf_counter_ns()
        try:
            self.proc.stdin.write(data)
            self.proc.stdin.flush()
            reply = self.responses.get(timeout=self.timeout)
        except queue.Empty as exc:
            raise TimeoutError(f"Worker timeout: {operation or request.get('op')}; "
                               f"stderr={self.stderr.decode('utf8', 'replace')}") from exc
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
        if isinstance(reply, Exception):
            raise RuntimeError(f"{reply}; stderr={self.stderr.decode('utf8', 'replace')}") from reply
        header, body = reply
        if header.get("id") != request["id"]:
            raise AssertionError(f"Response ID mismatch: {header.get('id')} != {request['id']}")
        return header, body, elapsed_ms

    def close(self):
        if not self.closed.is_set():
            try:
                self.proc.stdin.close()
            except (BrokenPipeError, OSError):
                pass
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=3)
            self.closed.set()
            self.memory_reader.join(timeout=1)
            self.reader.join(timeout=1)
            self.error_reader.join(timeout=1)
            self.proc.stdout.close()
            self.proc.stderr.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def render(worker, path, page=0, side=1800, operation="preview", completion_clock=None):
    payload = {"raw_frame": True}
    if operation == "render":
        payload["thumb_side"] = side
    header, body, elapsed = worker.request(operation, path=str(path), page=page,
                                           max_side=side, payload=payload)
    if completion_clock is not None:
        completion_clock.append(time.perf_counter_ns())
    if not header.get("ok"):
        raise AssertionError(f"{operation} failed: {header}")
    width, height, stride = (header.get(key) for key in ("width", "height", "stride"))
    if (not all(type(v) is int and v > 0 for v in (width, height, stride))
            or stride != width * 3 or len(body) != stride * height):
        raise AssertionError(f"Invalid RGB dimensions: {header}")
    return {
        "elapsed_ms": elapsed, "width": width, "height": height, "stride": stride,
        "sha256": hashlib.sha256(body).hexdigest(),
        "engine": header.get("engine", "python-baseline"),
    }


def generate_fixtures(folder):
    """PDF IDs/timestamps and generated image pixels are reproducible."""
    from PIL import Image, ImageDraw
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, NumberObject, FloatObject, RectangleObject

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    vector = folder / "vector_200_pages.pdf"
    c = canvas.Canvas(str(vector), pagesize=(612, 792), invariant=1, pageCompression=1)
    for page in range(200):
        c.setFont("Helvetica-Bold", 16)
        c.drawString(36, 755, f"Viewer benchmark - page {page + 1:03d}")
        c.setFont("Helvetica", 8)
        for row in range(44):
            y = 724 - row * 15
            c.setStrokeColorRGB(.2, .35, .5)
            c.line(32, y - 4, 580, y - 4)
            for col in range(5):
                c.line(32 + col * 110, y - 4, 32 + col * 110, y + 11)
            c.drawString(38, y, f"Record {row:02d}  Page {page + 1}  ABC 0123456789  test document")
            c.setFillColorRGB((row % 4) / 5, (page % 7) / 8, .6)
            c.rect(490, y, 45 + row % 13, 5, fill=1, stroke=0)
            c.setFillColorRGB(0, 0, 0)
        c.showPage()
    c.save()

    scanned = folder / "scan_40_pages.pdf"
    c = canvas.Canvas(str(scanned), pagesize=(612, 792), invariant=1, pageCompression=1)
    randomizer = random.Random(20261030)
    for page in range(40):
        low = Image.frombytes("L", (120, 160), randomizer.randbytes(120 * 160))
        low = low.point(lambda x: 225 + x // 9)
        image = low.resize((1200, 1600), Image.Resampling.BILINEAR).convert("RGB")
        draw = ImageDraw.Draw(image)
        draw.text((45, 30), f"Synthetic scan page {page + 1}", fill="black", font_size=28)
        for row in range(35):
            y = 100 + row * 40
            draw.line((45, y + 27, 1140, y + 27), fill=(65, 65, 65), width=2)
            draw.text((50, y), f"Item {row} / page {page + 1}: sample 1234567890 ABC DEF", fill="black", font_size=22)
        data = io.BytesIO()
        image.save(data, "JPEG", quality=85, subsampling=0)
        c.drawImage(ImageReader(io.BytesIO(data.getvalue())), 0, 0, 612, 792)
        c.showPage()
    c.save()

    geometry = folder / "geometry.pdf"
    reader = PdfReader(vector)
    writer = PdfWriter()
    for index in range(8):
        page = writer.add_page(reader.pages[index])
        if index in (0, 1, 2, 3):
            page.cropbox = RectangleObject((17, 29, 591, 763))
            page[NameObject("/Rotate")] = NumberObject(index * 90)
        elif index == 4:
            page[NameObject("/UserUnit")] = NumberObject(2)
        elif index == 5:
            page.cropbox = RectangleObject((-40, -30, 710, 910))
        elif index == 6:
            page.mediabox = RectangleObject((0, 0, 595.2756, 841.8898))
            page.cropbox = RectangleObject((4.12345, 8.98765, 588.76543, 832.11111))
            page[NameObject("/UserUnit")] = FloatObject(1.25)
            page[NameObject("/Rotate")] = NumberObject(270)
        else:
            page[NameObject("/Rotate")] = NumberObject(180)
    with geometry.open("wb") as target:
        writer.write(target)
    reader.stream.close()

    widgets = folder / "widget.pdf"
    c = canvas.Canvas(str(widgets), pagesize=(612, 792), invariant=1, pageCompression=1)
    c.setFont("Helvetica", 14)
    c.drawString(40, 740, "AcroForm compatibility fixture")
    c.acroForm.textfield(name="review", value="Original form value", x=40, y=670, width=250, height=24)
    c.showPage()
    c.save()
    return {"vector": vector, "scan": scanned, "geometry": geometry, "widget": widgets}


def describe_fixture(path):
    from pypdf import PdfReader
    reader = PdfReader(path)
    count = len(reader.pages)
    reader.stream.close()
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path), "pages": count}


def summary(values):
    ordered = sorted(values)
    return {"n": len(ordered), "median": statistics.median(ordered),
            "p95": ordered[max(0, math.ceil(.95 * len(ordered)) - 1)],
            "min": ordered[0], "max": ordered[-1]}


def signature(record):
    return tuple(record[k] for k in ("width", "height", "stride", "sha256"))


def correctness(commands_, fixtures):
    checks = []
    with Worker(commands_["python"]) as old, Worker(commands_["rust"]) as new:
        for name, path in fixtures.items():
            expected = describe_fixture(path)["pages"]
            left, _, _ = old.request("inspect", path=str(path))
            right, _, _ = new.request("inspect", path=str(path))
            checks.append({"case": f"{name}:inspect", "pass": left.get("ok") is True and
                           right.get("ok") is True and left.get("count") == right.get("count") == expected,
                           "rust_engine": right.get("engine"), "pages": expected})
            pages = range(expected) if name in ("geometry", "widget") else (0, expected // 2, expected - 1)
            for page in pages:
                for op, side in (("preview", 1000), ("preview", 1800), ("render", 370)):
                    a = render(old, path, page, side, op)
                    b = render(new, path, page, side, op)
                    checks.append({"case": f"{name}:{page}:{op}:{side}", "pass": signature(a) == signature(b),
                                   "rust_engine": b["engine"], "python": a, "rust": b})
        for operation, kwargs in (
            ("search", {"path": str(fixtures["vector"]), "page": 0,
                        "payload": {"query": "Record", "limit": 3}}),
            ("neighbors", {"path": str(fixtures["vector"]), "payload": {}}),
            ("release", {}),
        ):
            a, ab, _ = old.request(operation, **kwargs)
            b, bb, _ = new.request(operation, **kwargs)
            diagnostics = ("id", "engine", "fallback_reason")
            aa = {k: v for k, v in a.items() if k not in diagnostics}
            ba = {k: v for k, v in b.items() if k not in diagnostics}
            checks.append({"case": f"compat:{operation}", "pass": aa == ba and ab == bb,
                           "rust_engine": b.get("engine"), "ok": b.get("ok")})
    return checks


def measure(command, path, pages, repetition, implementation):
    start = time.perf_counter_ns()
    worker = Worker(command)
    timings = []
    try:
        header, _, inspect_ms = worker.request("inspect", path=str(path))
        if not header.get("ok") or header.get("count") != pages:
            raise AssertionError(header)
        completion_clock = []
        first = render(worker, path, completion_clock=completion_clock)
        cold_ms = (completion_clock[0] - start) / 1_000_000
        first["stage"] = "first_preview_request"
        timings.append(first)
        for stage, selected, side, op in (
            ("sequential", list(range(1, min(pages, 13))), 1800, "preview"),
            ("revisit", [min(pages - 1, p) for p in (0, 4, 8, 4, 0, 8)], 1800, "preview"),
            ("thumbnail", list(range(min(pages, 12))), 370, "render"),
        ):
            for page in selected:
                item = render(worker, path, page, side, op)
                item.update(stage=stage, page=page)
                timings.append(item)
        return {"implementation": implementation, "repetition": repetition,
                "cold_open_first_preview_ms": cold_ms,
                "inspect_request_ms": inspect_ms,
                "first_engine": first["engine"], "timings": timings,
                "sampled_peak_process_tree_rss_bytes": worker.peak_tree_rss,
                "memory_samples": worker.memory_samples, "memory_warning": worker.memory_warning}
    finally:
        worker.close()


def collect_summary(runs, parity_ok):
    rows = []
    datasets = sorted({run["dataset"] for run in runs})
    for dataset in datasets:
        selected = [r for r in runs if r["dataset"] == dataset]
        for stage in ("cold_open_first_preview", "sequential", "revisit", "thumbnail"):
            values = {}
            engines = Counter()
            for implementation in ("python", "rust"):
                own = [r for r in selected if r["implementation"] == implementation]
                if stage == "cold_open_first_preview":
                    data = [r["cold_open_first_preview_ms"] for r in own]
                    if implementation == "rust":
                        engines.update(r["first_engine"] for r in own)
                else:
                    data = [item["elapsed_ms"] for r in own for item in r["timings"] if item["stage"] == stage]
                    if implementation == "rust":
                        engines.update(item["engine"] for r in own for item in r["timings"] if item["stage"] == stage)
                values[implementation] = summary(data)
            native = set(engines) == {"rust-pdfium"}
            row = {"dataset": dataset, "stage": stage, "unit": "ms", **values,
                   "rust_response_engines": dict(engines), "strict_parity_passed": parity_ok}
            if native and parity_ok:
                row["python_median_divided_by_rust_median"] = values["python"]["median"] / values["rust"]["median"]
            else:
                row["speed_ratio_withheld_reason"] = "pixel mismatch" if not parity_ok else "includes Python compatibility fallback"
            rows.append(row)
    return rows


def environment(library, rust):
    import importlib.metadata
    import pdf_page_dragger as viewer
    import pypdfium2
    import bridge
    versions = {}
    for package in ("PySide6", "pypdfium2", "pypdf", "reportlab", "Pillow", "psutil"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None
    cpu_model = platform.processor() or None
    if sys.platform == "linux":
        try:
            cpu_model = next(line.split(":", 1)[1].strip() for line in
                             Path("/proc/cpuinfo").read_text().splitlines() if line.startswith("model name"))
        except (OSError, StopIteration):
            pass
    return {"platform": platform.platform(), "machine": platform.machine(), "cpu_model": cpu_model,
            "python": sys.version, "cpu_count": os.cpu_count(), "versions": versions,
            "viewer_version": viewer.APP_VERSION, "repository_head": commit,
            "baseline_commit": bridge.BASELINE_COMMIT,
            "baseline_source_sha256": sha256(ROOT / "pdf_page_dragger.py"),
            "pdfium_version": str(pypdfium2.PDFIUM_INFO), "pdfium_library": str(library),
            "pdfium_sha256": sha256(library), "rust_binary": str(rust),
            "rust_binary_sha256": sha256(rust),
            "rust_source_sha256": sha256(ROOT / "rust-lab/src/main.rs"),
            "bridge_sha256": sha256(ROOT / "rust-lab/bridge.py"),
            "benchmark_script_sha256": sha256(__file__),
            "cargo_manifest_sha256": sha256(ROOT / "rust-lab/Cargo.toml"),
            "cargo_lock_sha256": sha256(ROOT / "rust-lab/Cargo.lock")}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rust", type=Path, default=Path(__file__).parent / "target/release" / ("viewer-rust-worker.exe" if os.name == "nt" else "viewer-rust-worker"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--fixtures", type=Path, help="Generated fixture directory; overwritten deterministically")
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--correctness-only", action="store_true")
    args = parser.parse_args(argv)
    if args.repetitions < 5:
        parser.error("Use at least five alternating repetitions")
    rust = args.rust.resolve()
    if not rust.is_file():
        parser.error(f"Rust worker missing: {rust}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    folder = args.fixtures or args.out.parent / "fixtures"
    fixtures = generate_fixtures(folder)
    before = {name: describe_fixture(path) for name, path in fixtures.items()}
    library = pdfium_path()
    command = commands(rust, library)
    result = {"schema": 1, "scope": "PDF worker startup/rendering/IPC only; not whole application or GUI",
              "utc_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "method": {"repetitions": args.repetitions,
                         "order": "alternating Python/Rust then Rust/Python",
                         "cold": "new worker process; OS filesystem cache is NOT cleared",
                         "timing": "monotonic wall clock; render requests include IPC and full RGB reception",
                         "memory": "20 ms sampled sum of process-tree RSS; includes fallback children; shared pages may be counted twice; not allocation peak; PID namespace mapping verified",
                         "baseline": "actual application worker_launch() marshal bytecode path",
                         "rust_scope": "Rust PDFium rendering with cached exact pypdf geometry from a persistent Python helper",
                         "render_cache": "no GUI image cache; worker document caches active; revisits rerender",
                         "inputs": "deterministic synthetic PDFs, not user's real documents",
                         "limitations": ["No Windows GUI or installed EXE timing", "No claim about full Rust rewrite",
                                         "Same PDFium library is deliberately used for both implementations"]},
              "environment": environment(library, rust), "fixtures": before, "runs": []}
    print("Checking page count and exact RGB equality...", flush=True)
    result["correctness"] = correctness(command, fixtures)
    parity_ok = all(check["pass"] for check in result["correctness"])
    result["strict_parity_passed"] = parity_ok
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
    if not args.correctness_only:
        for dataset in ("vector", "scan"):
            for repetition in range(args.repetitions):
                order = ("python", "rust") if repetition % 2 == 0 else ("rust", "python")
                for implementation in order:
                    print(f"{dataset} {repetition + 1}/{args.repetitions}: {implementation}", flush=True)
                    run = measure(command[implementation], fixtures[dataset], before[dataset]["pages"], repetition, implementation)
                    run["dataset"] = dataset
                    result["runs"].append(run)
                args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
    result["summary"] = collect_summary(result["runs"], parity_ok)
    result["memory_summary"] = [
        {"dataset": dataset, "implementation": implementation,
         "unit": "bytes", "sampled_peak_process_tree_rss": summary(values)}
        for dataset in ("vector", "scan") for implementation in ("python", "rust")
        if (values := [r["sampled_peak_process_tree_rss_bytes"] for r in result["runs"]
                       if r["dataset"] == dataset and r["implementation"] == implementation
                       and r["sampled_peak_process_tree_rss_bytes"] is not None])
    ]
    result["source_files_unchanged"] = all(sha256(path) == before[name]["sha256"] for name, path in fixtures.items())
    final_environment = environment(library, rust)
    result["implementation_files_unchanged"] = all(
        value == final_environment[key] for key, value in result["environment"].items()
        if key.endswith("_sha256"))
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps({"report": str(args.out), "strict_parity_passed": parity_ok,
                      "checks": len(result["correctness"]), "inputs_unchanged": result["source_files_unchanged"]}, ensure_ascii=False))
    return 0 if parity_ok and result["source_files_unchanged"] and result["implementation_files_unchanged"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
