"""Is this thing actually working?

    python3 -m lib.metrics

Three numbers decide whether the system earns more autonomy, and they are
reported together on purpose — each one is misleading alone.

  agreement   share of decided cases I approved unedited.
              Alone it is gameable: a system that only ever says CLARIFY is
              never wrong and never useful.
  coverage    share of decisions where at least one rule fired.
              This is what stops agreement being gamed by abstention.
  overturn    per-rule debit rate. Finds the specific rule that is wrong,
              rather than telling me the system "feels off".
"""

from __future__ import annotations

from collections import Counter

from lib import cases, rules


def main() -> int:
    all_cases = list(cases.all_cases())
    decided = [c for c in all_cases if c.get("verdict")]

    print(f"\n  cases            {len(all_cases)}  ({len(decided)} with a verdict)")
    if not decided:
        print("\n  No verdicts yet — every number below is undefined, not zero.")
        print("  Decide on real requests, then capture what you actually did.\n")
        return 0

    outcomes = Counter(c["verdict"]["outcome"] for c in decided)
    agreement = outcomes["approved"] / len(decided)
    covered = sum(1 for c in decided if not c["decision"].get("novel"))
    escalated = sum(1 for c in decided if c["decision"].get("escalate"))

    print(f"  agreement        {agreement:.0%}   " + "  ".join(f"{k}={v}" for k, v in outcomes.items()))
    print(f"  coverage         {covered / len(decided):.0%}   (a rule fired)")
    print(f"  escalation rate  {escalated / len(decided):.0%}")

    ledger = rules.load_stats()
    by_id = {r.id: r for r in rules.load("triage") + rules.load("risk")}
    noisy = [
        (rid, s) for rid, s in ledger.items()
        if s.get("fired", 0) >= 3 and s.get("overturned", 0) / s["fired"] > 0.25
    ]
    if noisy:
        print("\n  rules I keep overriding:")
        for rid, s in sorted(noisy, key=lambda x: -x[1]["overturned"] / x[1]["fired"]):
            r = by_id.get(rid)
            print(f"    {rid}  {s['overturned']}/{s['fired']} overturned   {r.title if r else ''}")
        print("    → these are the rules reflect should propose changes to first.")

    print("\n  The bar for more autonomy is in ops/metrics.md.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
