# Svif Validation Static Verification — 2026-08-28

## Result

Credential-free static verification **succeeded** for the current validation candidate.

- Project: `urn:svif:validation:cloud-mail-cloudflare`
- Repository: `mattamior/cloud-mail`
- Ref: `svif/cloudflare-validation`
- Immutable candidate: `5b32462f3725327805f0dd696475a16f07b666aa`
- Workflow: `Svif Validation`
- Workflow run: `33102032043`
- Verify job: `98621961739` — `success`
- Delivery job: `98622215176` — `skipped`

## Verified boundary

The successful verify job established all currently required credential-free static checks for Validation Project #2:

- resolved the immutable candidate and checked out that exact SHA;
- passed Agnir and Svif validation-contract conformance;
- installed Worker dependencies from the frozen lockfile;
- installed frontend dependencies from the frozen lockfile;
- built the Vue frontend;
- rendered the non-secret isolated validation configuration;
- validated the Worker bundle, static assets, and declared bindings through Wrangler dry-run.

No Cloudflare provider credentials were required for this verification boundary.

## Delivery / observation status

Automatic provider actuation remained disabled. The `Deliver isolated validation candidate` job was skipped because live validation authority was not enabled.

Therefore this evidence proves static verification only. It does **not** claim successful Cloudflare actuation, isolated D1/KV provisioning, `/api/health` observation, frontend observation, or end-to-end delivery success.

## Prior failure disposition

Run `33098133983` remains failed evidence. Its conformance failure was caused by the overfit `checks.assets` source-form assertion and was corrected by commit `dde68f0b2c55224ba5e36bc6d7c30671ff311b25`. It is not rewritten as success.
