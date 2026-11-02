"""sgen009 traceability v7: occurrence-bound claim validation.

Every claim parses LABELED occurrences in the manuscript (not substring presence):
- primary estimate: every 'ρ = X' occurrence must equal the locked displayed value;
- intervals: every bracketed [lo, hi] occurrence must be ordered and equal the locked pair;
- secondaries: label-bound values (null-calibrated/TMOD-alias/alternate-library/unadjusted);
- counts: whole-token matches (\\bN\\b) so 2070 cannot masquerade as 207.
Each claim records manuscript line numbers, artifact path + field + sha256.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ledger import sha256_file  # noqa: E402

EXT = 'lock_s/results/external_v1.json'
ELIG = 'generations/pgen003/eligibility_recompute_v1.json'
AMAN = 'atlas/v4/manifest.json'


def _f(obj, dotted):
    cur = obj
    for part in dotted.split('.'):
        cur = cur[int(part)] if part.isdigit() else cur[part]
    return cur


def _clean(tok: str) -> str:
    # strip AT MOST ONE trailing punctuation character (repeated punctuation stays and fails NUM)
    return tok[:-1] if tok and tok[-1] in '.,;:)' else tok


def _disp(v, dec):
    return f'{round(float(v), dec):.{dec}f}' if dec else str(int(v))


NUM = r'-?\d+(?:\.\d+)?(?:e-?\d+)?'


def validate(text: str, ext: dict, elig: dict, aman: dict) -> dict:
    text = text.replace('−', '-').replace('–', '-').replace('…', '...')
    lines = text.splitlines()
    out = {}

    def lines_of(needle):
        return [i + 1 for i, ln in enumerate(lines) if needle in ln]

    def occ(name, values, expected):
        out[name] = {'occurrences': values, 'expected': expected,
                     'matches': bool(values) and all(v == expected for v in values)}

    # rho: EVERY rho symbol must be followed by a complete valid token equal to expected
    rho_positions = [m.start() for m in re.finditer('ρ', text)]
    rho_vals = []
    rho_ok = bool(rho_positions)
    for pos in rho_positions:
        m = re.match(r'ρ\s*=\s*(\S+)', text[pos:])
        if not m:
            rho_ok = False
            rho_vals.append('<malformed>')
            continue
        tok = _clean(m.group(1))
        if not re.fullmatch(NUM, tok):
            rho_ok = False
        rho_vals.append(tok)
    occ('rho-primary', rho_vals, _disp(ext['primary']['estimate'], 3))
    out['rho-primary']['matches'] = bool(out['rho-primary']['matches'] and rho_ok)
    out['rho-primary']['manuscript_lines'] = lines_of('ρ')
    out['rho-primary']['artifact'] = f"{EXT}:primary.estimate"
    # intervals: every bracket pair with numeric content must parse fully, be ordered, equal expected
    elo, ehi = (_disp(ext['primary']['ci95_donor_percentile'][0], 3),
                _disp(ext['primary']['ci95_donor_percentile'][1], 3))
    ivals, iv_ok = [], True
    for m in re.finditer(r'\[', text):
        end = text.find(']', m.start())
        seg = text[m.start():end + 1] if end > 0 else text[m.start():m.start() + 40]
        mm = re.fullmatch(r'\[(' + NUM + r'),\s*(' + NUM + r')\]', seg)
        if mm:
            ivals.append([mm.group(1), mm.group(2)])
            if not float(mm.group(1)) < float(mm.group(2)):
                iv_ok = False
        elif ',' in seg:
            iv_ok = False  # comma-bearing bracket that is not an exact interval: reject (incl NaN/[,])
    out['primary-interval'] = {'occurrences': ivals, 'expected': [elo, ehi],
                               'matches': bool(ivals) and iv_ok and all(x == [elo, ehi] for x in ivals),
                               'artifact': f'{EXT}:primary.ci95_donor_percentile'}
    for label, field in (('null-calibrated', 'S1_null_calibrated'), ('TMOD-alias', 'S2_tmod1_alias208'),
                         ('alternate-library', 'S3_v1_1_dual_library'), ('unadjusted', 'S4_unadjusted')):
        _toks = []
        for _m in re.finditer(re.escape(label), text):
            _mm = re.match(r'\s+(\S+)', text[_m.end():])
            _toks.append(_clean(_mm.group(1)) if _mm else '<missing-token>')
        _toks = [x if re.fullmatch(NUM, x) else '<invalid:' + x + '>' for x in _toks]
        occ(label, _toks,
            _disp(ext['secondary_holm_family'][field]['estimate'], 3))
        out[label]['artifact'] = f'{EXT}:secondary_holm_family.{field}.estimate'
        out[label]['manuscript_lines'] = lines_of(label)
    lomo = ext['stability_not_decision']['leave_one_model_out']
    occ('lomo-range', re.findall(r'\((' + NUM + r')\.\.\.', text), _disp(min(lomo.values()), 3))
    out['lomo-range']['artifact'] = f'{EXT}:stability_not_decision.leave_one_model_out (min/max)'
    occ('lomo-range-hi', re.findall(r'\.\.\.(' + NUM + r')\)', text), _disp(max(lomo.values()), 3))
    # context-bound counts: every labeled occurrence must match
    ctx = [('genes-207', r'(?:fixed |within the )(\S+?)-gene', str(ext['primary']['n_fixed_genes']), f'{EXT}:primary.n_fixed_genes'),
           ('genes-207-coords', r'(\S+) with external displacement', str(ext['primary']['n_fixed_genes']), f'{EXT}:primary.n_fixed_genes'),
           ('models-148', r'\((\S+) models,| (\S+) Sanger organoid models|(\S+) models =', str(ext['primary']['n_models_analyzed']), f'{EXT}:primary.n_models_analyzed'),
           ('patients-142', r'(?:to |/ |= \*\*)(\S+) patients', str(elig['c_patients_full']), f'{ELIG}:c_patients_full'),
           ('panel-250', r'(\S+?)(?:-gene evidence| panel genes| selected genes|-gene panel \(outcome)', str(aman['panel_genes']), f'{AMAN}:panel_genes'),
           ('archived-144', r'(\S+) covariate', str(ext['primary']['n_donors_analyzed']), f'{EXT}:primary.n_donors_analyzed')]
    for name, pat, exp, art in ctx:
        _vals = [next(g for g in m if g) if isinstance(m, tuple) else m for m in re.findall(pat, text)]
        _vals = [v for v in _vals if any(ch.isdigit() for ch in v)]  # numeric assertions only; word tokens are prose
        occ(name, _vals, exp)
        out[name]['artifact'] = art
    occ('atlas-fdr-format-7', re.findall(r'\((\d+) and 8 FDR', text), str(aman['annotation_counts']['S1_format_FDR<0.05']))
    occ('atlas-fdr-serum-8', re.findall(r'and (\d+) FDR', text), str(aman['annotation_counts']['S1_serum_FDR<0.05']))
    return out


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', default='generations/sgen009/traceability_v17.json')
    out_path = ROOT / ap.parse_args().report
    ms = (ROOT / 'manuscript/manuscript_draft_v1.md').read_text()
    ext = json.loads((ROOT / EXT).read_text())
    elig = json.loads((ROOT / ELIG).read_text())
    aman = json.loads((ROOT / AMAN).read_text())
    text = ms.replace('−', '-').replace('–', '-')
    claims = validate(text, ext, elig, aman)
    neg = {}
    for name, bad in (('wrong_abstract_estimate', text.replace('ρ = -0.146', 'ρ = -0.999', 1)),
                      ('swapped_secondary_labels', text.replace('null-calibrated -0.209', 'null-calibrated -0.217').replace('unadjusted -0.217', 'unadjusted -0.209')),
                      ('reversed_interval', text.replace('[-0.175, -0.114]', '[-0.114, -0.175]')),
                      ('token_2070', text.replace('207-gene panel', '2070-gene', 1)),
                      ('abstract_count_999', text.replace('142 patients post-lock', '999 patients post-lock', 1)),
                      ('rho_integer_syntax', text.replace('ρ = -0.146,', 'ρ = 1,', 1)),
                      ('count_comma_escape', text.replace('(148 models,', '(1,480 models,', 1)),
                      ('count_exponent_escape', text.replace('fixed 207-gene', 'fixed 2.07e3-gene', 1)),
                      ('rho_approx_escape', text.replace('ρ = -0.146 [', 'ρ ≈ -0.999 [', 1)),
                      ('secondary_suffix_escape', text.replace('null-calibrated -0.209', 'null-calibrated -0.209oops', 1))):
        try:
            neg[name] = not all(v['matches'] for v in validate(bad, ext, elig, aman).values())
        except Exception:
            neg[name] = True
    inv = {}
    for rel, runner in (('manuscript/figures/figure1_primary.svg', 'src/make_figure1.py'),
                        ('atlas/v4/genes.csv', 'src/build_atlas_v4.py + atlas/v4/manifest.json'),
                        ('atlas/v4/exclusions.csv', 'src/build_atlas_v4.py + atlas/v4/manifest.json'),
                        ('atlas/v4/paired_observations.csv', 'src/build_atlas_v4.py + atlas/v4/manifest.json'),
                        ('reviews/c10_robustness_table_v1.md', 'manual from lock_s/results/external_v1.json; verified src/sgen008_checks.py')):
        inv[rel] = {'sha256': sha256_file(ROOT / rel), 'runner_or_provenance': runner}
    report = {'claims': claims, 'negative_fixtures_rejected': neg,
              'artifact_hashes': {EXT: sha256_file(ROOT / EXT), ELIG: sha256_file(ROOT / ELIG), AMAN: sha256_file(ROOT / AMAN)},
              'inventory': inv, 'reproduction_report_of_record': 'generations/sgen002/reproduction_report_v3.json',
              'pass': bool(all(v['matches'] for v in claims.values()) and all(neg.values()))}
    with open(out_path, 'x') as fh:
        fh.write(json.dumps(report, indent=1))
    print(json.dumps({'pass': report['pass'], 'neg': neg,
                      'bad': [k for k, v in claims.items() if not v['matches']]}, indent=1))
    return 0 if report['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
