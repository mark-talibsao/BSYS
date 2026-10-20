"""Case store.

A case is one decision plus, later, what I actually did with it. Cases are the
training set: `reflect` reads them, `evals` freezes the best of them as
regression tests.

Cases are immutable once a verdict is recorded. A revised view of a case is a
new case that `supersedes` it — rewriting history here would quietly invalidate
every metric computed from it.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

REPO = Path(__file__).resolve().parent.parent
CASES = REPO / "cases"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _dir_for(ts: str) -> Path:
    d = CASES / ts[:4]
    d.mkdir(parents=True, exist_ok=True)
    return d


def next_id(ts: str | None = None) -> str:
    ts = ts or now()
    day = ts[:10]
    existing = list(_dir_for(ts).glob(f"C-{day}-*.json"))
    return f"C-{day}-{len(existing) + 1:04d}"


def path_for(case_id: str) -> Path:
    return CASES / case_id[2:6] / f"{case_id}.json"


def create(domain: str, request: dict, decision: dict) -> dict:
    ts = now()
    case = {
        "id": next_id(ts),
        "created": ts,
        "domain": domain,
        "request": request,
        "decision": decision,
        "verdict": None,
        "supersedes": None,
    }
    save(case)
    return case


def save(case: dict) -> Path:
    p = path_for(case["id"])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(case, indent=2, sort_keys=False) + "\n")
    return p


def load(case_id: str) -> dict:
    return json.loads(path_for(case_id).read_text())


def all_cases() -> Iterator[dict]:
    for p in sorted(CASES.glob("*/C-*.json")):
        yield json.loads(p.read_text())
