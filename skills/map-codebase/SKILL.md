---
name: map-codebase
description: Read-only discovery of an existing or legacy codebase before changing it. Use on first contact with a repo, before the first SRS or architecture document for an existing system, or when the area you're about to change is unfamiliar.
---

# Map the codebase

Don't change anything in this skill. Your job is to understand the system and write it down.

## Find out

1. **Build & run:** how to build, run locally, and run the tests. Actually run them and record what passes, what fails and how long it takes.
2. **Structure:** entry points, main modules and what each owns, external systems (DBs, queues, APIs, file drops, PLC/historian/OT interfaces if any).
3. **Test coverage:** which areas have tests and which have none. Note tests that are skipped, flaky or slow.
4. **Hotspots:** files that change most often and where bugs cluster:
   ```bash
   git log --since=1.year --name-only --pretty=format: | sort | uniq -c | sort -rn | head -30
   ```
5. **Conventions:** naming, error handling, logging, config, dependency injection. New code must match these, even if you'd do it differently.
6. **Hazards:** dead code that looks live, global state, hidden side effects (cron jobs, triggers, stored procedures), magic config, code nobody understands.

## Write

Save `docs/codebase-map.md` with those six headings, kept short and factual. Mark anything you inferred but couldn't confirm as **(unverified)**.
Propose updates to `context/TEAM.md` (verify commands, environments) for the user to approve.

Refresh only the relevant section when you return to an area later. Don't redo the whole map.
