# Cloud Mail Svif Validation — Next Actions

1. Keep provider actuation disabled until live validation is explicitly authorized.
2. When live validation is authorized, configure the non-secret repository variable `SVIF_ENABLE_VALIDATION_DELIVERY=true` and protected `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` in the `svif-validation` environment without moving secret values through chat or Agnir evidence.
3. Require account/token preflight success before any resource discovery/mutation, then deliver only a successfully verified immutable candidate to isolated `cloud-mail-svif-validation` Worker/D1/KV resources.
4. Require `/api/health` exact-revision + D1/KV/assets checks and `/` frontend observation before recording successful delivery/observation.
5. Do not merge the validation branch into production `main` automatically; any application change intended for `main` remains a separate project decision.

## Completed

- Migration to Agnir/Svif-native validation structure: commit `250e5173f3cb0258e865097f9f9cd632aabe95f0`.
- Initial Svif Validation run `33098133983` failed because of an overfit health-hook source-form checker; no provider actuation occurred.
- Checker fix: commit `dde68f0b2c55224ba5e36bc6d7c30671ff311b25`.
- Credential-free static verification is proven for immutable candidate `5b32462f3725327805f0dd696475a16f07b666aa` by Svif Validation run `33102032043`; verify job `98621961739` succeeded and delivery job `98622215176` was skipped.
- Evidence is recorded in `.agnir/evidence/static-verification-2026-08-28.md`.
