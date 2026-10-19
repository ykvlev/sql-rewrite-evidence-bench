<div align="center">

# SREB

### SQL Rewrite Evidence Benchmark

**Language models rewrite SQL for speed and silently change the result.**<br>
This dataset publishes, for every rewrite, the database state that breaks it<br>
and the rows that prove it — not a success rate.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23472642.svg)](https://doi.org/10.5281/zenodo.23472642)
[![validate dataset](https://github.com/ykvlev/sql-rewrite-evidence-bench/actions/workflows/validate.yml/badge.svg)](https://github.com/ykvlev/sql-rewrite-evidence-bench/actions/workflows/validate.yml)
[![Live leaderboard](https://img.shields.io/badge/leaderboard-live-39D0D0)](https://ykvlev.github.io/sql-rewrite-evidence-bench/leaderboard.html)
[![🤗 Dataset](https://img.shields.io/badge/%F0%9F%A4%97-dataset-yellow)](https://huggingface.co/datasets/ykvlev/sreb)
[![License: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey)](LICENSE)

</div>

---

```
  user asks: make this query faster

  reference   SELECT ... UNION ALL SELECT ...   ->  [1,1,1,1]   ✓ correct
  candidate   SELECT ... WHERE a = 0 OR b = 0   ->  [1,1,1]     ✗ one row gone

              faster? yes.    error? none.    result? different.
```

All four models that answered this family broke it — three replaced `UNION ALL` with
`OR`, one wrapped it in `DISTINCT`. Both changes remove duplicate rows. A reader with
an unreturned book *and* a zero fee belongs in the result **twice**.

<div align="center">

| 204 query families | 5 712 frozen states | 6 models | 34 272 executed checks |
|:---:|:---:|:---:|:---:|
| 3 schemas | 28 per family | 7B and 3B | MySQL 8.4.11 |

</div>

```python
from datasets import load_dataset

evidence = load_dataset("ykvlev/sreb", "evidence")
# every refutation comes with the state that caused it and the differing rows
```

---

## What a record gives you

| Field | Meaning |
|---|---|
| `reference_sql` | the original query |
| `candidate_sql` | what the model proposed, verbatim |
| `status` | `refuted` · `preserved` · `no_rewrite` · `unsupported` · `error` |
| `refuting_states` | the state profiles that break the candidate |
| `witness` | reference rows vs candidate rows on a refuting state |
| `protocol` | DBMS version, model digest, sampling parameters, input hashes |

## Why this is different

| Existing work | What it gives | What is missing |
|---|---|---|
| Spider, BIRD | text-to-SQL evaluation | no rewrite validation |
| GenRewrite, R-Bot, LLM-R2 | success rates on benchmarks | no per-rewrite executable witness |
| Cosette, VeriEQL | formal equivalence proofs | only for supported constructs |

SREB keeps the evidence, not just the score. Every record is reproducible:
DBMS version, model digest, sampling parameters, state profile, and a counterexample
that can be replayed.

## What this dataset does **not** claim

- `preserved` means *no refuting state was found in a finite state bank*. It is **not**
  a proof of equivalence, and the dataset never says otherwise.
- Witnesses are **not minimised**: the recorded state is the first one that refuted the
  candidate, not the smallest possible.
- Predecessors exist — [SQL-RewriteBench](https://arxiv.org/abs/2607.09251) and
  [provensql](https://doi.org/10.5281/zenodo.21854387). See
  [`docs/POSITIONING.md`](docs/POSITIONING.md) for an honest comparison.

## Dataset layout

```
data/
  corpus/    query families per schema: DDL + constraints + reference SQL
  states/    frozen state banks: 8 designed profiles + 20 seeded random per family
  runs/      model outputs, one file per (model, family): raw response, parsed candidate
  evidence/  per-family outcomes: status, refuting states, witness rows
```

Full format specification: [`docs/DATASET_CARD.md`](docs/DATASET_CARD.md).

## What the models did

| Model | Proposed | Refuted | Refuted % | No rewrite |
|---|---:|---:|---:|---:|
| qwen2.5:3b | 85 | 39 | **45.9 %** | 97 |
| deepseek-coder-v2 | 77 | 27 | 35.1 % | 126 |
| llama3.2:3b | 53 | 26 | **49.1 %** | 140 |
| qwen2.5-coder:7b | 30 | 12 | 40.0 % | 173 |
| phi3.5:3.8b | 30 | 8 | 26.7 % | 156 |
| qwen2.5:7b | 32 | 8 | 25.0 % | 169 |

**120 refuted rewrites in 75 families.** The two 3B models refuted almost half of what
they proposed — size does not save you, and smaller models still rewrite with confidence.
Counter-example worth noting: Phi-3.5 at 3.8B refutes only 26.7 %, less than the 7B models.

Live table with witnesses: [leaderboard](https://ykvlev.github.io/sql-rewrite-evidence-bench/leaderboard.html).

## Reproducing

Everything published here is recomputed from the data alone:

```bash
pip install -r scripts/requirements.txt
python scripts/check_corpus.py            # integrity, hashes, pins, schema constraints
python scripts/recompute_tables.py        # rebuild docs/tables.md from data/evidence/
```

Model collection and DBMS evaluation scripts are **not part of this release**: the dataset
publishes their outputs, and each record carries the engine version, model digest, sampling
parameters and input hashes needed to audit it. Protocol details in
[`docs/REPRODUCE.md`](docs/REPRODUCE.md).

## Scale and status

Corpus: **204 query families on three synthetic schemas** — 68 library (3 tables),
68 shop (7 tables), 68 university (7 tables). Each family has 28 frozen states: 8 designed
profiles (fixed, empty, no_rows, multiplicity, zero_value, nullable, boundary, ties) and
20 pseudo-random states from fixed seeds — **5 712 family–state pairs**. Every state was
loaded into MySQL 8.4.11 with real foreign keys, UNIQUE and CHECK constraints enabled, and
every reference query was executed on it.

Model answers and evidence cover **all 204 families**: six models, 1 224 run records,
1 224 evidence records, **34 272 executed checks**. Error and `unsupported` outcomes are
recorded as such, never replayed.

Cross-DBMS check: the schema and all reference queries execute on PostgreSQL 16.15 without
modification, and on the 12 seed families the reference results and candidate
classifications match MySQL exactly (0 divergences over 336 state pairs).
See [`docs/CROSS_DBMS.md`](docs/CROSS_DBMS.md).

Not included: `gemma4:26b` (needs 17.3 GB, machine has 15.7 GB and no GPU) and a
deterministic rule baseline (the rule module is an analyser, not a rewrite generator).

## Citation

```bibtex
@dataset{yakovlev_sreb,
  title     = {SREB: SQL Rewrite Evidence Benchmark},
  author    = {Yakovlev, Artem},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.23472642},
  url       = {https://doi.org/10.5281/zenodo.23472642}
}
```

ORCID: [0009-0006-8617-7895](https://orcid.org/0009-0006-8617-7895)

## Licence

Data and documentation: **CC BY 4.0** · Code (scripts, CI): **MIT**

<div align="center">
<sub>Built with MySQL 8.4.11 · Ollama · 34 272 executed checks · every number recomputable</sub>
</div>
