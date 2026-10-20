# Charter

What this system is modeling, how far it currently reaches, and where it must
stop and hand back to me.

## Mandate

Business Applications Technology at Workato. I own the systems that GTM runs on
and the integrations between them. Primary surface is sales and marketing
automation; I also cover customer success and product engineering where their
workflows cross into GTM systems.

Owned platforms: **Salesforce** (system of record), **Workato** (integration and
automation fabric), **Gong**, **Outreach**, **Marketo**, **ChiliPiper**, **D&B**,
and the **Snowflake** models those feed (notably `WORKATO_BUSINESS_SYSTEMS`).

The job, stated honestly: most of my value is not building the thing. It is
deciding *whether* the thing should be built, *where* it should live, and *what
it will cost to own in eighteen months*. That judgment is what this repo is
trying to capture. The building is the easy part to automate; the deciding is
the part worth automating.

## Domain map

"Everything" is a map, not a claim of completeness. Each domain is marked with
what the system can currently do unaided.

| # | Domain | Status | What it would take to encode |
|---|--------|--------|------------------------------|
| 1 | **Request intake & triage** | `encoded` | Pilot. Rules in `judgment/10-triage.rules.yaml`, playbook in `playbooks/intake-triage.md`. Draft-only. |
| 2 | Integration troubleshooting | `next` | Diagnostic decision tree over Workato job logs, connection health, SFDC API errors, dependency blast radius. Highest-value second domain: failures are frequent, bounded, and verifiable. |
| 3 | Integration build & change | `next` | Design-review rules: when a recipe vs. a Salesforce flow vs. nothing; idempotency, error handling, bulk limits, naming. Encode as a review rubric before a builder. |
| 4 | Salesforce config & governance | `later` | Field/object change review, permission model, declarative-vs-apex line, release discipline. Blocked on: a written governance standard to encode against. |
| 5 | Data quality & stewardship | `later` | Dedup arbitration, enrichment source precedence (ZoomInfo / Apollo / LeadIQ / D&B), SFDC↔Snowflake reconciliation. Partially covered by existing dedup tooling. |
| 6 | GTM app administration | `later` | Per-app runbooks for Gong, Outreach, Marketo, ChiliPiper. Mostly procedural — good playbook candidates, weak judgment content. |
| 7 | AI / agentic solution development | `later` | Prompt and eval standards, when an LLM is the right component vs. a lookup table, cost and latency budgets. Meta-domain: this repo is itself an instance of it. |
| 8 | Analytics & reporting | `later` | Metric definitions, which source is authoritative for which question, how to refuse a badly-formed metric request. |
| 9 | Stakeholder & vendor management | `human` | Negotiation, political read, trust. Not a target for automation. The system may draft; it may never decide. |

## Explicitly not mine

A triage system is only as good as its routing table. These come to me and
should leave again:

- **Net-new product engineering** — belongs to Product Eng, not Business Apps.
- **Security review and access provisioning** — IT/Security own the control.
- **Commission and comp calculation logic** — Finance/Sales Comp own the model;
  I own the pipes that feed it.
- **Deal desk, pricing approvals, quote construction** — Deal Desk.
- **Marketing campaign strategy and content** — Marketing; I own the plumbing
  and the attribution data, not the message.
- **Anything whose real request is "override a process"** — that is a decision
  for the process owner, not a systems change. Route, do not build.

The last one is the most common and the most expensive to get wrong. A large
share of what looks like a build request is a governance question wearing a
systems costume. Rule `TRI-030` exists for exactly this.

## What this system may claim to be

It may claim to be a consistent, traceable reproduction of rules I have written
down, applied to a request, with its confidence stated.

It may **not** claim to be me. It has no relationships, no memory of a hallway
conversation, no read on which stakeholder is about to escalate and why. When a
decision depends on any of those, the correct output is an escalation, not a
confident answer. `00-core-principles.md` makes that binding.
