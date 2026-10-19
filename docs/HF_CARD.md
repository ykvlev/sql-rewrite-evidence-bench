---
license: cc-by-4.0
language:
  - en
pretty_name: "SREB: SQL Rewrite Evidence Benchmark"
tags:
  - sql
  - databases
  - query-optimization
  - text-to-sql
  - evaluation
  - reproducibility
size_categories:
  - 10K<n<100K
task_categories:
  - text-generation
  - table-question-answering
configs:
  - config_name: evidence
    data_files: data/evidence/*.json
  - config_name: runs
    data_files: data/runs/*/*.json
  - config_name: corpus
    data_files: data/corpus/*.json
  - config_name: states
    data_files: data/states/states.json
---

# SREB: SQL Rewrite Evidence Benchmark

A dataset of **executable evidence** for SQL query rewrites proposed by language models.

Most SQL benchmarks ask *"write a query for this question"*. Most rewrite papers report a
success rate. SREB publishes something different: for every rewrite, **the database state
on which the result changes and the rows that prove it**.

```
reference [1,1,1,1]    candidate [1,1,1]    ->  multiplicities lost
```

## Why it is different

| Existing work | What it gives | Missing |
|---|---|---|
| Spider, BIRD | text-to-SQL evaluation | no rewrite validation |
| GenRewrite, R-Bot, LLM-R2 | success rates on benchmarks | no per-rewrite witness |
| Cosette, VeriEQL | formal proofs for supported SQL | coverage, and no run-level evidence |

SREB keeps the evidence, not the score. Every record is reproducible: database version,
model digest, sampling parameters, state profile, and the rows that differ.

## What is inside

| Config | Content |
|---|---|
| `corpus` | query families: schema DDL, constraints, reference SQL, breaking profile |
| `states` | frozen state banks generated under the real schema constraints |
| `runs` | model responses with digest, quantization and sampling parameters |
| `evidence` | outcome per (family, model): status, refuting states, row witness |

Outcome values: `refuted`, `preserved`, `no_rewrite`, `unsupported`, `error`.

`preserved` means **no refuting state was found** on the finite bank. It is not a proof of
equivalence, and the dataset never claims otherwise.

## Reproduce

```bash
git clone https://github.com/ykvlev/sql-rewrite-evidence-bench
pip install -r scripts/requirements.txt
python scripts/check_corpus.py --repo-root .        # hashes, pins, integrity
python scripts/recompute_tables.py --repo-root .    # rebuild summary tables
```

Every published number is recomputable from `data/` without rerunning a model.

## Scale (v0.3.0)

- query families: **204** across three schemas (library, online shop, university)
- frozen states: **5 712** (28 profiles per family)
- model runs: **1 224** (6 models × 204 evaluated families)
- evidence: **204 families**, evaluated on MySQL 8.4.11
- total checks: **34 272** (model × family × state)
- models: Qwen2.5-Coder-7B, Qwen2.5-7B, Qwen2.5-3B, Phi-3.5-mini-3.8B,
  DeepSeek-Coder-V2, Llama-3.2-3B

Cross-DBMS check: the schemas and the 136 library/shop reference queries execute
on PostgreSQL 16.15 without modification; on the 12 seed families the reference results and
candidate classifications match MySQL exactly (0 divergences over 336 state pairs). The
university schema has not been ported yet.

## Limitations

- Synthetic schemas: coverage of real workloads is partial.
- A finite state bank cannot prove equivalence.
- Witnesses are **not minimised**: the recorded state is the first one that refuted the
  candidate, not the smallest possible.
- Model behaviour changes across engine versions; the engine version is part of the record.
  The six models span Ollama 0.40.4–0.40.6.
- Small models can return invalid SQL: 23 answers are `unsupported` and 33 are `error` of
  1 224 (recorded, not retried).

## Licence

Data and documentation: CC BY 4.0. Code: MIT.

## Citation

```bibtex
@dataset{yakovlev_sreb,
  title  = {SREB: SQL Rewrite Evidence Benchmark},
  author = {Yakovlev, Artem},
  year   = {2026},
  note   = {ORCID 0009-0006-8617-7895},
  url    = {https://github.com/ykvlev/sql-rewrite-evidence-bench}
}
```
