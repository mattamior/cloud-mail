# Checkpoint — 2026-08-28 02:06 +08:00

## Scope

Validation Project #2 migration on `mattamior/cloud-mail`, authoritative ref `svif/cloudflare-validation`.

## Durable facts

- Predecessor ref: `zerolocal/cloudflare-validation`.
- Migration commit: `250e5173f3cb0258e865097f9f9cd632aabe95f0`.
- First Svif Validation workflow run: `33098133983`.
- Run `33098133983` failed in `Verify Svif and Agnir validation contracts` before dependency install, frontend build, Wrangler dry-run, provider actuation, or observation.
- Failure cause: conformance checker overfit the Cloud Mail health-hook implementation by requiring literal `checks.assets`; the existing source expresses the assets check as `assets: Boolean(env.assets)`.
- Protected delivery job for that run was skipped; no Cloudflare resource mutation or endpoint observation occurred.
- Checker fix commit: `dde68f0b2c55224ba5e36bc6d7c30671ff311b25`.
- At checkpoint time, no successful Svif Validation workflow result for the checker fix has been recorded yet.
- `SVIF_ENABLE_VALIDATION_DELIVERY` remains the explicit non-secret authority gate for live provider actuation; provider actuation is disabled by default.

## Status classification

- Cold-start/control-plane migration: implemented.
- Static validation: not yet proven after checker fix.
- Delivery validation: not attempted under Svif after successful static validation.
- Observation validation: not attempted under Svif.
- End-to-end validation: not proven.

## Resume point

Resume by checking/running Svif Validation for the current `svif/cloudflare-validation` head, then persist successful immutable-candidate verification evidence if and only if the credential-free verification job actually succeeds. Do not enable Cloudflare delivery merely to complete the checkpoint.
