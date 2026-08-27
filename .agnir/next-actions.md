# Cloud Mail Svif Validation — Next Actions

1. Complete the branch migration to Svif/Agnir-native validation artifacts and remove active `.chatgpt/`, `ZEROLOCAL.yaml`, predecessor workflow/script/config names from `svif/cloudflare-validation`.
2. Run the new branch verification workflow and require Agnir/Svif conformance, frontend build, Worker dependency install, config render, and Wrangler dry-run to succeed without Cloudflare credentials.
3. Record the immutable candidate SHA and verification workflow evidence in Agnir.
4. Keep provider actuation disabled until live validation is explicitly authorized.
5. For live validation, configure the non-secret repository variable `SVIF_ENABLE_VALIDATION_DELIVERY=true` and protected `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` in the `svif-validation` environment without moving values through chat.
6. Require account/token preflight success before any resource discovery/mutation, then deliver only the verified candidate to isolated `cloud-mail-svif-validation` Worker/D1/KV resources.
7. Require `/api/health` exact-revision + D1/KV/assets checks and `/` frontend observation before recording successful delivery/observation.
8. Do not merge the validation branch into production `main` automatically; any application change intended for `main` remains a separate project decision.
