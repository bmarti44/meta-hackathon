"""Regression coverage for the 2026-10-29 allocations remediation shadow root."""
import hashlib
from pathlib import Path

import pytest

import model_call

ROOT = Path(__file__).resolve().parent.parent


def test_pinned_allocations_restored():
    digest = hashlib.sha256((ROOT / "config/allocations.json").read_bytes()).hexdigest()
    assert digest == "796482ea5e368e2de47039e80b7e5c461ed7bad84efa3a3e5d4bbe8c38405d9b"


def test_shadow_root_identities():
    sha = model_call.verify_budget_root()
    amended = ROOT / "config/allocations_amended_20261029.json"
    assert sha == hashlib.sha256(amended.read_bytes()).hexdigest()
    assert (model_call.BUDGET_ROOT / "ledger").resolve() == (ROOT / "ledger").resolve()
    assert (model_call.BUDGET_ROOT / "config/resources.json").resolve() == \
        (ROOT / "config/resources.json").resolve()


def test_shadow_drift_fails_closed(tmp_path, monkeypatch):
    bad = tmp_path / "shadow"
    (bad / "config").mkdir(parents=True)
    (bad / "config/allocations.json").write_text("{}")  # not the amended file
    (bad / "config/resources.json").symlink_to(ROOT / "config/resources.json")
    (bad / "ledger").symlink_to(ROOT / "ledger")
    monkeypatch.setattr(model_call, "BUDGET_ROOT", bad)
    with pytest.raises(RuntimeError, match="identity mismatch"):
        model_call.verify_budget_root()
