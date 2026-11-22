---
name: grill-the-plan
description: Interview the user to sharpen a vague request, plan or design before any code is written. Use when requirements are fuzzy, when the user says "grill me", or before an SRS for anything larger than a day's work.
---

# Grill the plan

Reach a shared understanding before building. Treat the plan as a tree of decisions: each one unlocks the decisions that depend on it.

## Rounds

1. List the decisions you can ask about **now**, the ones whose prerequisites are settled.
2. Ask them all in one round. Number them, and give your recommended answer for each:

   ```
   Q1. <decision>: <context and options>
   → Recommended: <answer>
   ```

3. Wait for answers, then ask the next round.

## Rules

- Facts are your job. Look up anything in the code, config, tickets or docs. Only ask the user about **decisions**.
- Always cover: who uses it, what "done" looks like, what must not break, data and security constraints, how it gets to production, and how it's rolled back.
- Finish when no open decisions remain. Summarise the agreed decisions and ask the user to confirm. Then hand off to `write-srs`.
