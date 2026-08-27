# Cloud Mail Svif Validation — Current State

This branch is a non-founding validation case for Svif Core `0.2`, Software Delivery Profile `0.2`, and Agnir Core `0.1` using the existing Cloud Mail application.

## Project entry point

- Repository: `mattamior/cloud-mail`
- Authoritative validation ref: `svif/cloudflare-validation`
- Predecessor validation ref: `zerolocal/cloudflare-validation`
- Agnir discovery: top-level `AGNIR.yaml`
- Svif self-description: top-level `SVIF.yaml`
- Provider adapter: `adapters/cloudflare-validation.json`

The production-oriented `main` branch and its existing production deployment workflow remain outside this validation mutation boundary.

## Validation intent

The validation must demonstrate that a fresh Executor can enter this branch from repository state alone, recover durable project context through Agnir, verify an immutable Cloud Mail candidate without production credentials, and optionally deliver/observe that exact candidate in an isolated Cloudflare environment only when protected authority is explicitly enabled.

## Static verification criteria

A successful verification phase requires all of the following:

- Agnir cold start resolves `AGNIR.yaml` and its state/next-actions/decisions/evidence locators.
- Svif `0.2` + `software-delivery/0.2` are declared without relying on predecessor `.chatgpt/` or `ZEROLOCAL.yaml` artifacts.
- Worker and frontend dependencies install from frozen lockfiles.
- The Vue frontend builds into the Worker asset directory.
- A non-secret isolated Wrangler configuration renders with placeholder D1/KV identities and a disposable build-only app secret.
- Wrangler dry-run validates the Worker bundle, static assets, D1/KV bindings, and validation configuration.
- Verification receives no Cloudflare production credential values.
- The immutable Git SHA used for verification is explicit and becomes the only automatic-delivery candidate.

## Protected delivery criteria

Automatic validation delivery is disabled unless the non-secret repository variable `SVIF_ENABLE_VALIDATION_DELIVERY=true` is present.

When live validation is explicitly enabled, delivery must additionally prove:

- the protected Cloudflare token/account pairing is valid before resource discovery or mutation;
- only validation-specific resources named `cloud-mail-svif-validation` are discovered, created, or reused;
- the exact SHA emitted by verification is checked out for delivery;
- D1/KV provisioning is discover-before-create and retry-safe by stable validation-specific name;
- the isolated Worker is deployed without production custom domains, production D1/KV identifiers, R2, email routing, AI binding, or production cron triggers;
- the isolated D1 schema is initialized after deployment;
- `/api/health` externally reports the exact delivered revision and healthy D1, KV, and assets bindings;
- `/` externally serves the Cloud Mail frontend app shell.

Provider/action success alone is not sufficient; the external observations above are required before delivery is considered successfully observed.

## Predecessor evidence

The predecessor ZeroLocal validation branch established useful implementation evidence but did not complete provider delivery:

- workflow run `33050376135` verified immutable candidate `b6182583b6282e97dd3204208b0a5d242f387d2b` successfully;
- credential-free frontend build and Wrangler dry-run passed;
- the first protected attempt lacked credentials;
- retry deploy job `98449843043` then received protected values but Cloudflare rejected the configured account identity with API code `7003` before KV/D1 discovery or any provider mutation;
- no predecessor live deployment or endpoint observation succeeded.

This predecessor result is migration evidence only. Svif validation must establish its own current verification/delivery/observation evidence.

## Current implementation status

- `svif/cloudflare-validation` was created from predecessor ref `zerolocal/cloudflare-validation`.
- Migration commit `250e5173f3cb0258e865097f9f9cd632aabe95f0` replaced active `.chatgpt/`, `ZEROLOCAL.yaml`, predecessor workflow/script/config names with Agnir/Svif-native validation artifacts while leaving production `main` untouched.
- Svif Validation workflow run `33098133983` executed against candidate `250e5173f3cb0258e865097f9f9cd632aabe95f0` and failed during the conformance step before dependency install/build/dry-run.
- The failure was a checker defect, not an application defect: `conformance/check_svif_validation.py` required the literal source form `checks.assets`, while the existing health hook validly expresses the same contract as `assets: Boolean(env.assets)`.
- Protected delivery in run `33098133983` was skipped, so no Cloudflare actuation or observation occurred.
- Checker fix commit `dde68f0b2c55224ba5e36bc6d7c30671ff311b25` relaxes that implementation-form assumption while preserving the semantic health-hook requirement.
- The checker fix is committed but has not yet produced a recorded successful Svif Validation run at this checkpoint. Static validation therefore remains **not yet proven**.
- Provider actuation remains disabled by default; no live Svif delivery or observation has been claimed.

## Checkpoint

- Timestamp: `2026-08-28T02:06:00+08:00`
- Reason: explicit user checkpoint after Validation Project #2 migration and first checker-failure diagnosis.
- Resumability: resume from `svif/cloudflare-validation` at or after checker fix commit `dde68f0b2c55224ba5e36bc6d7c30671ff311b25`; first establish a successful credential-free static verification run, record its immutable candidate/run evidence, and keep provider actuation disabled unless separately authorized.
