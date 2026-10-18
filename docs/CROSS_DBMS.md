# Cross-DBMS verification: PostgreSQL 16.15

Status: the evaluation mechanism was re-run on PostgreSQL for the 12 seed families on
2026-10-19. Full-corpus PostgreSQL evidence is not published in v0.2.0; this document
records the portability check and its limits.

## What was verified

The published MySQL evidence for the 12 seed families of the library schema was
recomputed on PostgreSQL 16.15 from the same inputs:

| Input | Value |
|---|---|
| Corpus | `data/corpus/families.json` (12 families, unchanged reference SQL) |
| State bank | `data/states/states.json`, the same 28 states |
| Model answers | the saved runs in `data/runs/` (three seed models, unchanged) |
| DBMS | PostgreSQL 16.15 (previous series preflight used the same version) |
| DDL | the corpus DDL, executed without any adaptation |
| Reference executions | 12 families × 28 states = 336 |
| Candidate checks | 12 families × 28 states × 3 models = 1 008 |

For every state the reference and the candidate were executed read-only in a clean
private schema, and the resulting row lists were compared; the per-(model, family, state)
outcome was then compared with the refuting-state sets published in `data/evidence/`.

## Result

- **DDL adaptation required: none.** The library DDL (`INTEGER PRIMARY KEY`,
  `VARCHAR` lengths, inline foreign keys) and all 12 reference queries executed on
  PostgreSQL unchanged.
- **Status mismatches with the MySQL evidence: 0** of 1 008 candidate checks.

The raw check record is stored in [cross_dbms_seed_check.json](cross_dbms_seed_check.json).
No per-state rows or pins are duplicated there; the record is a verification log, not a
second evidence bank.

## Why the comparison is meaningful, and what it does not show

- Equivalence is checked **within one engine**: the reference and the candidate run on the
  same DBMS, so engine-specific row order rules do not affect the verdict. MySQL sorts
  NULLs first in ascending order and PostgreSQL sorts them last, so the *ordering of rows
  in a witness* can differ between engines; the refuting state and the multiset difference
  do not.
- The check covers the 12 seed families only. It shows that the mechanism ports, not that
  every one of the 136 families behaves identically on PostgreSQL. In particular, queries
  with engine-specific functions would need dialect review before a full PostgreSQL run.
- The dataset format stores one `dbms` per evidence file. Adding a second engine as
  first-class evidence requires a format extension (separate evidence per engine or a
  `dbms` field per record) and is left for the next version.
