# total-skills

A team-owned skill pack for AI coding agents (Claude Code, Cursor, Codex) that follows a full SDLC:
discover → requirements (SRS) → architecture (SAD) → plan → TDD build → review → ship → final report,
with GitHub workflow, CI/CD and visual code understanding built in.

## Skills

| Phase | Skill | Output |
|---|---|---|
| Router | `using-total-skills` | picks the workflow |
| 0 Discover | `discover-environment` | `docs/environment.md`: stack, infra, cloud, CI/CD (queryable) |
| | `map-codebase` | `docs/codebase-map.md` |
| | `visualize-codebase` | `docs/visual/codebase.html`: diagrams, module map, hotspots, reading tour |
| | `choose-git-strategy` | `docs/git-strategy.md` |
| 1 Requirements | `grill-the-plan` | agreed decisions |
| 2 SRS | `write-srs` | `SRS.md` (FR / NFR / REG IDs) |
| 3 Architecture | `write-architecture` | `SAD.md` |
| 4 Plan | `plan-slices`, `issues`, `project-management` | `PLAN.md`, GitHub issues, project board, Gantt chart |
| 5 Build | `build-in-slices`, `git-workflow`, `diagnose` | code + tests, clean commits |
| 6 Review | `review`, `visualize-changes`, `open-pr`, `address-pr-comments`, `resolve-conflicts` | PR, change map |
| 7 Release | `ship-to-production`, `ci-cd` | release note |
| 8 Close | `final-report` | `REPORT.md` with traceability matrix |
| Always | `encode-lesson` | rule / test / skill update |

Plus:
- `hooks/git-guard.py`: blocks force-push, `reset --hard`, `clean -f`, `branch -D`, direct pushes to main/develop/release, `gh pr merge`, and changing branch protection.
- `scripts/change-map.py`: interactive HTML change map / hotspot map from any git range (Python stdlib only).
- `scripts/gantt.py`: interactive Gantt (critical path, dependencies, status) + Mermaid gantt, from `PLAN.md`, JSON or a GitHub Project.

## Setup
1. Fill in `context/TEAM.md`.
2. Install in Claude Code:
   ```bash
   claude --plugin-dir /path/to/total-skills
   ```
   Or copy `skills/*` into a repo's `.claude/skills/` to share with that repo's team. The hook and script need the plugin install.
3. In each project, start with: "run discover-environment".

## Visualize changes without an agent
```bash
python3 scripts/change-map.py --repo /path/to/project --base origin/main --head HEAD --out changes.html
python3 scripts/change-map.py --repo /path/to/project --hotspots --since "1 year ago" --out hotspots.html
```

## Gantt chart without an agent
```bash
python3 scripts/gantt.py --plan docs/<feature>/PLAN.md --start 2026-12-01 --out gantt.html --mermaid gantt.md
python3 scripts/gantt.py --github-project <org> <project-number> --out status.html
```

## Adding a skill
- Folder `skills/<name>/SKILL.md` with `name` and `description` frontmatter; the description says **when** to use it.
- Keep it under ~80 lines; put long tables in `references/`.
