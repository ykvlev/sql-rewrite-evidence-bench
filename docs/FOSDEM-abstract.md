# FOSDEM PGDay 2027 — proposal draft

**Status:** draft, not submitted. Deadline: 2026-12-01 23:59 CET.

**Track fit:** PostgreSQL, query optimisation, tooling around query rewriting.

## Title

When a rewrite looks faster but breaks the result: executable counterexamples for
LLM-proposed SQL rewrites

## Abstract (for the CFP form)

Large language models are increasingly used to propose SQL rewrites for performance.
A rewrite can be syntactically valid, run faster, and still change the result: duplicate
rows collapse, NULL semantics shift, ordering or LIMIT is lost. Measuring execution time
alone cannot catch this, and formal equivalence checkers only cover a subset of SQL.

This talk presents an approach that checks rewrites against the states a schema actually
allows, and records the evidence rather than a score. For each candidate rewrite the
approach executes the reference and the candidate on a bank of database states generated
under the real constraints, and when the results differ it stores the refuting state and
the concrete rows that prove the difference.

Two findings from the pilot dataset:

- A model specialised in code was **not** safer than a general-purpose one: it rewrote more
  often and its rewrites were refuted more often.
- Three different models independently produced the same wrong rewrite, replacing
  `UNION ALL` with `UNION`: row multiplicities disappeared, and none of the randomly
  generated states caught it — only the states designed for multiplicity did.

The talk argues that PostgreSQL practitioners adopting LLM-assisted rewriting need a
validation step before trusting a speedup, and shows a reproducible protocol that can be
run against a real database.

## What the audience gets

- A concrete failure mode that survives review because it is not visible in timing.
- A reproducible procedure: state profiles, execution, minimal counterexample.
- An open dataset and scripts, with every number recomputable.

## Speaker

Artem Yakovlev, Polytechnic College, Novgorod State University (ORCID 0009-0006-8617-7895).

## Notes for internal use (remove before submission)

- Keep the abstract under the CFP character limit; check the form when it opens.
- The talk is 45 minutes: budget ~20 minutes for the approach, ~15 for the findings,
  ~10 live demonstration of a counterexample.
- The dataset link should point to a released version with a DOI, not to master.
