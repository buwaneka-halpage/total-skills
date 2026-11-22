---
name: git-workflow
description: Day-to-day git discipline for the chosen strategy (branching, commits, worktrees, syncing, finishing a branch). Use when starting work on a task, committing, syncing with the base branch, or when work on a branch is complete.
---

# Git workflow

Read `docs/git-strategy.md` first and follow its rules. If it's missing, run `choose-git-strategy`.

## Start
1. Sync: `git fetch origin` and branch from the up-to-date base named in the strategy.
2. Name the branch per the strategy, including the issue number: `feat/123-export-csv`.
3. For parallel work, use a separate worktree (`git worktree add ../<repo>-123 -b feat/123-…`), and check first that you're not already in one.

## Commit
- One logical change per commit, message `type(scope): subject` and `Refs #123`.
- Before each commit: `git diff --staged` review, no secrets or generated junk, run the verify commands from `context/TEAM.md`.
- Never mix refactoring with behaviour changes.

## Stay current
- Sync with the base at least daily (merge or rebase per strategy). On conflict → `resolve-conflicts`.

## Finish (when the task's tests pass)
Present exactly these options and wait:
1. **Open a PR** (→ `open-pr`, the normal path)
2. **Keep the branch** for later
3. **Discard**: only on explicit request, after showing what would be lost

## Never, without explicit approval for that specific command
`push --force` (use `--force-with-lease` if approved), push directly to protected branches, `reset --hard`, `clean -fd`, `branch -D`, rewriting published history, changing branch protection.
