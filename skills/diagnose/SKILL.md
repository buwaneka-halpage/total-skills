---
name: diagnose
description: Systematic debugging for failures, flaky tests, incidents and performance regressions. Use when something is broken, throwing, failing in CI, slow, or behaving differently between environments.
---

# Diagnose

## 1. Build a feedback loop first

This is most of the work. Get a fast, repeatable pass/fail signal that fails on **this** bug. In rough order of preference:

1. A failing automated test at the nearest seam
2. A script hitting the service (curl / CLI) with a fixed input
3. Replaying a captured payload, log or event
4. A minimal harness with dependencies mocked
5. Old version vs new version on the same input (diff), or `git bisect run`

Make it faster and more deterministic before you go on (pin time, seed randomness, isolate I/O).

## 2. Hypothesise and test

- Write down 2–3 hypotheses ranked by likelihood. Test the cheapest one that would rule out the most.
- Change one thing at a time. Read actual state with logs, a debugger or queries. Don't guess.

## 3. Fix the root cause

- Fix where the system first went wrong, not where the symptom appeared.
- A guard, retry, or swallowed error is only a fix if the state it handles is legitimate.
- Search for the same fault elsewhere.
- Keep the reproducing test as a regression test.

## 4. Report

Symptom → root cause → fix → evidence (test output). If finding it took a deep dig, suggest the log, metric or alert that would have shown it straight away.

**Redact secrets, tokens and customer/personal data** from anything you show.
