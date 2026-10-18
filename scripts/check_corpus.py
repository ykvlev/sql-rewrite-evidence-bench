"""Validate SREB dataset integrity.

    python scripts/check_corpus.py [--repo-root .]

Rules:
  1. If manifest.json exists, every listed file must match its sha256.
  2. Every family in corpus/families.json must have a reference SQL and a schema.
  3. Every state in states/states.json must reference an existing family.
  4. Evidence marked "refuted" must carry refuting_states and a witness.
Exits non-zero on any violation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    root = ap.parse_args().repo_root.resolve()
    errors: list[str] = []
    checked = 0

    manifest = root / "manifest.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for rel, expected in (data.get("files") or {}).items():
            path = root / rel
            if not path.exists():
                errors.append(f"manifest lists missing file: {rel}")
                continue
            if sha256(path) != expected:
                errors.append(f"hash mismatch: {rel}")
            checked += 1

    families_file = root / "data" / "corpus" / "families.json"
    state_file = root / "data" / "states" / "states.json"
    family_ids: set[str] = set()

    if families_file.exists():
        corpus = json.loads(families_file.read_text(encoding="utf-8"))
        for fam in corpus.get("families", []):
            fid = fam.get("id")
            if not fid:
                errors.append("family without id")
                continue
            if fid in family_ids:
                errors.append(f"duplicate family id: {fid}")
            family_ids.add(fid)
            if not fam.get("reference_sql"):
                errors.append(f"family {fid}: no reference_sql")
        if not corpus.get("ddl"):
            errors.append("corpus: no schema DDL")

    if state_file.exists():
        states = json.loads(state_file.read_text(encoding="utf-8"))
        for st in states.get("states", []):
            if family_ids and st.get("family") not in family_ids:
                errors.append(f"state references unknown family: {st.get('family')}")

    for ev_file in (root / "data" / "evidence").glob("*.json"):
        ev = json.loads(ev_file.read_text(encoding="utf-8"))
        if ev.get("status") == "refuted":
            if not ev.get("refuting_states"):
                errors.append(f"{ev_file.name}: refuted without refuting_states")
            if not ev.get("witness"):
                errors.append(f"{ev_file.name}: refuted without witness")
        checked += 1

    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print("  -", e)
        return 1
    print(f"OK: checked {checked} entries, no violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
