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

The single most useful signal, and it is not in any field: **who actually spoke
last, and what the last two messages say to each other.**

### The relay trap — read this before writing any query

`Workato Integrations` is **not a bot.** It relays human comments, prefixed
`**Comment by** @someone`, and it also posts automation. Filtering it by author
name throws away real comments — including Mark's own — and then reports the
wrong person as last to speak.

This is not hypothetical. On 2026-10-20 that exact filter made BTSUP-77725,
BTSUP-77579 and BTSUP-69584 read as "waiting on Mark" when he had already
delivered the work and was the last to speak. Four tickets got a wrong reply,
one requester was confused into asking "anything you need from me?", and Mark
had to correct the thread himself. `BTS-070` exists to stop it recurring.

So: resolve the true author from the body first, then classify.

```
if author is "Workato Integrations":
    if body starts with "**Comment by** @X":  true author = X
    else:                                      automation, skip
```

Only these are unconditionally automation: `Automation for Jira`, `BT Genie`,
`Assist`, `Atlassian Assist`. Most status noise is these, and sorting by
`updated` alone will say a ticket moved yesterday when nothing human has
happened in three months.

### Read the last two, never the last one

One message tells you who typed most recently. **Two tell you what was asked and
whether it was answered** — which is what decides the next step and who owns it.

On BTSUP-76347 the last message was Brandon confirming the Okta mapping; the one
before it was Mark asking Brandon to check. That pair says the *colleague* loop
closed and the *user* loop — Megan, still blocked — is open. Reading one line
pointed the reply at Brandon and asked an abstract question. `BTS-071`.

### Then classify

| Last true author | Ticket open | Action |
|---|---|---|
| Mark | yes | **close or follow up** (`BTS-072`) — never ask for scope already satisfied |
| requester | yes | ours to answer |
| colleague, answering Mark | yes | the user loop is probably still open — reply to **the user** (`BTS-073`) |

Addressing matters as much as content: name the person whose action closes the
ticket and give them exactly one thing to do. A colleague who answered an
internal question is not the audience; the person who cannot do their job is.

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
