# sgen010 — DepMap 26Q3 metadata discriminator (ledger-first SPEC)

Locked before any probing, 2026-10-29. Inputs are the two user-supplied metadata
files only; neither contains dependency outcomes.

## Inputs (hashes recorded at acquisition)
- data/Model.csv — sha256 65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7 (789,805 bytes; copied from ~/Downloads, source hash identical)
- data/CRISPRScreenMap.csv — sha256 43cc528614053d4c5a96729c2d782375227231a0cfea23de6c519b8989fa1252 (41,721 bytes; copied from ~/Downloads, source hash identical)
- lock_s/cohort.csv (locked; 148 models, donor_ID = COSMIC individual_ID)
- generations/sgen001/identity_reconciliation_v1.json (142 Passports patients authoritative)

## Question
Does DepMap 26Q3 metadata identify a CRISPR-screened model pool that is
(a) countable at patient level (PatientID present), and (b) donor-disjoint from
the 148-model / 142-patient spent external cohort C on every available join key?
If yes, how large is the disjoint screened pool, at model and patient level?

## Method (metadata only; no outcome access)
1. Model.csv: row count, distinct PatientID, GrowthPattern / ModelType /
   DepmapModelType distributions; 3D/organoid-class subset counts.
2. CRISPRScreenMap.csv: screen count, distinct screened ModelID; inner join to
   Model.csv -> screened patients.
3. Donor disjointness vs cohort C on every candidate key present in both:
   cohort donor_ID vs Model COSMICID; cohort model names (from identity
   reconciliation) vs CellLineName/StrippedCellLineName; cohort sample_ID
   prefixes vs any Model identifier column. Report each overlap separately.
   A model counts as C-overlapping if ANY key matches (conservative union).
4. Disjoint screened pool = screened models minus union-overlap models; report
   model count and distinct-patient count. Also report disjoint screened
   patients (a patient is excluded if ANY of their models overlaps C).

## Decision rule (fixed before probing)
- POOL_IDENTIFIED: disjoint screened pool >= 100 models AND >= 100 patients
  (a fresh patient-level biological evaluation is at least structurally
  possible; power/endpoint design is a later generation).
- POOL_TOO_SMALL: otherwise.
Either verdict is a used discriminator result. No outcome file is downloaded,
opened, or referenced by this generation.

## Failure modes named in advance
- Join keys may not connect (DepMap COSMICID is a sample-level ID; cohort
  donor_ID is individual-level): then disjointness rests on name keys only and
  the verdict must say so.
- PatientID missingness in Model.csv shrinks the countable pool.

## Amendment (2026-10-29, before v3 probing)
v1 keys did not connect. v2 Passports HCMI bridge covered 48/148 models
(50/142 patients) -> POOL_IDENTIFIED_BRIDGE_PARTIAL. v3 completes the bridge
locally by reproducing pgen003 Witness A exactly (normalized
model_name+synonyms join of cohort sample_IDs on the same
passports_model_list_20260921.csv; pgen003 reported 148/148 resolved, 142
patients, 0 multi-patient). v3 must independently reproduce those counts
before using the patient set; exclusion then = every Passports model of the
142 C patients (SIDM / BROAD_ID / COSMIC_ID / names) joined to DepMap
Model.csv. Decision rule and thresholds unchanged. No network, no outcomes.

## Amendment v4 (2026-10-29, before v4 probing; responds to sol-high review v1, score 68)
Verified findings adopted: (1) HIGH - screened models with no Passports linkage
are IDENTITY_UNRESOLVED, not proven disjoint; the established pool is restricted
to models resolved to a Passports patient (SIDP) that is not a C patient.
(2) Patient counting reported in both DepMap PatientID and Passports SIDP
spaces; patient-strict exclusion propagates through connected components of
the PatientID<->SIDP bipartite linkage. (3) All input hashes pinned and
enforced (DepMap files, Passports list, locked cohort); Witness-A map pinned
by canonical-mapping sha256, not counts alone. (4) DepmapModelType
distribution added. (5) Wording narrowed to "no dependency-outcome access"
(Model.csv clinical columns parsed by the CSV reader are dropped unused).
(6) Both outputs computed fully, then written. Decision rule unchanged
(>=100 models AND >=100 patients) but now applied to the ESTABLISHED
(resolved, patient-strict) pool; unresolved counts reported as a named
residual, incl. the organoid subset. Corrective ledger entries record that
v1/v2 were disclosed adaptive repairs (v2 bridge preceded its amendment).

## Amendment v5 (2026-10-29, before v5 probing; responds to sol-high re-review v2, score 84, no high/critical)
(1) Identity tiers: strong ID routes (BROAD_ID/SIDM/HCMI/COSMIC, semicolon-
tokenized) define confirmed patient assignment only when unanimous; conflicting
strong routes -> IDENTITY_CONFLICT quarantine. NAME route is candidate evidence
only: never an identity edge, never sufficient for established status, but any
candidate hit on a C patient excludes conservatively. (2) Patient-component
graph built from ALL Model.csv rows using confirmed assignments; classification
checks C-component membership before unresolved. (3) SPEC diagnostics restored
(screen rows, distinct PatientIDs whole-table/screened, per-key C-overlap).
(4) Outputs serialized to temp files then renamed as a pair (rollback on
failure). Decision rule unchanged, applied to established pool (SIDP space).
Review v2 text was recovered from the model-call event stream after the
wrapper's output file was not written; receipt gap recorded in ledger.

## Close-out (lead, 2026-10-29)
POOL_IDENTIFIED on the established (confirmed-identity) basis: 1,106 screened
models / 1,069 confirmed Passports patients (1,068 DepMap PatientIDs), zero
cohort-C overlap on all routes. 253 screened models identity-unresolved and 2
name-only are excluded, incl. organoids 11 established / 97 not established
(named residual: organoid disjointness NOT established by this screen).
Sol-high arc 68 -> 84 -> 90 (v5, zero high/critical). v6/v7 fix the v3-review
medium (C-component candidate evidence) and three write-pair lows; counts
identical; 8 focused tests in tests/test_sgen010_v5.py. Re-review completed 2026-10-29 after user-authorized allocation increase: v7 scored 92 (0 medium/high/critical; 4 low residuals: write_pair adversarial race windows + failure-path test coverage - accepted, single-writer context).
