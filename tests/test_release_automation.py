from __future__ import annotations
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import ci_common
import prepare_compliance as compliance
import publish_release as publisher
from build_common import BuildError, atomic_json
from github_release import load_prepared_release, release_notes


class FakeResponse(io.BytesIO):
    def geturl(self):return 'https://download.qt.io/source.xz'


class TestConfigAndCompliance(unittest.TestCase):
    def test_version_matches_real_source_and_publication_is_explicit(self):
        config=ci_common.release_config(ROOT)
        self.assertEqual(config['version'], '3.13.41'); self.assertIs(type(config['publish']),bool)
    def test_manual_false_is_not_treated_as_true(self):
        self.assertFalse(ci_common.release_config(ROOT, 'false')['publish'])
        self.assertTrue(ci_common.release_config(ROOT, 'true')['publish'])
        with self.assertRaises(BuildError):ci_common.release_config(ROOT, '1')
    def test_paths_stay_in_repository(self):
        for name in ('../outside', '/absolute', 'a\\b'):
            with self.assertRaises(BuildError):ci_common.inside(ROOT,name)
    def test_all_preserved_notice_bytes_restore(self):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)
            compliance.restore_metadata(ROOT/'tools/build/compliance_metadata.json', target)
            self.assertTrue((target/'NOTICES_KO.txt').is_file())
            self.assertEqual(len(compliance.source_records(target)),5)
            self.assertGreater(len([p for p in target.rglob('*') if p.is_file()]),300)
    def test_corrupt_metadata_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp);record=json.loads((ROOT/'tools/build/compliance_metadata.json').read_text())
            record['sha256']='0'*64;(p/'bad.json').write_text(json.dumps(record))
            with self.assertRaises(BuildError):compliance.restore_metadata(p/'bad.json',p/'out')
    def archive_record(self,data):
        return {'path':'OpenSource_Sources/source.xz','source_url':'https://download.qt.io/source.xz',
                'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    def test_archive_size_hash_and_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            data=b'checked source';record=self.archive_record(data);opened=[]
            def open_source(*args,**kwargs):opened.append(1);return FakeResponse(data)
            path=compliance.download_source(Path(temp),record,open_source)
            self.assertEqual(path.read_bytes(),data)
            compliance.download_source(Path(temp),record,open_source);self.assertEqual(opened,[1])
    def test_changed_archive_not_committed(self):
        with tempfile.TemporaryDirectory() as temp:
            data=b'good source';record=self.archive_record(data)
            with self.assertRaises(BuildError):
                compliance.download_source(Path(temp),record,lambda *a,**k:FakeResponse(b'bad data'))
            self.assertFalse((Path(temp)/record['path']).exists())
            self.assertEqual(list(Path(temp).rglob('*.part')),[])
    def test_unapproved_archive_origin_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            record=self.archive_record(b'x');record['source_url']='http://unapproved.invalid/source'
            with self.assertRaises(BuildError):compliance.download_source(Path(temp),record)


class FakeGitHub:
    def __init__(self,folder,plan,*,draft=True,existing=0,corrupt=False):
        self.folder=folder;self.plan=plan;self.created=0;self.commands=[];self.verified=[]
        self.release={'id':11,'tag_name':plan['tag'],'draft':draft,'body':plan['notes'],
                      'name':plan['title'],'prerelease':plan['prerelease'],'html_url':'https://github.com/example/viewer/releases/11'}
        self.items={a['name']:dict(name=a['name'],size=a['bytes'],digest=a['sha256']) for a in plan['assets'][:existing]}
        if corrupt:self.items[next(iter(self.items))]['digest']='bad'
        self.existing=existing
    def check(self):pass
    def resume_or_find_release(self,*args):return self.release if self.existing else None
    def create_draft(self,plan):self.created+=1;return self.release
    def remember_release(self,*args):pass
    def assets(self,*args):return list(self.items.values())
    def verify_asset(self,repo,asset,record):
        if asset['size']!=record['bytes'] or asset['digest']!=record['sha256']:raise BuildError('hash mismatch')
        self.verified.append(record['name'])
    def view_release(self,*args,**kwargs):return self.release
    def command(self,args,**kwargs):
        self.commands.append(args)
        if args[:2]==['release','upload']:
            name=Path(args[3]).name
            if name in self.items:raise AssertionError('overwriting an existing asset')
            a=next(x for x in self.plan['assets'] if x['name']==name)
            self.items[name]=dict(name=name,size=a['bytes'],digest=a['sha256'])
        if '--draft=false' in args:
            if len(self.items)!=len(self.plan['assets']):raise AssertionError('publishing before all assets')
            if not all(a['name'] in self.verified for a in self.plan['assets']):raise AssertionError('publishing before verification')
            self.release['draft']=False
        return 0,'',''


class TestCheckedPublication(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.folder=Path(self.temp.name)
        notes=release_notes('3.13.41','v3.13.41','viewer.py','viewer.zip','checked change')
        self.plan={'schema':1,'tool_version':'1.5.10','viewer_version':'3.13.41','repo':'example/viewer',
                   'tag':'v3.13.41','title':'The Viewer 3.13.41','notes':notes,'notes_path':str(self.folder/'RELEASE_NOTES.md'),
                   'folder':str(self.folder),'publish':False,'prerelease':False,'assets':[]}
        for name,data in [('viewer.py',b'source'),('viewer.zip',b'zip'),('VERSION_GUIDE.txt',b'guide'),
                           ('RELEASE_NOTES.md',notes.encode()),('SHA256SUMS.txt',b'sums')]:
            (self.folder/name).write_bytes(data)
            self.plan['assets'].append(dict(name=name,path=str(self.folder/name),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    def test_draft_stays_unpublished(self):
        client=FakeGitHub(self.folder,self.plan)
        result=publisher.upload_checked(client,self.plan)
        self.assertTrue(result['draft']);self.assertEqual(client.created,1)
        self.assertFalse(any('--draft=false' in c for c in client.commands))
    def test_publication_follows_all_asset_checks(self):
        self.plan['publish']=True;client=FakeGitHub(self.folder,self.plan)
        self.assertFalse(publisher.upload_checked(client,self.plan)['draft'])
    def test_partial_draft_resumes_without_overwriting(self):
        client=FakeGitHub(self.folder,self.plan,existing=2)
        publisher.upload_checked(client,self.plan)
        self.assertEqual(client.created,0)
        self.assertEqual(sum(c[:2]==['release','upload'] for c in client.commands),3)
    def test_corrupt_existing_asset_refuses_any_upload(self):
        client=FakeGitHub(self.folder,self.plan,existing=1,corrupt=True)
        with self.assertRaises(BuildError):publisher.upload_checked(client,self.plan)
        self.assertEqual(client.commands,[])
    def test_incomplete_public_release_preserved(self):
        client=FakeGitHub(self.folder,self.plan,draft=False,existing=1)
        with self.assertRaises(BuildError):publisher.upload_checked(client,self.plan)
        self.assertEqual(client.commands,[])
    def test_identical_public_release_needs_no_mutation(self):
        client=FakeGitHub(self.folder,self.plan,draft=False,existing=5)
        publisher.upload_checked(client,self.plan);self.assertEqual(client.commands,[])
    def test_changed_local_file_refuses_any_write(self):
        client=FakeGitHub(self.folder,self.plan);(self.folder/'viewer.zip').write_bytes(b'changed')
        with self.assertRaises(BuildError):publisher.upload_checked(client,self.plan)
        self.assertEqual(client.commands,[]);self.assertEqual(client.created,0)
    def test_downloaded_plan_rebases_windows_paths(self):
        plan=copy.deepcopy(self.plan)
        for a in plan['assets']:a['path']='C:\\old\\'+a['name']
        plan['folder']='C:\\old';plan['notes_path']='C:\\old\\RELEASE_NOTES.md'
        atomic_json(self.folder/'Upload_Plan.json',plan)
        restored=load_prepared_release(self.folder)
        self.assertTrue(all(Path(a['path']).parent==self.folder for a in restored['assets']))
    def test_non_main_workflow_cannot_publish(self):
        with patch.dict(os.environ,{'GITHUB_ACTIONS':'true','GITHUB_REF':'refs/heads/not-main'}):
            with self.assertRaises(BuildError):publisher.main()


if __name__=='__main__':unittest.main()
