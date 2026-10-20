---
name: reflect
description: Weekly learning pass — read the captured corrections, find where the rules were wrong, and propose rule changes as a reviewable PR. This is the self-learning loop. Use weekly, or after a run of corrections. Keywords: reflect, weekly review, learn, improve rules, retro, propose rules, what did I correct.
---

# Reflect

Turn accumulated corrections into proposed rule changes. This is the only path
by which the system's behaviour changes, and it is deliberately slow, visible
and gated.

## Steps

1. **Read the evidence.**
   - `python3 -m lib.metrics` — agreement, coverage, and which rules are being
     overturned.
   - Every case with a verdict since the last reflect pass.

2. **Cluster the corrections by cause, not by field.** Three cases where I
   changed `disposition` for three different reasons are three findings. Three
   cases where I changed different fields for the same reason are one finding,
   and it is the one worth acting on.

3. **For each cluster, name which failure it is.** The remedy differs:

   | failure | what you see | remedy |
   |---|---|---|
   | missing rule | `novel: true`, or rules fired but none addressed the real consideration | propose a new rule, `status: proposed`, confidence 0.5 |
   | wrong predicate | right rule, fires in cases it should not | tighten `when` |
   | wrong precedence | right rules fired, wrong one won | adjust `precedence`, and say what now outranks what |
   | stale rule | consistently overturned | propose retirement with a written reason |
   | bad `because` | rule fires correctly but its stated reason is not the real one | rewrite `because` — this is a real finding, not a cosmetic one |

   The last row is the easiest to skip and the most corrosive to leave. A rule
   whose stated reason is not its real reason will be applied correctly until
   the day it is applied by analogy, and then it fails in a way nobody can
   diagnose.

4. **Write the diff.** New rules start `status: proposed`, `confidence: 0.5`,
   `provenance.source: correction`, and `provenance.cases` listing the case IDs
   that produced them. Provenance is not bookkeeping — it is how a future
   reflect pass tells a rule earned from evidence from one someone asserted.

5. **Add a golden case** for anything the change is meant to fix, in
   `evals/golden/`, with the comment explaining *why it is golden* — what
   future mistake it is there to catch.

6. **Run the gate:** `python3 -m evals.run`. A broken golden case means either
   the change is wrong or the case is stale and needs retiring with a written
   reason. There is no third option, and "probably fine" is not one.

7. **Open a PR.** Never commit rule changes directly to the working branch.
   The PR body states: what I corrected, what the system now believes, and what
   would prove it wrong.

## Boundaries

- Never propose a change to `20-risk.rules.yaml`. Tiering grows only by Mark's
  explicit edit. If the corrections suggest a tier is wrong, say so in the PR
  body as a question and leave the file alone.
- Never raise a rule's confidence by hand. Confidence is derived from the
  ledger; a hand-raised number is a lie that compounds.
- Proposing fewer, better rules beats proposing many. A rule set that grows
  every week and never retires anything is a rule set nobody is honest with.

## Output

A PR, plus three sentences to me: what changed, what it was based on, and what
you are still unsure about. The third sentence is the useful one.
