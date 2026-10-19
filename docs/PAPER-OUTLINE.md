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

## 6. Pilot results (v0.2.0, numbers from `data/`)

The v0.2.0 corpus has 204 families on three schemas (library, shop, university); the
evidence covers all 204 families, 28 states each, six models and 34 272 executed checks on
MySQL 8.4.11 (120 refuted rewrites in 75 families).

- The code-specialised models rewrote more often and were refuted more often than the
  general-purpose ones. `deepseek-coder-v2` proposed 77 rewrites (27 refuted),
  `qwen2.5-coder:7b` 30 (12 refuted), `qwen2.5:7b` 32 (8 refuted), `phi3.5:3.8b` 30
  (8 refuted, plus 15 unparsable answers). The two 3B models rewrote aggressively:
  `qwen2.5:3b` proposed 85 rewrites (39 refuted, 6 unparsable, 16 execution errors),
  `llama3.2:3b` proposed 53 (26 refuted, 1 unparsable, 10 execution errors).
- Four of the six models independently produced the same wrong rewrite class (`UNION ALL` →
  `OR` or `DISTINCT` over the union), losing row multiplicities; `union_bag` and
  `lib_union_bag_books` were refuted by every one of those four models. Several families have
  an identical normalised wrong candidate produced by two or more models, e.g. `UNION`
  rewritten as `OR` or `IN`, which keeps duplicates that `UNION` removes.
- The models fail in different ways on the same family: `union_bag` is broken by an `OR`
  rewrite in three models and by `DISTINCT` over `UNION ALL` in the fourth. Invalid SQL is
  also part of the record: missing derived-table aliases, `ONLY_FULL_GROUP_BY` violations,
  hallucinated clauses such as `WITHIN ...`, and unknown columns are stored as
  `error`/`unsupported`, not discarded.

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
