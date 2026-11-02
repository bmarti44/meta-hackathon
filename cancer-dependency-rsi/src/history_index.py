"""Bounded, paged history directory (PLAN round-5 residual #1).

Guarantees for ANY history size:
- No single rendered page exceeds PAGE_MAX_ENTRIES entries (header included:
  the partition directory itself is paged hierarchically).
- Every attempt ID is addressable: header page -> partition page -> entries,
  plus direct lookup(attempt_id) in O(1) via the in-memory map (the runner
  mediates lookups; the proposer cites IDs, never dumps the directory).
Partitions are by direction_id, sub-partitioned by insertion order into
pages of PAGE_MAX_ENTRIES fixed-size rows.
"""
from __future__ import annotations

import math

PAGE_MAX_ENTRIES = 50


class HistoryIndex:
    def __init__(self, entries: list[dict]):
        # entries: fixed-size rows with at least attempt_id + direction_id
        self._by_id: dict[str, dict] = {}
        parts: dict[str, list[dict]] = {}
        for e in entries:
            self._by_id[e["attempt_id"]] = e
            parts.setdefault(str(e.get("direction_id", "undirected")), []).append(e)
        self._partitions: list[dict] = []  # {partition_id, direction_id, page, entries}
        for direction in sorted(parts):
            rows = parts[direction]
            for p in range(0, len(rows), PAGE_MAX_ENTRIES):
                self._partitions.append({
                    "partition_id": f"{direction}#{p // PAGE_MAX_ENTRIES}",
                    "direction_id": direction,
                    "entries": rows[p:p + PAGE_MAX_ENTRIES],
                })

    @property
    def n_partitions(self) -> int:
        return len(self._partitions)

    def header_page(self, page: int = 0) -> dict:
        """One bounded page of the partition directory (counts + ID ranges only)."""
        summaries = [{
            "partition_id": p["partition_id"], "direction_id": p["direction_id"],
            "count": len(p["entries"]),
            "first_id": p["entries"][0]["attempt_id"], "last_id": p["entries"][-1]["attempt_id"],
        } for p in self._partitions]
        pages = max(1, math.ceil(len(summaries) / PAGE_MAX_ENTRIES))
        if not 0 <= page < pages:
            raise IndexError(f"header page {page} out of range (0..{pages - 1})")
        return {"page": page, "n_pages": pages, "n_partitions": len(summaries),
                "n_attempts": len(self._by_id),
                "partitions": summaries[page * PAGE_MAX_ENTRIES:(page + 1) * PAGE_MAX_ENTRIES]}

    def partition_page(self, partition_id: str) -> list[dict]:
        for p in self._partitions:
            if p["partition_id"] == partition_id:
                return list(p["entries"])
        raise KeyError(partition_id)

    def lookup(self, attempt_id: str) -> dict:
        """Runner-mediated ID resolution (logged by caller)."""
        return self._by_id[attempt_id]

    def locate(self, attempt_id: str) -> str:
        e = self._by_id[attempt_id]
        direction = str(e.get("direction_id", "undirected"))
        for p in self._partitions:
            if p["direction_id"] == direction and any(r["attempt_id"] == attempt_id for r in p["entries"]):
                return p["partition_id"]
        raise KeyError(attempt_id)  # unreachable if built from same entries
