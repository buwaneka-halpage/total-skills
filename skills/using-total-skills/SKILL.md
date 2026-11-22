---
name: using-total-skills
description: Router for the team's engineering skills and SDLC. Use at the start of any coding, debugging, git, GitHub, CI/CD, documentation or release task to pick the right workflow, and whenever it's unclear which skill applies.
---

# Using the team skills

Before any non-trivial work, read:
1. `context/TEAM.md` (in this plugin): team rules. Overrides generic habits.
2. `docs/environment.md` (in the project): stack, infra, cloud, CI/CD, decisions. **If it's missing, run `discover-environment` first.**
3. `docs/git-strategy.md`: branching rules.

## The lifecycle

```
PHASE 0: DISCOVER (once per project, refreshed when infra changes)
  discover-environment   inventory: stack, infra, cloud, CI/CD, source control
  map-codebase           code structure, tests, hotspots (existing code)
  visualize-codebase     visual onboarding guide
  choose-git-strategy    analyze history or decide from requirements → docs/git-strategy.md

PHASES 1–8: DELIVER
  1 grill-the-plan       gather requirements
  2 write-srs            SRS with FR / NFR / REG IDs
  3 write-architecture   SAD
  4 plan-slices          tasks  ──→ issues (draft → GitHub)
  5 build-in-slices      TDD    ──→ git-workflow (branch, commit, sync)
  6 review               ──→ visualize-changes, open-pr, address-pr-comments, resolve-conflicts
  7 ship-to-production   ──→ ci-cd (only if in scope)
  8 final-report

ANY TIME: diagnose (broken), encode-lesson (learned something), visualize-changes (what changed?)
```

## Pick the entry point

- New or unfamiliar project → Phase 0.
- User asks "what does this project use…?" → answer from `docs/environment.md` (`discover-environment` query mode).
- New feature or behaviour change → 1 → 8.
- Small change → `git-workflow` → `build-in-slices` → `review` → `open-pr`.
- Bug → `diagnose` → `review` → `open-pr`.
- "What changed?" / large PR / after a pull → `visualize-changes`.
- PR feedback → `address-pr-comments`. Conflicts → `resolve-conflicts`. CI red → `ci-cd`.

Use the lightest path that fits. Scale documents to the change.

## Always

1. **State assumptions** before non-trivial work. List them and say you'll proceed unless corrected.
2. **Stop on contradictions.** If the SRS, SAD, code and ticket disagree, name the conflict and ask.
3. **Look facts up yourself:** code, config, `docs/environment.md`. Ask only for decisions.
4. **Prove it.** "Done" means a test or command you ran, with its output.
5. **Show, don't tell.** For structure, flows or large changes, use a diagram or `visualize-changes` before walls of text.
6. **Draft first for anything outward-facing.** Issues, PRs, comments and replies are drafted to `drafts/` and posted only after the user approves.
7. **Stay in scope.** Note unrelated problems. Don't fix them in the same change.
8. **Production is different.** Anything reaching a shared or production environment goes through `ship-to-production`.
