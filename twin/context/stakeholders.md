# Stakeholders

Populated 2026-10-20 from observed routing in BTSUP and #ask-bt — who Mark
actually hands things to, not an org chart. Names are here because routing
without them fails in the specific way that matters: right team, wrong person,
nothing decided, request back in a week.

Work identities and team ownership only. No personal data, and requester names
stay out of `cases/` (see `cases/README.md`).

## Routing table

| When | Goes to | Evidence |
|---|---|---|
| Licensed-app provisioning (any app with seats) | **Firefighter** App Provisioning workflow | BTS-020; "raise an App Provisioning request via Firefighter" |
| Okta mapping, SSO loops, SAML errors | **IT** — Benny Tan, Brandon Tang | BTS-031; BTSUP-77436, 77614 |
| BT support triage, provisioning execution | **BT Support** — Anna Monica De Los Reyes, Ivan Yuri Uy, Marc Parilla | recurring co-assignees across the queue |
| Enrichment credit pools (ZoomInfo, Apollo, LeadIQ) | **Marketing Ops** — Rachel Cusumano, Filmer Rose Evangelista | BTS-030; "please work with Marketing Ops team" |
| Quote/pricing/approval policy | **Deal Desk** — Kiera Coggins, Jeff DaSilva | TRI-011; BSYS-28150 "Deferring to Deal Desk" |
| Vendor entitlement / CSM contact | **Megan Guerra** (finds the AE/CSM) | BTS-032; Marketo → Judy Weldin, Adobe |
| MCP / AI tooling direction | Kevin Deng, Michael Fan | DemandBase MCP access thread |
| Data warehouse, dbt, BI_DB | **BI team** | #ask-bt dbt and `bi_db.crossbeam` requests |

## Requesting teams

Sales Ops · Revenue Ops · Customer Success · Presales (Vivun replacement
programme) · EMEA SDR · Marketing Ops · Deal Desk · Product Eng · Finance
(Coupa/NetSuite/Tipalti).

Presales and the Vivun replacement are currently the densest source of real
build work — BSYS-29169, 29064, 29427, 29476, 29518 all hang off it.

## Bots and workflows that behave like stakeholders

- **BT Genie** — creates and transitions BTSUP tickets from #ask-bt. Most
  status noise in the channel is this, not a human.
- **Assist** — raises requests from Slack.
- **Firefighter** — app provisioning and approvals. Its "provisioned" status is
  not reliable on its own; several tickets are users provisioned in Firefighter
  but not actually in the app.

## Still missing

`decision_owner` per team — who can say yes, as distinct from who asks. The
routing table above is where things *go*, which is observable; who can *approve*
is not, and it is the field that most often decides whether a route lands or
bounces. Worth one pass to fill in by hand.

## Out of scope on purpose

Political read, trust level, who is about to escalate and why. P8: the system
has no standing to hold that, and writing it down would invite rules to act on
it. Where a decision turns on it, the output is an escalation to Mark.
