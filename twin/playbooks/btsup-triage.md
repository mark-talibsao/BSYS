# Playbook — BT support triage (BTSUP + #ask-bt)

Companion to `judgment/11-btsup.rules.yaml`. The rules decide *what*; this is
the mechanics of carrying it out in Jira without leaving a mess behind.

## 1. Scope first

A BTSUP ticket is mine only when I am **assigned or mentioned** (`BTS-001`).
The wider queue is the whole BT service desk — the last 14 days carried 80
tickets, 53 of them auto-generated Firefighter provisioning. Never triage from
the unfiltered queue; never mine rules from it.

Useful JQL:

```
project = BTSUP AND assignee = currentUser() AND resolution = EMPTY ORDER BY updated ASC
```

Oldest-updated first, because staleness is the thing that hides.

**Careful with `comment ~ "Mark Talibsao"`** to find mentions. It matches any
comment containing the name, including the 300-row user tables people paste
into tickets. It returned a false positive on the first run. Verify the hit is
actually a comment *by* or *addressed to* me before treating it as mine.

## 2. Who is waiting on whom

The single most useful signal, and it is not in any field: **the last non-bot
commenter.**

- Last human comment is mine → waiting on the requester.
- Last human comment is someone else's → waiting on me.

Bots to filter: `Automation for Jira`, `Workato Integrations`, `BT Genie`,
`Assist`, `Atlassian Assist`. Most status noise in a thread is these, and
sorting by `updated` alone will tell you a ticket moved yesterday when nothing
human has happened in three months.

`Workato Integrations` is ambiguous — it both relays human comments ("**Comment
by** @someone") and posts automation. Read the body, not the author.

## 3. Closing a ticket properly

**The Resolved transition does not set the resolution field.** This is the trap.
A ticket transitioned to Resolved or Closed with `resolution` still null stays
invisible to "done" filters and keeps appearing in every `resolution = EMPTY`
query — forever. BTSUP-53821 sat Closed-but-unresolved for four months for
exactly this reason, and it is why `BTS-050` and `BTS-052` both carry
`require: set_resolution`.

The close is therefore always three steps, in this order:

1. **Comment** — what the root cause was, what was done, and an invitation to
   reopen. Post before the status change so the requester's notification
   carries the explanation.
2. **Transition** to Resolved.
3. **Set the resolution explicitly** as a separate field edit.

Transition paths differ by current status and issue type, so read the available
transitions rather than assuming an id:

| From | To Resolved |
|---|---|
| Biz Sys Review | `141` "Resolved" |
| In Progress | `111` "Work Completed" |
| In Triage | **no direct path** — go `41` In Progress first, then `111` |

## 4. Resolution values

| Value | When |
|---|---|
| `Done` | work completed, requester confirmed |
| `Fixed` | a defect or misconfiguration was corrected |
| `Advice Provided` | no change made; the answer or workaround was the deliverable |
| `No Reply from User` | the follow-up ladder ran out (`BTS-052`) |
| `Cannot Reproduce` | the reported state was not observable |
| `Won't Do` | out of scope, or unactionable on the current path |
| `Escalated - BT` | handed to another team with the path named |

Pick the one that describes *why it is closing*, not how it felt. A ticket
closed because nobody replied is `No Reply from User`, even if the underlying
request was reasonable.

## 5. Before closing without confirmation

`BTS-041` says do not close on an unconfirmed fix — but the follow-up ladder
(`BTS-051`, `BTS-052`) overrides it once the user has been chased twice. When
closing without confirmation, the comment must say so plainly and invite
reopening. "We never got an explicit confirmation from you, so if X is still
happening please reopen" is honest and costs nothing.
