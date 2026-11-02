# Continuation 2 — concrete progress while required review remains unavailable

The previous goal turn was **progress**: it changed code and produced retained diagnostic evidence. This continuation also makes progress; it does not claim the goal is achieved or waive Lock1.

## Evidence atlas component

`atlas/provisional_v1/genes.csv` covers all 250 selected genes. It reports measured within-model, medium-fixed format changes and format-fixed medium changes in original Chronos units. `paired_observations.csv` retains 3,000 rows: 250 genes × (7 format + 5 medium pairs), with both original condition values and their difference. Model-equal summaries avoid giving ACH-003040 extra weight for its two pairs. Support is six format models and four medium models; verified donor counts are unresolved, not equated to model counts.

Eligibility is explicit: 216 development-primary genes, 207 confirmatory genes, 43 confirmatory exclusions with reasons. Published library classes are attributed as prior annotations, not discoveries. Biomarker, inferential uncertainty, invariance and external evidence remain explicitly unavailable/not evaluated. This is a provisional inventory, not final C7 or a supported discovery.

An isolated copy of the exact source/input files reproduced the three CSV hashes exactly with no stochastic model call. The current locked environment was reused; this is a **component reproduction only**, not full C11. Reproduction v1 used an overstrong metadata label about external files being unavailable to the child; that assertion is withdrawn. Corrected v2 states accurately that no external outcome files were copied and that the subprocess was not filesystem-sandboxed. The original report remains preserved.

## Metadata identity and provenance audit

All cached release files and provenance-manifest entries checked against pinned sizes/SHA-256 values pass. Opaque-byte checksum access to quarantined containers was logged before opening them; no outcome values were decoded or analyzed. The exposure log is verified by its originally pinned prefix, with new records appended.

The initial audit implementation treated library-screen rows as biological-model rows and falsely flagged dual-library rows and minLib selection; those audit defects were corrected and their failed report retained. The corrected audit regenerates 178 library-screen rows → 162 biological models → 148 eligible models/144 donors, excluding 13 Broad-overlapping donors. No cohort membership, library selection or biological outcome changed.

The original split manifest's `donor_ids` field was a 148-entry per-model donor list with 144 unique donors. The metadata mapping was correct, but the field could be misused as independent donor IDs. The corrected pre-lock manifest now has 144 unique `donor_ids` plus explicit `sample_to_donor` for every one of the unchanged 148 models. Each original sample-to-donor assignment was checked before conversion. Prior split and data manifests are retained, content-addressed, and referenced. The G2 lock must hash the new representation; this checkpoint is not a lock.

## Remaining blocker and pending choice

The required CLI consultations still have no model response; retained launch failures are not scientific negative results. The installed CLI is still 0.165.0. Official documentation confirms the normal exec/JSON/ephemeral interfaces but supplies no verified remedy for this observed in-process initialization failure under the current permission context:

- [Official CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Official security documentation](https://learn.chatgpt.com/docs/security)

No permissions were broadened, no credentials relocated, and no alternate provider was invoked. A user route-choice question is pending: permit the same mandated Sol models/efforts through built-in agents, or retain the explicit `codex exec` requirement from GOAL.md and PLAN §0.1. An unanswered question is not approval. No agent has been spawned and no route change has been made.

The scientific uncertainty redesign, residual G2 fixes and independent Sol-high >=90 approval remain necessary before Lock1 or a policy pilot. All C1–C13 completion criteria retain their original meaning. Separate scientific/prediction/policy statuses remain unchanged. Additional metered spend remains $0; unknown material host costs continue to prevent C9 certification.
