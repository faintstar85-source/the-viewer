"""Static repository checks: no GUI, installation or network is needed."""
from __future__ import annotations
import ast
from pathlib import Path
import tempfile
from ci_common import ROOT, release_config
from prepare_compliance import restore_metadata, source_records


def main() -> None:
    config = release_config()
    for directory in (ROOT / 'scripts', ROOT / 'tests', ROOT / 'tools' / 'build'):
        for path in directory.glob('*.py'):
            compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')
    source = ROOT / config['source']; tree = ast.parse(source.read_text(encoding='utf-8-sig'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in
                {'_VIEWER_PDF_ENGINE_SOURCE', '_VIEWER_PDF_EDIT_SOURCE'} for t in node.targets):
            compile(ast.literal_eval(node.value), node.targets[0].id, 'exec')
    with tempfile.TemporaryDirectory() as temp:
        restore_metadata(ROOT / 'tools' / 'build' / 'compliance_metadata.json', Path(temp))
        records = source_records(Path(temp))
        assert len(records) == 5
    print('Repository and pinned build metadata validated:', config['version'])


if __name__ == '__main__':
    main()
