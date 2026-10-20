"""Triage CLI — decide on an incoming request. Draft only.

    python3 -m lib.triage decide --file requests/example.yaml
    python3 -m lib.triage decide --file req.yaml --json
    python3 -m lib.triage show C-2026-10-20-0001
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from lib import cases, decide as decider


def load_request(path: Path) -> dict:
    text = path.read_text()
    ctx = yaml.safe_load(text) if path.suffix in (".yaml", ".yml") else json.loads(text)
    if not isinstance(ctx, dict) or "request" not in ctx:
        sys.exit(f"{path}: expected a mapping with a top-level `request` key")
    return ctx


def cmd_decide(args) -> int:
    ctx = load_request(Path(args.file))
    decision = decider.decide("triage", ctx)

    if args.json:
        print(json.dumps(decision, indent=2))
    else:
        title = ctx["request"].get("title", Path(args.file).stem)
        print(f"\n{title}\n{'─' * len(title)}")
        print(decider.explain(decision))
        print()
        if decision["autonomy"] == "draft_only":
            print("  → draft only. Nothing runs until you approve it.\n")

    if not args.no_save:
        case = cases.create("triage", ctx["request"], decision)
        print(f"  case {case['id']}   capture your verdict with:")
        print(f"    python3 -m lib.capture --case {case['id']} --verdict approved\n")
    return 0


def cmd_show(args) -> int:
    case = cases.load(args.case_id)
    print(json.dumps(case, indent=2))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="lib.triage", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("decide", help="decide on a request file")
    d.add_argument("--file", required=True)
    d.add_argument("--json", action="store_true")
    d.add_argument("--no-save", action="store_true", help="do not write a case")
    d.set_defaults(fn=cmd_decide)

    s = sub.add_parser("show", help="print a stored case")
    s.add_argument("case_id")
    s.set_defaults(fn=cmd_show)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
