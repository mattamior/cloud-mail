# Predecessor validation evidence

Source ref: `zerolocal/cloudflare-validation`

This evidence is retained to preserve the factual outcome of the predecessor validation without making it authoritative for the Svif validation state.

- Predecessor protocol: ZeroLocal v0.1.
- Verification workflow run: `33050376135`.
- Verified immutable candidate: `b6182583b6282e97dd3204208b0a5d242f387d2b`.
- Credential-free verification result: succeeded (Worker/frontend dependency install, frontend build, isolated config render, Wrangler dry-run).
- Initial protected actuation attempt: blocked because Cloudflare protected credentials were unavailable.
- Retry deploy job: `98449843043`.
- Retry result: failed before validation resource discovery/mutation because the Cloudflare account identity was rejected with API code `7003`.
- Provider mutation status through those attempts: none.
- External deployment observation: none.

The predecessor branch remains the source for the original detailed state, decisions, workflow, and logs. The Svif validation branch does not copy secret values and does not claim that the predecessor provider delivery succeeded.
