---
name: open-pr
description: Prepare and open a GitHub pull request with a reviewer-friendly description, visual change summary and evidence. Use when a branch is ready for review. Always draft-first.
---

# Open a PR

## Before
- `review` has passed on the diff; verify commands are green; branch is synced with base.
- Commits are clean (squash fixups if the strategy uses rebase/merge).

## Draft the body: `drafts/pr/<branch>.md`

```markdown
## Why
<problem, links: Closes #123, SRS FR-x>
## What changed
<3–6 bullets; plus a Mermaid diagram if structure or flow changed (see visualize-changes)>
## Evidence
- Before: <failing test / screenshot / output>
- After:  <passing test / screenshot / output>
## Blast radius
<what could break, who's affected; one-way or reversible door>
## Rollback
<revert / flag off / down-migration>
## Reviewer guide
<suggested file reading order; where to look hardest>
```

Title: `type(scope): subject` (≤ 72 chars).

## Then
1. Run `visualize-changes` for large diffs (> ~10 files or ~400 lines) and link the change map.
2. Show the draft. After approval: `git push -u origin <branch>` and `gh pr create --title … --body-file drafts/pr/<branch>.md --base <base>` (add `--draft` if the user wants a draft PR on GitHub).
3. Report the PR URL. Opening a PR never authorises merging.
