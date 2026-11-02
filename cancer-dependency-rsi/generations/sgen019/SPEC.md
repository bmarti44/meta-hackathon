# sgen019 — CONDITIONAL processed-vector feasibility + Lock-S audit (question A)
Status: RECORDED, NOT ACTIVATED. Activation requires the user-supplied portal
bundle below. Source: reviews/xhigh_next_targets_v3.md (FRONTIER_EXHAUSTED).

## Required input bundle (user, via ordinary authorized portal access)
1. Complete file listing of the relevant Sanger processed-data release /
   NextGen file set: exact filenames, release/version, descriptions, docs.
2. Source-specific processed fitness/dependency matrix at Lock-S granularity
   + schema + processing documentation.
3. Metadata linking matrix columns -> screens -> samples -> models -> stable
   patient/donor IDs, incl exclusions and aggregation relationships.
4. Documentation of any combining across screens/replicates/conditions/sources.
Staging rule: numerical outcome files stay UNOPENED until feasibility is
established from listings/docs/metadata and this SPEC is re-locked.

## Pre-outcome feasibility (kill rule)
Establish source/version, usable vectors, patient grouping, eligible units,
and Lock-S-contract compatibility WITHOUT inspecting outcome values.
FAIL_TO_ESTABLISH (stop) if linkage/provenance/granularity/compatibility
cannot be established, or would require endpoint change or cohort-C reuse.

## If feasible (separate lock before any numbers)
Freeze exclusions, grouping, transformations, sensitivity contrasts,
statistic, interpretation. Exploratory patient-level sensitivity ONLY.
## Never establishes
Raw-count validity; effects erased by preprocessing; causal patient response;
independent confirmation of Lock-S; any terminal-determination change.
