# Systems map

The world model. Rules reference these names; keep them stable.

> **Scaffold.** The platform list below is accurate. The ownership, volume and
> integration-path columns are the parts only you can fill, and they are the
> parts rules will depend on — `TRI-004` is only as good as the dependency
> picture behind it. Fill as you go; an empty cell is honest, a guessed one is
> not.

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

## Integration inventory

Not enumerated here on purpose — the dependency tracker is authoritative and
this file would go stale within a month. Look it up; do not remember it.
