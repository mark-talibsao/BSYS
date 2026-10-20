# Stakeholders

> **Scaffold — fill this yourself.** Deliberately left empty rather than
> populated with plausible-looking names. A fabricated stakeholder map is worse
> than none: rules would route to people who do not hold the decision, and the
> error would be invisible until something lands on the wrong desk.

What each entry needs, and why the system needs it:

```
- team:
  decision_owner:        # who can say yes, not who asks
  escalation_path:
  what_they_own:         # the policy, not the system
  what_they_ask_me_for:  # recurring request shapes → candidates for playbooks
  known_friction:        # where handoffs break; informs ROUTE warmth
```

`decision_owner` is the field that matters. Most routing failures are not
"wrong team" — they are "right team, person who cannot approve it", and the
request comes back a week later with nothing decided.

## What stays out of here

Political read, trust level, who is about to escalate and why. P8 is explicit:
the system has no standing to hold that, and writing it down would invite rules
to act on it. Where a decision turns on it, the output is an escalation to me.
