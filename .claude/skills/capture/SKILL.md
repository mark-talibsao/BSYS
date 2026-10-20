---
name: capture
description: Record what Mark actually did with a drafted decision — approved, edited or rejected — and credit or debit the rules that produced it. Use immediately after a triage draft gets a verdict. Keywords: capture, correction, feedback, "that's wrong", approve, reject, verdict, learn from this.
---

# Capture a correction

The most valuable event in this system. A correction is worth more than ten
decisions, because decisions only exercise the rules and corrections change
them.

## Steps

1. **Identify the case.** The case ID from the triage run. If the decision was
   never saved as a case, there is nothing to learn from — note that and move
   on rather than reconstructing it from memory.

2. **Classify the verdict:**
   - `approved` — used as drafted.
   - `edited` — right shape, wrong in some fields. Record exactly which fields
     via `--set field=value`. Only the rules that set a changed field get
     debited, which is why precision here matters.
   - `rejected` — wrong call entirely.

3. **Get the one-line why.** Required for edited and rejected. Ask for it if it
   was not given, and ask for the *reason*, not the restatement:
   - restatement: "should have been BUILD"
   - reason: "blast radius was the deciding factor, not effort"

   The second one can become a rule. The first one cannot.

4. **Run it:**
   ```
   python3 -m lib.capture --case <id> --verdict edited \
       --set disposition=BUILD --why "blast radius, not effort"
   ```

5. **Stop there.** Do not edit a rule file. Do not propose one inline. The
   correction is now evidence; `reflect` turns accumulated evidence into a
   proposed diff; it merges by PR with the evals as the gate. A rule changed in
   the heat of a correction is a rule fitted to one case.

## Tone

No apology, no re-litigation, no "you're absolutely right". Record it and move
on. The system being wrong is the expected state early — that is what the
agreement metric is for, and the metric only works if corrections are recorded
rather than argued with.
