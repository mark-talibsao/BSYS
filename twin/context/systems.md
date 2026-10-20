# Systems map

The world model. Rules reference these names; keep them stable.

> Partly populated 2026-10-20 from observed BTSUP and #ask-bt traffic. Owner
> and change-window columns are still yours to fill — `TRI-004` is only as good
> as the dependency picture behind it. An empty cell is honest, a guessed one
> is not.

## Platforms

| System | Role | Owner | Change window | Notes |
|---|---|---|---|---|
| Salesforce | system of record for accounts, contacts, opps | | | everything downstream assumes SFDC is right |
| Workato | integration + automation fabric | | | prod recipe state is `R3` — see `20-risk.rules.yaml` |
| Snowflake | analytics store; `WORKATO_BUSINESS_SYSTEMS` schema | | | reporting truth, not operational truth |
| Gong | call recording + conversation intelligence | | | source for transcript-driven opp work |
| Outreach | sales engagement | | | |
| Marketo | marketing automation | | | lead lifecycle + attribution upstream |
| ChiliPiper | routing + scheduling | | | routing rules are policy — see P3 |
| D&B | firmographic enrichment | | | one of several enrichment sources; precedence undecided |

### Also in the real queue, absent from the first draft

| System | Role | Notes |
|---|---|---|
| Okta | SSO / identity | IT-owned. Sandbox refreshes break SSO until the user re-verifies by email (BTSUP-68078). Manually-created profiles get bad Okta mappings (BTSUP-77614). |
| Firefighter | app provisioning + approvals | "Provisioned" in Firefighter does not reliably mean provisioned in the app. Verify in the app. |
| Nooks | sales calling / SDR tooling | Active build area: Direct + Workato workspaces, needs SFDC, ZoomInfo, Apollo, LeadIQ, Gong connections. |
| BoostUp | forecasting | Recurring manual provisioning (A162). |
| Salesforce CPQ | quoting | Quote data centre must match the customer's; US is the default when unknown (BTSUP-75536). |
| NetSuite / Coupa / Tipalti | finance stack | Finance-owned; reaches Mark via address-sync and integration-user questions. |
| LinkedIn Sales Navigator | prospecting | Mark maintains the Sales Navigator CRM mapping **only**. LinkedIn Business Manager is not maintained (BTSUP-76443). |
| Claude / Codex / ChatGPT | AI tooling | Budget limits and MCP enablement are now a major inbound category with no written policy. |

## Standing facts worth encoding

- **SFDC is operational truth, Snowflake is analytical truth.** When they
  disagree about a live record, SFDC wins and the pipeline is the bug. When
  they disagree about a historical aggregate, Snowflake wins and the report
  reading SFDC directly is the bug. Most "the numbers don't match" escalations
  resolve to this distinction, and almost none of them start there.
- **Enrichment has no single winner.** ZoomInfo, Apollo, LeadIQ and D&B each
  win on different fields. Until precedence is written down per field, every
  enrichment arbitration is a judgment call and should be flagged as one rather
  than silently resolved.
- **Routing rules look like config and behave like policy.** ChiliPiper and
  assignment rules decide who gets paid attention. P3 applies.
- **Integration users are measured by consumption, never by last login.**
  `integration@workato.com` and `integrations.cs-external@workato.com` both run
  live automations and exist separately so API consumption can be attributed
  per department. A stale login date is not evidence of an idle account, and
  deactivating on one kills recipes silently (BTS-022).
- **Personal production connections never belong in a recipe.** AHQ workspaces
  already carry shared Salesforce connections; the request is a provisioning
  request, not a connection request (BTS-021).
- **CPQ Genie covers quotes and quote lines only** — not Orders or Contract
  changes, which live in the Salesforce CPQ process (BSYS-28150).

## Integration inventory

Not enumerated here on purpose — the dependency tracker is authoritative and
this file would go stale within a month. Look it up; do not remember it.
