from __future__ import annotations
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import release_artifact as artifacts
import publish_release as publisher
from build_common import BuildError, atomic_json, read_json, sha256
from github_release import GitHubClient, release_notes
from test_release_automation import FakeGitHub


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.folder = self.root / 'bundle'
        self.folder.mkdir()
        self.config = dict(schema=1, source='viewer.py', notes='notes.md', version='3.13.41',
                           tag='v3.13.41', publish=False, prerelease=False)
        self.source = b'source'
        for name, data in {'viewer.py': self.source, 'requirements.txt': b'pkg==1\n',
                           'build.py': b'build', 'workflow.yml': b'windows-2022', 'notes.md': b'notes'}.items():
            (self.repo / name).write_bytes(data)
        atomic_json(self.repo / 'release.json', self.config)
        self.git('init', '-q')
        self.git('config', 'user.email', 'tests@example.invalid')
        self.git('config', 'user.name', 'Tests')
        self.commit()
        self.identity = artifacts.input_identity(self.repo, check_worktree=True)
        self.origin = {'id': 70, 'head_sha': self.git('rev-parse', 'HEAD').decode().strip(), 'run_attempt': 2,
                       'repository': {'full_name': 'example/viewer'}, 'head_repository': {'full_name': 'example/viewer'},
                       'path': artifacts.WORKFLOW, 'head_branch': 'main', 'event': 'push', 'conclusion': 'failure'}
        self.asset = {'id': 90, 'name': artifacts.artifact_name(self.config, self.identity),
                      'expired': False, 'digest': 'sha256:' + 'a' * 64,
                      'workflow_run': {'id': 70, 'head_sha': self.origin['head_sha']}}
        notes = release_notes('3.13.41', 'v3.13.41', 'viewer.py', 'viewer.zip', 'checked change')
        self.plan = dict(schema=1, tool_version='1.5.10', viewer_version='3.13.41', repo='example/viewer',
                         tag='v3.13.41', title='The Viewer 3.13.41', notes=notes, publish=False, prerelease=False,
                         notes_path=str(self.folder / 'RELEASE_NOTES.md'), folder=str(self.folder),
                         build_checks_verified=True, installer_build_verified=True, assets=[])
        for name, data in [('viewer.py', self.source), ('viewer.zip', b'zip'),
                           ('The_Viewer_Setup_3.13.41_x64.exe', b'exe'), ('VERSION_GUIDE.txt', b'guide'),
                           ('RELEASE_NOTES.md', notes.encode()), ('SHA256SUMS.txt', b'sums')]:
            (self.folder / name).write_bytes(data)
            self.plan['assets'].append(dict(name=name, path=str(self.folder / name), bytes=len(data),
                                           sha256=hashlib.sha256(data).hexdigest()))
        atomic_json(self.folder / 'Upload_Plan.json', self.plan)
        for name in artifacts.EVIDENCE_FILES:
            (self.folder / name).write_bytes(b'verified environment')
        self.summary = dict(schema=2, inputs=self.identity, commit=self.origin['head_sha'], repository='example/viewer',
                            run_id=70, run_attempt=1, status='passed', windows_exe_checks_passed=True,
                            tested_platform='win32', viewer_version='3.13.41', source_sha256=sha256(self.repo / 'viewer.py'),
                            source_checks=10, exe_checks=10, final_location_checks=10,
                            installer_sha256=sha256(self.folder / 'The_Viewer_Setup_3.13.41_x64.exe'),
                            release_source_sha256=sha256(self.folder / 'viewer.py'),
                            environment_files={n: sha256(self.folder / n) for n in artifacts.EVIDENCE_FILES})
        atomic_json(self.folder / 'BUILD_VERIFICATION.json', self.summary)
        self.source_info = {'sha256': sha256(self.repo / 'viewer.py'), 'required_check_count': 10}

    def git(self, *args):
        return artifacts.git(self.repo, *args)

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')

    def verify(self):
        with patch.object(artifacts, 'inspect_source', return_value=self.source_info):
            return artifacts.verify_bundle(self.folder, self.config, artifacts.input_identity(self.repo),
                                           'example/viewer', self.origin, root=self.repo)

    def client(self, release=None, candidates=None):
        fixture = self

        class Client:
            gh = '/fake/gh'
            calls = []

            def view_release(self, *args):
                return release

            def api(self, endpoint):
                self.calls.append(endpoint)
                if '/attempts/' in endpoint:
                    return {'jobs': [{'name': n, 'run_attempt': 1, 'conclusion': 'success'}
                                     for n in ('validate', 'windows-build')]}
                if endpoint.endswith('/artifacts/90'):
                    return fixture.asset
                if '/artifacts?' in endpoint:
                    return {'artifacts': candidates if candidates is not None else [fixture.asset]}
                if endpoint.endswith('/runs/70'):
                    return fixture.origin
                raise AssertionError(endpoint)

        return Client()


class TestInputIdentity(Fixture):
    def test_exported_source_bom_and_newlines_keep_separate_verified_hashes(self):
        exported = b'\xef\xbb\xbf' + self.source
        (self.folder / 'viewer.py').write_bytes(exported)
        self.plan['assets'][0].update(bytes=len(exported), sha256=sha256(self.folder / 'viewer.py'))
        atomic_json(self.folder / 'Upload_Plan.json', self.plan)
        self.summary['release_source_sha256'] = sha256(self.folder / 'viewer.py')
        atomic_json(self.folder / 'BUILD_VERIFICATION.json', self.summary)
        self.assertNotEqual(self.summary['release_source_sha256'], self.summary['source_sha256'])
        self.verify()

    def test_only_publication_intent_can_change(self):
        self.config['publish'] = True
        atomic_json(self.repo / 'release.json', self.config)
        self.commit()
        self.assertEqual(artifacts.input_identity(self.repo, check_worktree=True), self.identity)
        original = (self.folder / 'Upload_Plan.json').read_bytes()
        plan = self.verify()
        self.assertTrue(plan['publish'])
        self.assertEqual((self.folder / 'Upload_Plan.json').read_bytes(), original)

    def test_source_dependencies_build_workflow_and_notes_invalidate_reuse(self):
        for name in ('viewer.py', 'requirements.txt', 'build.py', 'workflow.yml', 'notes.md'):
            with self.subTest(name=name):
                self.git('reset', '--hard', self.origin['head_sha'])
                (self.repo / name).write_bytes(b'changed')
                self.commit()
                self.assertNotEqual(artifacts.input_identity(self.repo), self.identity)
                with self.assertRaises(BuildError):
                    self.verify()

    def test_prerelease_change_is_not_publication_only(self):
        self.config['prerelease'] = True
        atomic_json(self.repo / 'release.json', self.config)
        self.commit()
        with self.assertRaises(BuildError):
            self.verify()

    def test_dirty_input_and_line_ending_conversion_refused(self):
        (self.repo / 'requirements.txt').write_bytes(b'pkg==1\r\n')
        with self.assertRaises(BuildError):
            artifacts.input_identity(self.repo, check_worktree=True)

    def test_summary_cannot_claim_different_commit(self):
        self.summary['commit'] = 'b' * 40
        atomic_json(self.folder / 'BUILD_VERIFICATION.json', self.summary)
        with self.assertRaises(BuildError):
            self.verify()

    def test_legacy_or_incomplete_checks_fail_closed(self):
        for key, value in [('schema', 1), ('exe_checks', 9), ('windows_exe_checks_passed', False),
                           ('installer_sha256', '0' * 64), ('environment_files', {})]:
            with self.subTest(key=key):
                summary = dict(self.summary, **{key: value})
                atomic_json(self.folder / 'BUILD_VERIFICATION.json', summary)
                with self.assertRaises(BuildError):
                    self.verify()

    def test_dependency_evidence_and_asset_tampering_refused(self):
        for name in ('BUILD_DEPENDENCIES.txt', 'viewer.zip'):
            with self.subTest(name=name):
                original = (self.folder / name).read_bytes()
                (self.folder / name).write_bytes(b'tampered')
                with self.assertRaises(BuildError):
                    self.verify()
                (self.folder / name).write_bytes(original)


class TestSelection(Fixture):
    def select(self, client, run=''):
        return artifacts.select_artifact(client, 'example/viewer', self.config, self.identity, run)

    def test_same_artifact_selected_on_new_or_failed_job_retry(self):
        with patch.dict(os.environ, {'GITHUB_RUN_ATTEMPT': '9'}):
            self.assertEqual(self.select(self.client({'draft': True}))['artifact_id'], 90)

    def test_public_tag_is_preserved_without_artifact_lookup_or_build(self):
        client = self.client({'draft': False, 'html_url': 'https://example.invalid/release'})
        self.assertEqual(self.select(client)['mode'], 'public')
        self.assertEqual(client.calls, [])

    def test_missing_or_expired_draft_artifact_never_triggers_rebuild(self):
        for candidates in ([], [dict(self.asset, expired=True)]):
            with self.assertRaises(BuildError):
                self.select(self.client({'draft': True}, candidates))

    def test_new_version_can_build_but_explicit_missing_run_cannot(self):
        self.assertEqual(self.select(self.client(candidates=[]))['mode'], 'build')
        with self.assertRaises(BuildError):
            self.select(self.client(candidates=[]), '70')

    def test_ambiguous_builds_require_explicit_run(self):
        with self.assertRaises(BuildError):
            self.select(self.client({'draft': True}, [self.asset, dict(self.asset, id=91)]))
        client = self.client({'draft': True})
        self.assertEqual(self.select(client, '70')['artifact_id'], 90)
        self.assertIn('/actions/runs/70/artifacts?', client.calls[0])

    def test_fork_non_main_or_other_workflow_refused(self):
        for key, value in [('head_branch', 'topic'), ('path', 'other.yml'), ('event', 'pull_request'),
                           ('head_repository', {'full_name': 'other/viewer'})]:
            with self.subTest(key=key):
                original = self.origin[key]
                self.origin[key] = value
                with self.assertRaises(BuildError):
                    self.select(self.client())
                self.origin[key] = original

    def test_original_attempt_jobs_checked_even_when_release_failed(self):
        client = self.client()
        artifacts.verify_jobs(client, 'example/viewer', self.origin, 1)
        self.assertIn('/attempts/1/jobs?', client.calls[0])
        with self.assertRaises(BuildError):
            artifacts.verify_jobs(client, 'example/viewer', self.origin, 2)
        with self.assertRaises(BuildError):
            artifacts.verify_jobs(client, 'example/viewer', self.origin, 3)

    def test_missing_digest_is_not_trusted(self):
        self.asset.pop('digest')
        with self.assertRaises(BuildError):
            self.select(self.client())


class TestRestoreAndPublish(Fixture):
    def test_same_artifact_partial_upload_retry_promotes_only_after_all_checks(self):
        self.plan['publish'] = True
        client = FakeGitHub(self.folder, self.plan, existing=2)
        self.assertFalse(publisher.upload_checked(client, self.plan)['draft'])
        self.assertEqual(sum(c[:2] == ['release', 'upload'] for c in client.commands), 4)
        self.assertEqual(client.created, 0)

    def test_changed_draft_notes_are_not_silently_replaced(self):
        client = FakeGitHub(self.folder, self.plan, existing=6)
        client.release['body'] = 'changed notes'
        with self.assertRaises(BuildError):
            publisher.upload_checked(client, self.plan)
        self.assertEqual(client.commands, [])

    def test_existing_tag_with_other_inputs_is_never_moved(self):
        ref = {'ref': 'refs/tags/v3.13.41', 'object': {'type': 'commit', 'sha': self.origin['head_sha']}}
        client = self.client()
        with patch.object(client, 'api', return_value=[ref]):
            publisher.verify_existing_tag(client, 'example/viewer', 'v3.13.41', self.identity, self.repo)
            (self.repo / 'viewer.py').write_bytes(b'different source')
            self.commit()
            with self.assertRaises(BuildError):
                publisher.verify_existing_tag(client, 'example/viewer', 'v3.13.41',
                                              artifacts.input_identity(self.repo), self.repo)

    def test_new_draft_pins_target_to_verified_commit(self):
        client = object.__new__(GitHubClient)
        client.folder = self.folder
        client.emit = lambda value: None
        fake = FakeGitHub(self.folder, self.plan)
        self.plan['target_commitish'] = self.origin['head_sha']
        with patch.object(client, 'api', return_value=fake.release) as api:
            client.create_draft(self.plan)
        self.assertEqual(api.call_args.kwargs['payload']['target_commitish'], self.origin['head_sha'])
        self.assertTrue(api.call_args.kwargs['payload']['draft'])

    def archive(self):
        path = self.root / 'artifact.zip'
        with zipfile.ZipFile(path, 'w') as output:
            for child in self.folder.iterdir():
                output.write(child, child.name)
        self.asset['digest'] = 'sha256:' + sha256(path)
        return path

    def test_restore_original_bundle_then_promote_without_upload_or_rebuild(self):
        archive = self.archive()
        self.config['publish'] = True
        atomic_json(self.repo / 'release.json', self.config)
        self.commit()
        identity = artifacts.input_identity(self.repo, check_worktree=True)

        def download(command, **kwargs):
            self.assertEqual(command, ['/fake/gh', 'api', 'repos/example/viewer/actions/artifacts/90/zip'])
            kwargs['stdout'].write(archive.read_bytes())

        with patch.object(artifacts.subprocess, 'run', side_effect=download), \
                patch.object(artifacts, 'input_identity', return_value=identity), \
                patch.object(artifacts, 'inspect_source', return_value=self.source_info):
            receipt = artifacts.restore(self.client(), 'example/viewer', '90', self.config, identity, root=self.repo)
            plan = artifacts.verify_bundle(self.repo / 'dist', self.config, identity, 'example/viewer',
                                           receipt['origin'], root=self.repo)
        self.assertEqual(read_json(self.repo / 'dist' / 'Upload_Plan.json')['publish'], False)
        client = FakeGitHub(self.repo / 'dist', plan, existing=6)
        result = publisher.upload_checked(client, plan)
        self.assertFalse(result['draft'])
        self.assertFalse(any(c[:2] == ['release', 'upload'] for c in client.commands))
        self.assertEqual(client.created, 0)

    def test_archive_digest_and_path_traversal_fail_before_extraction(self):
        archive = self.archive()
        target = self.root / 'extracted'
        with self.assertRaises(BuildError):
            artifacts.extract_checked(archive, target, 'sha256:' + '0' * 64)
        self.assertFalse(target.exists())
        with zipfile.ZipFile(archive, 'w') as output:
            output.writestr('../outside', 'bad')
        with self.assertRaises(BuildError):
            artifacts.extract_checked(archive, target, 'sha256:' + sha256(archive))
        self.assertFalse((self.root / 'outside').exists())

    def test_different_remote_build_same_name_never_writes(self):
        for draft in (True, False):
            for mismatch in ('size', 'digest'):
                with self.subTest(draft=draft, mismatch=mismatch):
                    client = FakeGitHub(self.folder, self.plan, draft=draft, existing=6)
                    client.items['viewer.zip'][mismatch] = 999 if mismatch == 'size' else '0' * 64
                    with self.assertRaises(BuildError):
                        publisher.upload_checked(client, self.plan)
                    self.assertEqual(client.commands, [])
                    self.assertEqual(client.created, 0)

    def test_unexpected_remote_asset_is_preserved_and_blocks_publication(self):
        client = FakeGitHub(self.folder, self.plan, existing=6)
        client.items['unexpected.exe'] = dict(name='unexpected.exe')
        with self.assertRaises(BuildError):
            publisher.upload_checked(client, self.plan)
        self.assertEqual(client.commands, [])

    def test_identical_public_release_is_read_only(self):
        self.plan['publish'] = True
        client = FakeGitHub(self.folder, self.plan, draft=False, existing=6)
        self.assertFalse(publisher.upload_checked(client, self.plan)['draft'])
        self.assertEqual(client.commands, [])

    def test_release_becomes_public_before_first_write(self):
        client = FakeGitHub(self.folder, self.plan, existing=6)
        with patch.object(client, 'view_release', return_value=dict(client.release, draft=False)):
            with self.assertRaises(BuildError):
                publisher.upload_checked(client, self.plan)
        self.assertEqual(client.commands, [])

    def test_real_remote_digest_verifier_rejects_size_and_hash_mismatch(self):
        record = self.plan['assets'][0]
        client = object.__new__(GitHubClient)
        client.emit = lambda value: None
        valid = dict(state='uploaded', size=record['bytes'], digest='sha256:' + record['sha256'])
        client.verify_asset('example/viewer', valid, record)
        for asset in (dict(valid, size=999), dict(valid, digest='sha256:' + '0' * 64)):
            with self.assertRaises(BuildError):
                client.verify_asset('example/viewer', asset, record)


if __name__ == '__main__':
    unittest.main()
