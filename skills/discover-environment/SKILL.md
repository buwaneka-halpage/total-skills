---
name: discover-environment
description: Build or refresh the project's environment inventory (stack, dependencies, infrastructure, cloud provider, CI/CD, source control, environments) in docs/environment.md. Use before development starts on any project, when the user asks what the project uses ("which database / cloud / CI do we use?"), or when infrastructure files change.
---

# Discover the environment

Produce `docs/environment.md`: the single place the agent and the user look up "what does this project use?". Every other skill reads it first.

## Modes

- **Query:** the user asks a question → answer from `docs/environment.md` and cite the line. If it's not there, say so and offer to discover it. Don't guess.
- **Discover:** no file yet → run all steps below.
- **Refresh:** the file exists → re-check only sections whose evidence files changed (`git log --since=<file's date> --name-only`).

## Steps (read-only; never install, deploy or log in)

1. **Stack & dependencies:** detect from manifests. `package.json`/lockfiles, `pyproject.toml`/`requirements*.txt`, `pom.xml`/`build.gradle`, `*.csproj`/`*.sln`, `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`. Record language versions, frameworks, package manager, test framework, and major libraries.
2. **Infrastructure:** IaC and runtime files. Detect them with the signal table in `references/signals.md`.
3. **Cloud provider:** decide from the signals table. Evidence beats guesses: list every file that supports the conclusion. Several providers is a valid answer.
4. **CI/CD:** which system, which workflows, what they run (build, test, lint, deploy), which branches and environments they deploy to, and required checks.
5. **Source control & tracking:** remote host (`git remote -v`), default branch, issue/PR templates, CODEOWNERS, labels in use (`gh label list` if available).
6. **Environments & secrets handling:** dev/test/staging/prod names and URLs from config and pipelines. Record *where* secrets come from (Key Vault, Secrets Manager, GitHub secrets), never their values.
7. **Ask the user** only for what files can't tell you: who owns production, change approval, whether CI/CD is in scope for this work.

## Output: `docs/environment.md`

Use `references/template.md`. Rules:
- Every fact carries its evidence: `Azure (infra/main.bicep, azure-pipelines.yml)`.
- Anything inferred but unconfirmed is marked **(unverified)**.
- Show a summary to the user and ask them to confirm the **Decisions** section (CI/CD scope, cloud plugin, branching strategy).

## After discovery

- **Cloud plugins:** recommend the official plugin for each detected provider, from `references/cloud-plugins.md`. Install only after the user approves.
- **No branching strategy recorded** → run `choose-git-strategy`.
- **Existing codebase** → run `map-codebase` and offer `visualize-codebase`.
