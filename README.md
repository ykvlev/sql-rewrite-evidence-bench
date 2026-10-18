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

Work in progress. Seed corpus: 12 query families from the library domain, 28 frozen states
each (336 checks per model), three models evaluated. Scaling to 200+ families, 8 models,
two DBMS engines.

## Licence

- Data and documentation: CC BY 4.0
- Code (scripts, CI): MIT

## Citation

See [CITATION.cff](CITATION.cff). DOI is assigned on release.
