"""Project CLI skeleton. Gate-locked commands fail loudly naming the gate.

Usage: uv run python src/cli.py <command>
Commands: bootstrap audit-data reproduce-baselines run-pilot run-cycle
evaluate-policy lock-science evaluate-external reproduce status resume
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATES = {"audit-data": "G0", "reproduce-baselines": "G1", "run-pilot": "G2", "run-cycle": "G3",
         "evaluate-policy": "G4", "lock-science": "G5", "evaluate-external": "Lock2", "reproduce": "G6"}


def _status() -> dict:
    p = ROOT / "status.json"
    return json.loads(p.read_text()) if p.is_file() else {"phase": "0-bootstrap/1-audit", "note": "status.json not yet generated; see STATUS.md"}


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "status"
    if cmd in ("status", "resume"):
        print(json.dumps(_status(), indent=2))
        print("STATUS.md:", (ROOT / "STATUS.md").exists(), "| resume: read PLAN.md, GOAL.md, cancer-dependency-rsi/STATUS.md, then STATUS 'Next action'")
        return 0
    if cmd == "bootstrap":
        print("bootstrap: env =", (ROOT / ".venv").exists(), "| config =", (ROOT / "config/resources.json").exists())
        return 0
    if cmd == "evaluate-external":
        # Scientific-only track (user-approved 2026-10-28): external_eval enforces the
        # Lock2 hash commit, exposure logging and single execution itself.
        # Always dispatches through the bounded launcher (reservation, watchdog, timeout).
        sys.path.insert(0, str(ROOT / "src"))
        import external_eval
        import run_external_eval
        try:
            r = run_external_eval.launch(ROOT)
        except external_eval.LockError as exc:
            print(str(exc), file=sys.stderr)
            return 3
        print(json.dumps({k: r.get(k) for k in ("returncode", "timed_out", "wall_s", "stdout_tail", "stderr_tail")}, indent=1))
        return 0 if r.get("returncode") == 0 else 1
    if cmd in GATES:
        print(f"REFUSED: '{cmd}' not yet unlocked (requires gate {GATES[cmd]}). See PLAN.md phases + STATUS.md.", file=sys.stderr)
        return 3
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
