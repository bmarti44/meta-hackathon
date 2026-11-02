"""Total deterministic direction-status function (PLAN 0.4.2; Lock 1).

Pure function over admissible evidence. Conventions frozen here:
- Quartiles: numpy percentile, linear interpolation, over the domain's
  best-valid-q values (one per direction with >=1 valid attempt).
- Ties: best_q >= Q3 => promising (requires IQR > 0); best_q <= Q1 and
  attempts >= 3 => unpromising (requires IQR > 0); IQR == 0 => unknown.
- Empty frontier / no valid attempts => promise unknown, fragility unknown.
- dominant failure: one outcome_class in {implementation_failure,
  invalid_result} counts > 50% of attempts AND attempts >= 2.
- named fix: repair_citation = {node_id, fix_class in FIX_CLASSES} present
  on at least one attempt record in the direction.
- independent configs: distinct canonical config_id values.
- A later valid success resets the conceptual-failure history for 'dead'.
- Precedence (recoverability): dead > recoverable > na.
- Recomputation from all admissible evidence each call (no sticky states);
  'saturated' is an allocation label with reactivation: expires after
  `saturated_pause_iters` iterations or immediately when a new valid attempt
  in the direction improves best_q by >= saturated_epsilon.
Returns the 4 fields + derived saturated + evidence attempt IDs used.
"""
from __future__ import annotations

import numpy as np

FIX_CLASSES = {"bug_fix", "support_fix", "legalization", "numeric_fix"}
SATURATED_EPSILON = 0.02
SATURATED_K = 3  # attempts since last improvement


def _quartiles(vals: list[float]) -> tuple[float, float] | None:
    if not vals:
        return None
    q1, q3 = np.percentile(np.asarray(vals, dtype=float), [25, 75], method="linear")
    return float(q1), float(q3)


def direction_status(attempts: list[dict], domain_best_qs: list[float],
                     iterations_since_saturated: int | None = None,
                     saturated_pause_iters: int = 2) -> dict:
    ids = [a.get("attempt_id") for a in attempts]
    n = len(attempts)
    depth = ("unexplored" if n == 0 else "underexplored" if n <= 2
             else "explored" if n <= 6 else "well_explored")
    valid = [a for a in attempts if a.get("valid") and a.get("q") is not None]
    best_q = max((float(a["q"]) for a in valid), default=None)

    promise = "unknown"
    qs = _quartiles([q for q in domain_best_qs if q is not None])
    if best_q is not None and qs is not None:
        q1, q3 = qs
        if q3 > q1:
            if best_q >= q3:
                promise = "promising"
            elif best_q <= q1 and n >= 3:
                promise = "unpromising"

    # fragility: requires both LOMO range and sensitivity sign info on >=1 valid attempt
    fragility = "unknown"
    checked = [a for a in valid if a.get("lomo_range") is not None and a.get("sensitivity_sign_flip") is not None]
    if checked:
        fragility = "fragile" if any(float(a["lomo_range"]) > 0.15 or a["sensitivity_sign_flip"] for a in checked) else "robust"

    classes = [a.get("outcome_class") for a in attempts]
    dominant_impl = n >= 2 and any(classes.count(c) * 2 > n for c in ("implementation_failure", "invalid_result"))
    has_fix = any(isinstance(a.get("repair_citation"), dict)
                  and a["repair_citation"].get("node_id") in ids
                  and a["repair_citation"].get("fix_class") in FIX_CLASSES
                  for a in attempts)
    ordered_attempts = sorted(attempts, key=lambda a: a.get("seq", 0))
    last_success = max((i for i, a in enumerate(ordered_attempts) if a.get("valid") and a.get("outcome_class") == "success"), default=-1)
    conceptual_configs = {a.get("config_id") for a in ordered_attempts[last_success + 1:] if a.get("outcome_class") == "conceptual_failure" and a.get("config_id")}
    if len(conceptual_configs) >= 2:
        recoverability = "dead"
    elif dominant_impl and has_fix:
        recoverability = "recoverable"
    else:
        recoverability = "na"

    saturated = False
    if depth == "well_explored" and valid:
        ordered = sorted(valid, key=lambda a: a.get("seq", 0))
        best_so_far, gains = -np.inf, []
        for a in ordered:
            gains.append(float(a["q"]) - best_so_far if best_so_far > -np.inf else np.inf)
            best_so_far = max(best_so_far, float(a["q"]))
        recent = gains[-SATURATED_K:] if len(gains) >= SATURATED_K else []
        saturated = bool(recent) and all(g < SATURATED_EPSILON for g in recent)
        if saturated and iterations_since_saturated is not None and iterations_since_saturated >= saturated_pause_iters:
            saturated = False  # pause expired: allocation reactivation

    return {"depth": depth, "promise": promise, "fragility": fragility,
            "recoverability": recoverability, "saturated": saturated,
            "best_q": best_q, "n_attempts": n, "evidence_attempt_ids": ids}
