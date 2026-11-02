# sgen015 — Sanger CMP paired-format resource discriminator (metadata only)

Context: determination v3 (INCONCLUSIVE) reopening condition (2): matched
component-level paired-format L/B, >=367 independent matched components for
one qualified endpoint. User direction 2026-10-29: examine Sanger CMP.

## Question
Does the Sanger Cell Model Passports / CMP ecosystem contain derivation-
matched model pairs (same patient: 2D cell line + 3D/organoid model, or same
model in two formats) WITH CRISPR screens on both sides, at a scale and
identity quality that could supply component-level paired-format L/B for a
future locked design, disjoint from cohort C's 142 patients?

## Sources (metadata only; no outcome matrices opened/downloaded)
- data/passports_model_list_20260921.csv (local, hash known): model_id,
  patient_id, parent_id (derivation), model_type, growth_properties.
- CMP download index https://cog.sanger.ac.uk/cmp/download/ (listing only)
  + any screened-model metadata files it indexes (names/sizes; small
  metadata files may be fetched with receipts; NO gene-effect matrices).
- Passports API metadata endpoints if needed (models/patients records only).

## Computations (fixed)
1. Patient-level pairing: patients with >=1 organoid-type model AND >=1
   cell-line-type model; derivation-linked pairs via parent_id chains.
2. Screen availability: which paired models have CRISPR screens on BOTH
   sides (per CMP screened-model metadata / Passports fields).
3. Disjointness vs C: exclude any patient in the 142 C SIDP set (pinned map
   via sgen010 Witness-A canonical hash check route).
4. Scale gates: >=367 independent patients with two-sided screened pairs =
   RESOURCE_PRESENT; 100-366 = RESOURCE_PARTIAL; <100 = RESOURCE_ABSENT.
   Report also organoid-only screened patient counts (context for B-route).
5. Identity quality: pairing basis per pair (same patient_id only vs
   derivation chain), ambiguities counted.

## Decision rule
Verdict label per (4). Any PASS only authorizes a separate locked design
generation (sol-xhigh) — no outcome access in sgen015. Outcome matrices on
CMP remain untouched regardless of verdict.

## Close-out (lead, 2026-10-29)
RESOURCE_ABSENT (v3). Passports snapshot: 2,266 models, zero patients with
both organoid and cell-line models, zero cross-type derivation chains.
Screened organoid patients: 142 (all of C) + 13 outside C. Sanger CMP cannot
supply derivation-matched paired-format L/B; the 13 fresh screened organoid
patients are far below any Lock-S-scale replication need. Review arc 88->96.
