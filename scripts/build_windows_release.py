"""Drive the existing checked Windows builder without its packaging GUI."""
from __future__ import annotations
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

from ci_common import ROOT, BUILD_TOOLS, release_config, inside
from build_common import BuildError, atomic_json, read_json
from github_release import prepare_release, verify_plan_files
from installer_build import find_iscc


def build() -> dict:
    if os.name != 'nt':
        raise BuildError('The Windows release must be built on a Windows runner')
    config = release_config(publish_override=os.environ.get('INPUT_PUBLISH'))
    repository = os.environ.get('GITHUB_REPOSITORY', 'faintstar85-source/the-viewer')
    source = inside(ROOT, config['source'])
    notes = inside(ROOT, config['notes']).read_text(encoding='utf-8-sig')
    compiler = find_iscc()
    if not compiler:
        raise BuildError('Inno Setup compiler ISCC.exe was not found on the Windows runner')
    run = ROOT / 'build' / 'windows-run'
    run.mkdir(parents=True, exist_ok=False)
    workspace = Path(os.environ.get('RUNNER_TEMP', str(ROOT / 'build'))) / 'TVBuild'
    job = {'source': str(source), 'icon_path': '', 'engines_root': '',
           'run_dir': str(run), 'workspace': str(workspace),
           'stage': str(workspace / 'jobs' / uuid.uuid4().hex), 'cleanup_stage': True,
           'make_installer': True, 'iscc': str(compiler), 'release_repo': repository,
           'include_office': False, 'builder_root': str(ROOT),
           'compliance_root': str(ROOT / 'build' / 'compliance')}
    atomic_json(run / 'job.json', job)
    subprocess.run([sys.executable, '-u', str(BUILD_TOOLS / 'build_runner.py'), str(run / 'job.json')], check=True)
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
    atomic_json(dist / 'BUILD_VERIFICATION.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return plan


if __name__ == '__main__':
    build()
