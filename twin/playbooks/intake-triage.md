# Playbook — request intake & triage

The pilot domain. Every incoming ask — Slack, Jira, email, a hallway "quick
question" — goes through this before it gets effort.

## 1. Procedure

1. **Capture the raw ask verbatim.** Do not paraphrase it into the shape you
   expect. The words people choose carry the real request, and "can you just…"
   is diagnostic.
2. **Fill the context** (§2). Fields you cannot fill stay empty — an empty
   field is information, and guessing one to make a rule fire is the single
   easiest way to corrupt this system.
3. **Look up blast radius.** `search_recipe_dependencies` for anything touching
   a recipe, object or field. This is not optional: `TRI-004` blocks the
   decision until `impact.blast_radius.looked_up` is true, because P1 says so.
4. **Run the decision.** `python3 -m lib.triage decide --file <request>.yaml`
5. **Read the `because` lines, not just the disposition.** If a rule's reasoning
   does not actually apply to this request, that is a correction waiting to
   happen — capture it rather than quietly ignoring the output.
6. **Draft the response** in the shape §4 gives for the disposition.
7. **Send it yourself.** Nothing here executes.
8. **Capture the verdict** — `python3 -m lib.capture`. This is the step that is
   easy to skip and the only step that makes the system improve.

## 2. Context schema

```yaml
request:
  title:                       # one line, for humans
  source:                      # slack | jira | email | meeting | self
  raw:                         # the ask, verbatim
  requester: { name:, team:, seniority: }   # ic | manager | director | vp | svp | cxo
  topic:                       # pricing | commission | campaign_strategy | ...
  asks_for: []                 # new_field | new_object | new_report | new_integration
                               # bug_fix | access | permission_change | data_change
                               # enhancement | question
  asks_to: []                  # bypass | exception | override | suppress_validation
  systems: []                  # salesforce | workato | gong | outreach | marketo
                               # chilipiper | dnb | snowflake
  audience:                    # internal | external_customers
  blocked_by:                  # process | system | data | access | none
  states_problem:              # bool — did they describe a problem?
  states_solution:             # bool — did they hand down an implementation?
  has_written_requirements:    # bool
  consequence_of_inaction:     # none | unknown | inconvenience | <describe it>
  deadline_days:               # int
  users_affected:              # int
  revenue_linked:              # bool
  recurring:                   # bool — will this be asked again?
  similar_prior_requests:      # int
  production_impact:           # bool — is something broken right now?
  encodes_policy:              # bool — does this bake a business rule into plumbing?
  policy_owner_signed_off:     # bool
  declarative_option_exists:   # bool — flow / validation rule / native feature
  declarative_meets_written_requirement: # bool
  duplicate_of:                # ticket ref, or omit
  effort_band:                 # XS | S | M | L | XL
impact:
  blast_radius:
    looked_up:                 # bool — did you actually run the lookup?
    recipes:                   # int
    objects: []
  records_affected:            # int
  reversible:                  # bool
action:                        # what would happen on approval
  kind:
  system:
  environment:                 # dev | production
  audience:                    # internal | customer | prospect | partner | external
  reversible:                  # bool
  records_affected:            # int
```

Two fields do disproportionate work. `consequence_of_inaction` kills roughly a
third of requests on its own. `declarative_option_exists` decides CONFIG vs
BUILD, which is the difference between an afternoon and a thing I own forever.

## 3. Dispositions

| | meaning | what I owe the requester |
|---|---|---|
| `CLARIFY` | cannot decide yet | the specific questions, not "more detail please" |
| `DUPLICATE` | already tracked | the link, and who to follow |
| `ROUTE` | not mine | the owner's name, and a warm handoff if it is political |
| `DECLINE` | not worth it | the reason **and** the nearest cheap alternative (P6) |
| `CONFIG` | solvable declaratively | what I'll change, and when |
| `BUILD` | genuine integration work | scope, blast radius, effort band, sequencing |
| `QUEUE` | real but not now | where it sits and what would move it up |

## 4. Response shapes

**ROUTE** — name the owner, say why in one sentence, offer the handoff.
Never route by forwarding silently; that reads as a brush-off and comes back.

**DECLINE** — the consequence of inaction is the argument. "Nothing breaks if
we don't, and three things break if I stop what I'm on" is honest and lands.
Then the alternative: the existing report, the manual workaround, the smaller
version.

**BUILD** — lead with blast radius, then effort, then sequencing. In that order
every time; it trains people to ask about impact before deadline.

**CLARIFY** — ask the four, and say why you are asking: *what breaks if we do
nothing, who is affected, what you do today instead, what "done" looks like.*

## 5. Known gaps

- Effort banding is not encoded. `effort_band` is a human input today; the
  system consumes it but cannot estimate it.
- No rule yet distinguishes "urgent because quarter-end" from "urgent because
  the requester is loud". That distinction is real and currently lives only in
  my head — a candidate for the first mined rule.
- Political context is deliberately absent (P8). `TRI-050` is a blunt stand-in.
