"""Checked configuration shared by local validation and GitHub Actions."""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BUILD_TOOLS = ROOT / 'tools' / 'build'
sys.path.insert(0, str(BUILD_TOOLS))
from build_common import BuildError, inspect_source


def inside(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise BuildError('Invalid repository-relative path')
    path = Path(relative)
    if path.is_absolute() or any(p in ('.', '..') for p in path.parts):
        raise BuildError('Path must remain inside the repository')
    target = (root / path).resolve()
    if root.resolve() not in target.parents:
        raise BuildError('Path leaves the repository')
    return target


def release_config(root: Path = ROOT, publish_override: str | None = None) -> dict:
    config = json.loads((root / 'release.json').read_text(encoding='utf-8-sig'))
    if not isinstance(config, dict) or config.get('schema') != 1:
        raise BuildError('Unsupported release configuration')
    version = config.get('version')
    if not isinstance(version, str) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise BuildError('Use a numeric version such as 3.13.41')
    for flag in ('publish', 'prerelease'):
        if type(config.get(flag)) is not bool:
            raise BuildError('Release flag must be a boolean: ' + flag)
    source = inside(root, config.get('source', ''))
    notes = inside(root, config.get('notes', ''))
    if source.suffix != '.py' or notes.suffix != '.md' or not notes.is_file():
        raise BuildError('Viewer source and release notes are required')
    if inspect_source(source)['version'] != version:
        raise BuildError('APP_VERSION and release.json version differ')
    if not notes.read_text(encoding='utf-8-sig').strip():
        raise BuildError('Release notes are empty')
    result = dict(config, tag='v' + version)
    if publish_override not in (None, ''):
        if publish_override not in ('true', 'false'):
            raise BuildError('publish input must be true or false')
        result['publish'] = publish_override == 'true'
    return result


def main() -> None:
    config = release_config(publish_override=os.environ.get('INPUT_PUBLISH'))
    print(json.dumps({k: config[k] for k in ('version', 'tag', 'publish', 'prerelease')}, ensure_ascii=False))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
            for key in ('version', 'tag', 'publish', 'prerelease'):
                value = str(config[key]).lower() if isinstance(config[key], bool) else config[key]
                output.write(f'{key}={value}\n')


if __name__ == '__main__':
    main()
