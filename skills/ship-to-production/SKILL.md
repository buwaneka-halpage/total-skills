---
name: ship-to-production
description: Safely release a change to a shared or production environment. Use for deployments, releases, database migrations, config or infrastructure changes, feature-flag flips, and anything that touches production data.
---

# Ship to production

Never run a production-affecting command without the user's explicit go-ahead **for that specific command**.

## Pre-flight (all must be true)

- [ ] Review passed; CI green on the exact commit being shipped
- [ ] Rollback path written down and tested where possible (previous version, flag off, down-migration)
- [ ] Migrations are backward compatible with the currently running version
- [ ] Logs, metrics and alerts exist to tell whether it's working
- [ ] Change window, approvals and change ticket meet `context/TEAM.md` → *Release process*
- [ ] Owners and on-call know it's happening

## Rollout

1. Deploy to the lowest environment first and verify.
2. Go to production gradually where possible (canary, % rollout, single site/region first).
3. After each step, check the agreed signals (error rate, latency, business metric) for the agreed soak time.
4. If any signal degrades, **roll back first, investigate second**.

## After

Post a short release note: what shipped, links, verification evidence, rollback command. If anything went wrong, run `encode-lesson`.
