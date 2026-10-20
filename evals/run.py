"""Regression suite for judgment.

    python3 -m evals.run
    python3 -m evals.run --verbose

A golden case is a request plus an assertion about what I would have decided.
They are the reason a rule change is a reviewable event rather than a vibe: if
you change a rule and a golden case breaks, exactly two things can be true —
the change is wrong, or the case is stale and needs retiring *with a written
reason*. There is no third option, and "it's probably fine" is not one.

Assertions available in a golden file's `expect` block:

    disposition      exact match
    owner            exact match
    risk_tier        exact match
    must_fire        every listed rule id fired
    must_not_fire    none of the listed rule ids fired
    escalates        bool — is this blocked for a human?
    min_confidence   float
    max_confidence   float
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from lib import decide as decider

GOLDEN = Path(__file__).resolve().parent / "golden"


def check(expect: dict, d: dict) -> list[str]:
    fails = []
    for key in ("disposition", "owner", "risk_tier", "priority", "mechanism"):
        if key in expect and d.get(key) != expect[key]:
            fails.append(f"{key}: expected {expect[key]!r}, got {d.get(key)!r}")

    fired = set(d.get("rules_fired", []) + d.get("risk_rules_fired", []))
    for rid in expect.get("must_fire", []):
        if rid not in fired:
            fails.append(f"{rid} did not fire")
    for rid in expect.get("must_not_fire", []):
        if rid in fired:
            fails.append(f"{rid} fired but should not have")

    if "escalates" in expect and bool(d.get("escalate")) != expect["escalates"]:
        fails.append(f"escalates: expected {expect['escalates']}, got {bool(d.get('escalate'))}")
    if "min_confidence" in expect and d["confidence"] < expect["min_confidence"]:
        fails.append(f"confidence {d['confidence']} below floor {expect['min_confidence']}")
    if "max_confidence" in expect and d["confidence"] > expect["max_confidence"]:
        fails.append(f"confidence {d['confidence']} above ceiling {expect['max_confidence']}")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="evals.run", description=__doc__)
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args(argv)

    files = sorted(GOLDEN.glob("*.yaml"))
    if not files:
        print("no golden cases — the rule set is currently untested")
        return 1

    passed, failed = 0, []
    print()
    for path in files:
        doc = yaml.safe_load(path.read_text())
        d = decider.decide(doc.get("domain", "triage"), doc)
        fails = check(doc.get("expect", {}), d)
        name = path.stem
        if fails:
            failed.append((name, fails))
            print(f"  FAIL  {name}")
            for f in fails:
                print(f"          {f}")
        else:
            passed += 1
            print(f"  pass  {name}  →  {d.get('disposition')}  ({d['confidence']})")
        if args.verbose:
            print(decider.explain(d, doc.get("domain", "triage")))

    print(f"\n  {passed}/{len(files)} golden cases reproduce my calls.")
    if failed:
        print("\n  A broken golden case means the change is wrong, or the case is")
        print("  stale and needs retiring with a written reason. Pick one.\n")
        return 1
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
