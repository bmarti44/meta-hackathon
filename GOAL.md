# GOAL v4 — research first (adopted 2026-10-29)

Supersedes the RSI framing (archived at archive_rsi_v3/GOAL_v3_rsi.md). The policy-vs-fixed-exploration
comparison, C9 cost accounting, and gate ceremony are dropped as goals.

## Objective
Produce a result that changes how someone interprets or acts on cancer dependency
data, and get it in front of people who can use it (preprint + released code/tables).

## Lead question
**How much of the published "organoid-specific" dependency catalogue is a culture-medium
artifact rather than tumor biology, and which nominated targets are affected?**

Why this one: organoid media are lipid- and nutrient-poor compared with serum or
plasma, so dependencies that appear only in organoid screens (sterol synthesis,
possibly heme/OXPHOS/FA synthesis) may not hold in vivo, where tumors get LDL.
Two 2026 Nature papers (NextGen/Broad, Herranz-Ors/Sanger) now offer organoid
dependency catalogues, and nobody has quantified the medium-attributable share
genome-wide.

Already established (do not claim as novel): medium-not-format for SQLE/MSMO1
(Neiswender et al., Nature 2026, minipool 2x2), LDLR/SREBP sterol-starvation
physiology, Wnt-secretion dependency without exogenous Wnt.

## Deliverables
1. Per-gene medium-attribution table for every organoid-vs-2D differential dependency:
   library-matched (Humagne-CD FBS vs TSM vs organoid media), lineage-adjusted,
   and doubling/dynamic-range-aware. Flag hits as medium-attributable,
   format/biology-candidate, or unresolved.
2. Fraction of published organoid-specific hits that are medium-attributable, with
   the named targets most affected (e.g. sterol, heme, FA synthesis).
3. A doubling-corrected re-analysis of the core-essential "weakening" in dome screens
   (artifact vs biology), set against Herranz-Ors 2026.
4. Short preprint (resource/technical note scale) plus released code and tables.
5. One concrete wet-lab test proposed to a collaborator: lipid/LDL add-back or
   statin/SQLE-inhibitor potency in matched FBS vs organoid medium.

## Working rules
- Science over process: one review per finding, no cost ledgers or gate scoring.
- Novelty check (literature + your own downloaded papers) BEFORE calling anything new.
- Hold out patients for confirmation as before; report negatives plainly.
- Known confounders to always address: CRISPR library (all organoid/TSM screens are
  Humagne-CD; most FBS screens are Avana), lineage, screen dynamics/doublings, lab/batch.
