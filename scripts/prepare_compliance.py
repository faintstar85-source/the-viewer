"""Restore the existing notices and fetch matching source archives by SHA-256."""
from __future__ import annotations
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import urllib.request
from urllib.parse import urlparse
import uuid
import zipfile

from ci_common import ROOT, inside
from build_common import BuildError, sha256


def restore_metadata(package: Path, target: Path) -> None:
    record = json.loads(package.read_text(encoding='utf-8'))
    if record.get('schema') != 1 or record.get('encoding') != 'zip+base64':
        raise BuildError('Unsupported compliance metadata')
    data = base64.b64decode(record['data'], validate=True)
    if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise BuildError('Compliance metadata checksum mismatch')
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        if len(entries) > 2000 or len({e.filename for e in entries}) != len(entries):
            raise BuildError('Invalid compliance archive entries')
        for entry in entries:
            if entry.is_dir() or entry.flag_bits & 1 or entry.file_size > 16 * 1024**2:
                raise BuildError('Invalid compliance archive member')
            destination = inside(target, entry.filename)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(entry))


def source_records(target: Path) -> list[dict]:
    qt = json.loads((target / 'QT_SOURCE_MANIFEST.json').read_text(encoding='utf-8-sig'))
    certifi = json.loads((target / 'CERTIFI_SOURCE_MANIFEST.json').read_text(encoding='utf-8-sig'))
    if qt.get('qt_version') != '6.11.1' or qt.get('pyside_version') != '6.11.1' or certifi.get('version') != '2026.4.22':
        raise BuildError('Source versions differ from the pinned runtime')
    modules = qt.get('modules', {})
    if set(modules) != {'qtbase', 'qtsvg', 'qtimageformats', 'pyside'}:
        raise BuildError('Required Qt module sources are missing')
    return [*modules.values(), certifi]


def download_source(target: Path, record: dict, opener=urllib.request.urlopen) -> Path:
    destination = inside(target, record['path'])
    url = urlparse(record['source_url'])
    if url.scheme != 'https' or url.netloc not in {'download.qt.io', 'files.pythonhosted.org'} or url.username or url.password:
        raise BuildError('Unsupported source archive origin')
    if type(record.get('bytes')) is not int or not 0 < record['bytes'] < 512 * 1024**2:
        raise BuildError('Invalid source archive size')
    if destination.is_file() and destination.stat().st_size == record['bytes'] and sha256(destination) == record['sha256']:
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + '.' + uuid.uuid4().hex + '.part')
    try:
        request = urllib.request.Request(record['source_url'], headers={'User-Agent': 'TheViewer-build'})
        digest = hashlib.sha256(); size = 0
        with opener(request, timeout=120) as response, temporary.open('xb') as output:
            if urlparse(response.geturl()).scheme != 'https':
                raise BuildError('Source archive redirected away from HTTPS')
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                size += len(block)
                if size > record['bytes']:
                    raise BuildError('Source archive is larger than recorded')
                digest.update(block); output.write(block)
        if size != record['bytes'] or digest.hexdigest() != record['sha256']:
            raise BuildError('Source archive size/SHA-256 mismatch: ' + record['path'])
        os.replace(temporary, destination)
        return destination
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    target = ROOT / 'build' / 'compliance'
    restore_metadata(ROOT / 'tools' / 'build' / 'compliance_metadata.json', target)
    for record in source_records(target):
        path = download_source(target, record)
        print('Source verified:', path.name, flush=True)
    # Run the same original gate before handing the directory to the builder.
    from license_gate import prepare_license_materials
    import tempfile
    with tempfile.TemporaryDirectory(prefix='viewer-license-check-') as temp:
        prepare_license_materials(ROOT / 'pdf_page_dragger.py', Path(temp) / 'verified', selected=str(target))
    print('Compliance preparation verified')


if __name__ == '__main__':
    main()
