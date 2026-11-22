# total-skills

A small, team-owned skill pack for AI coding agents (Claude Code, Cursor, Codex), modelled on the
Define → Plan → Build → Verify → Review → Ship lifecycle.

| SDLC stage | Skill | Output |
|---|---|---|
| 0. Understand existing system | `map-codebase` | `docs/codebase-map.md` |
| 1. Requirements gathering | `grill-the-plan` | agreed decisions |
| 2. Requirements spec | `write-srs` | `SRS.md` (FR/NFR/REG IDs) |
| 3. Architecture | `write-architecture` | `SAD.md` |
| 4. Planning | `plan-slices` | `PLAN.md` |
| 5. TDD build | `build-in-slices`, `diagnose` | code + tests |
| 6. Review | `review` | findings + verdict |
| 7. Release | `ship-to-production` | release note |
| 8. Close-out | `final-report` | `REPORT.md` with traceability matrix |
| Continuous | `encode-lesson` | rule / test / skill update |
| Router | `using-total-skills` | |

## Setup
1. Fill in `context/TEAM.md`. This is where the team-specific value lives.
2. Install locally in Claude Code:
   ```bash
   claude --plugin-dir ./total-skills
   ```
   Or copy `skills/*` into a repo's `.claude/skills/` to share it with everyone on that repo.
3. Use it for a week, then prune: delete anything the agent ignores or you never trigger.

## Adding a skill
- Folder `skills/<name>/SKILL.md` with `name` and `description` frontmatter.
- The description says **when** to use it. That's what makes the agent pick it.
- Keep it under ~80 lines. Put long checklists in a `references/` file next to it.
