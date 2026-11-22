---
name: resolve-conflicts
description: Resolve git merge or rebase conflicts by understanding the intent of both sides, then verifying with tests. Use when a merge, rebase, cherry-pick or PR shows conflicts.
---

# Resolve conflicts

## 1. Know where you are
```bash
git status            # which operation: merge, rebase, cherry-pick?
ls .git/rebase-merge .git/rebase-apply .git/MERGE_HEAD 2>/dev/null
```
**During a rebase, "ours" is the branch being rebased onto (base) and "theirs" is your commit.** This is the opposite of a merge. State which is which before touching anything.

## 2. Understand both sides, per file
- `git log --oneline --left-right HEAD...MERGE_HEAD -- <file>` (or the rebase equivalent) and read the commits/PRs that touched the conflicting lines.
- Write one line per conflict: "Base changed X because …; our branch changed Y because …".

## 3. Resolve
- **Mechanical** (both added imports, formatting, adjacent edits, renamed symbol): combine both.
- **Semantic** (both changed the same logic differently): keep both intents if they're compatible, and explain how.
- **Unclear or incompatible intent:** stop and present both versions side by side with your recommendation. The user decides.
- Lockfiles and generated files: regenerate with the tool, don't hand-merge.
- Remove all markers: `git diff --check` and `grep -rn '^<<<<<<<\|^>>>>>>>' .` must be empty.

## 4. Verify
Build and run the full verify commands. A conflict resolution isn't done until tests pass. Then `git add` and continue the operation (`--continue`).

Never `--abort`, `reset --hard` or force-push without approval. Pushing a rebased branch needs `--force-with-lease`, and only with approval.
