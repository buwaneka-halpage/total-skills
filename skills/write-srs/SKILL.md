---
name: write-srs
description: Write a Software Requirements Specification (SRS) for a feature, change or new system. Use after requirements are gathered (grill-the-plan) and before architecture or code, for anything larger than a small fix.
---

# Write the SRS

The SRS is the contract. The architecture, tests, review and final report all trace back to its requirement IDs.

Save to `docs/<feature>/SRS.md` (or the location in `context/TEAM.md`):

```markdown
# SRS: <title>        Version / date / author / status

## 1. Purpose & scope: problem, users, what's in and out of scope
## 2. Current behaviour: (existing systems) how it works today; link to docs/codebase-map.md
## 3. Functional requirements
| ID   | Requirement (system shall …) | Priority | Acceptance criteria |
|------|------------------------------|----------|---------------------|
| FR-1 | …                            | Must     | Given / When / Then |
## 4. Non-functional requirements: performance, security, availability, data, compliance (NFR-1 …), each measurable
## 5. Constraints & assumptions
## 6. Must not change: existing behaviour that must keep working (REG-1 …)
## 7. Open questions
```

- Every requirement has an ID and a checkable acceptance criterion. "Fast" is not checkable; "p95 < 300 ms" is.
- For existing systems, section 6 is mandatory. It's what prevents regressions in old code.
- Blocking open questions → back to `grill-the-plan`. Get approval before `write-architecture`.
