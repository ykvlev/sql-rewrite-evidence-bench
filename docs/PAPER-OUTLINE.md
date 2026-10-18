# SREB paper — outline

Working outline for the arXiv preprint and the FOSDEM PGDay 2027 talk.
Nothing here is final; every number must come from `data/` before publication.

## Working title

**SQL Rewrite Evidence Benchmark: executable counterexamples for language-model rewrite suggestions**

Alternative for the talk: *When a rewrite looks faster but breaks the result.*

## The claim in one sentence

Published rewrite quality is measured by counts of successful-looking suggestions; we
propose to measure it by the database states on which a suggestion is provably wrong,
and we release the first dataset of such evidence.

## 1. Introduction

- Rewriting SQL is common practice for performance; language models now suggest rewrites.
- A rewrite can be syntactically valid, faster, and wrong: multiplicities collapse,
  NULL semantics shift, ordering or LIMIT is lost.
- Timing benchmarks cannot see this. Formal checkers cover a subset of SQL.
- Contribution: evidence-first evaluation, an open dataset with witnesses, a repro protocol.

## 2. Related work

| Group | Examples | What it gives | What it does not |
|---|---|---|---|
| Formal equivalence | Cosette, VeriEQL, HoTTSQL | proofs for supported constructs | coverage of full SQL, per-run evidence |
| Rewrite generation | GenRewrite, LLM-R2, R-Bot, QUITE | systems, success rates | executable witnesses |
| Benchmarks | Spider, BIRD, TACO | text-to-SQL evaluation | rewrite validation |
| DBMS testing | Pivoted Query Synthesis, NoREC, SQLancer, QED | finding engine bugs | evaluating model rewrites |

Positioning: SREB is not another text-to-SQL benchmark and not a formal prover. It is a
record of what happened when a model's rewrite met a database.

## 3. What counts as evidence

Define the terminology the dataset uses:

- **allowed state** — a database instance satisfying the declared schema and constraints.
- **state profile** — the property a state is built to exercise (empty, nullable,
  multiplicity, boundary, ties, random).
- **refutation** — reference and candidate return different results on an allowed state.
- **witness** — the refuting state and the rows that differ, in a form a human can read.
  Witnesses are not minimised: no state-reduction procedure was run, so they are the first
  refuting state found, not the smallest one.

Explicitly: absence of refutation on a finite bank is **not** a proof of equivalence.
The dataset must never imply otherwise.

## 4. Dataset construction

- Schemas with explicit constraints; query families per schema.
- Family = (schema, reference SQL, intended profile).
- State generation: profile templates + seeded random instances, frozen before model runs.
- Hashing: corpus and state bank sha256 frozen in `manifest.json`; a run with other hashes
  is invalid.
- Model protocol: digest, quantization, temperature, context length, max tokens, one answer
  per query, no seed where the engine allows none.

## 5. Evaluation protocol

For each (family, model):

1. Parse the candidate; reject unsupported or unsafe statements.
2. For each allowed state: create a clean database, apply the state, run reference and
   candidate read-only, compare rows.
3. Record outcome: `preserved` / `refuted` / `no_rewrite` / `unsupported` / `error`.
4. If refuted, store the profile, the state seed and the row difference.

## 6. Pilot results (numbers pending final dataset)

The v0.2.0 corpus has 136 families on two schemas; the pilot evidence below covers the
12-family library seed, 28 states each, 336 checks per model, three models.

- The code-specialised model rewrote more often and was refuted more often than the
  general-purpose model — the opposite of the intuition that specialisation helps.
- All three models independently produced the same wrong rewrite (`UNION ALL` → `OR`),
  losing row multiplicities; only the states designed for multiplicity, nullable columns
  and ties caught it, and none of the random states did.
- Two models failed on the same family with *different* mechanisms, which matters for
  error taxonomies.

## 7. Reproducibility

- Every published number recomputable from `data/` without rerunning a model.
- Every run is traceable to its model digest, sampling parameters, DBMS version and the
  corpus/state-bank hashes pinned in its record. Model collection and evaluation scripts
  are not part of v0.2.0, so a rerun requires reproducing the recorded protocol.
- Engine version is part of the record: behaviour changes across releases.

## 8. Limitations

- Synthetic schemas: partial coverage of real workloads.
- Finite state banks: no completeness claims.
- One or two DBMS engines in the pilot.
- Model sets age quickly; the dataset is designed to accept new models without breaking.

## 9. Availability

Repository, Zenodo DOI (version and concept), HuggingFace dataset card, leaderboard.

## 10. Open questions for the community

- Which state profiles are worth standardising?
- How should refutation rate be normalised against rewrite propensity?
- Can formal methods consume the witnesses as seeds?

## Checklist before any submission

- [ ] every number in the text recomputed from `data/`
- [ ] corpus and state bank hashes match `manifest.json`
- [ ] model digests listed
- [ ] limitations section says plainly that preserved ≠ proven
- [ ] dataset DOI resolves to the released version, not to master
- [ ] no personal data anywhere in the dataset
