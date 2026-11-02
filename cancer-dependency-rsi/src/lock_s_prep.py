"""Scientific-lock preparation (pre-Lock2; NO outcome values).

Builds frozen inputs for the scientific-only external evaluation:
  lock_s/covariates.csv   Layer-A covariates per gene (L_g, AdherentMean reference, |AdherentMean|)
  lock_s/cohort.csv       148 C models, donor IDs, primary/alternate library
  lock_s/presence.json    ID-only presence registry of (sample, library, gene) rows in Table 6
Table 6 is streamed from the quarantined zip; only the sample_ID, gene and library
columns are retained. The LFC column is discarded unread (never converted, stored,
printed or aggregated). An exposure record is appended before streaming.
"""
from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import estimators  # noqa: E402
from ledger import append_record  # noqa: E402

OUT = ROOT / 'lock_s'
ZIP = ROOT / 'data/raw/sanger_figshare/S2_Supplementary_Tables.zip'
T6 = 'supplementary_table_6_revision.csv'


def main() -> int:
    OUT.mkdir(exist_ok=True)
    scopes = json.loads((ROOT / 'data/gene_scopes.json').read_text())
    g207 = list(scopes['confirmatory207'])
    g208 = list(scopes['tmod1_alias208'])
    alias = scopes['alias_map']  # Broad symbol -> Sanger symbol
    cand = json.loads((ROOT / 'data/confirmatory_gene_candidates.json').read_text())['confirmatory_genes']
    assert sorted(cand) == sorted(g207) and len(set(g207)) == 207, 'gene scope mismatch'

    # Layer-A covariates (development data only)
    meta, eff, tidx = estimators.load_dev()
    L = estimators.lability(estimators.format_pairs(meta, eff))
    rows = []
    for g in sorted(set(g208)):
        ref = alias.get(g, g)  # reference-table symbol (TMOD -> TMOD1 per gene_scopes alias_map)
        rows.append({'gene_broad': g, 'gene_sanger': alias.get(g, g), 'in_207': g in g207, 'in_208': True,
                     'L': repr(float(L[g])), 'AdherentMean': repr(float(tidx.loc[ref, 'AdherentMean'])),
                     'base_strength': repr(abs(float(tidx.loc[ref, 'AdherentMean'])))})
    with open(OUT / 'covariates.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    # Cohort (metadata only)
    C = json.loads((ROOT / 'data/split_manifest.json').read_text())['C_external']
    xw = list(csv.DictReader(open(ROOT / 'data/crosswalk_sanger_screened.csv', encoding='utf-8-sig')))
    libs: dict[str, set] = {}
    for r in xw:
        libs.setdefault(r['sample_ID'], set()).add(r['library'])
    coh = []
    for s in C['sample_ids']:
        prim = C['library_rule'][s]
        other = sorted(libs.get(s, set()) - {prim})
        coh.append({'sample_ID': s, 'donor_ID': str(C['sample_to_donor'][s]), 'library_primary': prim,
                    'library_alternate': other[0] if other else ''})
    with open(OUT / 'cohort.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(coh[0])); w.writeheader(); w.writerows(coh)

    # ID-only presence registry
    append_record(ROOT / 'data/exposure_log.jsonl', {
        'actor': 'lock_s_prep.py', 'operation': 'table6_id_columns_only_stream', 'partition': 'C_quarantined',
        'path': f'{ZIP.relative_to(ROOT)}::{T6}', 'outcome_values_decoded': False,
        'purpose': 'pre-Lock2 presence registry (sample_ID, gene, library) for missing-cell rule; LFC column discarded unread',
        'authorization': 'user approved scientific-only track 2026-10-28T17:08 local'})
    samples = {r['sample_ID'] for r in coh}
    sanger_genes = {alias.get(g, g) for g in g208} | set(g208)
    present: dict[str, dict[str, list]] = {}
    header = None
    libvals: dict[str, int] = {}
    with zipfile.ZipFile(ZIP) as z, z.open(T6) as raw:
        rd = csv.reader(io.TextIOWrapper(raw, encoding='utf-8'), delimiter=' ')
        header = next(rd)
        i_s, i_g, i_l = header.index('sample_ID'), header.index('gene'), header.index('library')
        for row in rd:
            lib = row[i_l]
            libvals[lib] = libvals.get(lib, 0) + 1
            s, g = row[i_s], row[i_g]
            if s in samples and g in sanger_genes:
                present.setdefault(s, {}).setdefault(lib, []).append(g)
            del row  # LFC field never accessed
    reg = {'header': header, 'library_row_counts': libvals, 'samples_found': len(present),
           'per_sample': {s: {lib: sorted(set(v)) for lib, v in d.items()} for s, d in sorted(present.items())}}
    # summarize completeness for primary/alternate libraries
    miss_primary, miss_alt, dup = {}, {}, {}
    for c in coh:
        d = reg['per_sample'].get(c['sample_ID'], {})
        for lib, store in ((c['library_primary'], miss_primary), (c['library_alternate'], miss_alt)):
            if not lib:
                continue
            have = set(d.get(lib, []))
            m = sorted(g for g in g207 if alias.get(g, g) not in have)
            if m:
                store[c['sample_ID']] = m
        for lib, v in present.get(c['sample_ID'], {}).items():
            if len(v) != len(set(v)):
                dup[f"{c['sample_ID']}|{lib}"] = len(v) - len(set(v))
    tm = alias.get('TMOD', 'TMOD1')
    reg['summary'] = {'missing_207_primary': miss_primary, 'missing_207_alternate': miss_alt,
                      'duplicate_rows': dup,
                      'tmod1_present_primary': sum(tm in reg['per_sample'].get(c['sample_ID'], {}).get(c['library_primary'], []) for c in coh)}
    (OUT / 'presence.json').write_text(json.dumps(reg, indent=1))
    print(json.dumps({'header': header, 'libs': libvals, 'samples_found': len(present),
                      'n_missing_primary': len(miss_primary), 'n_missing_alt': len(miss_alt),
                      'dups': len(dup), 'tmod1_present_primary': reg['summary']['tmod1_present_primary'],
                      'n_dual': sum(bool(c['library_alternate']) for c in coh)}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
