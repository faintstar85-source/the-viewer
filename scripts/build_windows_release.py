"""Drive the existing checked Windows builder without its packaging GUI."""
from __future__ import annotations
import json
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

from ci_common import ROOT, BUILD_TOOLS, release_config, inside
from build_common import BuildError, atomic_json, read_json, clean_environment
from github_release import prepare_release, verify_plan_files
from installer_build import find_iscc, inspect_iscc
from release_artifact import input_identity
from build_common import sha256

KOREAN_SHA256 = 'a9427833f1975fb13dcaa09bc38aa16eba07698ce9d9596575fdd3362f2646a1'


def prepare_installer_compiler(compiler: str, destination: Path) -> Path:
    """Supply the pinned upstream translation without altering the runner installation."""
    compiler = Path(compiler).resolve()
    if (compiler.parent / 'Languages' / 'Korean.isl').is_file():
        return inspect_iscc(str(compiler))
    translation = (BUILD_TOOLS / 'inno' / 'Korean.isl').read_bytes()
    if hashlib.sha256(translation).hexdigest() != KOREAN_SHA256:
        raise BuildError('The pinned Korean installer translation has changed')
    shutil.copytree(compiler.parent, destination)
    languages = destination / 'Languages'; languages.mkdir(exist_ok=True)
    # The BOM makes the source encoding explicit for every supported Inno version.
    (languages / 'Korean.isl').write_bytes(b'\xef\xbb\xbf' + translation.lstrip(b'\xef\xbb\xbf'))
    return inspect_iscc(str(destination / compiler.name))


def build() -> dict:
    if os.name != 'nt':
        raise BuildError('The Windows release must be built on a Windows runner')
    config = release_config(publish_override=os.environ.get('INPUT_PUBLISH'))
    inputs = input_identity(check_worktree=True)
    repository = os.environ.get('GITHUB_REPOSITORY', 'faintstar85-source/the-viewer')
    source = inside(ROOT, config['source'])
    notes = inside(ROOT, config['notes']).read_text(encoding='utf-8-sig')
    compiler = find_iscc()
    if not compiler:
        raise BuildError('Inno Setup compiler ISCC.exe was not found on the Windows runner')
    run = ROOT / 'build' / 'windows-run'
    run.mkdir(parents=True, exist_ok=False)
    compiler = prepare_installer_compiler(compiler, ROOT / 'build' / 'inno-setup')
    workspace = Path(os.environ.get('RUNNER_TEMP', str(ROOT / 'build'))) / 'TVBuild'
    job = {'source': str(source), 'icon_path': '', 'engines_root': '',
           'run_dir': str(run), 'workspace': str(workspace),
           'stage': str(workspace / 'jobs' / uuid.uuid4().hex), 'cleanup_stage': True,
           'make_installer': True, 'iscc': str(compiler), 'release_repo': repository,
           'include_office': False, 'builder_root': str(ROOT),
           'compliance_root': str(ROOT / 'build' / 'compliance')}
    atomic_json(run / 'job.json', job)
    subprocess.run([sys.executable, '-u', str(BUILD_TOOLS / 'build_runner.py'), str(run / 'job.json')],
                   check=True, env=clean_environment())
    result = read_json(run / 'Build_Result.json')
    if result.get('status') != 'passed' or result.get('windows_exe_checks_passed') is not True:
        raise BuildError('The original Windows EXE checks did not pass')
    if result.get('viewer_version') != config['version']:
        raise BuildError('Build version mismatch')
    plan = prepare_release({'repo': repository, 'tag': config['tag'], 'title': 'The Viewer ' + config['version'],
                            'py': result['release_py']['path'], 'zip': result['zip']['path'],
                            'installer': result['installer']['path'], 'output': str(ROOT / 'build' / 'staged'),
                            'changes': notes, 'publish': config['publish'], 'prerelease': config['prerelease'],
                            'build_result': result}, emit=print)
    verify_plan_files(plan)
    dist = ROOT / 'dist'; dist.mkdir(exist_ok=False)
    for record in plan['assets']:
        shutil.copy2(record['path'], dist / record['name'])
    # The standard loader rebases paths after download from the immutable Actions artifact.
    atomic_json(dist / 'Upload_Plan.json', plan)
    summary = {key: result[key] for key in ('tool_version', 'viewer_version', 'status', 'source_sha256',
               'source_checks', 'exe_checks', 'final_location_checks', 'windows_exe_checks_passed', 'tested_platform', 'python')}
    summary['commit'] = os.environ.get('GITHUB_SHA', '')
    summary['installer_sha256'] = result['installer']['sha256']
    summary['release_source_sha256'] = result['release_py']['sha256']
    # Preserve the actual dependency resolution and toolchain used by these bytes.
    # A retry reuses them; it does not resolve version ranges again.
    shutil.copy2(run / 'installed_versions.txt', dist / 'BUILD_DEPENDENCIES.txt')
    environment = read_json(run / 'Environment.json')
    environment.update(python=sys.version, image_os=os.environ.get('ImageOS', ''),
                       image_version=os.environ.get('ImageVersion', ''),
                       compiler_files={p.relative_to(compiler.parent).as_posix(): sha256(p)
                                       for p in compiler.parent.rglob('*') if p.is_file()})
    atomic_json(dist / 'BUILD_ENVIRONMENT.json', environment)
    if input_identity(check_worktree=True) != inputs:
        raise BuildError('Build inputs changed during the Windows build')
    summary.update(schema=2, inputs=inputs, repository=repository,
                   run_id=int(os.environ['GITHUB_RUN_ID']), run_attempt=int(os.environ['GITHUB_RUN_ATTEMPT']),
                   environment_files={name: sha256(dist / name) for name in
                                      ('BUILD_DEPENDENCIES.txt', 'BUILD_ENVIRONMENT.json')})
    atomic_json(dist / 'BUILD_VERIFICATION.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return plan


if __name__ == '__main__':
    build()
