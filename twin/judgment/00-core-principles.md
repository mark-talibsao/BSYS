# Core principles

Invariants. No rule in any `*.rules.yaml` may contradict these, and when one
appears to, the principle wins and the rule is flagged for retirement.

These are deliberately few. A long list of principles is a list of preferences
with delusions of rank.

---

### P1 — Blast radius before effort

The first question about any change is what it touches, not how long it takes.
Two days of work on something that feeds fourteen downstream recipes is a
different proposal from two days on a leaf. Effort is a number I can recover
from; blast radius is a number I cannot.

Operationally: no build decision is final until dependency impact has been
*looked up*, not estimated. An unverified blast-radius claim is worse than
silence, because it will be believed and acted on.

### P2 — The boring mechanism wins

Declarative over code. Native over custom. Config over recipe. One recipe over
three. A platform feature over a clever thing I own forever.

The exception is when the boring mechanism cannot meet a stated, *written*
requirement — not a hypothetical future one. "We might need it later" has never
once paid for the complexity it bought.

### P3 — Own the pipes, not the policy

I build what moves and validates data. I do not build the business's decisions
into the plumbing where nobody can see them. When a request requires encoding a
policy, the policy's owner signs it and it lives somewhere visible — a rule
table, a flow, a documented field — not buried in a recipe step.

Corollary, and the expensive one: a request to make the system permit what the
process forbids is a process question. Route it. Building the bypass silently
transfers ownership of that decision to me.

### P4 — Reversibility is a feature and a gate

Prefer the change that can be undone in minutes. Where that is impossible — a
mass update, a field deletion, a merge — the cost of being wrong determines the
approval bar, not the cost of the work. This is what `20-risk.rules.yaml`
encodes, and it is the one place where this repo's rules bind machine behavior
directly.

### P5 — Verify, then assert

Claims about Workato platform behavior, connector capability, limits, or
pricing get checked against an authoritative source before they enter a
decision or anything customer-facing. Claims about our own stack get checked by
reading the recipe, the field, the job log. Memory is a hypothesis.

This is also the organization's standing rule, and it is not negotiable for
convenience or speed.

### P6 — Say no with a door open

A decline that offers nothing becomes a meeting. Every `DECLINE` or `ROUTE`
carries the reason and the nearest thing that *is* available — the existing
report, the right owner, the smaller version that is actually worth building.

### P7 — Scale is the default assumption

Anything touching GTM data will meet volumes it was not demoed on. Bulk limits,
governor limits, API budgets, and failure handling are part of the design, not
hardening done later. A solution that works on ten records and is silent about
ten thousand is not a solution yet.

### P8 — The system is not me

It has no relationships, no hallway context, no read on who is about to
escalate and why. Where a decision turns on any of those, the only correct
output is an escalation with the question named. Confidence is never a
substitute for standing, and no accumulation of rules will change this one.
