# sgen001 adjudication dossier v1 — identity + C1/C6 (for sol-high adjudication; lead does not self-certify)

## Identity (Question 1): RESOLVED — Passports grouping authoritative
Receipted evidence: generations/sgen001/identity_reconciliation_v1.json (src/sgen001_identity.py).
Patient records explicitly state same-patient sampling: SIDP01937 comment links WTSI-COLIVM_031
(sample SIDS02042, age 69) and WTSI-COLIVM_061 (SIDS02059, age 70); SIDP01939 links WTSI-COLO_478
(primary) with WTSI-COLIVM_051 and carries WTSI-COLIVM_090 as a third sample (ages 74/74/76).
S2 Supplementary Table 2 `individual_ID` (source of locked cohort donor_IDs) therefore behaves as
attendance/sample-level for these records. Locked cohort: 148 models / **142 patients** (not 144 donors).
Frozen consequence: Lock-S execution and BOUND decision preserved unchanged. Its donor bootstrap
split 2 same-patient model pairs into separate clusters (2 of 142 patients), so the reported
archived 144-group estimate/interval/decision [-0.175,-0.114] used covariate-ID groups for 142 patients; effects on patient-weighted estimate, interval and decision are unknown in size and direction (see identity_erratum_v1.json, which supersedes all earlier 'slightly understate' wording incl. identity_reconciliation_v1.json). A 142-patient interval cannot be computed from retained artifacts (only
donor-averaged D_g retained; per-model arrays would require re-decoding spent C outcomes) and
would in any case be exploratory sensitivity, never a second confirmatory test. The BOUND claim
henceforth carries this cluster caveat in every rendering (manuscript updated).

## Novelty/consequence (Question 2): dossier for adjudication
- Claim frozen as in novelty_audit_v4 §1 / v5 corrections (S3 = §2.10.1/§3.7, Tables S17–S19).
- Backward references (NEW, generations/sgen001/backward_references.json, Europe PMC REST 200):
  S1 72 refs, S2 96 refs (PMID 42557320), S3 38 refs; title-keyword screen for format/medium/
  minipool yields only false positives ("transformation", "organ formation"). Label: title-level
  screen of complete reference lists, not full-text inspection of each reference.
- Forward citations, concept/preprint screens, P3/P5 abstract dispositions: novelty_audit_v5.
- Still outstanding (explicit): S1 supplement PDF line inspection beyond minipool code route;
  exhaustive screening beyond relevance top-25 of the 3,634-hit broad set; non-Europe-PMC sources.
- Consequence statement unchanged (v5 §5 analogue): within this panel, measured format lability
  is not a supported transfer warning; direct transfer/context evidence is required per target.

## Requested adjudication
Reviewer: render C1 and C6 (MET/PARTIAL/UNMET) with reasons vs spec §12, and confirm/refute the
identity disposition + interval caveat wording. Score the dossier package 0–100 with all
low/medium/high/critical issues; >=90 + zero unresolved high/critical required to close sgen001.
