# SREB — SQL Rewrite Evidence Benchmark

A dataset of **executable evidence** for SQL query rewrites proposed by language models.

Most SQL benchmarks ask *"write a query for this question"*. Most rewrite papers report
a success rate. SREB publishes something different: for every rewrite, **the state of the
database on which the result changes, and the specific rows that prove it**.

```
reference [1,1,1,1]   candidate [1,1,1]   ->  multiplicity lost, 3 refuting states
```

## Why this is different

| Existing | What it gives | What is missing |
|---|---|---|
| Spider, BIRD | text-to-SQL evaluation | no rewrite validation |
| GenRewrite, R-Bot, LLM-R2 | success rates on benchmarks | no per-rewrite executable witness |
| Cosette, VeriEQL | formal equivalence proofs | only for supported constructs |

SREB keeps the evidence, not just the score. Every record is reproducible: DBMS version,
model digest, sampling parameters, state profile, and a minimal counterexample.

## Dataset layout

```
data/
  corpus/    query families: schema DDL + reference SQL
  states/    frozen state banks: profiles (empty, nullable, multiplicity, boundary, random)
  runs/      model outputs, one file per (model, query): raw response, parsed candidate
  evidence/  per-query outcomes: status, refuting states, minimal witness rows
```

See [docs/DATASET_CARD.md](docs/DATASET_CARD.md) for the full format specification.

## What a record contains

- `family` — query family id, schema name, reference SQL
- `model` — model name, digest, quantization, parameters
- `candidate_sql` — the proposed rewrite, verbatim
- `status` — `preserved` / `refuted` / `no_rewrite` / `unsupported` / `error`
- `refuting_states` — state profiles that break the rewrite
- `witness` — reference rows vs candidate rows on the minimal state
- `protocol` — DBMS version, temperature, seed, context length

## Reproducing

```bash
pip install -r scripts/requirements.txt
python scripts/check_corpus.py        # validate corpus and state bank integrity
python scripts/run_model.py --model qwen2.5-coder:7b --corpus data/corpus
python scripts/evaluate.py --run data/runs/<run> --dbms mysql
```

Every script pins hashes: a run is only valid if the corpus and state bank hashes match
the frozen manifest.

## Status

Corpus **v0.2**: 136 query families on two synthetic schemas — 68 in the library (3
tables) and 68 in the shop (7 tables: categories, products, customers, orders,
order_items, payments, reviews). Each family has 28 frozen states: 8 designed profiles
(fixed, empty, no_rows, multiplicity, zero_value, nullable, boundary, ties) and 20
pseudo-random states from fixed seeds — 3 808 family–state pairs in total. Every state
was loaded into MySQL 8.4.11 with real foreign keys and CHECK constraints enabled, and
every reference query was executed on it.

Model runs and executable evidence currently cover the 12-family library seed: three
models (`qwen2.5-coder:7b`, `qwen2.5:7b`, `phi3.5:3.8b`), 36 run records, 36 evidence
records, 1 008 executed checks. Every data file is SHA-256 frozen in `manifest.json`;
`python scripts/check_corpus.py` passes locally and in CI, and
`python scripts/recompute_tables.py` reproduces `docs/tables.md` from `data/evidence/`.

Next: model runs on the expanded corpus, a second DBMS engine, and more models.

## Licence

- Data and documentation: CC BY 4.0
- Code (scripts, CI): MIT

## Citation

See [CITATION.cff](CITATION.cff). DOI is assigned on release.
