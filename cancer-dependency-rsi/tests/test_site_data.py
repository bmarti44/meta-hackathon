"""Site data/claims guards (sol review r1 regression coverage)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


def _genes():
    return {g["g"]: g for g in json.loads((SITE / "data/genes.json").read_text())}


def test_top_medium_gains_are_medium_consistent():
    stats = json.loads((SITE / "data/stats.json").read_text())
    genes = _genes()
    for entry in stats["top_medium_gains"]:
        assert genes[entry["g"]]["f"] == 1, entry["g"]


def test_hit_counts_match_flags():
    genes = list(_genes().values())
    stats = json.loads((SITE / "data/stats.json").read_text())
    assert sum(g["f"] > 0 for g in genes) == stats["n_hits"] == 456
    assert sum(g["f"] == 1 for g in genes) == stats["n_medium"] == 387
    assert [g["g"] for g in genes if g["f"] == 3] == ["LSM7"]


def test_flag_zero_is_not_labelled_no_significant_difference():
    html = (SITE / "index.html").read_text()
    assert '"No significant difference"' not in html
    # the plain-English badge reads "No real difference"; the technical label is kept for researchers
    assert "below hit threshold" in html.lower()


def test_publication_status_is_honest():
    html = (SITE / "index.html").read_text()
    assert "Technical note preprint" not in html
    assert "accompanying the preprint" not in html
    assert "Unpublished draft" in html


def test_causal_phrases_stay_out():
    html = (SITE / "index.html").read_text()
    for phrase in ("needs the dome", "separate food from shape", "Δ shape only",
                   "what the medium explains", "fully explained by the medium",
                   "shape-only contrast", "shape without food change"):
        assert phrase not in html, phrase
