# Cloud Mail Svif Validation — Next Actions

1. Verify the current `svif/cloudflare-validation` head after checker fix commit `dde68f0b2c55224ba5e36bc6d7c30671ff311b25`; require Agnir/Svif conformance, frozen dependency installs, frontend build, non-secret config render, and Wrangler dry-run to succeed without Cloudflare credentials.
2. Record the immutable candidate SHA and successful verification workflow/run evidence in `.agnir/evidence/`; do not treat the failed run `33098133983` as verification success.
3. Confirm the protected delivery job remains skipped while `SVIF_ENABLE_VALIDATION_DELIVERY` is not explicitly set to `true`.
4. Keep provider actuation disabled until live validation is explicitly authorized.
5. For live validation, configure the non-secret repository variable `SVIF_ENABLE_VALIDATION_DELIVERY=true` and protected `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` in the `svif-validation` environment without moving values through chat.
6. Require account/token preflight success before any resource discovery/mutation, then deliver only the verified candidate to isolated `cloud-mail-svif-validation` Worker/D1/KV resources.
7. Require `/api/health` exact-revision + D1/KV/assets checks and `/` frontend observation before recording successful delivery/observation.
8. Do not merge the validation branch into production `main` automatically; any application change intended for `main` remains a separate project decision.
