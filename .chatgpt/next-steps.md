# Next Steps

1. In GitHub Actions protected secrets available to the `zerolocal-validation` environment/repository, store `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. Do not move either value through chat.
2. Scope the Cloudflare API token to the intended account with only `Workers Scripts Edit`, `Workers KV Storage Edit`, and `D1 Edit` required by the validation workflow.
3. Rerun the failed jobs for workflow run `33050376135`; the successful validation job already established candidate revision `b6182583b6282e97dd3204208b0a5d242f387d2b`.
4. Confirm the deploy job discovers or creates only `cloud-mail-zerolocal-validation` KV and D1 resources, deploys the isolated Worker, and initializes its isolated D1 schema.
5. Confirm `/api/health` reports the exact candidate revision with D1, KV, and assets healthy, and `/` serves the Cloud Mail frontend.
6. Checkpoint the observed deployment URL, revision, provider resources, and workflow evidence.
7. Open a pull request to `main` only after isolated validation is observed successfully; do not merge automatically because the existing `main` workflow is production-oriented.
