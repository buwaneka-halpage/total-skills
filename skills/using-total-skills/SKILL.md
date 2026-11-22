---
name: using-total-skills
description: Router for the team's engineering skills and SDLC. Use at the start of any coding, debugging, review, documentation or release task to pick the right workflow, and whenever it's unclear which skill applies.
---

# Using the team skills

Read `context/TEAM.md` (in this plugin) before any non-trivial work. It holds our stack, environments and rules, and it overrides generic habits.

## The lifecycle

```
0. map-codebase        existing system? understand it first (read-only)
1. grill-the-plan      gather requirements
2. write-srs           SRS: FR / NFR / REG requirements with IDs
3. write-architecture  SAD: design, decisions, requirement mapping
4. plan-slices         ordered tasks, each tied to requirement IDs
5. build-in-slices     test-driven implementation, slice by slice
6. review              against SRS + SAD + checklist
7. ship-to-production  release safely
8. final-report        traceability matrix + evidence
   encode-lesson       after anything painful
   diagnose            any time something breaks
```

## Pick the entry point

- Unfamiliar or legacy repo → start at 0.
- New feature or behaviour change → 1 → 8 in order.
- Small change (one file, no behaviour change in the SRS sense) → `build-in-slices` → `review`. Skip the documents.
- Bug → `diagnose`, then `review`. Add an SRS only if the "bug" is really a requirements change.

Use the lightest path that fits. Scale documents to the change: a one-page SRS is fine.

## Always

1. **State assumptions** before non-trivial work. List them and say you'll proceed unless corrected.
2. **Stop on contradictions.** If the SRS, SAD, code and ticket disagree, name the conflict and ask.
3. **Look facts up yourself.** Read the code, config and docs before asking the user.
4. **Prove it.** "Done" means a test or command you ran, with its output.
5. **Stay in scope.** Note unrelated problems. Don't fix them in the same change.
6. **Production is different.** Anything reaching a shared or production environment goes through `ship-to-production`.
