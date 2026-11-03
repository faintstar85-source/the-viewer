"""Select and restore an immutable, checked Actions artifact; never rebuild a draft.

Only release.json's publish flag is excluded from the input identity. Every other
tracked byte (including dependencies, workflow, tools and notes) must match.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile

from ci_common import ROOT, release_config
from build_common import BuildError, atomic_json, inspect_source, read_json, sha256
from github_release import GitHubClient, github_environment, load_prepared_release

WORKFLOW = '.github/workflows/release.yml'
EVIDENCE_FILES = {'BUILD_DEPENDENCIES.txt', 'BUILD_ENVIRONMENT.json'}


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(['git', '-C', str(root), *args])


def input_identity(root: Path = ROOT, ref: str = 'HEAD', *, check_worktree=False) -> dict:
    files = {}
    for entry in git(root, 'ls-tree', '-rz', '--full-tree', ref).split(b'\0'):
        if not entry:
            continue
        info, path_bytes = entry.split(b'\t', 1)
        mode, kind, blob = info.decode().split()
        name = path_bytes.decode('utf-8')
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise BuildError('Unsupported build input (symlink/submodule): ' + name)
        data = git(root, 'cat-file', 'blob', blob)
        if check_worktree and ((root / name).is_symlink() or (root / name).read_bytes() != data):
            raise BuildError('Build input differs from committed bytes: ' + name)
        if name == 'release.json':
            config = json.loads(data)
            config.pop('publish', None)
            data = canonical(config)
        files[name] = {'mode': mode, 'sha256': hashlib.sha256(data).hexdigest()}
    if 'release.json' not in files:
        raise BuildError('Missing release configuration in build inputs')
    return {'schema': 1, 'files': files, 'sha256': hashlib.sha256(canonical(files)).hexdigest()}


def artifact_name(config: dict, identity: dict) -> str:
    return 'viewer-windows-' + config['version'] + '-' + identity['sha256']


def positive_id(value) -> int:
    if not re.fullmatch(r'[1-9][0-9]*', str(value)):
        raise BuildError('Expected a positive GitHub ID')
    return int(value)


def pages(client, endpoint: str, key: str) -> list:
    result = []
    for page in range(1, 10001):
        batch = client.api(endpoint + ('&' if '?' in endpoint else '?') + f'per_page=100&page={page}')
        items = batch.get(key) if isinstance(batch, dict) else None
        if not isinstance(items, list):
            raise BuildError('Invalid paginated GitHub response: ' + key)
        result.extend(items)
        if len(items) < 100:
            return result
    raise BuildError('GitHub pagination limit exceeded')


def validate_origin(client, repo: str, artifact: dict, expected_name: str) -> dict:
    if (artifact.get('name') != expected_name or artifact.get('expired') is not False
            or not re.fullmatch(r'sha256:[0-9a-f]{64}', artifact.get('digest') or '')):
        raise BuildError('Artifact name, expiry or SHA-256 evidence is invalid')
    positive_id(artifact['id'])
    origin = artifact.get('workflow_run') or {}
    run_id = positive_id(origin.get('id'))
    run = client.api(f'repos/{repo}/actions/runs/{run_id}')
    if (run.get('id') != run_id or (run.get('repository') or {}).get('full_name') != repo
            or (run.get('head_repository') or {}).get('full_name') != repo
            or run.get('path') != WORKFLOW or run.get('head_branch') != 'main'
            or run.get('event') not in ('push', 'workflow_dispatch')
            or run.get('head_sha') != origin.get('head_sha')
            or not re.fullmatch(r'[0-9a-f]{40}', run.get('head_sha') or '')):
        raise BuildError('Artifact did not originate from this main-branch release workflow')
    # A failed release job is allowed. The original attempt's validation and
    # Windows job are checked separately after reading its sealed build summary.
    return run


def select_artifact(client, repo: str, config: dict, identity: dict, reuse_run_id='') -> dict:
    release = client.view_release(repo, config['tag'])
    if release is not None and not release['draft']:
        return {'mode': 'public', 'url': release['html_url']}
    name = artifact_name(config, identity)
    endpoint = f'repos/{repo}/actions/artifacts'
    if reuse_run_id:
        endpoint = f'repos/{repo}/actions/runs/{positive_id(reuse_run_id)}/artifacts'
    matches = [a for a in pages(client, endpoint + '?name=' + name, 'artifacts')
               if a.get('name') == name and a.get('expired') is False]
    if not matches:
        if release is not None or reuse_run_id:
            raise BuildError('No retained matching build artifact. Existing draft preserved; use a new version. '
                             'Legacy/expired artifacts cannot be promoted automatically.')
        return {'mode': 'build', 'artifact_name': name}
    if len(matches) != 1:
        raise BuildError('Multiple matching builds; specify reuse_run_id. No build or release was changed.')
    artifact = matches[0]
    run = validate_origin(client, repo, artifact, name)
    return {'mode': 'reuse', 'artifact_id': artifact['id'], 'run_id': run['id'], 'artifact_name': name}


def verify_bundle(folder: Path, config: dict, identity: dict, repo: str, origin: dict,
                  *, root: Path = ROOT) -> dict:
    plan = load_prepared_release(folder)
    summary = read_json(folder / 'BUILD_VERIFICATION.json')
    if (summary.get('schema') != 2 or summary.get('inputs') != identity
            or summary.get('commit') != origin['head_sha'] or summary.get('repository') != repo
            or summary.get('run_id') != origin['id']):
        raise BuildError('Build source, dependency/workflow inputs or origin do not match')
    # Recompute from the original Git objects, not just the downloaded assertion.
    if input_identity(root, origin['head_sha']) != identity:
        raise BuildError('Original build commit has different inputs')
    if (plan['repo'] != repo or plan['tag'] != config['tag'] or plan['viewer_version'] != config['version']
            or plan['prerelease'] != config['prerelease']
            or plan.get('build_checks_verified') is not True or plan.get('installer_build_verified') is not True):
        raise BuildError('Artifact release configuration or installer verification differs')
    source = inspect_source(root / config['source'])
    if (summary.get('status') != 'passed' or summary.get('windows_exe_checks_passed') is not True
            or summary.get('tested_platform') != 'win32' or summary.get('viewer_version') != config['version']
            or summary.get('source_sha256') != source['sha256']
            or any(summary.get(k) != source['required_check_count'] for k in
                   ('source_checks', 'exe_checks', 'final_location_checks'))):
        raise BuildError('Complete source/Windows/final-location verification is required')
    installer = next((a for a in plan['assets'] if a['name'].endswith('.exe')), None)
    py = next(a for a in plan['assets'] if a['name'].endswith('.py'))
    if (not installer or summary.get('installer_sha256') != installer['sha256']
            or summary.get('release_source_sha256') != py['sha256']):
        raise BuildError('Source/installer hashes differ from the verified build')
    # The existing exporter rewrites the embedded icon, BOM and native newlines.
    # Its output hash is distinct from the committed input hash; both are bound
    # to the original successful workflow and the immutable artifact digest.
    evidence = summary.get('environment_files') or {}
    if set(evidence) != EVIDENCE_FILES:
        raise BuildError('Resolved dependency/toolchain evidence is missing')
    for name, digest in evidence.items():
        if not (folder / name).is_file() or sha256(folder / name) != digest:
            raise BuildError('Build environment evidence was changed: ' + name)
    # Publication is an intent of THIS run; changing it does not rebuild bytes.
    plan['publish'] = config['publish']
    return plan


def verify_jobs(client, repo: str, origin: dict, attempt: int) -> None:
    attempt = positive_id(attempt)
    if attempt > origin['run_attempt']:
        raise BuildError('Artifact claims a future run attempt')
    jobs = pages(client, f"repos/{repo}/actions/runs/{origin['id']}/attempts/{attempt}/jobs", 'jobs')
    for name in ('validate', 'windows-build'):
        matches = [j for j in jobs if j.get('name') == name and j.get('run_attempt') == attempt]
        if len(matches) != 1 or matches[0].get('conclusion') != 'success':
            raise BuildError('Original build attempt did not pass: ' + name)


def extract_checked(archive: Path, destination: Path, digest: str) -> None:
    if 'sha256:' + sha256(archive) != digest:
        raise BuildError('Downloaded Actions artifact SHA-256 mismatch')
    with zipfile.ZipFile(archive) as bundle:
        members = bundle.infolist()
        names = [m.filename for m in members]
        if (len(names) != len(set(names)) or len(names) > 20 or not names
                or sum(m.file_size for m in members) > 8 * 1024**3):
            raise BuildError('Invalid artifact archive inventory')
        for member in members:
            name = member.filename
            if (name in ('', '.', '..') or any(c in name for c in '/\\:\x00')
                    or member.is_dir() or (member.external_attr >> 16) & 0o170000 == 0o120000):
                raise BuildError('Unsafe artifact archive entry: ' + name)
        bundle.extractall(destination)


def restore(client, repo: str, artifact_id: str, config: dict, identity: dict, *, root=ROOT) -> dict:
    artifact = client.api(f'repos/{repo}/actions/artifacts/{positive_id(artifact_id)}')
    if artifact.get('id') != positive_id(artifact_id):
        raise BuildError('GitHub returned a different artifact ID')
    origin = validate_origin(client, repo, artifact, artifact_name(config, identity))
    dist = root / 'dist'
    if dist.exists():
        raise BuildError('Restore requires a fresh dist directory')
    with tempfile.TemporaryDirectory(dir=root) as temp:
        temp = Path(temp)
        archive = temp / 'artifact.zip'
        with archive.open('wb') as output:
            subprocess.run([client.gh, 'api', f"repos/{repo}/actions/artifacts/{artifact['id']}/zip"],
                           stdout=output, check=True, timeout=3600, env=github_environment())
        extracted = temp / 'dist'
        extracted.mkdir()
        extract_checked(archive, extracted, artifact['digest'])
        plan = verify_bundle(extracted, config, identity, repo, origin, root=root)
        summary = read_json(extracted / 'BUILD_VERIFICATION.json')
        verify_jobs(client, repo, origin, summary.get('run_attempt'))
        expected = {a['name'] for a in plan['assets']} | EVIDENCE_FILES | {'Upload_Plan.json', 'BUILD_VERIFICATION.json'}
        if {p.name for p in extracted.iterdir()} != expected:
            raise BuildError('Unexpected files in the release artifact')
        # Keep original plan/summary bytes, including the original publish flag.
        extracted.rename(dist)
    receipt = {'schema': 1, 'artifact_id': artifact['id'], 'artifact_digest': artifact['digest'],
               'origin': origin, 'inputs_sha256': identity['sha256']}
    atomic_json(dist / 'ARTIFACT_RESTORE.json', receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=('select', 'restore'))
    args = parser.parse_args()
    if (os.environ.get('GITHUB_ACTIONS') != 'true' or os.environ.get('GITHUB_REF') != 'refs/heads/main'
            or os.environ.get('GITHUB_EVENT_NAME') not in ('push', 'workflow_dispatch')):
        raise BuildError('Artifact selection is restricted to the main-branch release workflow')
    config = release_config(publish_override=os.environ.get('INPUT_PUBLISH'))
    identity = input_identity(check_worktree=True)
    repo = os.environ['GITHUB_REPOSITORY']
    gh = shutil.which('gh')
    if not gh:
        raise BuildError('GitHub CLI is unavailable')
    client = GitHubClient(gh, ROOT / 'build' / 'artifact-selection', emit=print)
    if args.operation == 'select':
        result = select_artifact(client, repo, config, identity, os.environ.get('INPUT_REUSE_RUN_ID', ''))
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
                for key, value in result.items():
                    output.write(f'{key}={value}\n')
        if result['mode'] == 'public' and os.environ.get('GITHUB_STEP_SUMMARY'):
            with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as report:
                report.write(f"Already public; preserved without build or writes: {result['url']}\n\n"
                             'No new artifact verification or publication was performed.\n')
    else:
        result = restore(client, repo, os.environ['RELEASE_ARTIFACT_ID'], config, identity)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
