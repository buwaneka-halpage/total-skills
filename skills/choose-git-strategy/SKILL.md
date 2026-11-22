---
name: choose-git-strategy
description: Analyze an existing repo's git history to identify its branching strategy, or recommend one for a new project from its requirements, then present options and record the user's choice. Use at project start, when docs/git-strategy.md is missing, or when the user asks about branching, releases or merge strategy.
---

# Choose the git strategy

Output: `docs/git-strategy.md` (and the Decisions line in `docs/environment.md`). `git-workflow` enforces it.

## A. Existing repo: find out what's really happening

Run read-only and summarise. Don't trust a README's claims over the history.

```bash
git branch -r --sort=-committerdate | head -40                   # long-lived branches? develop, release/*, hotfix/*
git for-each-ref --format='%(refname:short) %(committerdate:relative)' refs/remotes | sort -k2 | head -40
git log --first-parent --oneline -50 origin/<default>            # merge commits vs squash vs direct commits
git log --merges --oneline -30                                   # merge sources
git tag --sort=-creatordate | head -20                           # release cadence & versioning (semver? dates?)
git log --since=90.days --format='%ad' --date=short origin/<default> | sort | uniq -c   # commit frequency
gh api repos/{owner}/{repo}/branches/<default>/protection 2>/dev/null  # required reviews/checks
gh pr list --state merged --limit 30 --json headRefName,baseRefName,mergedAt,createdAt # branch lifetimes
```

Report: "You're effectively using **X**", with evidence (branch names, merge style, average PR lifetime, release tags), plus problems found (stale branches, very long-lived branches, direct pushes to main, no protection).

## B. New project: decide from requirements

Read the SRS and `docs/environment.md`. The deciding factors:

| Factor | Points toward |
|---|---|
| Deploy continuously, one live version, good test coverage | Trunk-based / GitHub Flow |
| Small team, PR review required, deploy from main | GitHub Flow |
| Scheduled releases, release stabilisation/QA period | Release branches (trunk + `release/x.y`) |
| Several versions supported in production simultaneously (customer sites, plants, regulated versions) | Release branches with backport, or GitFlow |
| Formal change approval per release, separate QA team | GitFlow or release branches |
| Many parallel agents / developers | Trunk-based with short branches + feature flags |

## Present options (always, both modes)

Show 2–4 relevant options in this format, recommended first:

```
Option: <name>  (Recommended)
  Diagram:   (Mermaid gitGraph showing main/feature/release flow)
  Fits because: <tie to evidence / requirements>
  Costs:     <what's harder>
  Rules:     branch names, merge method (squash/merge/rebase), protection, release tagging, hotfix path
```

Catalogue: `references/strategies.md`. After the user chooses, write `docs/git-strategy.md` with the rules section and the diagram. For an existing repo, list the migration steps (e.g. delete stale branches, enable protection) as **proposals**. Don't change remote settings yourself.
