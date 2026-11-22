---
name: project-management
description: Plan, track and report project schedules and status as Gantt charts, synced with the team's project management tool (GitHub Projects by default; Jira, Azure Boards, Linear, Asana, Notion, MS Project via adapters). Use when the user asks for a timeline, Gantt chart, schedule, status report, "where are we?", or wants plan tasks put on a project board.
---

# Project management

The user prefers **Gantt charts**. Show schedule and status as a Gantt first, then text.

## 0. Which tool?
Read `docs/environment.md` → *Project management*. If missing, detect it (see `references/adapters.md` → Detection) and ask the user to confirm. Default: **GitHub Projects**.
Every write to a PM tool (create project/items, change dates, status, fields) is **draft-first**: show the change list, apply only after approval.

## 1. Plan → schedule
Input: `docs/<feature>/PLAN.md` from `plan-slices` (tasks with Phase, Depends, Estimate in working days, Owner).
```bash
python3 <plugin>/scripts/gantt.py --plan docs/<feature>/PLAN.md --start <YYYY-MM-DD> \
  --title "<feature>" --out docs/<feature>/gantt.html --mermaid docs/<feature>/gantt.md
```
- `gantt.html`: interactive chart (phases, dependency arrows, **critical path**, status colours, today line). Publish it as an Artifact if available, or send the file.
- `gantt.md`: Mermaid `gantt` block. GitHub renders it natively, so paste it into the PLAN, issues, PR descriptions or the project README.
Review the schedule with the user: end date, critical path, overloaded owners, tasks with no dependencies that could start earlier.

## 2. Push to the PM tool
Use the matching adapter in `references/adapters.md`. Required mapping, whatever the tool:

| Plan | PM field |
|---|---|
| Task T<n> | Issue / work item (link the GitHub issue from `issues`) |
| Phase | Milestone / Epic / single-select "Phase" |
| Start / computed start | Start date |
| Computed end | Target / due date |
| Depends | "Blocked by" link (or a note in the body if unsupported) |
| Estimate | Number field "Estimate (days)" |
| Owner | Assignee |
| Status | Status (Todo / In progress / Blocked / Done) |

Write the created item IDs/URLs back into `PLAN.md`.

## 3. Track
On "status?", "where are we?", or weekly:
1. Pull current state from the tool (GitHub: `gantt.py --github-project <owner> <number>`; others via adapter export to JSON → `gantt.py --json`).
2. Render the Gantt and compare it with the baseline (the first approved `gantt.md`, kept as `gantt-baseline.md`).
3. Report in this order: Gantt, then **slipped tasks** (actual/forecast end > baseline end) with the critical-path impact, blocked items and why, and what's next this week.
Never change dates, owners or scope in the tool to "fix" a slip. Propose re-planning to the user.

## 4. Close
For `final-report`: include baseline vs actual Gantt and the list of slips with causes.
