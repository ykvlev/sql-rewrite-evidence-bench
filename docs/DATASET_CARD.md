# Dataset card — SREB v0.1

## Purpose

To make SQL rewrite quality measurable with executable evidence rather than declared
success rates. A model that claims a rewrite preserves the result must survive the
allowed states of the database; when it does not, the dataset records exactly where.

## What the seed contains

| Item | Count |
|---|---|
| Query families (library schema) | 12 |
| Frozen states per family | 28 |
| Family–state pairs | 336 |
| Models | 3 (`qwen2.5-coder:7b`, `qwen2.5:7b`, `phi3.5:3.8b`) |
| Run records (model × family) | 36 |
| Evidence records (model × family) | 36 |
| Executed checks (model × family × state) | 1 008 |

## Structure

### corpus/families.json

Schema DDL, the constraints it enforces, and the query families with a query-shape
profile. `profile` is derived from the reference SQL only, never from model answers.

```json
{
  "schema": "library",
  "ddl": ["CREATE TABLE lib_readers (...)", "..."],
  "constraints": ["lib_readers.id PRIMARY KEY", "lib_loans.reader_id REFERENCES lib_readers(id)"],
  "families": [
    {"id": "loan_count", "reference_sql": "SELECT ...", "profile": "outer_join_aggregate",
     "intent": "Число выдач, включая ноль", "ordered": true}
  ]
}
```

### states/states.json

Frozen bank of database states. One bank of 28 states is applied to every family and
expanded one record per (family, state) pair, so each record is self-contained:

```json
{"family": "loan_count", "profile": "multiplicity_0", "profile_family": "multiplicity",
 "seed": 0, "rows": {"lib_readers": [[...]], "lib_books": [[...]], "lib_loans": [[...]]}}
```

`profile` is the stable state id used by evidence (`fixed_0`, `empty_0`, `no_loans_0`,
`multiplicity_0`, `zero_fee_0`, `nullable_0`, `boundary_0`, `ties_0`,
`random_uniform_0` … `random_uniform_19`); `profile_family` groups the ids
(`fixed`, `empty`, `no_loans`, `multiplicity`, `zero_fee`, `nullable`, `boundary`,
`ties`, `random_uniform`). Random states carry the generator seed.

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

### manifest.json

SHA-256 of every file under `data/`, plus the recomputable counts, the model digests and
the provenance of the upstream runs. A file that is not listed is a validation error, so
no data can escape the frozen hashes.

## Integrity rules

1. Every file under `data/` must be listed in `manifest.json` with its sha256; a mismatch
   means the dataset was modified after freezing.
2. `manifest.counts` must be recomputable from `data/` alone.
3. `status: refuted` requires at least one state in `refuting_states` and a non-empty
   witness whose state is one of them; `preserved`/`no_rewrite` must not carry states.
4. `status: preserved` means no refuting state was found — it does **not** prove
   equivalence.
5. Models are described by digest, not by name alone. Two runs of "the same" tag can differ.
6. Every family must have a run record for every model directory and an evidence file.

## Known limitations

- Synthetic schemas: coverage of real-world query shapes is partial.
- A finite state bank is not a proof; `preserved` is evidence of absence, not absence of bugs.
- Model behaviour changes with engine version; the engine version is part of the protocol.
- One response per (model, family), temperature 0, no explicit seed: the raw text is
  stored as produced but a rerun is not guaranteed to be byte-identical.
- Candidate rewrites were executed on MySQL only in this seed; portability to other
  engines is not established.
