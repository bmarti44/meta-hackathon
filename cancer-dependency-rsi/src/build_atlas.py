"""Deterministic pre-Lock1 evidence inventory from Layer A; no hypothesis selection.

A provisional atlas is not a discovery, equivalence test, or policy result.
All reported environmental changes are in released Chronos units. Missing
inferential and external evidence is recorded rather than imputed.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import resource
import time
import numpy as np
import pandas as pd
import estimators
from ledger import append_record, sha256_file

ROOT = Path(__file__).resolve().parent.parent


def paired_observations(meta, effects, panel):
    rows = []
    for axis, treatment, held, a, b in [
        ('format', 'Growth Format', 'Culture medium', 'Dome', 'Plastic'),
        ('medium', 'Culture medium', 'Growth Format', 'OPAC', 'RPMI/FBS'),
    ]:
        for (model, fixed), group in meta.groupby(['DepMap ID', held], sort=True):
            arm_a, arm_b = group[group[treatment] == a], group[group[treatment] == b]
            if len(arm_a) != 1 or len(arm_b) != 1:
                continue
            sa, sb = arm_a.cell_line_name.iloc[0], arm_b.cell_line_name.iloc[0]
            for gene in panel:
                va, vb = float(effects.loc[sa, gene]), float(effects.loc[sb, gene])
                if not np.isfinite([va, vb]).all():
                    raise ValueError(f'nonfinite original paired values: {gene}/{model}/{axis}')
                rows.append({'gene':gene,'axis':axis,'model_id':model,'held_condition':fixed,
                    'condition_a':a,'condition_b':b,'screen_a':sa,'screen_b':sb,
                    'score_a':va,'score_b':vb,'delta_a_minus_b':va-vb,
                    'measurement_system':'Chronos','donor_id':'unresolved',
                    'evidence_status':'observed_paired_bundle_change_no_inference'})
    return pd.DataFrame(rows)


def summaries(pairs, axis):
    subset = pairs[pairs.axis == axis]
    # Every model contributes equally, even when it has two measured pairs.
    per = subset.assign(abs_delta=subset.delta_a_minus_b.abs()).groupby(['gene','model_id'], sort=True).agg(
        score_a=('score_a','mean'),score_b=('score_b','mean'),delta=('delta_a_minus_b','mean'),
        abs_delta=('abs_delta','mean'))
    out = {}
    for gene, group in per.groupby(level='gene', sort=True):
        measured = subset[subset.gene == gene]
        out[gene] = {
            f'{axis}_n_models':len(group), f'{axis}_n_pairs':len(measured),
            f'{axis}_n_verified_donors':None,
            f'{axis}_mean_score_a':float(group.score_a.mean()),
            f'{axis}_mean_score_b':float(group.score_b.mean()),
            f'{axis}_mean_delta_a_minus_b':float(group.delta.mean()),
            f'{axis}_observed_lability':float(group.abs_delta.mean()),
            f'{axis}_min_paired_delta':float(measured.delta_a_minus_b.min()),
            f'{axis}_max_paired_delta':float(measured.delta_a_minus_b.max()),
            f'{axis}_both_delta_signs_observed':bool((measured.delta_a_minus_b > 0).any() and (measured.delta_a_minus_b < 0).any()),
            f'{axis}_mean_score_a_le_minus_0_5':bool(group.score_a.mean() <= -0.5),
            f'{axis}_mean_score_b_le_minus_0_5':bool(group.score_b.mean() <= -0.5),
        }
    return out


def build(root=ROOT):
    meta, effects, reference = estimators.load_dev()
    library = pd.read_csv(root/'data/raw/broad_figshare/minipool_library_composition.csv')
    panel = sorted(library.loc[library['All test genes'] == True, 'Gene'])
    if len(panel) != 250 or len(set(panel)) != 250:
        raise ValueError('panel must contain exactly 250 unique released test genes')
    scopes = json.loads((root/'data/gene_scopes.json').read_text())
    exclusions = json.loads((root/'data/selection_exclusions.json').read_text())
    tier_a = set(exclusions['tierA_direct_outliers_excluded'])
    schema = json.loads((root/'data/sanger_table6_schema.json').read_text())
    missing_external = set(schema['panel250_missing'])
    observed = paired_observations(meta,effects,panel)
    by_axis = {axis:summaries(observed,axis) for axis in ('format','medium')}
    classes = [c for c in library if c not in {'Gene','All test genes'}]
    lib = library.set_index('Gene')
    rows = []
    for gene in panel:
        primary_reasons = []
        if gene in tier_a: primary_reasons.append('Tier-A_outcome_informed_selection_exclusion')
        if gene == 'TMOD': primary_reasons.append('TMOD_alias_unadjudicated_primary')
        mapped = scopes.get('alias_map',{}).get(gene,gene)
        if mapped not in reference.index:
            primary_reasons.append('missing_Broad_reference_symbol')
        elif float(reference.loc[mapped,'AdherentN']) < 400:
            primary_reasons.append('Broad_reference_AdherentN_lt_400')
        primary = gene in scopes['primary216']
        if primary == bool(primary_reasons):
            raise ValueError(f'primary membership/reason disagreement: {gene}')
        confirm_reasons = list(primary_reasons)
        if gene in missing_external:
            confirm_reasons.append('missing_exact_symbol_in_Sanger_Table6_schema')
        confirm = gene in scopes['confirmatory207']
        if confirm == bool(confirm_reasons):
            raise ValueError(f'confirmatory membership/reason disagreement: {gene}')
        row = {'gene':gene,'panel_member':True,'development_primary_eligible':primary,
            'confirmatory_eligible':confirm,'development_exclusion_reasons':';'.join(primary_reasons),
            'confirmatory_exclusion_reasons':';'.join(confirm_reasons),
            'published_library_classes':';'.join(c for c in classes if bool(lib.loc[gene,c])),
            'prior_knowledge_status':'author_library_classification_only_not_gene_specific_novelty_audit',
            'environment_evidence':'paired_bundle_measurements_exploratory',
            'environment_uncertainty':'unresolved_donor_identity_and_inadequate_legacy_interval_no_inferential_CI',
            'heterogeneity_interpretation':'signs_and_ranges_descriptive_only_controls_also_flip',
            'dependency_interpretation':'condition_mean_threshold_flags_descriptive_not_confirmed_vulnerability',
            'biomarker_evidence':'not_evaluated',
            'external_transfer_evidence':'not_evaluated_Lock2_quarantine',
            'external_contradiction':'not_evaluated',
            'invariance_equivalence_evidence':'not_evaluated_no_invariance_claim',
            'causal_mechanism_evidence':'not_identified',
            'atlas_status':'PROVISIONAL_PRELOCK1_NOT_A_DISCOVERY'}
        for axis in by_axis:
            row.update(by_axis[axis][gene])
        rows.append(row)
    return pd.DataFrame(rows), observed


def write(output:Path, root=ROOT):
    if output.exists():
        raise RuntimeError('immutable atlas output exists; choose a new explicit version')
    output.mkdir(parents=True)
    start=time.monotonic()
    atlas, observations=build(root)
    atlas.to_csv(output/'genes.csv',index=False,float_format='%.12g')
    observations.to_csv(output/'paired_observations.csv',index=False,float_format='%.12g')
    (output/'exclusions.csv').write_text(atlas.loc[~atlas.confirmatory_eligible,
        ['gene','development_primary_eligible','confirmatory_eligible','development_exclusion_reasons','confirmatory_exclusion_reasons']].to_csv(index=False))
    usage=resource.getrusage(resource.RUSAGE_SELF)
    inputs=['data/raw/broad_figshare/minipool_screen_metadata.csv',
        'data/raw/broad_figshare/minipool_chronos_gene_effects.csv',
        'data/raw/broad_figshare/minipool_library_composition.csv',
        'data/raw/broad_figshare/organoids_vs_2d_gene_dependency_tests_full.csv',
        'data/gene_scopes.json','data/selection_exclusions.json','data/sanger_table6_schema.json']
    report={'status':'PROVISIONAL_PRELOCK1','panel_genes':len(atlas),
        'development_primary_genes':int(atlas.development_primary_eligible.sum()),
        'confirmatory_genes':int(atlas.confirmatory_eligible.sum()),
        'confirmatory_excluded_genes':int((~atlas.confirmatory_eligible).sum()),
        'observation_rows':len(observations),
        'contrasts_by_axis':{a:{'models':int(g.model_id.nunique()),'pairs':int(g[['model_id','held_condition']].drop_duplicates().shape[0])} for a,g in observations.groupby('axis')},
        'external_outcome_values_accessed':False,'valid_inferential_claims':0,
        'uncertainty':'not_identified_by_this_inventory',
        'wall_s':time.monotonic()-start,'cpu_s':usage.ru_utime+usage.ru_stime,'peak_rss_bytes':usage.ru_maxrss,
        'input_hashes':{p:sha256_file(root/p) for p in inputs},
        'code_hashes':{p:sha256_file(root/p) for p in ['src/build_atlas.py','src/estimators.py']},
        'output_hashes':{p.name:sha256_file(p) for p in sorted(output.glob('*.csv'))}}
    (output/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    append_record(root/'ledger/experiments.jsonl',{'kind':'provisional_atlas_inventory','artifact':str(output),
        'manifest_sha256':sha256_file(output/'manifest.json'),'wall_s':report['wall_s'],
        'cpu_s':report['cpu_s'],'peak_rss_bytes':report['peak_rss_bytes'],
        'optimization':False,'external_outcome_values_accessed':False})
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    print(json.dumps(write(p.parse_args().output),indent=2))
