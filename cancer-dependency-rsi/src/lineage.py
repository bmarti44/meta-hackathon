"""Lineage DAG validation + identity levels (PLAN v2 §0.4.1)."""
from __future__ import annotations

ORIGINS = {"new": (0, 0), "refinement": (1, 1), "underexplored_extension": (1, 99),
           "combination": (2, 99), "repair": (1, 99)}


def parent_ids(node: dict) -> list[str]:
    """Accept legacy recorded IDs and generator parent objects with contributions."""
    parents = node.get("parents") or []
    if not isinstance(parents, list):
        raise ValueError("parents must be an array")
    out = []
    for p in parents:
        if isinstance(p, dict):
            if not isinstance(p.get("contribution"), str) or not p["contribution"].strip():
                raise ValueError("parent objects require a nonempty contribution")
            p = p.get("attempt_id")
        if not isinstance(p, str) or not p.strip():
            raise ValueError("parent ID must be a nonempty string")
        out.append(p)
    if len(set(out)) != len(out):
        raise ValueError("duplicate parent IDs")
    return out


def validate_node(node: dict, existing: dict[str, dict]) -> list[str]:
    """Return list of violations (empty = legal). existing: attempt_id -> node."""
    errs: list[str] = []
    origin = node.get("origin")
    try:
        parents = parent_ids(node)
    except ValueError as e:
        return [str(e)]
    if origin not in ORIGINS:
        errs.append(f"unknown origin: {origin!r}")
    else:
        lo, hi = ORIGINS[origin]
        if not (lo <= len(parents) <= hi):
            errs.append(f"origin {origin} requires {lo}..{hi} parents, got {len(parents)}")
    for p in parents:
        if p not in existing:
            errs.append(f"parent not found: {p}")
        elif existing[p].get("study_id") != node.get("study_id"):
            errs.append(f"parent {p} study mismatch")
        elif existing[p].get("evaluator_version") != node.get("evaluator_version"):
            errs.append(f"parent {p} evaluator-version mismatch")
    if origin == "repair" and not node.get("repairs_node"):
        errs.append("repair requires repairs_node citation")
    elif origin == "repair" and node["repairs_node"] not in parents:
        errs.append("repair citation must identify a parent")
    # acyclicity: node id must not be its own ancestor
    nid, stack, seen = node.get("attempt_id"), list(parents), set()
    while stack:
        cur = stack.pop()
        if cur == nid:
            errs.append("cycle: node is its own ancestor"); break
        if cur in seen or cur not in existing:
            continue
        seen.add(cur)
        try:
            stack.extend(parent_ids(existing[cur]))
        except ValueError as e:
            errs.append(f"invalid ancestor {cur}: {e}")
    return errs


def ancestry(node_id: str, existing: dict[str, dict]) -> set[str]:
    out, stack = set(), [node_id]
    while stack:
        cur = stack.pop()
        if cur in out or cur not in existing:
            continue
        out.add(cur)
        stack.extend(parent_ids(existing[cur]))
    return out
