---
name: review
description: Review a diff or pull request before merge. Use when asked to review code, before opening a PR, or before marking a task done.
---

# Review

Read the SRS, SAD and PLAN first if they exist. Review against what was intended, not just what was written.

## Check each axis

1. **Requirements:** does each FR in scope have code and a test? Are the REG ("must not change") items still covered?
2. **Design:** does it follow the SAD and existing codebase patterns? Is any deviation explained?
3. **Correctness:** edge cases, error paths, concurrency, time zones, units, nulls in old data.
4. **Tests:** would they fail if the code were wrong? Were characterization tests added before legacy code was changed?
5. **Security & data:** input validation, authz, secrets, injection, sensitive data in logs.
6. **Operability:** logs, metrics, failure modes, timeouts and retries, rollback-safe migrations.
7. **Simplicity:** dead code, needless abstraction, unclear names, refactor mixed with behaviour change.

Also apply every item in `context/TEAM.md` → *Review checklist*.

## Output

One line per finding, most severe first:

```
[blocker|major|minor|nit] path/to/file:line: what's wrong → suggested fix
```

Only flag what you can justify from the code. Then give the verdict: approve / approve with changes / changes required.
