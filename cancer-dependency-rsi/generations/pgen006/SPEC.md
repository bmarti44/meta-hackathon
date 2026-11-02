# pgen006 — replay-substrate readiness discriminator (metadata only)

> SUPERSEDED SECTIONS: the original task-instantiation and GO_REPLAY language
> below is superseded by the xhigh contract adjudication amendment at the end
> of this file (ENGINEERING_PILOT_SEPARATE; METADATA_SCREEN_PASS; no C13
> credit). Where they conflict, the amendment governs. The recordings are
> reused development data - no untouched-reserved-panel claim is made.

Authority: sol-xhigh new-targets consult 2026-10-29 (Rank 1 +
Discriminator SPEC), under pgen005 contract. This generation decides
GO_REPLAY / REPAIR_METADATA / FAIL_SUBSTRATE for a first policy cycle on
the C7 atlas. It accesses NO paired outcome values (presence/coverage only).

## Proposed task instantiation (to be frozen at cycle lock if GO_REPLAY)
Sequential evidence production on atlas v4 paired observations (3,000 rows;
7 models; 250 genes; format axis 1,750 rows, medium axis 1,250 rows):
policies order eligible (gene x axis) analyses within a model-partition and
stop; evaluator scores recovered lability classifications against the full
recorded atlas ground truth for the EVALUATION partition only.
- Partition (frozen here): DEVELOPMENT models = ACH-000108, ACH-000178,
  ACH-003040 (both axes recorded); EVALUATION models = ACH-001418,
  ACH-002958, ACH-003052 (format) + ACH-000048 (medium). Grouping unit =
  model (donor unresolved in atlas; models treated as independent sources,
  disclosed). No model appears on both sides.
- Action = reveal one recorded (gene, axis, model) paired observation.
  Cost per action: 1 evaluated node + estimated host/compute per pgen005
  accounting (model calls only for generation/review, charged equally).
- Comparators: fixed exploration (locked gene order) and uniform random
  (seeded); strongest fixed chosen on DEVELOPMENT partition only.
- Q* candidate (to lock numerically at cycle SPEC): recover >=90% of
  full-atlas sign-of-delta classifications on evaluation models. This
  discriminator does NOT lock Q*; it tests substrate readiness only.

## Readiness checks (all must pass for GO_REPLAY)
1. Identity/provenance: 100% of inventory rows resolve (gene in genes.csv
   atlas panel; model in Model.csv; screens recorded); zero ambiguous
   conflicting records (duplicate (gene,axis,model,held_condition) rows with
   differing presence is impossible by construction - duplicates counted).
2. Partition separation: zero model overlap dev/eval (by construction);
   report any shared screen IDs across partitions (must be zero for the
   frozen partition to be admissible).
3. Coverage: every action reachable under the proposed catalogue
   (gene x axis within partition models) either has a recorded observation
   or is excluded a priori from the catalogue with the exclusion frozen;
   report coverage fraction per partition x axis. GO requires the frozen
   catalogue = exactly the recorded set (100% coverage by restriction,
   with the restriction itself reported as a substrate limitation).
4. Execution minimum: >=1 complete held-out episode per policy/comparator
   constructible: evaluation partition has >=2 models and >=100 recorded
   actions per axis claimed.
5. Costs: per-action cost table definable under amended C9 basis for every
   reachable action (node charges + host-call accounting hooks exist).

## Decision labels
GO_REPLAY (all pass; authorizes cycle SPEC lock, not execution) /
REPAIR_METADATA (fixable gaps listed) / FAIL_SUBSTRATE (structural).
No label authorizes outcome access beyond recorded replay outcomes under a
future cycle lock; no biological claim is made by this generation.

## Amendment (xhigh contract adjudication 2026-10-29)
FRAMING: ENGINEERING_PILOT_SEPARATE. This discriminator is an engineering
rehearsal readiness screen, NOT a pgen005 task instantiation (pgen005's
sgen011-C clause stands; no C13 credit). Pass label is METADATA_SCREEN_PASS
(not GO_REPLAY). ACH-003052 (donor unresolved) is QUARANTINED from the
catalogue. Pilot catalogue restricted to the format axis for evaluation
(medium-axis EVAL has a single contributing model). Action identity includes
held_condition. Frozen inventory enforced exactly.

## Close-out (lead, 2026-10-29)
METADATA_SCREEN_PASS (v8; arc 58 -> 85 -> 91 -> 95). Engineering-pilot
substrate ready for a cycle SPEC lock: 2,750 catalogue actions
(held-condition-inclusive), DEV/EVAL patient-disjoint on recorded linkage,
ACH-003052 quarantined, format-axis evaluation (500 actions, 2 models).
Pass authorizes only cycle SPEC drafting/lock; no execution, no C13 credit.
