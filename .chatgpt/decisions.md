# Decisions

## 2026-08-27 — ZeroLocal adoption

- `mattamior/cloud-mail` is the canonical repository and uses ZeroLocal v0.1 with the official RPM profile.
- The active RPM ref during validation is `zerolocal/cloudflare-validation`.
- Provider-specific behavior is Cloudflare Workers; ZeroLocal Core lifecycle semantics remain provider-neutral.

## 2026-08-27 — Non-destructive validation boundary

- Validation runs in a separate Worker named `cloud-mail-zerolocal-validation`.
- Validation state is isolated in a D1 database and KV namespace with the same validation-specific name.
- Validation does not configure the production custom domain, production D1/KV identifiers, R2, email routing, AI binding, or production cron triggers.
- Existing `.github/workflows/deploy-cloudflare.yml` remains unchanged and only targets `main` as before.

## 2026-08-27 — Verification and provenance

- Pull-request validation is credential-free.
- A trusted push to the dedicated validation branch may use protected Cloudflare credentials only after the validation job succeeds.
- The deployment checks out and deploys the exact immutable revision validated in the same workflow run.
- Provider resources are discovered before creation and reused by name on retries.
- Wrangler success alone is insufficient: database initialization, `/api/health`, and the frontend root must all pass external observation.
