# sgen001 SPEC — patient-identity reconciliation + C6 novelty/consequence adjudication package
Ledger-locked before work. Metadata/literature only; NO new access to C outcome values; the locked
Lock-S execution and its reported interval are preserved unchanged regardless of outcome.

Question 1 (identity): Passports model_list_20260921 maps 148 C models to 142 patients while the
locked cohort carries 144 covariate donor_IDs. Pairs in conflict: SIDP01937 = WTSI-COLIVM_031
(donor 2180271) + WTSI-COLIVM_061 (2199999); SIDP01939 = WTSI-COLIVM_051 (2194560) +
WTSI-COLIVM_090 (2207757) (+WTSI-COLO_478 also donor 2194560). Determine from primary metadata
(cached Sanger figshare covariates, Passports model/sample/patient records via official API,
model parent/relationship fields) whether each pair is (a) same patient, distinct samples/models
(Passports grouping correct; covariate donor_ID is sample-level), (b) distinct patients
(Passports grouping erroneous), or (c) unresolved with named missing evidence. Disposition per model.
Consequence rule frozen now: if (a), record that the locked donor interval used 144 clusters where
142 patient clusters exist; quantify direction of bias only (more clusters -> interval not wider
than patient-level would be is NOT assumed; state honestly), do NOT recompute a replacement
confirmatory interval (C is spent; any recompute from retained donor artifacts, if feasible
without re-decoding outcomes, is labeled exploratory sensitivity, never a second external test).

Question 2 (C6 adjudication package): complete novelty_audit v5 outstanding items attainable
without new outcome access: backward-reference check for S1/S2/S3 (Europe PMC references
endpoints, retained JSON), S1 supplement (MOESM) minipool section inspection, S3 Tables S17-S19
existence/content check via PMC supplement listing. Screen results against the locked claim.
Deliver adjudication dossier v1: claim-by-prior matrix final, consequence statement, identity
dispositions, explicit remaining gaps. GO bar (sol-high review): >=90, zero unresolved
high/critical, reviewer renders C1/C6 MET/PARTIAL/UNMET with reasons. Lead does not self-certify.
Budgets: <=60 metadata requests, <=32 MiB, $0; model calls charge phase6_7/phase2 allocations.
