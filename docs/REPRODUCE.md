# Reproducing SREB

Every number in this repository must be obtainable from `data/` alone, without rerunning
any model. Rerunning a model is only needed to add a new model.

## 1. Check the dataset

```bash
python scripts/check_corpus.py --repo-root .
```

Verifies that every file listed in `manifest.json` matches its sha256, that every state
belongs to an existing family, that every `refuted` record carries refuting states and a
witness, and that every evidence file pins the current corpus and state-bank hashes. A
stale pin is a hard error: published evidence must never refer to inputs that are no
longer in the tree. CI runs exactly this command on every push.

## 2. Recompute the tables

```bash
python scripts/recompute_tables.py --repo-root .
```

Builds the summary tables (model × outcome, refutations per family) from `data/evidence/`.
The output must match `docs/tables.md` byte for byte; a mismatch means the published
tables are stale. CI reruns both the check and the regeneration and fails if the committed
file differs.

## 3. Model collection and evaluation

The scripts that collect model answers and execute candidates on a DBMS are **not part of
v0.2.0**; the dataset publishes their outputs instead. Each record carries everything needed
to audit it:

- `data/runs/<model>/<family>.json` — model name, digest, quantization, engine version,
  temperature, seed (null when unset), context length, max tokens, the exact prompt and the
  raw response, plus the parsed `candidate_sql`.
- `data/evidence/<family>.json` — DBMS and version, the corpus and state-bank pins, and per
  model: status, refuting states, the witness rows and the outcome of an independent replay
  in a fresh schema.
- `data/states/states.json` — the full rows of every allowed state, so a candidate can be
  re-executed against the same instances.

Re-running a model therefore requires reproducing the sampling protocol recorded in the
run file and the state rows from the bank; the frozen hashes make a run comparable only if
its inputs are identical.

## What must never change silently

The protocol is pinned by hash. If the corpus, the state bank or the generator source
changes, a new dataset version is required — the old runs stay valid for the old version
and must not be mixed with new ones.

| Pinned | Where |
|---|---|
| dataset version | `manifest.json`, `CITATION.cff`, each file under `data/` |
| corpus sha256 | `manifest.json` and `protocol.corpus_sha256` of each evidence file |
| state bank sha256 | `manifest.json` and `protocol.state_bank_sha256` of each evidence file |
| model digest | each file in `data/runs/` |
| DBMS version | each file in `data/evidence/` |
| sampling parameters | each file in `data/runs/` |
