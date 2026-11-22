# Branching strategies

## Trunk-based
Everyone integrates into `main` at least daily, using very short branches (hours) or direct commits behind feature flags. Releases are cut from main (tags).
- Good: least merge pain, fastest feedback, ideal for CI/CD and parallel agents.
- Needs: strong automated tests, feature flags, fast CI.

## GitHub Flow
`main` is always deployable. Branch per change (`feat/…`, `fix/…`), PR, review, CI, merge (usually squash), deploy.
- Good: simple, review on every change. The default for most web/services teams.
- Needs: deploy pipeline from main; branches kept short (< few days).

## Release branches (trunk + release/x.y)
Work lands on main as in GitHub Flow. At release time, cut `release/x.y`; only fixes go there (cherry-picked from main). Tag `vX.Y.Z` on the release branch.
- Good: stabilisation period and patching old versions without freezing main.
- Needs: backport discipline (fix on main first, then cherry-pick).

## GitFlow
`main` (released) + `develop` (integration) + `feature/*`, `release/*`, `hotfix/*`.
- Good: explicit, scheduled, versioned releases with formal QA gates.
- Costs: heavy merging, slow integration, poor fit for continuous deployment. Choose only when release governance requires it.

## Common rules (all strategies)
- Protect the default branch: PR required, CI required, no force-push.
- Branch names: `<type>/<issue#>-<slug>` e.g. `feat/123-export-csv`.
- Conventional commits: `type(scope): subject`.
- Delete branches after merge.
