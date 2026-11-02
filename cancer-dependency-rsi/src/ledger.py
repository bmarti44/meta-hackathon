"""Append-only JSONL ledgers + content hashing (stdlib only).

Every experiment/resource/review/claim event is one JSON line, fsynced on
append. Records are never edited or deleted; corrections are new records
that reference the superseded record id.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from pathlib import Path

NODE_STATES = ("proposed", "dispatched", "completed", "failed", "committed")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def context_hash(payload: dict) -> str:
    """Stable hash of a node's input context (sorted canonical JSON)."""
    return sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())


def append_record(ledger_path: Path, record: dict) -> dict:
    record = {"record_id": uuid.uuid4().hex, "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **record}
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True) + "\n"
    with open(ledger_path, "a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())
    return record


def read_records(ledger_path: Path) -> list[dict]:
    if not ledger_path.is_file():
        return []
    out = []
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out
