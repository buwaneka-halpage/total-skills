---
name: plan-slices
description: Break an approved SRS and architecture document into small, ordered, independently verifiable tasks. Use after the SAD is approved, or when a task feels too big to land in one change.
---

# Plan in slices

Prefer **vertical slices**: each one is a thin path through every layer that works end to end, rather than "all the DB, then all the API".

Save `docs/<feature>/PLAN.md`. For each task:

```
T<n>. <title>
  Satisfies: FR-2, NFR-1        (SRS IDs; every FR must appear in some task)
  Change:    files / modules (from the SAD)
  Proves:    the test(s) that show it works
  Depends:   T<x> or none
  Size:      S (<1h) / M (half day). Split anything bigger.
  Phase:     Foundation | Build | Verify | Release (or the project's own phases)
  Estimate:  working days, including review and testing (used for the Gantt chart)
  Owner:     who (optional)
  Status:    todo | in progress | blocked | done
  Start:     YYYY-MM-DD (only if fixed; otherwise scheduled from Depends)
  Issue:     #<n> (filled in by `issues`)
```

Rules:
- Each task leaves the system building, passing tests and deployable.
- **Existing code:** T1 is usually "characterization tests for the area we'll touch" (see `build-in-slices`).
- Put the riskiest slice early so surprises show up before most of the work is done.
- Migrations get their own tasks, in expand → migrate → contract order.
- Check that every FR/NFR ID is covered by at least one task.
- Render the schedule with `project-management` (Gantt) and show the plan **and** the Gantt to the user before building.
