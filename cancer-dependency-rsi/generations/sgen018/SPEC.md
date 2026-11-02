# sgen018 — Controlled condition-history return-pair inventory (metadata only)
(sol-xhigh Rank-3 target, reviews/xhigh_next_targets_v2.md)

## Question
Do recorded ModelCondition parent chains contain screened A->B->A histories
with maintained-A screened controls from a common starting lineage?
(metadata feasibility only; no outcomes.)

## Definitions (pre-committed)
- Chain: ParentModelConditionID links within one ModelID (ModelCondition.csv).
- Condition content key: (CellFormat, FormulationID); empty/unknown format or
  empty formulation => node unqualified (chain broken at that node).
- History path: >=3 consecutive qualified nodes with keys X->Y->X, Y != X
  (return) or X->X->X (maintained). Longer paths counted once per terminal node.
- Screened node: has >=1 strict-eligible sequence (sgen017 strict rules:
  no pDNA, PassesQC true, DrugTreated/IsEngineered/ExcludeFromCRISPRCombined
  explicitly false) with Library recorded.
- Qualified model: >=1 screened return terminal AND >=1 screened maintained
  terminal sharing the same first qualified ancestor node and same Library.

## Outputs / kill rule
Chain depth distribution; qualified-path counts by pattern; screened
terminals; qualified models (list capped, count primary).
HISTORY_RESOURCE: ABSENT if 0 qualified models; SPARSE 1-9; MATERIAL >=10.
Metadata kill rule: ABSENT/SPARSE stops this route (no outcome design).
Non-claims: adaptation/hysteresis are established concepts; branch assignment
randomization unknown; elapsed-time matching not assessable from these fields
(no dates); feasibility only. Sol-high review >=90 before close.

## Addendum (lead, 2026-10-29, post-review)
Pattern semantics committed: terminal 3-node windows of the recorded chain.
Pairing ancestor = first qualified ancestor of the chain (v2 code). Dangling
parents reported separately and never treated as roots. All dormant in this
snapshot (max depth 2).
