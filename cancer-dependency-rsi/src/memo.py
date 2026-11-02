"""Arm-owned memoized LLM state (PLAN round-5 residual #2; PLAN 0.4.5).

Key = sha256(output_type | arm_id | protocol_version | canonical_state_hash).
- A memo created by arm A is NEVER returned to arm B (cross-arm lookup is a
  cache miss by construction: arm_id is inside the key).
- Creation cost is charged once, to the creating arm, at creation time
  (recorded in the entry; the runner ledgers it). Reuse within the same arm
  is free and deterministic; reconstruction reads the memo, never re-invokes
  a model. Cache miss during replay => transition unsupported (caller rule).
- Execution-order invariance: with a deterministic generator stub, interleaved
  vs sequential arm execution yields identical per-arm memo contents.
"""
from __future__ import annotations

import hashlib
import json


def memo_key(output_type: str, arm_id: str, protocol_version: str, canonical_state: dict) -> str:
    state_hash = hashlib.sha256(json.dumps(canonical_state, sort_keys=True).encode()).hexdigest()
    raw = f"{output_type}|{arm_id}|{protocol_version}|{state_hash}"
    return hashlib.sha256(raw.encode()).hexdigest()


class MemoStore:
    def __init__(self) -> None:
        self._store: dict[str, dict] = {}
        self.charges: list[dict] = []  # {arm_id, key, cost} creation charges only

    def get_or_create(self, output_type: str, arm_id: str, protocol_version: str,
                      canonical_state: dict, create_fn, creation_cost: float = 1.0) -> tuple[dict, bool]:
        """Return (entry, created?). create_fn() -> JSON-serializable payload."""
        key = memo_key(output_type, arm_id, protocol_version, canonical_state)
        if key in self._store:
            return self._store[key], False
        payload = create_fn()
        entry = {"key": key, "output_type": output_type, "arm_id": arm_id,
                 "protocol_version": protocol_version, "payload": payload}
        self._store[key] = entry
        self.charges.append({"arm_id": arm_id, "key": key, "cost": creation_cost})
        return entry, True

    def get(self, output_type: str, arm_id: str, protocol_version: str, canonical_state: dict) -> dict | None:
        return self._store.get(memo_key(output_type, arm_id, protocol_version, canonical_state))

    def arm_charges(self, arm_id: str) -> float:
        return sum(c["cost"] for c in self.charges if c["arm_id"] == arm_id)
