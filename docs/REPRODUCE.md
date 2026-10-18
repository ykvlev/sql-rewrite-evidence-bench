# Reproducing SREB

Every number in this repository must be obtainable from `data/` alone, without rerunning
any model. Rerunning a model is only needed to add a new model.

## 1. Check the dataset

```bash
python scripts/check_corpus.py --repo-root .
```

Verifies that every file listed in `manifest.json` matches its sha256, that every state
belongs to an existing family, and that every `refuted` record carries refuting states
and a witness. CI runs exactly this command on every push.

## 2. Recompute the tables

```bash
python scripts/recompute_tables.py --repo-root .
```

Builds the summary tables (model x outcome, refutations per family, profile contributions)
from `data/evidence/`. The output must match `docs/tables.md` byte for byte; a mismatch
means the published tables are stale.

## 3. Rerun a model

```bash
python scripts/run_model.py --model qwen2.5-coder:7b --out data/runs/qwen2.5-coder_7b
```

Requires a local Ollama at `127.0.0.1:11434`. The script refuses to run if the corpus or
state bank hashes differ from the frozen manifest: a run is only comparable if the inputs
are identical.

## 4. Re-evaluate on a DBMS

```bash
python scripts/evaluate.py --run data/runs/qwen2.5-coder_7b --dbms mysql
```

Starts from a clean database per state, applies the state rows, executes the reference
query and the candidate, and records the first difference. For MySQL and PostgreSQL the
connection parameters are documented in `scripts/requirements.txt` and `.env.example`.

## What must never change silently

The protocol is pinned by hash. If the corpus, the state bank or the generator source
changes, a new dataset version is required — the old runs stay valid for the old version
and must not be mixed with new ones.

| Pinned | Where |
|---|---|
| corpus sha256 | `manifest.json` |
| state bank sha256 | `manifest.json` |
| model digest | each file in `data/runs/` |
| DBMS version | each file in `data/evidence/` |
| sampling parameters | each file in `data/runs/` |
