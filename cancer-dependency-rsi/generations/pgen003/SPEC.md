# pgen003 SPEC — complete the pgen002 missing witnesses (metadata only)
Locked in ledger before any request. No count/outcome values. Budgets: <=200 official API/metadata
requests, <=32 MiB, <=900 s wall (recorded allocation from phase2_lock1 wall budget), $0.
Battery reserve unchanged from pgen002.

Witness A (C patient mapping): for each of the 80 C HCM-SANG models unmapped in
model_list_20260921, query the official Passports API (api.cellmodelpassports.sanger.ac.uk)
by exact model name; record patient_id or explicit not-found. PASS iff >=148-5 C models resolve
to patient_ids (unresolved <=5, each named) OR an authoritative statement of non-existence in
Passports is receipted per model. Then recompute C-overlap vs pgen002 matched patients.

Witness B (108 unmatched line keys): resolve via (i) Passports API name/synonym search per key,
(ii) if needed, official Project Score/Pacini figshare sample annotation (resolve via figshare
public API search; metadata files only). Heuristic expansions (NCI-/OCI- prefixes) are candidate
generators ONLY: a match counts only when the API/annotation record itself carries the alias.
PASS iff >=330/360 line keys resolve to unique patient_ids AND eligible patients after
C-overlap + Broad-minipool exclusions remain >=160.

Failure of either witness = FAILS-SCREEN for this specification (family remains open per
discriminator v2; next generation may use Broad-side metadata or user-supplied files).
All requests receipted as in pgen002. Ambiguous (multi-patient) keys are excluded, named.
