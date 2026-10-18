# Positioning of SREB — corrected

This note exists because our first formulation was **wrong** and was caught during
literature review on 2026-10-19. It is kept in the repository so the mistake is not
repeated and so reviewers can see the reasoning.

## What we claimed first (wrong)

> "SREB is the first dataset of executable evidence for SQL rewrites."

That is false. Two predecessors exist:

| Work | What it already does |
|---|---|
| **SQL-RewriteBench** (arXiv 2607.09251, 2026) | 180 instances, correctness-gated, full-denominator evaluation, a database and result evidence per instance |
| **provensql** (Zenodo 10.5281/zenodo.21854387, preprint 08.2026) | for a DIFFERENT verdict returns a **concrete executable counterexample database instance** as a replayable witness; 213 annotated rewrites, 511 mutations |

So "executable counterexample" is **not** our novelty. Writing it as ours would be
dishonest and a reviewer would find these two papers in minutes.

## What we can honestly claim

> To our knowledge, SREB is the first public dataset that links **model-proposed**
> rewrites to the **state violating the schema constraints** and to the **differing rows**,
> at the level of individual model samples rather than method scores.

The distinction is narrow but real:

- SQL-RewriteBench **scores methods** on instances; it is an evaluation harness.
- provensql is a **verdict tool** for individual rewrites: it answers "correct or
  different" and can produce a witness for that one rewrite.
- SREB records **what a model proposed across a corpus**, keeps the raw candidate, the
  refuting state profile and the witness together, and separates refutation rate from
  rewrite propensity.

## What that means for the paper

1. The claim in `PAPER-OUTLINE.md` §"claim in one sentence" must be replaced.
2. Related Work must cite both predecessors explicitly, not hide them.
3. The contribution should shift from "we have evidence" to **"we can say how adequate the
   evidence is"** — i.e. whether a finite bank of states catches the semantic errors that
   actually occur, and which state profiles are responsible for catching them.

## The open question this exposes

If counterexample evidence is not new, the defensible contribution is **adequacy**:
given a bank of allowed states, what fraction of wrong rewrites does it refute? That is a
mutation-adequacy question for SQL queries, and it is the direction the paper should take
instead of claiming priority on "evidence".
