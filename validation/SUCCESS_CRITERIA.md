# Svif Validation Project #2 — Success Criteria

Cloud Mail is a non-founding validation case. Success is evaluated against the current Svif/Agnir contracts, not against the predecessor conversation or ZeroLocal artifacts.

## 1. Cold-start recovery

PASS requires a fresh Executor starting from `mattamior/cloud-mail@svif/cloudflare-validation` to:

- find top-level `AGNIR.yaml` without an execution-surface-specific bootstrap file;
- resolve Current State, Next Actions, Decisions, and Evidence from the manifest locators;
- identify Svif `0.2`, Software Delivery `0.2`, and Agnir `0.1` from repository state;
- understand the validation/predecessor/production boundaries without predecessor-private context.

## 2. PLAN / trust-boundary establishment

Before mutation or provider actuation, the validation state must establish:

- immutable candidate identity;
- verification scope;
- isolated Cloudflare target/resource names;
- protected credential references and minimum scopes;
- automatic-delivery enablement policy;
- required external observations;
- repair behavior for credential/account/resource failures.

## 3. Credential-free VERIFY

PASS requires the workflow to verify one full immutable Git SHA while receiving no Cloudflare provider credentials, including:

- frozen Worker dependency install;
- frozen frontend dependency install;
- frontend build;
- Svif/Agnir validation conformance;
- rendering an isolated non-secret Wrangler config using placeholder resource IDs and disposable build-only application secret;
- Wrangler dry-run bundle/binding validation.

The verified SHA must be emitted as the candidate consumed by protected delivery.

## 4. Protected DELIVER

This stage is applicable only when explicitly authorized.

Automatic delivery requires `SVIF_ENABLE_VALIDATION_DELIVERY=true`. When enabled, PASS requires:

- protected credentials sourced only from the `svif-validation` environment;
- account/token pairing preflight before resource mutation;
- exact checkout of the SHA emitted by VERIFY;
- discovery-before-create for validation-specific KV/D1 resources;
- no mutation of production custom domains, production D1/KV identifiers, R2, email routing, AI binding, or production cron triggers;
- deployment only to the isolated `cloud-mail-svif-validation` Worker/resources.

A missing/invalid credential or account identity is a blocked/failed delivery outcome, not a verification failure and not delivery success.

## 5. OBSERVE

After successful delivery, PASS requires independent external observation:

- `/api/health` returns the exact delivered revision;
- D1, KV, and assets checks are all healthy;
- `/` serves the Cloud Mail frontend app shell.

Provider action success alone is insufficient.

## 6. Evidence and checkpointability

The validation must preserve durable evidence for:

- candidate identity;
- verification result/run;
- delivery result or blocked/failure classification;
- target/resource identities when actuation occurs;
- observation result when delivery succeeds;
- repair/next action;
- no secret values.

A fresh Executor must be able to resume from `AGNIR.yaml` without replaying the founding or predecessor chat.

## Overall validation result

- **Static validation success**: Sections 1–3 and 6 pass while delivery authority is disabled.
- **Delivery validation success**: Section 4 passes with protected authority.
- **End-to-end validation success**: Sections 1–6 pass, including successful external observation.

These states must not be conflated.
