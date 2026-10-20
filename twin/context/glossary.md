# Glossary

Terms the rules use with a specific, narrow meaning. Where a word is overloaded
in the business, the definition here is the one the rule means.

**blast radius** — the set of recipes, objects, fields and reports a change can
affect, *looked up* rather than estimated. `impact.blast_radius.looked_up`
is a claim about whether the lookup was run, not about whether someone thought
about it.

**consequence of inaction** — what breaks if we never do this. Not "it would be
nice", not "it saves time" without a number. The single most load-bearing
field in the intake schema.

**declarative option** — a Salesforce-native path: flow, validation rule, field
config, formula. The test in `TRI-020` is whether it meets a *written*
requirement, not whether it meets every imaginable future one.

**policy** — a business rule that decides an outcome for a person: who gets a
lead, what discount is allowed, when a deal counts. Distinct from a data rule,
which decides what a field may contain. Policy needs a named owner (P3); data
rules do not.

**reversible** — undoable in minutes, by me, without a data restore. A change
that needs a backup to undo is not reversible for the purposes of `RSK-002`.

**novel (decision)** — no rule fired. Means the system is improvising, which is
fine in reasoning and forbidden in side effects (`RSK-006`).

**upheld / overturned** — a rule is upheld when I approved a decision it
contributed to, and overturned when I changed a field it set. Both are counted
per firing, in `_stats.json`, by `capture` only.

**credit request vs credit investigation** — the distinction that decides who
owns a ZoomInfo credit ticket. A *request* is an ask for additional credits: a
budget decision, so Marketing Ops (`BTS-034`). An *investigation* is a credit
behaving unexpectedly — exhausted early, a separate pool, numbers not adding up
— which needs the admin console, so BT Support's ZoomInfo admin (`BTS-033`).
Not procurement-vs-reissue, which was the first and wrong reading of this.

**draft** — produced, shown, and not sent. Applies to Slack replies, Jira
comments, emails and record writes alike. There is no tier at which a draft
becomes an action implicitly; it takes a click.
