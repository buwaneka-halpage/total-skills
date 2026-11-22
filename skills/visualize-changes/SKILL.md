---
name: visualize-changes
description: Show what changed in a commit range, branch or PR visually (change map treemap, blast-radius graph, before/after diagrams, guided change story) instead of a raw diff. Use when the user asks what changed, before reviewing a large PR, after pulling new commits, or when opening a PR with a large diff.
---

# Visualize changes

## 1. Change map (always)

```bash
python3 <this-plugin>/scripts/change-map.py --repo . --base <base-ref> --head <head-ref> --out docs/visual/changes-<head>.html
```
(Range examples: `origin/main..HEAD` for a branch, `HEAD~5..HEAD` for recent commits, the PR's base and head for a PR.)

This gives a treemap of the repo (changed files coloured by added/removed lines; unchanged files greyed), a blast-radius list (files that import changed files), a commit timeline, and per-file diffs on click.

## 2. Change story (for anything over ~5 files)

Append to the same page, or publish it as an Artifact:
1. **One-sentence summary** and the **why** (from commits, PR or issue).
2. **Before / after diagrams:** a Mermaid diagram of the affected structure or flow, before and after, side by side. Highlight added nodes in green, removed in red, changed in amber.
3. **Guided tour:** changed files grouped by intent ("new endpoint", "schema migration", "tests", "renames only"), in suggested reading order, with mechanical changes collapsed.
4. **Risk markers:** migrations, public API changes, config/secrets, security-sensitive files, files with no test changes.

## Rules
- Diagrams must reflect the actual diff. Cite file paths.
- Group pure renames and formatting so they don't hide real changes.
- Large repos: limit the treemap to changed directories plus one level of context.
