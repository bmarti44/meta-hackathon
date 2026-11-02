import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import sgen008_checks as C  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def test_c10_exact_decision_rejects_substring():
    md = (ROOT / 'reviews/c10_robustness_table_v1.md').read_text()
    res = json.loads((ROOT / 'lock_s/results/external_v1.json').read_text())
    assert C.check_c10(md, res)
    assert not C.check_c10(md.replace('**yes (BOUND)**', '**not yes (BOUND)**', 1), res)
    assert not C.check_c10(md.replace('**yes (BOUND)**', '**yes (BOUND) rejected; final NOT_BOUND**', 1), res)
