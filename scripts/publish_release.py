"""Publish only checked Windows artifacts from this repository's main branch."""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import shutil

from ci_common import ROOT, release_config
from build_common import BuildError, atomic_json, read_json
from github_release import GitHubClient, verify_plan_files, same_notes
from release_artifact import input_identity, verify_bundle, positive_id


def verify_existing_tag(client, repo: str, tag: str, identity: dict, root: Path = ROOT) -> None:
    refs = client.api(f'repos/{repo}/git/matching-refs/tags/{tag}')
    if not isinstance(refs, list):
        raise BuildError('Could not verify existing tag')
    matches = [r for r in refs if r.get('ref') == 'refs/tags/' + tag]
    if not matches:
        return
    if len(matches) != 1:
        raise BuildError('Ambiguous existing tag')
    target = matches[0]['object']
    for _ in range(10):
        if not re.fullmatch(r'[0-9a-f]{40}', target.get('sha') or ''):
            raise BuildError('Invalid existing tag target')
        if target.get('type') == 'commit':
            if input_identity(root, target['sha']) != identity:
                raise BuildError('Existing tag has different build inputs; tag preserved')
            return
        if target.get('type') != 'tag':
            break
        target = client.api(f"repos/{repo}/git/tags/{target['sha']}")['object']
    raise BuildError('Could not resolve existing tag safely; tag preserved')


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
    expected_names = {a['name'] for a in plan['assets']}
    if set(by_name) - expected_names:
        raise BuildError('Unexpected remote assets; existing files were preserved')
    for record in plan['assets']:
        if record['name'] in by_name:
            client.verify_asset(repo, by_name[record['name']], record)
        else:
            missing.append(record)
    if not release['draft']:
        if missing or not same_notes(release.get('body') or '', plan['notes']):
            raise BuildError('This version is already public with different content; use a new version')
    else:
        # Recheck the release immediately before the first write. A competing
        # publication must not turn a draft retry into edits of public content.
        latest = client.view_release(repo, tag, release_id=release['id'])
        if not latest['draft']:
            raise BuildError('Release became public; existing files were preserved')
        if (not same_notes(latest.get('body') or '', plan['notes']) or latest.get('name') != plan['title']
                or bool(latest.get('prerelease')) != plan['prerelease']):
            raise BuildError('Draft metadata differs from the verified build; existing draft preserved')
        for record in missing:
            verify_plan_files(plan, client.check)
            if not client.view_release(repo, tag, release_id=release['id'])['draft']:
                raise BuildError('Release became public; upload stopped')
            client.command(['release', 'upload', tag, record['path'], '--repo', repo], timeout=3600)
        uploaded = client.assets(repo, release['id'])
        by_name = {a['name']: a for a in uploaded}
        if len(uploaded) != len(by_name) or set(by_name) != expected_names:
            raise BuildError('Remote asset inventory changed; publication stopped')
        for record in plan['assets']:
            if record['name'] not in by_name:
                raise BuildError('Uploaded asset is missing: ' + record['name'])
            client.verify_asset(repo, by_name[record['name']], record)
        if plan['publish']:
            verify_plan_files(plan, client.check)
            draft = client.view_release(repo, tag, release_id=release['id'])
            if (not draft['draft'] or not same_notes(draft.get('body') or '', plan['notes'])
                    or draft.get('name') != plan['title']
                    or bool(draft.get('prerelease')) != plan['prerelease']):
                raise BuildError('Release metadata changed before publication')
            client.command(['release', 'edit', tag, '--repo', repo, '--draft=false', '--latest'])
    final = client.view_release(repo, tag, release_id=release['id'])
    if not same_notes(final.get('body') or '', plan['notes']) or final.get('name') != plan['title']:
        raise BuildError('Final release metadata mismatch')
    if bool(final.get('prerelease')) != plan['prerelease'] or (plan['publish'] and final['draft']):
        raise BuildError('Final publication status differs from release.json')
    uploaded = client.assets(repo, final['id'])
    final_assets = {a['name']: a for a in uploaded}
    if len(uploaded) != len(final_assets) or set(final_assets) != expected_names:
        raise BuildError('Final asset inventory mismatch')
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
    repository = os.environ.get('GITHUB_REPOSITORY')
    receipt = read_json(ROOT / 'dist' / 'ARTIFACT_RESTORE.json')
    identity = input_identity(check_worktree=True)
    if (receipt.get('schema') != 1 or receipt.get('inputs_sha256') != identity['sha256']
            or receipt.get('artifact_id') != positive_id(os.environ.get('RELEASE_ARTIFACT_ID'))):
        raise BuildError('Expected immutable artifact restore receipt is missing')
    plan = verify_bundle(ROOT / 'dist', config, identity, repository, receipt['origin'])
    gh = shutil.which('gh')
    if not gh:
        raise BuildError('GitHub CLI is unavailable on the publisher runner')
    client = GitHubClient(gh, ROOT / 'dist', emit=print)
    verify_existing_tag(client, repository, plan['tag'], identity)
    # Pin new tags to the checked commit, even if main advances while building.
    plan['target_commitish'] = os.environ['GITHUB_SHA']
    result = upload_checked(client, plan)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as report:
            report.write(f"The Viewer {config['version']}: {'draft' if result['draft'] else 'published'}\n\n{result['url']}\n\n"
                         f"Verified original build run {receipt['origin']['id']}, artifact {receipt['artifact_id']}.\n")


if __name__ == '__main__':
    main()
