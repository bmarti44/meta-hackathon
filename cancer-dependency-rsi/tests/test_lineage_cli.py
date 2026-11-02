import subprocess, sys
from pathlib import Path
import pytest
import lineage

# The Lock-2 hash gate covers the raw Sanger download (121 MB, stored with Git LFS on GitHub, not in
# every checkout). Without it the gate refuses on that file first, so the exact refusal mode below
# can only be checked where the raw data is present.
SANGER_ZIP = Path(__file__).resolve().parent.parent / "data/raw/sanger_figshare/S2_Supplementary_Tables.zip"

BASE = {"study_id": "S1", "evaluator_version": "ev1"}

def test_origins_and_dag_rules():
    ex = {"a": {"attempt_id": "a", "parents": [], **BASE}, "b": {"attempt_id": "b", "parents": ["a"], **BASE}}
    assert lineage.validate_node({"attempt_id": "c", "origin": "combination", "parents": ["a", "b"], **BASE}, ex) == []
    assert any("requires" in e for e in lineage.validate_node({"attempt_id": "c", "origin": "refinement", "parents": ["a", "b"], **BASE}, ex))
    assert any("not found" in e for e in lineage.validate_node({"attempt_id": "c", "origin": "refinement", "parents": ["zz"], **BASE}, ex))
    assert any("repairs_node" in e for e in lineage.validate_node({"attempt_id": "c", "origin": "repair", "parents": ["a"], **BASE}, ex))
    assert lineage.ancestry("b", ex) == {"a", "b"}

@pytest.mark.skipif(not SANGER_ZIP.exists(), reason="needs data/raw/sanger_figshare/S2_Supplementary_Tables.zip (git lfs pull, or fetch per data/data_manifest.json)")
def test_cli_gate_lock():
    # evaluate-external must always refuse outside its single locked execution:
    # either the Lock2 gate (not yet unlocked) or, after Lock-S executed once,
    # the immutable-result single-execution refusal. Never a silent success.
    r = subprocess.run([sys.executable, "src/cli.py", "evaluate-external"], capture_output=True, text=True)
    combined = r.stderr + r.stdout
    # Exact known refusal modes (all fail-closed): Lock2 gate, spent-result
    # guard, or - since the 2026-10-29 remediation restored Lock-1 caps for
    # the frozen Lock-S launcher path - its budget-cap refusal. Amended caps
    # apply only via model_call's shadow BUDGET_ROOT, never to this path.
    last = combined.strip().splitlines()[-1] if combined.strip() else ""
    assert (r.returncode, last) in {
        (1, "RuntimeError: budget: phase model_calls cap exceeded"),  # restored Lock-1 caps on frozen launcher path
        (3, "REFUSED: hash mismatch for config/allocations.json"),    # Lock2 hash gate (pre-restoration state)
    } or (r.returncode != 0 and last.startswith("REFUSED:") and "already exists" in last)  # spent-result guard
    r2 = subprocess.run([sys.executable, "src/cli.py", "status"], capture_output=True, text=True)
    assert r2.returncode == 0
