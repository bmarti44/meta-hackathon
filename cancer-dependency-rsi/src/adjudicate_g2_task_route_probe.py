"""Apply the frozen verdict rules of g2-task-route-probe-v1 to the retained probe output (no network)."""
import hashlib, json, shutil
from pathlib import Path
ROOT = Path('/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi')
out = ROOT / 'reviews/g2_task_route_probe_v1.json'
raw_copy = ROOT / 'data/route_probe_26q3_v1/probe_raw_output.json'
raw = out.read_bytes()
if not raw_copy.exists():
    shutil.copyfile(out, raw_copy)
assert raw_copy.read_bytes() == raw
r = json.loads(raw)
assert 'verdict' not in r
r['probe_raw_output'] = {'file': 'data/route_probe_26q3_v1/probe_raw_output.json', 'sha256': hashlib.sha256(raw).hexdigest()}
r['requirements_table'] = {
    'primary_route_staff_post': {'status': 'SUPPORTED', 'evidence': 'post 7 by pmontgom: staff=true, admin=true, moderator=true, 2026-10-14 (R1, sha256 in R1_saved)'},
    'release_manifest_26Q3': {'status': 'UNRESOLVED', 'evidence': 'R2 official portal manifest https://depmap.org/portal/api/download/files returned HTTP 200 text/html (4,842 B) instead of CSV; guard stopped, no bypass, no identical retry'},
    'fallback_NextGen_Model_Manuscript_2026': {'status': 'INELIGIBLE_AS_INDEPENDENT_ROUTE', 'evidence': 'staff post 7 states the temporary dataset was removed and its screens were reprocessed into 26Q3; its screens are the manuscript screens (S0: 109 organoid screened models, 2DO 14 + 3DO 95) whose aggregate organoid outcomes are already used in Layer A (E5). R5 publication-declared data_page also served HTML.'},
    'E1_organoid_models_with_26Q3_crispr': {'status': 'UNRESOLVED', 'evidence': 'Model.csv/screen map not retrievable; staff post 6 documents GrowthPattern==Dome as the organoid filter in Model.csv'},
    'E2_documented_donor_ids': {'status': 'UNRESOLVED', 'evidence': 'cached manuscript model_metadata.csv has no donor/patient column (S0); 26Q3 Model.csv not retrieved'},
    'E3_E4_overlap_audit_vs_Broad_inputs_and_C': {'status': 'UNRESOLVED', 'evidence': 'requires 26Q3 donor/HCMI/Sanger identifiers; not retrieved'},
    'E5_unexposed_donors': {'status': 'UNRESOLVED_WITH_ADVERSE_AUTHORITATIVE_INDICATION', 'evidence': 'staff post 7: 26Q3 organoid data are the paper\'s new screens "processed with all other CRISPR screens". Reprocessing is not new biological evidence; all 109 manuscript organoid screened models are exposed. Unexposed donors exist only if 26Q3 contains organoid screens beyond the manuscript set, which no retrieved authoritative source documents.'},
    'E6_gene_universe': {'status': 'UNRESOLVED', 'evidence': 'gene-column availability not verifiable without dependency-matrix access (prohibited)'},
    'E7_processing_independence_from_C': {'status': 'UNRESOLVED_WITH_ADVERSE_INDICATION', 'evidence': 'staff post 7 names the dataset "CRISPR (DepMap Public 26Q3+Score, Chronos)": Sanger Project Score screens are jointly processed; whether Sanger organoid (C-cohort) screens enter that fit is undocumented here'},
    'E8_count_floor_80_donors': {'status': 'UNRESOLVED', 'evidence': 'no eligible-donor inventory obtained'}}
r['verdict'] = 'UNRESOLVED'
r['verdict_basis'] = ('Frozen rule: INELIGIBLE requires an authoritative, sufficiently complete 26Q3 inventory (Model.csv AND screen map); '
                      'the official manifest served HTML, so access/coverage/independence remain unknown. Not CANDIDATE_FOUND: no requirement E1-E8 has documented support. '
                      'A verification page does not establish dataset nonexistence.')
r['stop_criterion_met'] = True
r['stop_criterion_detail'] = ('Primary route unresolved within envelope (manifest HTML); single fallback authoritatively removed and consisting of already-exposed manuscript screens. '
                              'Acquisition branch stops; 3 of 6 requests unused and NOT spent on unplanned routes (e.g. 26Q3 announcement post) to preserve the frozen SPEC.')
r['adverse_indications_for_any_future_contract'] = [
    '26Q3 organoid screens are documented as reprocessed manuscript screens -> no new biological donors unless additional organoid screens are separately documented.',
    '26Q3 Chronos fit includes Sanger Score screens -> processing independence from C must be audited before any use.',
    'Panel genes (Tier-A selection) and the fixed 2D ordering source table derive from the manuscript organoid/2D comparison -> the same donors cannot serve as untouched reserved panels.']
r['effects'] = {'G2': 'FAIL (unchanged)', 'lock1_frozen': False, 'outcome_access_authorized': False, 'q': None, 'admissible_for_policy': False}
r['adjudicated_by'] = 'lead executor under frozen SPEC rules; pending independent Sol-high review'
out.write_text(json.dumps(r, indent=1))
print(hashlib.sha256(out.read_bytes()).hexdigest())
