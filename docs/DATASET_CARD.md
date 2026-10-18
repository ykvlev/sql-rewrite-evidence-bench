# Dataset card — SREB v0.1

## Purpose

To make SQL rewrite quality measurable with executable evidence rather than declared
success rates. A model that claims a rewrite preserves the result must survive the
allowed states of the database; when it does not, the dataset records exactly where.

## Structure

### corpus/families.json

```json
{
  "schema": "library",
  "ddl": ["CREATE TABLE borrowers (...)", "..."],
  "constraints": ["borrowers.id PRIMARY KEY", "loans.borrower_id REFERENCES borrowers(id)"],
  "families": [
    {"id": "loan_count", "reference_sql": "SELECT ...", "profile": "multiplicity"}
  ]
}
```

### states/states.json

Frozen bank of database states per family. Each state is a profile plus seed and rows:

```json
{"family": "loan_count", "profile": "multiplicity_0", "seed": 0, "rows": {...}}
```

Profiles cover what schemas actually allow: `fixed`, `empty`, `no_rows`, `multiplicity`,
`zero_value`, `nullable`, `boundary`, `ties`, plus random states from a seeded generator.

### runs/<model>/<family>.json

Raw model response and parsed candidate, with the model digest and sampling parameters.

### evidence/<family>.json

```json
{"family": "loan_count", "model": "qwen2.5-coder:7b", "status": "refuted",
 "refuting_states": ["multiplicity_0"], "witness": {"reference": [1,1,1,1], "candidate": [1,1,1]}}
```

## Integrity rules

1. Corpus and state bank hashes are frozen in `manifest.json`; a run whose hashes differ
   is invalid and must be discarded.
2. `status: refuted` requires at least one state in `refuting_states` and a non-empty witness.
3. `status: preserved` means no refuting state was found — it does **not** prove equivalence.
4. Models are described by digest, not by name alone. Two runs of "the same" tag can differ.
5. Every number in derived tables must be recomputable from `data/` alone.

## Known limitations

- Synthetic schemas: coverage of real-world query shapes is partial.
- A finite state bank is not a proof; `preserved` is evidence of absence, not absence of bugs.
- Model behaviour changes with engine version; the engine version is part of the protocol.
