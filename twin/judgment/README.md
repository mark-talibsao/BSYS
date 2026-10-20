# The rule format

Read this before editing anything in this directory. The format exists to make
three things possible that prose cannot do: **trace** a decision back to the
reasons that produced it, **test** whether a change to my thinking breaks my
past calls, and **measure** whether the system agrees with me.

## 1. The decision envelope

Every decision in every domain emits this shape. Domains add fields; none may
remove these.

```yaml
id:          D-2026-10-20-0014     # stable, sortable
domain:      triage
input_ref:   cases/2026/C-...json  # what was decided on
disposition: ROUTE                 # the call itself, from the domain's enum
confidence:  0.72                  # 0–1, see §4
rules_fired: [TRI-004, TRI-030]    # ordered, every rule that set a field
novel:       false                 # true when rules_fired is empty
conflicts:   []                    # rules that set the same field differently
escalate:    []                    # reasons a human must look; non-empty blocks
proposed_action:                   # what would happen on approval — never runs
  kind: slack_reply
  target: "#biz-systems-requests"
  body: "..."
rationale:   "One paragraph, my voice, naming the tradeoff."
```

`rules_fired` is not decoration. A decision that cannot name its reasons is a
decision the loop cannot learn from, and `reflect` treats it as a coverage gap.

## 2. The rule

```yaml
- id: TRI-030
  title: Governance question wearing a systems costume
  status: active            # active | proposed | retired
  precedence: 60            # higher wins a conflict; default 50
  when:
    all:
      - { field: request.asks_to, op: in, value: [bypass, exception, override] }
      - { field: request.blocked_by, op: eq, value: process }
  then:
    set:
      disposition: ROUTE
      owner: process_owner
    escalate: "Process exception — not a systems change."
  because: >
    A request to make the system allow something the process forbids is a
    request to change the process. Building the bypass makes me the owner of a
    decision that was never mine, and the exception becomes permanent.
  provenance:
    source: authored        # authored | correction | retro-mining
    cases: []
  confidence: 0.9
  added: 2026-10-20
```

Outcome counts are **not** in the rule file. They live in `_stats.json`, which
is machine-owned — `capture` writes it, `rules.py` merges it at load. The split
is deliberate: a serializer writing back into these files would strip the
comments and reflow the `because` blocks, and the reasoning is the part worth
keeping. Humans own the YAML, the machine owns the ledger, neither rewrites the
other.

### Predicates

Leaves are `{field, op, value}`. `field` is a dotted path into the decision
context. Operators:

`eq` `ne` `in` `not_in` `contains` `gt` `gte` `lt` `lte` `matches` (regex)
`exists` `missing` `any_in` (list intersects list) `all_in`

Combinators nest freely: `all` `any` `none`.

A missing field is not an error — it fails the predicate, except under `missing`
and `none`. This matters: incoming requests are ragged, and a rule set that
crashes on a half-filled intake form is a rule set nobody runs.

### Conflicts

Every matching rule fires. When two rules set the same field to different
values, the higher `precedence` wins and the loser is recorded in `conflicts`.
Equal precedence is **not** resolved silently — the field is left unset and the
decision escalates. Silent arbitrary resolution is how a rule set rots without
anyone noticing.

## 3. `because` is the actual artifact

The `when`/`then` is the executable part, but `because` is the part worth
keeping. Write it as the reason, not the restatement:

- bad: "Because requests that ask to bypass should be routed."
- good: "Building the bypass makes me the owner of a decision that was never
  mine, and the exception becomes permanent."

If you cannot write a `because` that would survive being read back to you by a
skeptical colleague, you do not have a rule. You have a preference, and it
belongs in the playbook as a default, not here.

## 4. Confidence, and how a rule earns it

| status | meaning | may set fields? |
|---|---|---|
| `proposed` | born from one correction or a mining pass; unproven | yes, but caps decision confidence at 0.5 and forces a review flag |
| `active` | upheld 3+ times with no overturn in the last 10 firings | yes |
| `retired` | overturned past threshold, or superseded | no — kept as evidence |

Promotion and demotion are computed, not asserted — `lib/rules.py` derives them
from the `_stats.json` ledger at load time. Do not hand-edit the ledger; the
numbers are only meaningful if every one of them came from a real correction.

Decision confidence starts at the minimum confidence of the rules that fired,
then takes penalties: `-0.2` if any fired rule is `proposed`, `-0.3` if any
conflict is **unresolved** (an equal-precedence tie). A `novel` decision — no
rule fired at all — is floored at `0.1`. Anything below `0.5` escalates
regardless of disposition.

A precedence-resolved override is recorded in `conflicts` but costs nothing. It
means the rule set had an opinion about which consideration outranks which,
which is the opposite of uncertainty.

The numbers are a bookkeeping device, not a probability. They exist so that
"the system is confident" is a claim with a definition behind it.

## 5. Changing a rule

1. Never edit a rule file during a task. Rules change between tasks, by PR.
2. `python3 -m evals.run` must pass before merge. A rule change that breaks a
   golden case is either a wrong change or a case that needs retiring with a
   written reason — those are the only two options.
3. Overturning a rule is normal. Retire it, write why, and leave it in the file.
   A rule set with no retirements is a rule set nobody is honest with.
