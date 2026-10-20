---
name: mine
description: Bootstrap rules from history — mine past Slack threads, Jira tickets, Gong calls and existing recipes for decisions Mark has already made, and propose them as rules. Use for cold-start on a new domain, before there are corrections to learn from. Keywords: mine, bootstrap, cold start, retro, extract rules, learn from history, new domain.
---

# Mine prior art

The cold-start problem: the correction loop needs corrections, and corrections
need a system that already decides. Mining bridges the gap by extracting
decisions I have already made, from the record.

## What makes a minable decision

Look for a **decision plus its reason**, together. A ticket that says "closed —
won't do" is a decision without a reason and teaches nothing. A Slack thread
where I said "not doing this, it bakes Deal Desk's policy into a recipe and
then I own their approvals" is a rule.

Sources, roughly in order of yield:
- **Slack threads in the Business Systems channels** — highest yield, because
  the reason is usually in the same message as the call.
- **Jira resolution comments** — reliable decisions, often missing the reason.
  Pair with the thread that preceded them.
- **Recipes with revealing comments** — a step commented "deliberately not
  doing X because Y" is a design rule.
- **Gong calls with internal stakeholders** — good for routing and ownership
  boundaries; noisy for everything else.

## Steps

1. **Pick one domain.** Mining everything at once produces a pile of
   near-duplicate rules with no precedence relationship between them. The
   domain map is in `twin/charter.md`.

2. **Pull 20–40 instances.** More than that and the clustering gets sloppy.

3. **Extract candidates** as `{decision, stated_reason, source_link}`. Keep the
   source link. A mined rule without provenance cannot be audited later, and
   mined rules are the ones most likely to be subtly wrong.

4. **Reject the ones without a reason.** Ruthlessly. A decision whose reason
   you inferred is a decision you invented. It will fire confidently and be
   wrong in exactly the cases that matter.

5. **Cluster into candidate rules.** A rule needs 2+ consistent instances. A
   single instance is a case, not a rule — file it in `cases/` and let the
   normal loop pick it up.

6. **Write them** into the domain's `.rules.yaml` with `status: proposed`,
   `confidence: 0.5`, `provenance.source: retro-mining`, and the source links
   in `provenance.cases`. Proposed status caps decision confidence at 0.5 and
   forces a review flag — mined rules should feel provisional, because they are
   reconstructions rather than things I said in the abstract.

7. **Write the `because` in my voice, from my words.** Use what I actually said
   in the source. If you find yourself writing a plausible-sounding reason
   rather than quoting one, you have crossed from mining into authoring — stop
   and flag the candidate for me to write myself.

8. **Golden-case the clear ones**, run `python3 -m evals.run`, open a PR.

## The failure mode to watch

Mining produces rules that describe what I *did*, which includes the times I
was wrong, rushed, or conceding to pressure. Three instances of me caving to
the same VP is a pattern, and encoding it would automate the caving.

When a cluster looks like a habit rather than a judgment, flag it as a question
in the PR instead of a rule: *"you did X three times — is that your rule, or
three bad weeks?"* That question is the most valuable thing a mining pass
produces, and it is the one thing the automated loop can never ask itself.
