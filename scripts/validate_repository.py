"""Static repository checks: no GUI, installation or network is needed."""
from __future__ import annotations
import ast
import base64
from pathlib import Path
import tempfile
import zlib
from ci_common import ROOT, release_config
from prepare_compliance import restore_metadata, source_records


def validate_backend_copies(source: str) -> None:
    """The lazy PDF worker carries its own backend; it must receive the fix too."""
    tree=ast.parse(source)
    def embedded(module,name):
        node=next(n for n in module.body if isinstance(n,ast.Assign) and
                  any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
        return ast.literal_eval(node.value)
    worker=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_viewer_fast_pdf_worker')
    calls=[n for n in ast.walk(worker) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
           and n.func.attr=='b85decode' and n.args and isinstance(n.args[0],ast.Constant)]
    if len(calls)!=1:raise ValueError('The independently bundled PDF backend could not be identified')
    capsule=zlib.decompress(base64.b85decode(ast.literal_eval(calls[0].args[0]))).decode('utf-8')
    compile(capsule,'PDF compatibility capsule','exec');inner=ast.parse(capsule)
    for name in ('_VIEWER_PDF_ENGINE_SOURCE','_VIEWER_PDF_EDIT_SOURCE'):
        compile(embedded(inner,name),name+':compat','exec')
    helpers={'_font_code_size','_font_width_table'}
    def functions(code):
        return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(code).body
                if isinstance(n,ast.FunctionDef) and n.name in helpers}
    expected=functions(embedded(tree,'_VIEWER_PDF_EDIT_SOURCE'))
    actual=functions(embedded(inner,'_VIEWER_PDF_EDIT_SOURCE'))
    if set(expected)!=helpers or expected!=actual:
        raise ValueError('Main and independently bundled PDF font-edit helpers differ')


def main() -> None:
    config = release_config()
    for directory in (ROOT / 'scripts', ROOT / 'tests', ROOT / 'tools' / 'build'):
        for path in directory.glob('*.py'):
            compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')
    source = ROOT / config['source']; text=source.read_text(encoding='utf-8-sig');tree = ast.parse(text)
    validate_backend_copies(text)
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
