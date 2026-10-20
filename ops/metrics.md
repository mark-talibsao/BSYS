# The bar

What this system has to demonstrate before it earns anything beyond
draft-and-approve. Written now, while it is easy to be honest, rather than
later when I want it to be true.

## The three numbers

`python3 -m lib.metrics` reports agreement, coverage and per-rule overturn
together, because each is misleading alone:

- **Agreement** — share of decided cases approved unedited. On its own it is
  trivially gameable: a system that answers `CLARIFY` to everything is never
  wrong and never useful.
- **Coverage** — share of decisions where a rule actually fired. This is what
  stops agreement being bought with abstention.
- **Overturn, per rule** — which specific rule I keep overriding. Tells me what
  to fix, not just that something is off.

## Gates

| Gate | Requires | Grants |
|---|---|---|
| G0 — today | nothing | draft-only, everything approved by me |
| G1 | 30+ decided cases, agreement ≥ 70%, coverage ≥ 60% | the system's disposition leads the draft instead of me writing it fresh |
| G2 | 100+ cases, agreement ≥ 85%, coverage ≥ 80%, no active rule above 25% overturn | `R1` actions batch-approve: one click for a run of internal, reversible writes |
| G3 | sustained G2 across two quarters, with an incident review on every miss | promote the stable playbooks into Workato recipes and a Genie, where they run without a Claude session |

G1 is deliberately unambitious. The failure mode I am guarding against is not a
system that is too cautious — it is one that gets trusted at 70% because the
first ten cases went well.

## What would make me shut it off

- Agreement above 90% with coverage below 50%. That is not a system that agrees
  with me; it is a system that has learned to abstain and is being scored on it.
- Any `R0`/`R1` action taken that I would not have taken, of any size. The
  tiering is the whole safety argument; one breach invalidates it.
- Rules accumulating without retirements. A rule set that only grows is a rule
  set nobody is being honest with, and its confidence numbers are decoration.
- Corrections stop being captured. The loop is the product. If capture lapses
  for a month, the rules are a snapshot of what I thought in October and should
  be treated as stale rather than authoritative.

## Known measurement problems

Agreement is measured against my own approval, which means it measures
consistency with me, not correctness. A rule I consistently approve can still be
wrong — the eval suite and the `because` lines are the only defense, and both
depend on being read rather than skimmed.

There is no counterfactual. I never see the decisions the system would have
made on requests I handled without running it, so coverage is optimistic by an
unknown amount.
