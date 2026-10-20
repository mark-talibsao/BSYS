"""Produce a typed decision from a request context.

Draft only. Nothing in this module takes an action, and the risk pass exists to
make that refusal explicit rather than implicit: every decision carries the tier
its proposed action would need, so "why didn't it just do it" has an answer in
the output instead of in someone's memory.
"""

from __future__ import annotations

from lib import rules


def decide(domain: str, ctx: dict) -> dict:
    """Apply a domain's rules, then tier the proposed action."""
    outcome = rules.apply(ctx, rules.load(domain))
    decision = outcome.to_dict()

    # The risk pass reads the decision it is tiering, so rules like RSK-005
    # (low confidence cannot buy autonomy) and RSK-006 (unencoded domain) can
    # see it.
    risk_ctx = {
        **ctx,
        "decision": {"confidence": decision["confidence"], "novel": decision["novel"]},
        "action": ctx.get("action", {}),
    }
    risk = rules.apply(risk_ctx, rules.load("risk"))
    decision["risk_tier"] = risk.fields.get("tier", "R3")
    decision["risk_rules_fired"] = risk.rules_fired
    decision["autonomy"] = "execute" if decision["risk_tier"] == "R0" else "draft_only"

    if not decision.get("disposition"):
        decision["disposition"] = "CLARIFY"
        decision["escalate"].append("no disposition set — falling back to CLARIFY")

    decision["domain"] = domain
    decision["blocked"] = bool(decision["escalate"]) or decision["confidence"] < 0.5
    return decision


def explain(decision: dict, domain: str = "triage") -> str:
    """Render the decision for a human, with each cited rule's reasoning."""
    by_id = {r.id: r for r in rules.load(domain) + rules.load("risk")}
    lines = [
        f"  disposition   {decision.get('disposition')}",
        f"  confidence    {decision.get('confidence')}"
        + ("  ← below floor" if decision.get("confidence", 0) < 0.5 else ""),
        f"  risk tier     {decision.get('risk_tier')}  ({decision.get('autonomy')})",
    ]
    for key in ("owner", "mechanism", "priority", "requires_design_review", "requires_volume_plan"):
        if key in decision:
            lines.append(f"  {key:<13} {decision[key]}")

    lines.append("")
    if decision.get("novel"):
        lines.append("  no rule fired — outside encoded territory, queued for reflect")
    for rid in decision.get("rules_fired", []) + decision.get("risk_rules_fired", []):
        r = by_id.get(rid)
        if not r:
            continue
        flag = "" if r.status == "active" else f" [{r.status}]"
        lines.append(f"  {rid}{flag}  {r.title}")
        because = " ".join(r.because.split())
        lines.append(f"      {because}")

    if decision.get("require"):
        lines += ["", "  need before this can move:"] + [f"    - {r}" for r in decision["require"]]
    if decision.get("escalate"):
        lines += ["", "  escalate:"] + [f"    ! {e}" for e in decision["escalate"]]
    if decision.get("conflicts"):
        lines += ["", "  conflicts:"] + [f"    ~ {c}" for c in decision["conflicts"]]
    return "\n".join(lines)
