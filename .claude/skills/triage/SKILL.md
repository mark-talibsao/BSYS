---
name: triage
description: Decide on an incoming Business Systems request — classify, size, route or decline — using the encoded rules in twin/judgment. Use when a request arrives via Slack, Jira, email or a meeting and needs a call. Produces a typed decision plus a drafted response; never executes. Keywords: triage, intake, request, "should we build this", prioritize, route, decline, new ask.
---

# Triage a request

## Before anything

Load `twin/judgment/00-core-principles.md`, `twin/charter.md`, and
`twin/playbooks/intake-triage.md`. The playbook's §2 is the context schema and
§4 is the response shapes — both are binding, not reference.

## Steps

1. **Capture the ask verbatim** into `request.raw`. Do not paraphrase it into
   the shape you expect. "Can you just…" is diagnostic and gets lost in a
   paraphrase.

2. **Fill the context** into a YAML file under `requests/`. A field you cannot
   determine stays empty. Guessing a field to make a rule fire is the single
   easiest way to corrupt this system — an empty field produces a CLARIFY,
   which is the correct outcome of not knowing.

3. **Look up blast radius for real.** Use
   `mcp__Workato_Dependency_Tracker_by_Workato_MCP__search_recipe_dependencies`
   for anything touching a recipe, object or field. Set
   `impact.blast_radius.looked_up: true` only if you actually ran it. `TRI-004`
   blocks the decision otherwise, and that block is the point.

4. **Run it:** `python3 -m lib.triage decide --file requests/<name>.yaml`

5. **Read the `because` lines.** If a fired rule's reasoning does not actually
   apply to this request, say so in your output — that is a correction waiting
   to happen, and noticing it is worth more than the decision was.

6. **Draft the response** in the shape §4 gives for the disposition. Lead with
   the call. For BUILD, blast radius first, then effort, then sequencing — in
   that order every time. For DECLINE and ROUTE, the alternative is mandatory
   (P6); a decline with nothing attached becomes a meeting.

7. **Hand it over.** Present the decision, the reasoning, and the draft. Do not
   post it, do not update the ticket, do not reply in Slack. Draft-only is the
   whole safety argument on day one.

8. **Tell them how to capture the verdict.** The case ID and the `lib.capture`
   command. This step gets skipped and it is the only step that makes the
   system improve.

## Verification

Any claim about Workato platform behaviour, connector capability or limits that
enters the reasoning gets checked against `mcp__AIRO_MCP__docs_get` first, and
cited. Set `decision.contains_unverified_platform_claim: true` if you could not
verify one — `TRI-051` will escalate it rather than let it ship.

## When no rule fires

Say so plainly: the decision comes back `novel: true` with confidence 0.1 and
tier R3. Decide anyway, mark it low-confidence, and name what would need to be
encoded. Do not reach for a rule that nearly matches — a rule stretched to fit
is worse than no coverage, because it looks like coverage in the metrics.
