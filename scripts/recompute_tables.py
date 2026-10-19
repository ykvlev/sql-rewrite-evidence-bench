"""Recompute the published summary tables from data/evidence/.

    python scripts/recompute_tables.py --repo-root .           # check (exit 1 on mismatch)
    python scripts/recompute_tables.py --repo-root . --write    # regenerate docs/tables.md

Every number in the published tables must be obtainable from data/ alone.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

STATUSES = ("refuted", "preserved", "no_rewrite", "unsupported", "error")


def gather(root: Path) -> dict:
    per_model: dict[str, Counter] = defaultdict(Counter)
    refuting_checks: dict[str, int] = defaultdict(int)
    checks_total: dict[str, int] = defaultdict(int)
    per_family: dict[str, list[tuple[str, str]]] = defaultdict(list)
    families = 0

    for path in sorted((root / "data" / "evidence").glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        families += 1
        fam = doc.get("family", path.stem)
        for rec in doc.get("evidence", []):
            model = rec.get("model", "?")
            status = rec.get("status", "error")
            per_model[model][status] += 1
            per_model[model]["proposed"] += status in ("refuted", "preserved")
            per_model[model]["checks"] += int(rec.get("checks") or 0)
            checks_total[model] += int(rec.get("checks") or 0)
            if status == "refuted":
                per_family[fam].append((model, ",".join(rec.get("refuting_states") or [])))
    return {"per_model": per_model, "per_family": dict(per_family), "families": families}


def render(data: dict) -> str:
    lines = ["# SREB summary tables", "",
             f"Families with evidence: **{data['families']}**. "
             "Generated from `data/evidence/` only.", "",
             "## Outcomes per model", "",
             "| Model | Proposed | " + " | ".join(s.capitalize() for s in STATUSES) + " | Checks |",
             "|---|---|" + "---|" * len(STATUSES) + "---|"]
    for model in sorted(data["per_model"]):
        c = data["per_model"][model]
        cells = [str(c.get(s, 0)) for s in STATUSES]
        lines.append(f"| {model} | {c.get('proposed', 0)} | " + " | ".join(cells) +
                     f" | {c.get('checks', 0)} |")
    lines += ["", "## Refuted families", "",
              "| Family | Model | Refuting states |", "|---|---|---|"]
    for fam in sorted(data["per_family"]):
        for model, states in data["per_family"][fam]:
            lines.append(f"| {fam} | {model} | {states} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = args.repo_root.resolve()

    data = gather(root)
    text = render(data)
    target = root / "docs" / "tables.md"

    if not data["families"]:
        print("no evidence files found; nothing to recompute")
        return 1

    if args.write:
        target.write_text(text, encoding="utf-8", newline="\n")
        print(f"written: {target}")
        return 0

    if not target.exists():
        print("docs/tables.md missing; run with --write")
        return 1
    if target.read_text(encoding="utf-8") != text:
        print("MISMATCH: docs/tables.md is stale relative to data/evidence/")
        return 1
    print(f"OK: tables match data for {data['families']} families")
    return 0


if __name__ == "__main__":
    sys.exit(main())
