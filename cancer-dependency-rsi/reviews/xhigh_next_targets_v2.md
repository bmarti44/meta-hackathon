1. **Cycle 2: NO. FAMILY_EXHAUSTED for the current budget-20 C7 delta-class acquisition family.**

   This is an operational stopping decision; it does not establish that every task on C7 is unlearnable. The available evidence gives no DEV-supported reason to select magnitude regression, a different observable, or a larger budget. Near-prior losses suggest weak demonstrated predictive signal; the winning acquisition removes W/V discrimination; model-level sign reversals weaken the case for transferable gains.

   **SPEC sketch:** close this family without another optimization cycle. Preserve the reproduced numbers alongside the rejected certification. Treat previously used EVAL models as used. Reopening requires a distinct, demonstrated DEV opportunity and a newly locked evaluation design; repairing documentation alone supplies neither. No terminal determination or C13/C8/C9 credit follows.

2. **Sanger: YES to one bounded manifest-only feasibility probe. Rank 1.**

   The decisive question is whether the resource connects **actual patients, derivation-matched raw inputs, and the frozen Lock-S calculation**. Availability of Sanger counts alone is insufficient.

   **SPEC sketch — required semantic fields** below are requirements, not assertions about existing Sanger column names:

   - **Resource/provenance:** `resource_id`, `release`, `source_study_id`, `source_cohort_id`, `manifest_version`, `derivation_provenance_id`.
   - **Biological unit/linkage:** `pseudonymous_patient_id`, `specimen_id`, `aliquot_id`, `derived_model_id`, `parent_specimen_id`, `biological_entity_type`, `derivation_type`, `pool_membership`, `donor_deduplication_key`.
   - **Eligibility/condition:** `species`, `disease`, `tissue`, `collection_timepoint`, `treatment_or_perturbation`, `exposure_duration`, `assay_modality`, `protocol_version`.
   - **Input roles/replication:** `sample_id`, `required_input_role`, `control_reference_id`, `biological_replicate_id`, `technical_replicate_id`, `batch_id`.
   - **Raw-object schema:** `file_id`, `URI`, `format`, `byte_size`, `checksum`, `processing_level`, `declared_count_semantics`, `matrix_orientation`, `sample_column_map`, `feature_identifier_namespace`, `reference_build`, `feature_annotation_version`.
   - **Lock-S reconstruction:** `lock_s_definition_hash`, `required_feature_set_hash`, `normalization_recipe_and_parameters`, `reference_set_ids`, `replicate_aggregation_rule`, `scoring_recipe_and_parameters`, `output_units_and_orientation`, and any required reference-label file IDs and linkage schema.
   - **Access feasibility:** `access_tier`, `download_charge`, `required_remote_compute`, `local_software_requirements`, `declared_resource_requirements`.

   **PASS_RESOURCE:** at least one genuine patient has a complete, unambiguous provenance chain and every input required by the frozen recipe; feature mapping and transformations are specified; access and execution fit $0 metered spend and local compute. Report the number of complete independent patients separately.

   **FAIL_TO_ESTABLISH:** any indispensable field or linkage is missing, ambiguous, pooled irrecoverably, or incompatible with the original derivation. A cell-line identifier cannot substitute for a patient identifier.

   This pass establishes mechanical reconstruction feasibility only. It establishes neither count quality nor sensitivity, statistical adequacy, or the ≥367-component external design. If the frozen Lock-S recipe is unavailable, the probe cannot pass.

   **Download boundary:** separate manifests and documentation only. No count objects, matrix previews, row samples, count summaries, or reference-label values.

3. **Same-condition repeats: YES as a repeat-observability census. Metadata cannot measure dependency instability. Rank 2.**

   **SPEC sketch:** construct an eligibility graph whose vertices are independently executed screens. Join screens only when they share a prespecified condition key:

   `canonical_model_id`, relevant `clone_id`, `perturbation_id`, `dose`, `exposure_duration`, `culture_medium_and_environment`, `assay_modality`, `library_hash`, `protocol_version`, and `endpoint_definition`.

   Establish replication using `screen_id`, `culture_start_id`, `biological_replicate_id`, `technical_replicate_id`, `raw_input_file_ids`, `passage`, `screen_date`, `batch_id`, `site`, and `rerun_reason`. Missing critical condition fields make an edge unqualified. Different analysis versions of the same raw screen are not independent repeats.

   The measurable metadata construct is **repeat coverage**: the fraction of eligible condition groups containing at least two independent biological screen executions, plus their timing, batch structure, and reasons for repetition. Repeated cultures remain clustered within their underlying model/component.

   This would evidence opportunities to estimate reproducibility or temporal recurrence under documented conditions. Metadata cannot establish dependency persistence, instability magnitude, direction, or biological mechanism. Rerun frequency can reflect scheduling or QC selection.

   A later locked outcome estimand could measure within-condition disagreement beyond a prespecified biological tolerance, accounting for measurement noise and rerun selection. Outcome access requires a feasible sample-size and confounding plan first.

   **Novelty risk: high.** Repeat-screen reproducibility is an established question. Calling it “persistence” adds no novelty; a defensible contribution needs a specific temporal or biological distinction and adequate independent replication.

4. **Other target: condition-history effects after return to the same condition. Rank 3; metadata feasibility only.**

   This candidate is absent from the supplied context. It asks whether dependency at condition A depends on prior exposure to B, using matched **A→B→A** and **A→A→A** histories.

   **SPEC sketch:** inventory `founder_lineage_id`, `parent_child_culture_links`, `branch_assignment`, complete `condition_history`, `switch_times`, `washout_or_recovery_interval`, `passage`, `screen_time`, `independent_culture_start_id`, and the assay/condition fields above. Require contemporaneous return-to-A and maintained-A branches with traceable common starting lineage.

   The future contrast is dependency in A after B versus dependency in A after continued A, at matched elapsed time. It could distinguish history dependence from effects of the current environment. Causal interpretation additionally requires randomized branching or a defensible control for branch selection.

   **Metadata kill rule:** stop after one bounded inventory if complete histories, independent biological branches, or time-matched controls are absent. Proceed only to design development if they exist; lock precision, replication, confounding controls, and recovery timing before opening outcomes.

   Novelty remains uncertain because adaptation and hysteresis are established concepts. Its discriminating value is the controlled history contrast. It supplies no automatic credit toward the blocked original designs.

All proposed probes are nonterminal. The ranking favors resolving a concrete resource blocker, then measuring available replication, then searching for a stronger biological contrast.

RANKED_TARGETS: 1. Sanger derivation-matched patient/raw-input manifest; 2. Same-condition repeat-observability census; 3. Controlled condition-history return pairs; 4. Current C7 acquisition family—FAMILY_EXHAUSTED.
FIRST_NEXT_GENERATION: Lock and execute one Sanger manifest-only feasibility probe with explicit provenance gates, zero count-value access, and no terminal determination.