"""Exercise the new PDF export worker in the checked Windows executable."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--exe',help='Optional executable or wrapper for local testing')
args=parser.parse_args()
if args.exe:
    EXE=Path(args.exe)
else:
    build=json.loads((ROOT/'build'/'windows-run'/'Build_Result.json').read_text(encoding='utf-8-sig'))
    if build.get('status')!='passed':raise RuntimeError('The Windows build did not pass')
    EXE=Path(build['exe'])
if not EXE.is_file():
    raise RuntimeError('The checked Windows executable is unavailable')


def run(job, success=True):
    completed = subprocess.run([str(EXE), '--pdf-export-worker'],
        input=(json.dumps(job, ensure_ascii=True)+'\n').encode('ascii'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    messages = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    if success:
        if completed.returncode != 0 or not any(x.get('ready') for x in messages):
            raise RuntimeError('Frozen PDF export failed: '+repr((completed.returncode, messages, completed.stderr[-1000:])))
    elif completed.returncode == 0 or not any(x.get('error') for x in messages):
        raise RuntimeError('Frozen PDF export did not report the missing input')


with tempfile.TemporaryDirectory(prefix='viewer-pdf-export-exe-') as directory:
    root=Path(directory);source=root/'source.pdf';writer=PdfWriter()
    for i in range(20):writer.add_blank_page(width=500+i,height=700)
    with source.open('wb') as stream:writer.write(stream)
    order=[17,0,13,17,4]
    job={'pages':[(str(source),n) for n in order], 'directory':str(root),
         'stem':'combined','separate':False}
    run(job)
    output=PdfReader(root/'combined.pdf')
    if [int(page.mediabox.width) for page in output.pages] != [517,500,513,517,504]:
        raise RuntimeError('Frozen combined PDF page order differs')
    run({**job,'stem':'separate','separate':True})
    files=[root/f'separate_{i+1:03d}.pdf' for i in range(len(order))]
    if [int(PdfReader(path).pages[0].mediabox.width) for path in files] != [517,500,513,517,504]:
        raise RuntimeError('Frozen separate PDF page order differs')
    run({**job,'pages':[(str(root/'missing.pdf'),0)],'stem':'missing'},success=False)
    if (root/'missing.pdf').exists():raise RuntimeError('Frozen failed export left an output')
print('PDF export worker passed: combined, separate, failure')
