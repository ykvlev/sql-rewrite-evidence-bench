# FOSDEM PGDay 2027 — submission

Deadline: **2026-12-01 23:59:59 CET** (2 December 01:59 Moscow). Notification by 2026-12-20.
Talk: 45 minutes + questions, English only. No abstract length limit in the form (minimum 30 characters).

## Title

When a rewrite looks faster but breaks the result: executable counterexamples for LLM-proposed SQL rewrites

## Abstract

Large language models are increasingly used to propose SQL rewrites for performance. A rewrite can be syntactically valid, run faster, and still change the result: duplicate rows collapse, NULL semantics shift, ordering or LIMIT is lost. Measuring execution time alone cannot catch this, and formal equivalence checkers only cover a subset of SQL.

This talk presents an approach that checks rewrites against the states a schema actually allows, and records the evidence rather than a score. For each candidate rewrite the approach executes the reference and the candidate on a bank of database states generated under the real constraints, and when the results differ it stores the refuting state and the concrete rows that prove the difference.

Two findings from the pilot dataset. First, a model specialised in code was not safer than a general-purpose one: it rewrote more often and its rewrites were refuted more often. Second, three different models independently produced the same wrong rewrite, replacing `UNION ALL` with a disjunction `OR`: row multiplicities disappeared, and none of the randomly generated states caught it — only the states built for multiplicity, NULL handling and ties did.

The talk argues that practitioners adopting LLM-assisted rewriting need a validation step before trusting a speedup, and shows a reproducible protocol that runs against a real database.

## What the audience gets

- A concrete failure mode that survives review because it is invisible in timing measurements.
- A reproducible procedure: state profiles, execution, and the rows that prove the difference.
- An open dataset and scripts where every published number can be recomputed.

## About the speaker

Artem Yakovlev, student, Polytechnic College of Yaroslav-the-Wise Novgorod State University.
ORCID: 0009-0006-8617-7895. Works on SQL query optimisation and on validation of
machine-generated query rewrites; author of the AI Database Optimizer toolkit and of the
SREB dataset.

## Submission notes (form field)

- **Track:** databases / query optimisation / tooling around query rewriting.
- **Travel and visa support:** a visa invitation letter would be needed for travel from Russia. The invitation policy mentions a valid paid registration while selected speakers receive a free ticket; please advise how to proceed in that case, and confirm when registration opens — the visa process has to start well before January.
- **Dataset:** the talk is based on a public dataset with a DOI (assigned on release) and on open scripts; the versioned release link will be included once published. A live demonstration of one counterexample takes about two minutes and needs only a laptop.
- **Recording:** please confirm whether the talk is recorded and published.
- **Materials:** slides can be provided before the event if recordings are made.

## Internal checklist (not part of the form)

- [ ] registration opened and completed
- [ ] visa invitation requested
- [ ] dataset DOI resolves to the released version, not to master
- [ ] abstract character count checked against the live form
- [ ] bio and photo added to the speaker profile
