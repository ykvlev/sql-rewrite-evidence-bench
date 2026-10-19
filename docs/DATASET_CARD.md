# Dataset card — SREB v0.2.0

## Purpose

To make SQL rewrite quality measurable with executable evidence rather than declared
success rates. A model that claims a rewrite preserves the result must survive the
allowed states of the database; when it does not, the dataset records exactly where.

## What the dataset contains

| Item | Count |
|---|---|
| Query families | 204 (68 library + 68 shop + 68 university) |
| Frozen states per family | 28 |
| Family–state pairs | 5 712 |
| Models with runs | 6 (`qwen2.5-coder:7b`, `qwen2.5:7b`, `qwen2.5:3b`, `phi3.5:3.8b`, `deepseek-coder-v2:latest`, `llama3.2:3b`) |
| Run records (model × family) | 1 224 |
| Evidence records (model × family) | 1 224 |
| Executed checks (model × family × state) | 34 272 |
| Families with frozen states | 204 (all) |
| Families with model runs | 204 (all) |

Coverage is complete for the corpus, the state banks and the model runs: every family has
28 frozen states, one answer per model and one evidence record per model. Six models are
included. `gemma4:26b` is resource-blocked on the collection machine: the 25.2B Q4_K_M
model is 17.3 GB, the machine has 15.7 GB of RAM and no GPU, and a single request did not
complete within 18 minutes. A deterministic rules baseline is not published because the rule
module in the source application is an analyser, not a rewrite generator; it produces
findings and suggestions rather than executable candidate SQL.

The primary execution engine is MySQL 8.4.11. The evaluation mechanism was additionally
cross-checked on PostgreSQL 16.15 for the 12 seed families (1 008 candidate checks, no status
mismatches, no DDL changes); see [CROSS_DBMS.md](CROSS_DBMS.md). PostgreSQL evidence is not
yet first-class in the dataset format; the university schema has not been ported to
PostgreSQL yet.

## Structure

### corpus/families.json, corpus/shop.json and corpus/university.json

One file per schema. Each declares the schema DDL, the constraints it enforces, and the
query families with a query-shape `profile` and a designed `breaking_profile`. `profile`
is derived from the reference SQL only, never from model answers; `breaking_profile` is
the state profile the family is designed to be challenged by (measured refutations live
in `evidence/`).

```json
{
  "schema": "library",
  "ddl": ["CREATE TABLE lib_readers (...)", "..."],
  "constraints": ["lib_readers.id PRIMARY KEY", "lib_loans.reader_id REFERENCES lib_readers(id)"],
  "families": [
    {"id": "loan_count", "schema": "library", "reference_sql": "SELECT ...",
     "profile": "outer_join_aggregate", "breaking_profile": "empty",
     "intent": "Число выдач, включая ноль", "ordered": true}
  ]
}
```

`shop.json` has the same shape for the shop schema (`categories`, `products`, `customers`,
`orders`, `order_items`, `payments`, `reviews`) with PK, FK, NOT NULL and CHECK
constraints on non-negative amounts and quantities and on enumerated columns.

### states/states.json

Two frozen banks, one per schema, each of 28 states: 8 designed profiles
(`fixed`, `empty`, `no_rows`, `multiplicity`, `zero_value`, `nullable`, `boundary`,
`ties`) and 20 pseudo-random states with fixed seeds 0…19. A bank is applied to every
family of its schema and expanded one record per (family, state) pair, so each record is
self-contained:

```json
{"family": "loan_count", "profile": "multiplicity_0", "profile_family": "multiplicity",
 "seed": 0, "rows": {"lib_readers": [[...]], "lib_books": [[...]], "lib_loans": [[...]]}}
```

`profile` is the stable state id used by evidence (`fixed_0`, `empty_0`, `no_loans_0`,
`multiplicity_0`, `zero_fee_0`, `nullable_0`, `boundary_0`, `ties_0`,
`random_uniform_0` … `random_uniform_19`); `profile_family` groups the ids
(`fixed`, `empty`, `no_loans`, `multiplicity`, `zero_fee`, `nullable`, `boundary`,
`ties`, `random_uniform`). Random states carry the generator seed.

The library bank is the frozen seed bank: its domain-named `no_loans_0` and `zero_fee_0`
implement the generic `no_rows` and `zero_value` profiles. The shop bank was generated
deterministically (`random.Random(1000 + seed)`), and every state was loaded into
MySQL in tables with real constraints — foreign keys and CHECK constraints enabled — before
any query was executed on it. A state that violates the schema is not part of the dataset.

### runs/<model>/<family>.json

One file per model and family. The model tag is in `model`; the directory name is a
filesystem-safe slug (a colon is not portable in a path).

```json
{"family": "loan_count", "model": "qwen2.5-coder:7b", "model_digest": "dae161e2…",
 "quantization": "Q4_K_M", "parameter_size": "7.6B",
 "protocol": {"engine": "ollama", "engine_version": "0.40.4", "temperature": 0,
              "seed": null, "num_ctx": 4096, "num_predict": 1200},
 "prompt": "...", "raw_response": {...}, "response_text": "...",
 "candidate_sql": "...", "markdown_removed": false, "provenance": {...}}
```

`seed: null` means the run protocol did not specify a seed; the engine default was used.
It is recorded as null rather than invented. `raw_response` is the engine response
verbatim, including token-level fields.

### evidence/<family>.json

One file per family with one evidence record per model. Outcomes:

| Status | Meaning |
|---|---|
| `refuted` | at least one state breaks the rewrite; `refuting_states` and `witness` are present |
| `preserved` | the candidate differs from the reference SQL and no state broke it (not a proof of equivalence) |
| `no_rewrite` | the model returned the reference query unchanged |
| `unsupported` | the candidate could not be parsed or used unsupported constructs |
| `error` | the reference/candidate could not be executed or no response was stored |

```json
{"family": "union_bag", "reference_sql": "...",
 "protocol": {"dbms": "mysql", "dbms_version": "8.4.11", "corpus_sha256": "...",
              "state_bank_sha256": "..."},
 "evidence": [
   {"model": "qwen2.5:7b", "model_digest": "...", "status": "refuted",
    "candidate_sql": "...", "refuting_states": ["multiplicity_0", "nullable_0", "ties_0"],
    "witness": {"state": "multiplicity_0", "state_profile": "multiplicity",
                "reference_rows": [[1], [1], [1], [1]],
                "candidate_rows": [[1], [1], [1]],
                "interface_equal": true, "independent_replay": "counterexample"},
    "checks": 28}
 ]}
```

Rows are exactly what the DBMS returned (a list of rows, a row is a list of column
values). `independent_replay` records that the refuting pair was executed again in a
fresh private schema.

The file protocol pins its inputs: `protocol.corpus_sha256` is the sha256 of the corpus
file of the evidence file's schema (`data/corpus/families.json` for the library schema,
`data/corpus/shop.json` for the shop schema), and `protocol.state_bank_sha256` is the
sha256 of `data/states/states.json`. `check_corpus.py` recomputes both and rejects a file
whose pin points to inputs that are no longer in the tree.

### manifest.json

SHA-256 of every file under `data/`, plus the recomputable counts, the model digests and
the provenance of the upstream runs. A file that is not listed is a validation error, so
no data can escape the frozen hashes.

`manifest.counts` is the machine-readable statement of coverage; `check_corpus.py` recomputes
every value from `data/`. `manifest.staging` records the current stage of the dataset —
for v0.2.0 it is `university-runs`: the corpus has 204 families on three schemas, the frozen
state banks cover all 204 and model runs and evidence also cover all 204; the PostgreSQL
cross-check covers the 12 seed families (see [CROSS_DBMS.md](CROSS_DBMS.md)). The same note
is repeated in the manifest and the dataset card so that coverage claims stay
machine-checkable.

## Integrity rules

1. Every file under `data/` must be listed in `manifest.json` with its sha256; a mismatch
   means the dataset was modified after freezing.
2. `manifest.counts` must be recomputable from `data/` alone.
3. `status: refuted` requires at least one state in `refuting_states` and a non-empty
   witness whose state is one of them; `preserved`/`no_rewrite` must not carry states.
4. `status: preserved` means no refuting state was found — it does **not** prove
   equivalence.
5. Models are described by digest, not by name alone. Two runs of "the same" tag can differ.
6. Every *evaluated* family must have a run record for every model directory and an
   evidence file. A run record may only exist for a family that has frozen states.
7. Every evidence file must pin the current corpus and state-bank hashes in its protocol;
   `check_corpus.py` recomputes them, so CI fails when evidence and inputs drift apart.

## Known limitations

- Synthetic schemas: coverage of real-world query shapes is partial.
- A finite state bank is not a proof; `preserved` is evidence of absence, not absence of bugs.
- Model behaviour changes with engine version; the engine version is part of the protocol.
- One response per (model, family), temperature 0, no explicit seed: the raw text is
  stored as produced but a rerun is not guaranteed to be byte-identical.
- Candidate rewrites were executed on MySQL only; the PostgreSQL cross-check covers the 12
  seed families and is not first-class evidence. The university schema has not been ported
  to PostgreSQL yet.
- The state bank is shared by all families of a schema: it stresses the schema, not every
  individual query shape. Coverage of edge cases that are specific to one family is a
  design target, not a guarantee.
- `breaking_profile` is a design intent, not a measurement.
- The model set is six models; the originally planned `gemma4:26b` did not fit the collection
  hardware (17.3 GB model on 15.7 GB RAM, no GPU) and is excluded. Engine versions span
  Ollama 0.40.4–0.40.6 because the series were collected on different days; the version is
  recorded in every run and evidence protocol.
- No deterministic rules baseline: the rule module of the source application is an analyser,
  not a rewrite generator.
- Service-level failures (empty or failed responses) are recorded as `error` and are not
  retried, because the protocol allows one answer per family: 33 of 1 224 records, mostly
  `qwen2.5:3b` (16) and `llama3.2:3b` (10).
- 23 answers are unparsable or invalid SQL and are stored as `unsupported` (15
  `phi3.5:3.8b`, 6 `qwen2.5:3b`, 1 `qwen2.5-coder:7b`, 1 `llama3.2:3b`); execution
  failures caused by the candidate SQL itself (missing derived-table aliases,
  `ONLY_FULL_GROUP_BY` violations, unknown columns) are `error` records, not silently
  dropped.
