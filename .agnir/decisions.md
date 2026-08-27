# Cloud Mail Svif Validation — Decisions

## 2026-08-28 — Non-founding validation boundary

- `mattamior/cloud-mail@svif/cloudflare-validation` is the authoritative entry point for Svif Validation Project #2.
- The validation branch is derived from `zerolocal/cloudflare-validation`, which remains predecessor evidence rather than being relabeled.
- Production `main` and `.github/workflows/deploy-cloudflare.yml` remain unchanged by this validation migration.
- The validation Project uses Agnir `0.1` cold-start continuity and Svif Core `0.2` + Software Delivery `0.2`.

## 2026-08-28 — Execution-surface-neutral continuity

- Top-level `AGNIR.yaml` is the repository/filesystem cold-start discovery anchor for this validation Project.
- Active `.chatgpt/` memory/bootstrap artifacts are removed from the Svif validation branch.
- Chat, GitHub Actions, and the predecessor validation conversation are not authoritative durable memory sources.

## 2026-08-28 — Isolated Cloudflare delivery

- New Svif validation resources use the stable name `cloud-mail-svif-validation` for Worker, D1, and KV.
- The GitHub Actions protected environment is `svif-validation` rather than the predecessor `zerolocal-validation` environment, so predecessor authority/configuration is not silently inherited.
- Existing production custom domains, production database/KV identifiers, R2, email routing, AI binding, and production cron triggers remain outside the validation deployment.
- Provider resources are discovered before creation and reused by stable validation-specific name on retries.

## 2026-08-28 — Verification, authority, provenance, and observation

- Credential-free verification resolves and checks out one full immutable Git SHA, builds the frontend, renders only non-secret validation configuration, and performs Wrangler dry-run validation.
- Verification authority does not imply protected delivery authority.
- Automatic provider actuation additionally requires `SVIF_ENABLE_VALIDATION_DELIVERY=true`.
- Protected Cloudflare credentials remain exclusively in the `svif-validation` protected environment; secret values must not be copied into chat, Project files, descriptors, or evidence.
- The protected delivery job checks out the exact SHA emitted by the successful verification job.
- Manual `workflow_dispatch` is an explicit delivery/recovery request but still reuses the verification job and therefore must validate the requested full SHA before actuation.
- Successful provider deployment is insufficient: `/api/health` must prove exact revision + D1/KV/assets health and `/` must prove frontend reachability.

## 2026-08-28 — Predecessor failure interpretation

- Predecessor workflow run `33050376135` successfully verified candidate `b6182583b6282e97dd3204208b0a5d242f387d2b`.
- Retry deploy job `98449843043` failed with Cloudflare API code `7003` at account-scoped KV discovery before resource mutation; the stored predecessor account identity was invalid for the intended request.
- No predecessor provider deployment or observation succeeded.
- The Svif validation environment intentionally starts with a fresh authority/configuration boundary instead of automatically retrying the predecessor protected configuration.
