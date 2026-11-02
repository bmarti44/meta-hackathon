"""Focused regression tests for sgen010 v5 identity logic (review-v2 findings)."""
import sgen010_screen_v7 as v5


def test_tokenize_multivalued_ids():
    assert v5.tokens("ACH-000833;ACH-001741;ACH-001189") == {
        "ACH-000833", "ACH-001741", "ACH-001189"}
    assert v5.tokens("ACH-000338;ACH-000338") == {"ACH-000338"}
    assert v5.tokens("") == set()
    assert v5.tokens(None) == set()


def test_strong_unanimous_confirms_name_candidate_ignored():
    # ACH-000561 pattern: strong routes unanimous, NAME adds a spurious patient
    out = v5.assign(
        strong={"BROAD_ID": {"SIDP00970"}, "SIDM": {"SIDP00970"},
                "COSMIC": {"SIDP00970"}},
        name_candidates={"SIDP00970", "SIDP00838"})
    assert out["status"] == "confirmed"
    assert out["patient"] == "SIDP00970"
    assert out["name_candidates"] == ["SIDP00838", "SIDP00970"]


def test_strong_conflict_quarantined():
    out = v5.assign(
        strong={"BROAD_ID": {"SIDP01069"}, "COSMIC": {"SIDP00619"}},
        name_candidates=set())
    assert out["status"] == "conflict"
    assert out["patient"] is None


def test_name_only_not_established():
    out = v5.assign(strong={}, name_candidates={"SIDP00001"})
    assert out["status"] == "name_only"
    assert out["patient"] is None


def test_no_evidence_unresolved():
    out = v5.assign(strong={}, name_candidates=set())
    assert out["status"] == "unresolved"


def test_candidate_c_hit_excludes():
    # any candidate evidence (incl. NAME) on a C patient excludes conservatively
    out = v5.assign(strong={"SIDM": {"SIDP99999"}}, name_candidates={"SIDPC"})
    assert v5.c_candidate_hit(out, {"SIDPC"}) is True
    out2 = v5.assign(strong={"SIDM": {"SIDP99999"}}, name_candidates=set())
    assert v5.c_candidate_hit(out2, {"SIDPC"}) is False


def test_write_pair_refuses_existing_and_leaves_no_orphan(tmp_path):
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    b.write_text("pre-existing")
    try:
        v5.write_pair([(a, {"x": 1}), (b, {"y": 2})])
        raised = False
    except FileExistsError:
        raised = True
    assert raised
    assert not a.exists()                      # rolled back / never published
    assert b.read_text() == "pre-existing"     # never overwritten
    assert not list(tmp_path.glob("*.tmp-*"))  # staging cleaned


def test_write_pair_publishes_both(tmp_path):
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    v5.write_pair([(a, {"x": 1}), (b, {"y": 2})])
    assert a.exists() and b.exists()
    assert not list(tmp_path.glob("*.tmp-*"))
