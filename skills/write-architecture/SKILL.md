---
name: write-architecture
description: Write a Software Architecture Document (SAD) describing how an approved SRS will be implemented. Use after the SRS is approved and before planning or coding.
---

# Write the architecture document

Save to `docs/<feature>/SAD.md`. Keep it as short as the change allows: a page for a feature, more for a new system.

```markdown
# SAD: <title>        Version / date / SRS version it implements

## 1. Context: the system and its neighbours (diagram: Mermaid is fine)
## 2. Current architecture: (existing systems) the relevant part as it is today, from docs/codebase-map.md
## 3. Proposed design: components added or changed, responsibilities, data flow
## 4. Interfaces: APIs, schemas, messages, file formats; versioning and compatibility
## 5. Data: models, migrations (expand → migrate → contract), retention
## 6. Cross-cutting: security, error handling, logging/metrics, performance, configuration
## 7. Decisions: for each significant choice: options considered, decision, why (ADR style)
## 8. Requirement mapping: FR/NFR ID → component(s) that satisfy it
## 9. Risks & rollback
```

## For existing code

- Extend the existing patterns. Only propose a new pattern in section 7, with a reason the old one can't work.
- Prefer the smallest change that meets the SRS. Big refactors are separate work with their own SRS.
- Identify the **seams**: places where new code can be inserted and tested without rewriting the old code.

Get approval before `plan-slices`.
