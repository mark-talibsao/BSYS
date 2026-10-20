# BSYS — a working model of how I decide

> Automate the work out of it — as a Sr. Business Systems professional.

This repo is not a folder of prompts. It is an attempt to make my **judgment**
executable: typed decisions, addressable rules, falsifiable claims, and a
correction loop that turns every "no, not like that" into a versioned diff.

## The thesis

You cannot automate judgment by writing prose about it. Prose is unfalsifiable —
you can't diff it, test it, or tell when it has gone stale. So judgment here is
encoded as four things that a machine can actually hold:

| | | |
|---|---|---|
| **Typed decisions** | every decision emits the same shape | you can compare mine to the system's |
| **Addressable rules** | every rule has an ID and is cited in the output | you can trace *why*, not just *what* |
| **Falsifiable rules** | every rule carries golden cases | changing a rule runs a regression suite |
| **Mechanical corrections** | an edit/reject mutates rule state and writes a case | learning rides on work I'm already doing |

## The loop

```
  incoming request
        │
        ▼
  ┌───────────┐   cites rule IDs   ┌──────────────┐
  │  decide   │───────────────────▶│  draft only  │   nothing executes
  └───────────┘                    └──────┬───────┘   without approval
        ▲                                 │
        │                     approve / edit / reject
        │                                 │
        │                                 ▼
        │                          ┌─────────────┐
        │                          │   capture   │  delta + one-line why
        │                          └──────┬──────┘
        │                                 ▼
        │                          ┌─────────────┐
        │                          │   cases/    │  the training set
        │                          └──────┬──────┘
        │                                 ▼
  ┌─────┴─────┐   PR of rule diffs  ┌─────────────┐
  │  rules/   │◀────────────────────│   reflect   │  weekly
  └───────────┘    gated by evals   └─────────────┘
```

A rule is never edited by the system directly. `reflect` proposes; `evals` gates;
I merge. That is the whole safety story on day one.

## Layout

```
twin/
  charter.md              who I am to this system; what it may and may not claim
  judgment/
    README.md             the rule format — read this first
    00-core-principles.md invariants that outrank every rule below
    10-triage.rules.yaml  pilot domain: request intake & triage
    20-risk.rules.yaml    risk tiering — what may ever run unattended
  playbooks/              step-by-step procedures a agent can execute
  context/                the world model: systems, stakeholders, vocabulary
cases/                    decisions + corrections; the training set
evals/                    golden cases; the regression suite for judgment
lib/                      rule engine, case store, triage CLI
ops/                      metrics: agreement rate, overturn rate, coverage
.claude/skills/           the invocable surface: /triage /capture /reflect /mine
```

## Quickstart

```bash
# decide on a request (draft only — never executes)
python3 -m lib.triage decide --file path/to/request.md

# record what I actually did with that draft
python3 -m lib.capture --decision <id> --verdict edited --why "blast radius, not effort"

# does the current rule set still reproduce my past calls?
python3 -m evals.run

# what is the system's agreement rate this month?
python3 -m lib.metrics
```

## Honest status

Encoded today: **request intake & triage**, draft-only, ~20 seed rules mined from
prior art and stated preference. Everything else in `twin/charter.md` is mapped
but not yet encoded. Agreement rate is unmeasured until there are corrections —
see `ops/metrics.md` for the bar this has to clear before anything is trusted.
