# Cases

One file per decision. A case is the decision plus, later, what I actually did
with it. Together they are the training set: `reflect` reads them, `evals`
freezes the best of them as regression tests, `lib.metrics` counts them.

```json
{
  "id": "C-2026-10-20-0001",
  "created": "2026-10-20T14:02:11+00:00",
  "domain": "triage",
  "request": { "...": "the context the decision was made on" },
  "decision": { "...": "the typed envelope, including rules_fired" },
  "verdict": {
    "outcome": "edited",
    "corrected": { "disposition": "BUILD" },
    "why": "blast radius was the deciding factor, not effort",
    "at": "2026-10-20T16:40:03+00:00"
  },
  "supersedes": null
}
```

## Rules of the store

**Immutable once a verdict lands.** `lib.capture` refuses to overwrite one. A
revised view of a case is a new case with `supersedes` pointing at the old one.
Rewriting history here would silently invalidate every metric computed from it,
and the invalidation would be undetectable afterwards.

**The `why` is the asset.** Everything else can be regenerated from the request;
the one line explaining the correction cannot. A verdict of `edited` with an
empty `why` is a number for the ledger and nothing for `reflect` — which is why
`capture` refuses it.

**Cases are committed.** They are evidence, they are small, and they are the
only durable record of how my judgment moved. A case store that lives only on
one laptop is a case store that gets lost in a reinstall.

## Privacy

Requests quote real people. Keep names at the level the decision actually needs
— team and seniority drive rules (`TRI-050`), individual identity does not.
`requester.name: "redacted"` is fine and is what the examples use. Never copy a
credential, token or customer record body into a case; reference where it lives
instead.
