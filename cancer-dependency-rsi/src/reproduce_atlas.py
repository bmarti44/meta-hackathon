"""Reproduce only the provisional atlas in an isolated source/input directory.

Uses the current locked environment, not a clean-room project installation.
No external outcome file is copied. This is protocol separation, not a
filesystem sandbox; the subprocess still has the host's normal read access.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from ledger import append_record,sha256_file

ROOT=Path(__file__).resolve().parent.parent


def reproduce(original:Path,report:Path):
    if report.exists():raise RuntimeError('immutable reproduction report exists')
    manifest=json.loads((original/'manifest.json').read_text())
    # Refuse to bless an altered retained atlas or changed source bytes.
    for name,digest in manifest['output_hashes'].items():
        if sha256_file(original/name)!=digest:raise ValueError(f'retained output tampered: {name}')
    frozen_sources={}
    for name,digest in {**manifest['input_hashes'],**manifest['code_hashes']}.items():
        source=ROOT/name
        if sha256_file(source)!=digest:
            retained=ROOT/'artifacts/sha256'/digest
            if name not in manifest['code_hashes'] or not retained.is_file() or sha256_file(retained)!=digest:
                raise ValueError(f'input/code changed without retained frozen bytes: {name}')
            source=retained
        frozen_sources[name]=source
    start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='cdrsi-atlas-reproduce-') as temp:
        clean=Path(temp)
        for rel in [*manifest['input_hashes'],*manifest['code_hashes'],'src/ledger.py']:
            target=clean/rel;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(frozen_sources.get(rel,ROOT/rel),target)
        out=clean/'out'
        env=__import__('os').environ.copy()
        env.pop('PYTHONPATH',None)
        proc=subprocess.run([sys.executable,str(clean/'src/build_atlas.py'),'--output',str(out)],
            cwd=clean,env=env,capture_output=True,text=True,timeout=60)
        if proc.returncode:
            raise RuntimeError(proc.stderr[-2000:])
        observed={name:sha256_file(out/name) for name in manifest['output_hashes']}
        result={'status':'PASS' if observed==manifest['output_hashes'] else 'FAIL',
            'scope':'provisional_atlas_component_only_not_C11_full_campaign',
            'isolated_source_and_input_copy':True,'clean_environment_installation':False,
            'external_outcome_files_copied':False,'filesystem_sandboxed':False,'stochastic_model_calls':0,
            'original_output_hashes':manifest['output_hashes'],'reproduced_output_hashes':observed,
            'python_executable':sys.executable,'python_version':sys.version,
            'requirements_lock_sha256':sha256_file(ROOT/'requirements-lock.txt'),
            'uv_lock_sha256':sha256_file(ROOT/'uv.lock'),'wall_s':time.monotonic()-start}
    report.write_text(json.dumps(result,indent=2)+'\n')
    append_record(ROOT/'ledger/experiments.jsonl',{'kind':'component_reproduction','artifact':str(report),
        'sha256':sha256_file(report),'status':result['status'],'scope':result['scope'],
        'wall_s':result['wall_s'],'stochastic_model_calls':0})
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--atlas',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();r=reproduce(a.atlas,a.report);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='PASS' else 1)
