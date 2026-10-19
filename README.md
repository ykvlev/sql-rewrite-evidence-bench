# SREB — SQL Rewrite Evidence Benchmark

[![validate dataset](https://github.com/ykvlev/sql-rewrite-evidence-bench/actions/workflows/validate.yml/badge.svg)](https://github.com/ykvlev/sql-rewrite-evidence-bench/actions/workflows/validate.yml)
[![Live leaderboard](https://img.shields.io/badge/leaderboard-live-39D0D0)](https://ykvlev.github.io/sql-rewrite-evidence-bench/leaderboard.html)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-dataset-yellow)](https://huggingface.co/datasets/ykvlev/sreb)
[![License: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey)](LICENSE)

> **Language models rewrite SQL for speed and silently change the result.**
> This dataset publishes, for every rewrite, the database state that breaks it
> and the rows that prove it — not a success rate.

```
  user asks: make this query faster

  reference   SELECT ... UNION ALL SELECT ...   ->  [1,1,1,1]   correct
  candidate   SELECT ... WHERE a=0 OR b=0       ->  [1,1,1]     one row gone

  faster?  yes.   error?  none.   result?  different.
```

All four evaluated models broke the query above — three replaced `UNION ALL` with
`OR`, one wrapped it in `DISTINCT`. Both changes remove duplicate rows.
One reader with an unreturned book *and* a zero fee should appear twice.

```python
from datasets import load_dataset
ds = load_dataset("ykvlev/sreb", "evidence")   # every refutation with its witness
```

## Why this is different

| Existing | What it gives | What is missing |
|---|---|---|
| Spider, BIRD | text-to-SQL evaluation | no rewrite validation |
| GenRewrite, R-Bot, LLM-R2 | success rates on benchmarks | no per-rewrite executable witness |
| Cosette, VeriEQL | formal equivalence proofs | only for supported constructs |

SREB keeps the evidence, not just the score. Every record is reproducible: DBMS version,
model digest, sampling parameters, state profile, and a counterexample that can be replayed.

**What it does not claim:** `preserved` means *no refuting state was found in a finite
state bank*. It is not a proof of equivalence, and the dataset never says otherwise.
Witnesses are not minimised — the recorded state is the first one that refuted the
candidate. See [docs/DATASET_CARD.md](docs/DATASET_CARD.md).

## Dataset layout

```
data/
  corpus/    query families per schema: DDL + constraints + reference SQL
  states/    frozen state banks: profiles (empty, nullable, multiplicity, boundary, random)
  runs/      model outputs, one file per (model, query): raw response, parsed candidate
  evidence/  per-query outcomes: status, refuting states, witness rows
```

See [docs/DATASET_CARD.md](docs/DATASET_CARD.md) for the full format specification.

## What a record contains

- `family` — query family id, schema name, reference SQL
- `model` — model name, digest, quantization, parameters
- `candidate_sql` — the proposed rewrite, verbatim
- `status` — `preserved` / `refuted` / `no_rewrite` / `unsupported` / `error`
- `refuting_states` — state profiles that break the rewrite
- `witness` — reference rows vs candidate rows on a refuting state
- `protocol` — DBMS version, temperature, seed, context length, input pins

## Reproducing

Everything published here is verified and recomputed from the data alone:

```bash
pip install -r scripts/requirements.txt
python scripts/check_corpus.py            # integrity, hashes, pins, schema constraints
python scripts/recompute_tables.py        # rebuild docs/tables.md from data/evidence/
```

Model collection and DBMS evaluation scripts are **not part of v0.2.0**: the dataset
publishes their outputs in `data/runs/` and `data/evidence/`, and each record carries the
engine version, model digest, sampling parameters and input hashes needed to audit it.
See [docs/REPRODUCE.md](docs/REPRODUCE.md) for the exact protocol.

## Status

Dataset version **0.2.0**. Corpus: **204 query families on three synthetic schemas** — 68
library (3 tables), 68 shop (7 tables) and 68 university (departments, teachers, students,
semesters, courses, enrollments, grades). Each family has 28 frozen states: 8 designed
profiles (fixed, empty, no_rows, multiplicity, zero_value, nullable, boundary, ties) and 20
pseudo-random states from fixed seeds — **5 712 family–state pairs**. Every state was loaded
into MySQL 8.4.11 with real foreign keys, UNIQUE and CHECK constraints enabled, and every
reference query was executed on it.

Model answers and executable evidence cover **136 families** (library and shop): four
models (`qwen2.5-coder:7b`, `qwen2.5:7b`, `phi3.5:3.8b`, `deepseek-coder-v2`), 544 run
records, 544 evidence records and **15 232 executed checks** on MySQL 8.4.11. Outcomes per
model are in [docs/tables.md](docs/tables.md): 45 rewrites were refuted, in 29 families, and
`union_bag` / `lib_union_bag_books` were broken by all four models. The 68 university
families have frozen states but are not yet evaluated by models.

The evaluation mechanism was cross-checked on PostgreSQL 16.15 on the 12 seed families:
identical outcomes in all 1 008 candidate checks and no DDL changes
([docs/CROSS_DBMS.md](docs/CROSS_DBMS.md)).

`gemma4:26b` is not included: the 25.2B Q4_K_M model needs 17.3 GB while the collection
machine has 15.7 GB of RAM and no GPU, and a single request did not complete within 18
minutes. Deterministic rule rewrites are not included either: the rule module in the source
application is an analyser, not a rewrite generator.

Every data file is SHA-256 frozen in `manifest.json`; `python scripts/check_corpus.py`
passes locally and in CI, and `python scripts/recompute_tables.py` reproduces
`docs/tables.md` from `data/evidence/`.

Next: model runs on the university schema, PostgreSQL evaluation on the full corpus, and
more models.

## Licence

- Data and documentation: CC BY 4.0
- Code (scripts, CI): MIT

## Citation

See [CITATION.cff](CITATION.cff). DOI is assigned on release.
