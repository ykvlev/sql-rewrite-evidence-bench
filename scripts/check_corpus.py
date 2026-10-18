"""Validate SREB dataset integrity.

    python scripts/check_corpus.py [--repo-root .]

Rules:
  1. If manifest.json exists, every listed file must match its sha256, and every file
     under data/ must be listed (so no data file escapes the frozen hashes).
  2. Every corpus file in data/corpus/*.json must declare a schema, a DDL and families;
     every family must have a reference SQL, a profile, a breaking_profile and a schema.
     Family ids are unique across all corpus files.
  3. Every state in states/states.json must reference an existing family.
  4. Every family must have a run record for every model directory and an evidence file
     once it is evaluated; a family without runs yet is allowed (staged dataset), but a
     run record may only exist for a family that has frozen states.
  5. Every run record must name its model, digest and sampling protocol; candidate_sql
     and raw_response keys must be present.
  6. Every evidence record must have an allowed status; "refuted" requires refuting_states
     and a witness, and the witness state must be one of the refuting states.
  7. Every evidence file must pin, in protocol.corpus_sha256 and
     protocol.state_bank_sha256, the current sha256 of its schema corpus file and of
     data/states/states.json. A stale pin is an error: published evidence would otherwise
     refer to inputs that are no longer in the tree.
  8. If manifest.json declares counts, they must be recomputable from data/ alone.
Exits non-zero on any violation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

STATUSES = {"preserved", "refuted", "no_rewrite", "unsupported", "error"}
BREAKING_PROFILES = {"multiplicity", "nullable", "empty", "boundary", "ties", "zero_value", "random"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_evidence_record(rel: str, rec: dict, errors: list[str], family_ids: set[str]) -> None:
    status = rec.get("status")
    if status not in STATUSES:
        errors.append(f"{rel}: unknown status {status!r}")
    if not rec.get("model"):
        errors.append(f"{rel}: evidence record without model")
    if not rec.get("model_digest"):
        errors.append(f"{rel}: evidence record without model digest")
    if status == "refuted":
        states = rec.get("refuting_states") or []
        witness = rec.get("witness") or {}
        if not states:
            errors.append(f"{rel}: refuted without refuting_states")
        if not witness:
            errors.append(f"{rel}: refuted without witness")
        elif witness.get("reference_rows") is None or witness.get("candidate_rows") is None:
            errors.append(f"{rel}: witness without reference or candidate rows")
        elif witness.get("state") not in states:
            errors.append(f"{rel}: witness state is not among refuting_states")
    elif status in {"preserved", "no_rewrite"}:
        if rec.get("refuting_states"):
            errors.append(f"{rel}: {status} record has refuting_states")
    if rec.get("family") and rec["family"] not in family_ids:
        errors.append(f"{rel}: evidence record for unknown family {rec['family']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    root = ap.parse_args().repo_root.resolve()
    errors: list[str] = []
    checked = 0

    listed: dict[str, str] = {}
    manifest = root / "manifest.json"
    if manifest.exists():
        data = load(manifest)
        listed = data.get("files") or {}
        for rel, expected in listed.items():
            path = root / rel
            if not path.exists():
                errors.append(f"manifest lists missing file: {rel}")
                continue
            if sha256(path) != expected:
                errors.append(f"hash mismatch: {rel}")
            checked += 1
        data_root = root / "data"
        if data_root.exists():
            for path in sorted(data_root.rglob("*")):
                if path.is_file():
                    rel = path.relative_to(root).as_posix()
                    if rel not in listed:
                        errors.append(f"data file is not frozen in manifest.json: {rel}")

    family_ids: set[str] = set()
    family_schema: dict[str, str] = {}
    corpus_hashes: dict[str, str] = {}
    corpus_root = root / "data" / "corpus"
    corpus_files = sorted(corpus_root.glob("*.json")) if corpus_root.exists() else []
    for corpus_file in corpus_files:
        rel = corpus_file.relative_to(root).as_posix()
        try:
            corpus = load(corpus_file)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{rel}: cannot parse ({exc})")
            continue
        schema = corpus.get("schema")
        if not schema:
            errors.append(f"{rel}: no schema name")
        else:
            corpus_hashes[schema] = sha256(corpus_file)
        if not corpus.get("ddl"):
            errors.append(f"{rel}: no schema DDL")
        for fam in corpus.get("families", []):
            fid = fam.get("id")
            if not fid:
                errors.append(f"{rel}: family without id")
                continue
            if fid in family_ids:
                errors.append(f"duplicate family id: {fid}")
            family_ids.add(fid)
            family_schema[fid] = fam.get("schema") or schema
            if (fam.get("schema") or schema) != schema:
                errors.append(f"family {fid}: schema differs from {rel}")
            if not fam.get("reference_sql"):
                errors.append(f"family {fid}: no reference_sql")
            if not fam.get("profile"):
                errors.append(f"family {fid}: no profile")
            if fam.get("breaking_profile") not in BREAKING_PROFILES:
                errors.append(f"family {fid}: bad breaking_profile {fam.get('breaking_profile')!r}")
        checked += 1

    state_counts: dict[str, int] = {}
    state_pairs = 0
    state_file = root / "data" / "states" / "states.json"
    states_hash: str | None = sha256(state_file) if state_file.exists() else None
    if state_file.exists():
        states = load(state_file)
        for st in states.get("states", []):
            state_pairs += 1
            fid = st.get("family")
            if family_ids and fid not in family_ids:
                errors.append(f"state references unknown family: {fid}")
            if not st.get("profile"):
                errors.append(f"state of {fid}: no profile")
            if st.get("rows") is None:
                errors.append(f"state {st.get('profile')} of {fid}: no rows")
            state_counts[fid] = state_counts.get(fid, 0) + 1
        checked += 1

    runs_root = root / "data" / "runs"
    run_slugs = sorted(p.name for p in runs_root.iterdir() if p.is_dir()) if runs_root.exists() else []
    run_records = 0
    evaluated: set[str] = set()
    checks = 0
    if runs_root.exists():
        for path in sorted(runs_root.glob("*/*.json")):
            rel = path.relative_to(root).as_posix()
            rec = load(path)
            run_records += 1
            checked += 1
            fid = rec.get("family")
            if fid not in family_ids:
                errors.append(f"{rel}: run for unknown family {fid!r}")
            else:
                evaluated.add(fid)
                checks += state_counts.get(fid, 0)
            if fid != path.stem:
                errors.append(f"{rel}: family does not match file name")
            if "schema" in rec and rec["schema"] != family_schema.get(fid):
                errors.append(f"{rel}: run schema does not match corpus schema")
            if not rec.get("model"):
                errors.append(f"{rel}: run without model name")
            if not rec.get("model_digest"):
                errors.append(f"{rel}: run without model digest")
            protocol = rec.get("protocol") or {}
            for field in ("temperature", "num_ctx", "num_predict"):
                if field not in protocol:
                    errors.append(f"{rel}: protocol without {field}")
            if "seed" not in protocol:
                errors.append(f"{rel}: protocol without seed (use null when unset)")
            if "candidate_sql" not in rec:
                errors.append(f"{rel}: run without candidate_sql key")
            if "raw_response" not in rec:
                errors.append(f"{rel}: run without raw_response")
            if state_counts.get(fid, 0) == 0:
                errors.append(f"{rel}: run record for a family without frozen states")

    evidence_root = root / "data" / "evidence"
    evidence_records = 0
    if evidence_root.exists():
        for path in sorted(evidence_root.glob("*.json")):
            rel = path.relative_to(root).as_posix()
            ev = load(path)
            checked += 1
            if ev.get("family") not in family_ids:
                errors.append(f"{rel}: evidence for unknown family {ev.get('family')!r}")
            if ev.get("family") != path.stem:
                errors.append(f"{rel}: family does not match file name")
            protocol = ev.get("protocol") or {}
            schema = ev.get("schema") or family_schema.get(ev.get("family"))
            expected_corpus = corpus_hashes.get(schema)
            pinned_corpus = protocol.get("corpus_sha256")
            if not pinned_corpus:
                errors.append(f"{rel}: protocol without corpus_sha256 pin")
            elif expected_corpus is None:
                errors.append(f"{rel}: cannot resolve corpus file for schema {schema!r}")
            elif pinned_corpus != expected_corpus:
                errors.append(f"{rel}: stale corpus_sha256 pin "
                              f"({pinned_corpus[:12]}… != {expected_corpus[:12]}…)")
            pinned_states = protocol.get("state_bank_sha256")
            if not pinned_states:
                errors.append(f"{rel}: protocol without state_bank_sha256 pin")
            elif states_hash is None:
                errors.append(f"{rel}: state bank file is missing")
            elif pinned_states != states_hash:
                errors.append(f"{rel}: stale state_bank_sha256 pin "
                              f"({pinned_states[:12]}… != {states_hash[:12]}…)")
            records = ev.get("evidence")
            if isinstance(records, list):
                for rec in records:
                    evidence_records += 1
                    rec = dict(rec)
                    rec.setdefault("family", ev.get("family"))
                    check_evidence_record(rel, rec, errors, family_ids)
            else:  # одна запись на файл (формат из первой редакции карточки)
                evidence_records += 1
                check_evidence_record(rel, ev, errors, family_ids)

    for fid in sorted(evaluated):
        if state_counts.get(fid, 0) == 0:
            errors.append(f"evaluated family without states: {fid}")
        for slug in run_slugs:
            if not (runs_root / slug / f"{fid}.json").exists():
                errors.append(f"missing run record: {slug}/{fid}.json")
        if not (evidence_root / f"{fid}.json").exists():
            errors.append(f"missing evidence file for evaluated family: {fid}")

    counts = (load(manifest).get("counts") or {}) if manifest.exists() else {}
    if counts:
        per_family = {state_counts[f] for f in state_counts}
        spf = per_family.pop() if len(per_family) == 1 else -1
        by_schema: dict[str, int] = {}
        for fid in family_ids:
            schema = family_schema.get(fid, "")
            by_schema[schema] = by_schema.get(schema, 0) + 1
        derived = {
            "families": len(family_ids),
            "families_by_schema": by_schema,
            "families_with_states": len(state_counts),
            "evaluated_families": len(evaluated),
            "states_per_family": spf,
            "state_family_pairs": state_pairs,
            "models": len(run_slugs),
            "run_records": run_records,
            "evidence_records": evidence_records,
            "checks": checks,
        }
        for key, value in derived.items():
            if key in counts and counts[key] != value:
                errors.append(f"manifest count {key}={counts[key]!r} does not match data ({value!r})")

    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print("  -", e)
        return 1
    print(f"OK: checked {checked} entries, no violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
