"""Run the preregistered diagnostic; not a research/policy generation."""
import json
import resource
import time
from pathlib import Path
import evaluator_v2
import evaluator_v3
from ledger import append_record, sha256_file
ROOT = Path(__file__).resolve().parent.parent


def main():
    spec = ROOT / 'reviews/prompts/g2_safety_probe_spec_v1.json'
    output = ROOT / 'reviews/g2_safety_probe_results_v1.json'
    if output.exists():
        raise RuntimeError('immutable diagnostic exists; do not repeat on resume')
    episodes = json.loads((ROOT / 'config/episodes.json').read_text())
    start = time.monotonic()
    records = []
    for branch in episodes['pilot_E0']['branches']:
        pair = {'branch_id': branch['branch_id'], 'config': branch['root_config']}
        for name, module in [('retired_v2', evaluator_v2), ('safety_draft_v3', evaluator_v3)]:
            r = module.evaluate(branch['root_config'], seed=20261028)
            pair[name] = {k: r.get(k) for k in ('valid','estimate','null_coverage','q','ci_width','invalid_reasons','admissible_for_policy')}
        records.append(pair)
    # Diagnostic reranking only; neither list may drive selection.
    ranks = {name: [p['branch_id'] for p in sorted(records, key=lambda p: p[name].get('q') or -1, reverse=True) if p[name]['valid']]
             for name in ('retired_v2', 'safety_draft_v3')}
    usage = resource.getrusage(resource.RUSAGE_SELF)
    result = {'spec_sha256': sha256_file(spec), 'records': records, 'diagnostic_rankings': ranks,
              'wall_s': time.monotonic()-start, 'cpu_s': usage.ru_utime+usage.ru_stime,
              'peak_rss_bytes': usage.ru_maxrss, 'status': 'NOT_ADMISSIBLE_FOR_POLICY',
              'scientific_claim': None, 'external_outcomes_accessed': False,
              'code_sha256': {str(p): sha256_file(ROOT/p) for p in ('src/evaluator_v2.py','src/evaluator_v3.py','src/estimators.py')}}
    output.write_text(json.dumps(result, indent=2)+'\n')
    append_record(ROOT/'ledger/experiments.jsonl', {'kind':'readiness_diagnostic','spec_sha256':result['spec_sha256'],
        'artifact':str(output.relative_to(ROOT)), 'artifact_sha256':sha256_file(output),'policy_optimization':False,
        'status':'completed','evaluations':12,'wall_s':result['wall_s'],'cpu_s':result['cpu_s'],'peak_rss_bytes':result['peak_rss_bytes']})
    print(json.dumps({'wall_s':result['wall_s'],'peak_rss_bytes':result['peak_rss_bytes'],'results':records},indent=2))

if __name__ == '__main__':
    main()
