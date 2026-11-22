---
name: build-in-slices
description: Implement code test-first, one small slice at a time, in new or legacy code. Use whenever writing or changing code, including picking up the next task from a plan.
---

# Build in slices

## Before touching existing code

If the code you're about to change has no tests:

1. **Characterization tests first.** Write tests that record what the code does *today*, even if it looks wrong. Assert on actual outputs. These are your safety net, not a spec.
2. **Find a seam.** If the code can't be tested as is (hard-wired DB, globals, statics), make the *smallest* mechanical change to get it under test: extract a function, inject a dependency, wrap a call. Commit that separately with no behaviour change.
3. Weird behaviour you find goes to the user as a question. Don't "fix" it, because something downstream may depend on it.

## Loop, for each task

1. **Red:** write a test that fails for the behaviour you're adding, named after the requirement (`test_FR2_…`). For a bug, the test reproduces it.
2. **Green:** write the least code that makes it pass.
3. **Clean:** refactor while tests stay green. Match the surrounding code's style, even if it's old-fashioned.
4. **Verify:** run the checks in `context/TEAM.md` and show the output.
5. **Commit:** one task per commit, referencing the task and requirement IDs.

## Rules

- Never mix refactoring and behaviour change in the same commit.
- Don't write more than ~100 lines without running something.
- No new dependency, config key or environment variable without saying so explicitly.
- Never weaken, skip or delete a test to get green. If a test is wrong, say why and ask.
- If the plan or SAD turns out wrong, stop and propose an update. Don't silently improvise a different design.
