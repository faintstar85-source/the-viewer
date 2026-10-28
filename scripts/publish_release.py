"""Publish only checked Windows artifacts from this repository's main branch."""
from __future__ import annotations
import json
import os
from pathlib import Path
import shutil

from ci_common import ROOT, release_config
from build_common import BuildError, atomic_json, read_json
from github_release import GitHubClient, load_prepared_release, verify_plan_files, same_notes


def upload_checked(client: GitHubClient, plan: dict) -> dict:
    """GitHub enforces the workflow job's contents:write token on every write."""
    verify_plan_files(plan, client.check)
    repo, tag = plan['repo'], plan['tag']
    release = client.resume_or_find_release(repo, tag)
    if release is None:
        release = client.create_draft(plan)
    client.remember_release(repo, tag, release)
    assets = client.assets(repo, release['id'])
    if len({a['name'] for a in assets}) != len(assets):
        raise BuildError('Duplicate remote asset names; existing files were preserved')
    by_name = {a['name']: a for a in assets}; missing = []
    for record in plan['assets']:
        if record['name'] in by_name:
            client.verify_asset(repo, by_name[record['name']], record)
        else:
            missing.append(record)
    if not release['draft']:
        if missing or not same_notes(release.get('body') or '', plan['notes']):
            raise BuildError('This version is already public with different content; use a new version')
    else:
        client.command(['release', 'edit', tag, '--repo', repo, '--title', plan['title'],
                        '--notes-file', plan['notes_path'], '--prerelease=' + str(plan['prerelease']).lower()])
        for record in missing:
            verify_plan_files(plan, client.check)
            client.command(['release', 'upload', tag, record['path'], '--repo', repo], timeout=3600)
        by_name = {a['name']: a for a in client.assets(repo, release['id'])}
        for record in plan['assets']:
            if record['name'] not in by_name:
                raise BuildError('Uploaded asset is missing: ' + record['name'])
            client.verify_asset(repo, by_name[record['name']], record)
        if plan['publish']:
            verify_plan_files(plan, client.check)
            draft = client.view_release(repo, tag, release_id=release['id'])
            if not draft['draft'] or not same_notes(draft.get('body') or '', plan['notes']):
                raise BuildError('Release metadata changed before publication')
            client.command(['release', 'edit', tag, '--repo', repo, '--draft=false', '--latest'])
    final = client.view_release(repo, tag, release_id=release['id'])
    if not same_notes(final.get('body') or '', plan['notes']) or final.get('name') != plan['title']:
        raise BuildError('Final release metadata mismatch')
    if bool(final.get('prerelease')) != plan['prerelease'] or (plan['publish'] and final['draft']):
        raise BuildError('Final publication status differs from release.json')
    final_assets = {a['name']: a for a in client.assets(repo, final['id'])}
    for record in plan['assets']:
        if record['name'] not in final_assets:
            raise BuildError('Final asset missing: ' + record['name'])
        client.verify_asset(repo, final_assets[record['name']], record)
    result = {'status': 'passed', 'tag': tag, 'url': final['html_url'], 'draft': final['draft'],
              'assets': len(plan['assets']), 'all_assets_sha256_verified': True}
    atomic_json(client.folder / 'Upload_Result.json', result)
    return result


def main() -> None:
    if os.environ.get('GITHUB_ACTIONS') != 'true' or os.environ.get('GITHUB_REF') != 'refs/heads/main':
        raise BuildError('Release publication is restricted to the main-branch Actions job')
    if os.environ.get('GITHUB_EVENT_NAME') not in ('push', 'workflow_dispatch'):
        raise BuildError('This event may not publish releases')
    config = release_config(publish_override=os.environ.get('INPUT_PUBLISH'))
    plan = load_prepared_release(ROOT / 'dist', emit=print)
    repository = os.environ.get('GITHUB_REPOSITORY')
    if plan['repo'] != repository or plan['tag'] != config['tag'] or plan['viewer_version'] != config['version']:
        raise BuildError('The downloaded build does not match this release configuration')
    summary = read_json(ROOT / 'dist' / 'BUILD_VERIFICATION.json')
    if summary.get('commit') != os.environ.get('GITHUB_SHA') or summary.get('windows_exe_checks_passed') is not True:
        raise BuildError('Artifact commit/Windows verification does not match this workflow run')
    if summary.get('status') != 'passed' or summary.get('viewer_version') != config['version']:
        raise BuildError('Windows build summary did not pass')
    if plan['publish'] != config['publish'] or plan['prerelease'] != config['prerelease']:
        raise BuildError('Artifact publication flags differ from this workflow run')
    gh = shutil.which('gh')
    if not gh:
        raise BuildError('GitHub CLI is unavailable on the publisher runner')
    result = upload_checked(GitHubClient(gh, ROOT / 'dist', emit=print), plan)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as report:
            report.write(f"The Viewer {config['version']}: {'draft' if result['draft'] else 'published'}\n\n{result['url']}\n")


if __name__ == '__main__':
    main()
