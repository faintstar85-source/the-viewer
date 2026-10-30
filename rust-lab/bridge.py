"""Keep the v3.13.45 UI and exact PDF geometry; replace only RGB rendering.

This is deliberately a hybrid experiment, not a complete Rust rewrite.
The unchanged worker's code is compiled before timed subprocess launches, just
as the original viewer's worker_launch does. Never load a cache from a user file.
"""
import atexit
import hashlib
import inspect
import json
import marshal
import os
from pathlib import Path
import sys
import tempfile

BASELINE_SHA256 = "c3f2c521693a791db9d91855b5ba6e8d38cb1c2598da2e92ec143cb7dc7aec79"
BASELINE_COMMIT = "b284c7e0f8d2e435667d0e736dd283d37aaf0903"

GEOMETRY_CODE = '''    geometry_readers = OrderedDict()

    def exact_geometry(path, index):
        from pypdf import PdfReader
        stat = os.stat(path)
        signature = (stat.st_mtime_ns, stat.st_size, stat.st_ino)
        if path in geometry_readers and geometry_readers[path][0] != signature:
            geometry_readers.pop(path)[1].stream.close()
        if path not in geometry_readers:
            reader = PdfReader(path, strict=False)
            if reader.is_encrypted and not reader.decrypt(''):
                reader.stream.close()
                raise ValueError('암호가 없는 PDF 파일을 선택하세요.')
            geometry_readers[path] = (signature, reader)
        geometry_readers.move_to_end(path)
        while len(geometry_readers) > 4:
            geometry_readers.popitem(last=False)[1][1].stream.close()
        metadata = geometry_readers[path][1].pages[int(index)]
        if any(a.get_object().get('/Subtype') == '/Widget'
               for a in (metadata.get('/Annots') or [])):
            return {'compatible': False}
        media, crop = metadata.mediabox, metadata.cropbox
        w = min(float(media.right), float(crop.right))-max(float(media.left), float(crop.left))
        h = min(float(media.top), float(crop.top))-max(float(media.bottom), float(crop.bottom))
        unit = float(metadata.get('/UserUnit', 1.))
        rotation = int(metadata.get('/Rotate', 0)) % 360
        if not math.isfinite(unit) or unit <= 0 or w <= 0 or h <= 0 or rotation not in (0, 90, 180, 270):
            return {'compatible': False}
        w, h = w*unit, h*unit
        if rotation in (90, 270):
            w, h = h, w
        return {'compatible': True, 'width': w, 'height': h, 'unit': unit}

'''


def verify_baseline(viewer):
    path = Path(viewer.__file__).resolve()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != BASELINE_SHA256:
        raise RuntimeError(f"Baseline changed; review Rust bridge first: {digest}")
    return path


def baseline_command(viewer):
    executable, arguments = viewer.worker_launch("--pdf-worker")
    return [executable, *arguments]


def compatibility_command(viewer):
    path = verify_baseline(viewer)
    cached = getattr(viewer, "_rust_compat_command", None)
    if cached is not None and Path(cached[-3]).is_file():
        return list(cached)
    source = inspect.getsource(viewer._viewer_fast_pdf_worker)
    # Geometry-only requests do not need a second copy of PDFium. Preserve the
    # original import for compatibility operations, but defer it until document().
    import_marker = "    import pypdfium2 as pdfium\n"
    document_marker = "    def document(path):\n"
    if source.count(import_marker) != 1 or source.count(document_marker) != 1:
        raise RuntimeError("PDFium lazy import markers changed")
    source = source.replace(import_marker, "    pdfium = None\n", 1)
    source = source.replace(document_marker, document_marker +
        "        nonlocal pdfium\n"
        "        if pdfium is None:\n"
        "            import pypdfium2 as pdfium\n", 1)
    marker = "    def runtime():\n"
    if source.count(marker) != 1:
        raise RuntimeError("Compatibility injection marker changed")
    source = source.replace(marker, GEOMETRY_CODE + marker, 1)
    marker = "    def release():\n"
    source = source.replace(marker, marker + "        while geometry_readers:\n            geometry_readers.popitem(last=False)[1][1].stream.close()\n", 1)
    marker = "                elif op in ('inspect', 'preview', 'render', 'search'):\n"
    if source.count(marker) != 1:
        raise RuntimeError("Compatibility operation marker changed")
    source = source.replace(marker,
        "                elif op == '_rust_geometry':\n"
        "                    result = {'geometry': exact_geometry(request['path'], request['page'])}\n" + marker, 1)
    namespace = {"sys": sys, "__file__": str(path), "__builtins__": __builtins__}
    exec(compile(source, str(path) + ":rust-geometry", "exec"), namespace)
    fd, cache = tempfile.mkstemp(prefix="TheViewer_RustGeometry_", suffix=".code")
    with os.fdopen(fd, "wb") as stream:
        marshal.dump(namespace["_viewer_fast_pdf_worker"].__code__, stream)
    atexit.register(lambda: Path(cache).unlink(missing_ok=True))
    bootstrap = ("import sys,marshal,types;f=open(sys.argv[1],'rb');c=marshal.load(f);f.close();"
        "g={'sys':sys,'__file__':sys.argv[2],'__builtins__':__builtins__};types.FunctionType(c,g)()")
    executable = Path(sys.executable)
    if executable.name.lower() == "pythonw.exe" and executable.with_name("python.exe").is_file():
        executable = executable.with_name("python.exe")
    command = [str(executable), "-u", "-c", bootstrap, cache, str(path), "--pdf-worker"]
    viewer._rust_compat_command = command
    return command


def pdfium_library():
    import pypdfium2_raw
    root = Path(pypdfium2_raw.__file__).resolve().parent
    for name in ("pdfium.dll", "libpdfium.so", "libpdfium.dylib"):
        path = root / name
        if path.is_file():
            return path.resolve()
    raise FileNotFoundError("Cannot locate the baseline pypdfium2 PDFium library")


def rust_command(viewer, rust_binary):
    binary = Path(rust_binary).resolve()
    if not binary.is_file():
        raise FileNotFoundError(f"Build the Rust worker first: {binary}")
    return [str(binary), "--pdfium", str(pdfium_library()),
            "--fallback-json", json.dumps(compatibility_command(viewer), ensure_ascii=True)]


def install(viewer, rust_binary):
    """Install into the current imported module, never overwrite application files."""
    command = rust_command(viewer, rust_binary)
    original_launch = viewer.worker_launch
    def launch(flag="--pdf-worker"):
        if flag == "--pdf-worker":
            return command[0], command[1:]
        return original_launch(flag)
    viewer.worker_launch = launch
    return command
