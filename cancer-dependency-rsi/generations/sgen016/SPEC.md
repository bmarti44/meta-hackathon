# sgen016 — Sanger derivation-matched patient/raw-input manifest feasibility probe
(manifests and documentation ONLY; zero count-value access; sol-xhigh Rank-1 target, reviews/xhigh_next_targets_v2.md)

## Question
Do public manifests connect, unambiguously: (a) genuine patients, (b)
derivation-matched RAW CRISPR count inputs, and (c) the frozen Lock-S
recipe (lock_s/scientific_protocol_v1.json), such that patient-level
reconstruction of Lock-S sensitivity would be mechanically feasible at
$0 metered spend on local compute?

## Required semantic fields (each: PRESENT/ABSENT/AMBIGUOUS in a named manifest)
R1 resource/provenance: resource_id, release, source_study_id, manifest_version
R2 patient linkage: pseudonymous_patient_id, specimen_id, derived_model_id,
   parent_specimen_id, derivation_type, donor_deduplication_key
R3 raw objects: file_id, URI, format, byte_size, checksum, processing_level
   (must include an object declared as raw/guide-level counts), sample_column_map,
   feature_identifier_namespace
R4 recipe: library identity (minLib/v1 per protocol library_rule), normalization
   and scoring recipe sufficient to reproduce the frozen Lock-S statistic class
R5 access: access_tier (public, no controlled-access application), no charge

## Manifest sources (fetch doc/listing/metadata only)
M1 figshare article 29472362 public API metadata (file inventory, versions)
M2 CMP download index https://cog.sanger.ac.uk/cmp/download/ (listing only)
M3 local data/crosswalk_sanger_screened.csv columns (already-held manifest;
   ID/flag columns only)
M4 local data/passports_model_list_20260921.csv columns (already-held)
Forbidden: downloading/opening any count matrix, preview, row sample, or
summary of count values; the locally retained processed matrices stay unopened
by this generation.

## Decision rule (pre-committed)
PASS_RESOURCE iff: >=1 patient has complete unambiguous chain patient ->
specimen -> screened model -> declared raw count object(s) with sample map,
recipe fields R4 satisfied, and R5 satisfied; report count of complete
independent patients. FAIL_TO_ESTABLISH otherwise, naming the failing R-group.
PASS establishes mechanical feasibility only (exploratory sensitivity use);
it does not alter Lock-S, Determination v3, or any C-gate.

## Accounting
Failures and absences are results. Sol-high review >=90 before close.
