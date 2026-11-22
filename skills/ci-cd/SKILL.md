---
name: ci-cd
description: Decide whether a task needs CI/CD work, then use, extend or create pipelines accordingly. Use when a change affects build, test or deploy steps, when CI fails, or when the user asks about pipelines.
---

# CI/CD

## 1. Gate: is CI/CD in scope?
Read `docs/environment.md` → Decisions → CI/CD scope:

| Scope | What you do |
|---|---|
| `none` | No pipeline work. Verify locally only. Mention any change that *would* need CI. |
| `existing-dont-touch` | Use the existing pipeline: read results, fix code to pass. Never edit pipeline files. |
| `existing-extend` | You may edit pipelines, as reviewed PR changes. |
| `create-new` | Design a new pipeline (step 3). |
| missing | Run `discover-environment` and ask the user. Don't assume. |

Then check if *this task* touches CI: new dependency/tool, new test type, new service or environment, new secret, changed build output, or the deploy target changed. If scope forbids the needed change, tell the user.

## 2. Failing CI
`gh run list --branch <b>`, `gh run view <id> --log-failed`. Classify: our diff's failure → fix code. Flaky → one re-run (`gh run rerun <id> --failed`), then report. Infrastructure/secret problem → report to the user. Never skip, disable or weaken a check to get green.

## 3. Creating or extending a pipeline
Use the CI system in the inventory (GitHub Actions by default). Pipeline stages in order, failing fast: install (cached) → lint/format → type check → unit tests → build → integration tests → security scan (dependencies, secrets) → package → deploy (staging, then production with approval gate).
- Pin action versions (prefer commit SHAs) and use least-privilege `permissions:`.
- Use OIDC federation to the cloud (`azure/login`, `aws-actions/configure-aws-credentials`, `google-github-actions/auth`) instead of long-lived secrets.
- Production deploys need a GitHub Environment with required reviewers.
- Validate before committing: `actionlint` if available. Explain the pipeline with a Mermaid flowchart in the PR.

Deploys themselves follow `ship-to-production`.
