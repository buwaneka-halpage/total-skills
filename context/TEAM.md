# Team context

Skills read this file. Fill in every TODO. Keep it short and factual. Agents follow it literally.

## Stack
- Languages / frameworks: TODO
- Repos and what lives where: TODO
- Key internal libraries / services: TODO

## Environments
- dev / test / staging / prod and how to reach each: TODO
- What an agent may run where (e.g. never write to prod DB): TODO

## Verify commands (run before every commit)
```bash
# TODO e.g.
# make lint
# make test
# make build
```

## Source control & collaboration
- Host: GitHub (issues, PRs, Actions). CLI: `gh`.
- Posting policy: **draft-first**. Agent writes issues/PRs/comments to `drafts/`, user approves, then agent posts.
- Branching strategy: per project in `docs/git-strategy.md` (see `choose-git-strategy`).
- Author may resolve PR threads: TODO yes/no
- Project management tool: GitHub Projects (default). Other tools used in some projects: TODO (Jira / Azure Boards / MS Project …)

## Conventions
- Branch naming: `<type>/<issue#>-<slug>` unless the project's git-strategy says otherwise
- Commit message format: `type(scope): subject` + `Refs #<issue>`
- Where specs/plans live: docs/specs/ (TODO confirm)

## Review checklist (team-specific)
- TODO e.g. every new endpoint has authz checks
- TODO e.g. no PII in logs

## Release process
- Change approval / ticket required: TODO
- Deploy windows / freezes: TODO
- Rollout method (canary, flags, sites): TODO
- Signals to watch and soak time: TODO
- Who to notify: TODO

## Hard rules
- Never commit secrets or credentials.
- Approved cloud/agent plugins (and whether telemetry is allowed): TODO
- TODO: data classification, export control, safety or compliance constraints that apply.
