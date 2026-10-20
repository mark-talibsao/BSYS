"""Correction capture — the only mechanism by which this system learns.

    python3 -m lib.capture --case C-2026-10-20-0001 --verdict approved
    python3 -m lib.capture --case C-... --verdict edited \
        --set disposition=BUILD --why "blast radius, not effort"
    python3 -m lib.capture --case C-... --verdict rejected --why "this is Deal Desk's call"

What it does: records the verdict on the case (immutably), then credits or
debits every rule that fired. A rule that set a field I then changed is
debited; a rule whose output I left alone is credited. Status follows from the
ledger — see twin/judgment/README.md §4.

What it deliberately does not do: edit a rule. Corrections accumulate as
evidence; `reflect` turns accumulated evidence into a proposed rule diff; I
merge it. Nothing here writes to a `.rules.yaml`.
"""

from __future__ import annotations

import argparse
import sys

from lib import cases, rules

VERDICTS = ("approved", "edited", "rejected")


def parse_set(pairs: list[str]) -> dict:
    out = {}
    for pair in pairs or []:
        if "=" not in pair:
            sys.exit(f"--set expects key=value, got {pair!r}")
        k, v = pair.split("=", 1)
        if v.lower() in ("true", "false"):
            v = v.lower() == "true"
        elif v.lstrip("-").isdigit():
            v = int(v)
        out[k.strip()] = v
    return out


def credit(case: dict, verdict: str, corrected: dict) -> dict:
    """Update the outcome ledger for every rule the decision cited.

    Credit is per-rule and value-aware: losing a precedence contest is not the
    same as being wrong, and conflating them hides precedence bugs behind
    apparently-unreliable rules.
    """
    ledger = rules.load_stats()
    by_id = {r.id: r for r in rules.load(case["domain"]) + rules.load("risk")}
    fired = case["decision"].get("rules_fired", []) + case["decision"].get("risk_rules_fired", [])

    for rid in fired:
        s = ledger.setdefault(rid, {"fired": 0, "upheld": 0, "overturned": 0})
        s["fired"] += 1
        rule = by_id.get(rid)
        sets = (rule.then.get("set") or {}) if rule else {}
        if verdict == "approved":
            s["upheld"] += 1
        elif verdict == "rejected":
            s["overturned"] += 1
        else:
            # Edited: debit a rule only where it set a corrected field *to the
            # wrong value*. A rule that proposed what I corrected to was right
            # and merely lost on precedence — debiting it would teach the
            # ledger that the correct rule is the unreliable one, and the
            # precedence bug that actually caused the miss would go unrecorded.
            wrong = any(k in sets and sets[k] != v for k, v in corrected.items())
            s["overturned" if wrong else "upheld"] += 1
        s["last"] = case["id"]
    rules.save_stats(ledger)
    return ledger


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="lib.capture", description=__doc__)
    ap.add_argument("--case", required=True, dest="case_id")
    ap.add_argument("--verdict", required=True, choices=VERDICTS)
    ap.add_argument("--set", nargs="*", default=[], dest="corrections",
                    help="field=value — what it should have said")
    ap.add_argument("--why", default="", help="one line. This is the part that matters.")
    args = ap.parse_args(argv)

    case = cases.load(args.case_id)
    if case.get("verdict"):
        sys.exit(f"{args.case_id} already has a verdict. Cases are immutable — "
                 "record a new case that supersedes it.")
    if args.verdict in ("edited", "rejected") and not args.why:
        sys.exit("--why is required for edited/rejected. A correction without a "
                 "reason teaches the ledger a number and teaches reflect nothing.")

    corrected = parse_set(args.corrections)
    case["verdict"] = {
        "outcome": args.verdict,
        "corrected": corrected,
        "why": args.why,
        "at": cases.now(),
    }
    cases.save(case)
    credit(case, args.verdict, corrected)

    print(f"  {args.case_id}: {args.verdict}")
    if corrected:
        for k, v in corrected.items():
            print(f"    {k}: {case['decision'].get(k)!r} → {v!r}")
    if args.why:
        print(f"    why: {args.why}")
    if args.verdict != "approved":
        print("\n  queued for the next reflect pass. Rules change by PR, not here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
