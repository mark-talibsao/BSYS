"""Rule engine.

Loads `twin/judgment/*.rules.yaml`, evaluates predicates against a decision
context, fires every matching rule, resolves conflicts by precedence, and
derives rule status from recorded outcomes.

Design notes worth keeping in mind before editing:

* A missing field fails its predicate rather than raising. Incoming requests are
  ragged; a rule set that crashes on a half-filled intake form is a rule set
  nobody runs. `missing` and `none` are the deliberate exceptions.
* A rule may declare `then.stop: true`, making it terminal: when it matches,
  rules of *lower* precedence are not evaluated at all. This exists for scope
  gates. "This ticket is not mine" has to mean no further rule contributes,
  otherwise domain rules fire on work that was never ours and drag the
  decision's confidence around for no reason.
* Equal-precedence conflicts are never resolved silently. The field is left
  unset and the decision escalates, because silent arbitrary resolution is how a
  rule set rots without anyone noticing.
* `status` is computed from outcomes, not read from the file. The file's status
  field is advisory for humans reading the diff.
* Outcome counts live in `_stats.json`, not in the rule files. Rule files are
  hand-written and comment-heavy; a serializer writing back to them would strip
  the reasoning, which is the part worth keeping. The ledger is machine-owned,
  the YAML is human-owned, and neither rewrites the other.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml

REPO = Path(__file__).resolve().parent.parent
JUDGMENT = REPO / "twin" / "judgment"
STATS = JUDGMENT / "_stats.json"

_MISSING = object()


# ── predicate evaluation ────────────────────────────────────────────────────

def resolve(ctx: dict, path: str) -> Any:
    """Walk a dotted path. Returns _MISSING rather than raising."""
    cur: Any = ctx
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return _MISSING
    return cur


def _as_list(v: Any) -> list:
    if v is _MISSING or v is None:
        return []
    return list(v) if isinstance(v, (list, tuple, set)) else [v]


def test_leaf(ctx: dict, leaf: dict) -> bool:
    op = leaf["op"]
    actual = resolve(ctx, leaf["field"])
    expected = leaf.get("value")

    if op == "exists":
        return actual is not _MISSING and actual not in (None, "")
    if op == "missing":
        return actual is _MISSING or actual in (None, "")

    if actual is _MISSING:
        # Absent data cannot satisfy a positive assertion. `ne` is positive here
        # on purpose: "this field is not X" should not be true of a field that
        # was never collected, or every rule fires on an empty form.
        return False

    if op == "eq":
        return actual == expected
    if op == "ne":
        return actual != expected
    if op == "in":
        return actual in _as_list(expected)
    if op == "not_in":
        return actual not in _as_list(expected)
    if op == "contains":
        return expected in actual if isinstance(actual, (list, tuple, set, str, dict)) else False
    if op == "any_in":
        return bool(set(map(str, _as_list(actual))) & set(map(str, _as_list(expected))))
    if op == "all_in":
        return set(map(str, _as_list(expected))) <= set(map(str, _as_list(actual)))
    if op == "matches":
        return bool(re.search(str(expected), str(actual)))
    if op in ("gt", "gte", "lt", "lte"):
        try:
            a, e = float(actual), float(expected)
        except (TypeError, ValueError):
            return False
        return {"gt": a > e, "gte": a >= e, "lt": a < e, "lte": a <= e}[op]
    if op in ("gte_len", "lte_len"):
        n = len(_as_list(actual))
        return n >= expected if op == "gte_len" else n <= expected
    raise ValueError(f"unknown operator: {op!r}")


def test(ctx: dict, node: Any) -> bool:
    """Evaluate a predicate node: a leaf, a combinator, or a bare list (= all)."""
    if isinstance(node, list):
        return all(test(ctx, n) for n in node)
    if not isinstance(node, dict):
        raise ValueError(f"bad predicate node: {node!r}")
    if "field" in node:
        return test_leaf(ctx, node)
    if "all" in node:
        return all(test(ctx, n) for n in node["all"])
    if "any" in node:
        return any(test(ctx, n) for n in node["any"])
    if "none" in node:
        return not any(test(ctx, n) for n in node["none"])
    raise ValueError(f"bad predicate node: {node!r}")


# ── rules ───────────────────────────────────────────────────────────────────

@dataclass
class Rule:
    id: str
    title: str
    precedence: int
    when: Any
    then: dict
    because: str
    confidence: float
    declared_status: str
    stats: dict
    provenance: dict
    source_file: str

    @property
    def status(self) -> str:
        """Derived, not asserted. See twin/judgment/README.md §4."""
        if self.declared_status == "retired":
            return "retired"
        fired = self.stats.get("fired", 0)
        upheld = self.stats.get("upheld", 0)
        overturned = self.stats.get("overturned", 0)
        if fired >= 5 and overturned / fired > 0.4:
            return "retired"  # overturned past threshold; flagged for a written retirement
        if upheld >= 3 and overturned == 0:
            return "active"
        if self.declared_status == "active" and fired == 0:
            return "active"  # authored and not yet challenged
        return "proposed"


@dataclass
class Outcome:
    fields: dict = field(default_factory=dict)
    rules_fired: list[str] = field(default_factory=list)
    conflicts: list[dict] = field(default_factory=list)
    escalate: list[str] = field(default_factory=list)
    require: list[str] = field(default_factory=list)
    confidence: float = 0.0
    novel: bool = True

    def to_dict(self) -> dict:
        return {
            **self.fields,
            "rules_fired": self.rules_fired,
            "conflicts": self.conflicts,
            "escalate": self.escalate,
            "require": self.require,
            "confidence": round(self.confidence, 2),
            "novel": self.novel,
        }


def load_stats() -> dict:
    if not STATS.exists():
        return {}
    return json.loads(STATS.read_text())


def save_stats(stats: dict) -> None:
    STATS.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n")


def load(domain: str) -> list[Rule]:
    """Load every rule file for a domain, ordered by precedence then id."""
    ledger = load_stats()
    rules: list[Rule] = []
    for path in sorted(JUDGMENT.glob("*.rules.yaml")):
        doc = yaml.safe_load(path.read_text()) or {}
        if doc.get("meta", {}).get("domain") != domain:
            continue
        for r in doc.get("rules", []):
            rules.append(
                Rule(
                    id=r["id"],
                    title=r.get("title", ""),
                    precedence=r.get("precedence", 50),
                    when=r["when"],
                    then=r.get("then", {}) or {},
                    because=r.get("because", "").strip(),
                    confidence=float(r.get("confidence", 0.5)),
                    declared_status=r.get("status", "proposed"),
                    stats=ledger.get(r["id"], {}),
                    provenance=r.get("provenance", {}) or {},
                    source_file=path.name,
                )
            )
    rules.sort(key=lambda r: (r.precedence, r.id))
    return rules


def apply(ctx: dict, rules: Iterable[Rule]) -> Outcome:
    """Fire every matching rule and resolve the result.

    A matching terminal rule (`then.stop: true`) first prunes everything below
    its precedence, so a scope gate genuinely gates.
    """
    rules = [r for r in rules if r.status != "retired"]
    gates = [r for r in rules if r.then.get("stop") and test(ctx, r.when)]
    if gates:
        floor = max(g.precedence for g in gates)
        rules = [r for r in rules if r.precedence >= floor]

    out = Outcome()
    # field -> (precedence, value, rule_id)
    claims: dict[str, tuple[int, Any, str]] = {}
    contested: set[str] = set()
    fired: list[Rule] = []

    for rule in rules:
        if not test(ctx, rule.when):
            continue
        fired.append(rule)
        out.rules_fired.append(rule.id)

        for key, value in (rule.then.get("set") or {}).items():
            prior = claims.get(key)
            if prior is None or rule.precedence > prior[0]:
                if prior is not None and prior[1] != value:
                    out.conflicts.append(
                        {"field": key, "winner": rule.id, "loser": prior[2], "reason": "precedence"}
                    )
                claims[key] = (rule.precedence, value, rule.id)
                contested.discard(key)
            elif rule.precedence == prior[0] and prior[1] != value:
                out.conflicts.append(
                    {"field": key, "tied": [prior[2], rule.id], "reason": "equal precedence — unresolved"}
                )
                contested.add(key)

        if rule.then.get("escalate"):
            out.escalate.append(f"{rule.id}: {rule.then['escalate']}")
        for req in rule.then.get("require") or []:
            if req not in out.require:
                out.require.append(req)

    out.fields = {k: v for k, (_, v, _) in claims.items() if k not in contested}
    for key in sorted(contested):
        out.escalate.append(f"unresolved conflict on `{key}` — equal-precedence rules disagree")

    out.novel = not fired
    out.confidence = score(fired, out)
    if out.confidence < 0.5:
        out.escalate.append(f"confidence {out.confidence:.2f} below 0.5 floor")
    return out


def score(fired: list[Rule], out: Outcome) -> float:
    """Confidence is bookkeeping, not probability — see judgment/README.md §4."""
    if not fired:
        return 0.1
    c = min(r.confidence for r in fired)
    if any(r.status == "proposed" for r in fired):
        c -= 0.2
    # Only unresolved ties cost confidence. A precedence-resolved override is
    # the designed path — it means the rule set had an opinion about which
    # consideration outranks which, which is the opposite of uncertainty.
    if any("tied" in c_ for c_ in out.conflicts):
        c -= 0.3
    return max(0.0, min(1.0, c))
