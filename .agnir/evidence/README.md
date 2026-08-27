# Validation Evidence

This directory is the durable Agnir evidence location for Cloud Mail Svif Validation Project #2.

Rules:

- A verification result may be recorded as succeeded only when backed by the actual immutable candidate and workflow/check output.
- A blocked or failed provider actuation must remain blocked/failed evidence; it must not be rewritten as delivery success.
- Delivery success requires actual Cloudflare actuation of the verified candidate.
- Observation success requires actual external `/api/health` and frontend checks against the delivered target.
- Secret values are never evidence. Only protected-store references, scopes, classifications, resource identities, workflow/run identifiers, and observable results belong here.
