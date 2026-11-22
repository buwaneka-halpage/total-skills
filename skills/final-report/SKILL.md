---
name: final-report
description: Write the final report that closes out a feature or project, tracing every requirement to its implementation and test evidence. Use when the work is merged or released, or when the user asks for a completion/handover report.
---

# Final report

Save to `docs/<feature>/REPORT.md`. Base every claim on evidence: commits, test runs, CI links, release notes. Never write "tested" without the evidence.

```markdown
# Final report: <title>        Date / version released / authors

## 1. Summary: what was delivered, in three sentences
## 2. Traceability matrix
| Req ID | Implemented in (files / PR) | Verified by (test names) | Result | Evidence |
|--------|-----------------------------|--------------------------|--------|----------|
## 3. Regression: REG-* items from the SRS and how each was confirmed
## 4. Deviations: differences from SRS/SAD and why (approved by whom)
## 5. Test summary: counts, coverage delta, test types, anything not tested and why
## 6. Release: environments, dates, rollout, rollback procedure
## 7. Known issues & follow-ups
## 8. Lessons learned: then run `encode-lesson` for each
```

Any requirement without a passing test or other evidence is marked **NOT VERIFIED**, never silently omitted.
