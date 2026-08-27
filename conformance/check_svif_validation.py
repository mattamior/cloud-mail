#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def section_scalar(text: str, section: str, key: str) -> str | None:
    in_section = False
    for line in text.splitlines():
        if re.match(rf"^{re.escape(section)}:\s*$", line):
            in_section = True
            continue
        if in_section and line and not line.startswith((" ", "\t", "#")):
            break
        if in_section:
            match = re.match(rf"^\s{{2}}{re.escape(key)}:\s*(.+?)\s*$", line)
            if match:
                return match.group(1).strip().strip("\"'")
    return None


def require_text(text: str, needles: list[str], label: str) -> None:
    for needle in needles:
        if needle not in text:
            fail(f"{label} missing required validation contract: {needle}")


def main() -> None:
    required = [
        "AGNIR.yaml",
        "SVIF.yaml",
        ".agnir/state.md",
        ".agnir/next-actions.md",
        ".agnir/decisions.md",
        ".agnir/evidence/README.md",
        ".agnir/evidence/predecessor-validation.md",
        "adapters/cloudflare-validation.json",
        "validation/SUCCESS_CRITERIA.md",
        "history/PREDECESSOR.md",
        ".github/workflows/svif-validation.yml",
        "scripts/svif-render-config.sh",
        "mail-worker/wrangler-svif.toml",
        "mail-worker/src/index.js",
        ".github/workflows/deploy-cloudflare.yml",
    ]
    for path in required:
        if not (ROOT / path).exists():
            fail(f"missing Svif validation artifact: {path}")

    for forbidden in (
        ".chatgpt",
        "ZEROLOCAL.yaml",
        ".github/workflows/zerolocal-validation.yml",
        "scripts/zerolocal-render-config.sh",
        "mail-worker/wrangler-zerolocal.toml",
    ):
        if (ROOT / forbidden).exists():
            fail(f"predecessor protocol artifact remains active: {forbidden}")

    agnir = (ROOT / "AGNIR.yaml").read_text(encoding="utf-8")
    svif = (ROOT / "SVIF.yaml").read_text(encoding="utf-8")
    if section_scalar(agnir, "agnir", "version") != "0.1":
        fail("AGNIR.yaml does not declare Agnir 0.1")
    if section_scalar(agnir, "agnir", "discovery_profile") != "repository-filesystem/0.1":
        fail("AGNIR.yaml does not declare repository-filesystem/0.1")
    if section_scalar(svif, "svif", "version") != "0.2":
        fail("SVIF.yaml does not declare Svif 0.2")
    if section_scalar(svif, "continuity", "protocol") != "agnir" or section_scalar(svif, "continuity", "compatibility") != "0.1":
        fail("SVIF.yaml does not declare Agnir 0.1 continuity")
    require_text(
        agnir,
        [
            'canonical: "mattamior/cloud-mail"',
            'authoritative_ref: "svif/cloudflare-validation"',
            'predecessor_ref: "zerolocal/cloudflare-validation"',
        ],
        "AGNIR.yaml",
    )
    require_text(
        svif,
        [
            '"software-delivery/0.2"',
            'role: "non-founding-validation"',
            'adapter: "adapters/cloudflare-validation.json"',
            'workflow: ".github/workflows/svif-validation.yml"',
            'SVIF_ENABLE_VALIDATION_DELIVERY=true',
        ],
        "SVIF.yaml",
    )

    for key in ("state", "next_actions", "decisions", "evidence"):
        locator = section_scalar(agnir, "memory", key)
        if not locator:
            fail(f"Agnir memory locator missing: {key}")
        if "://" not in locator and not (ROOT / locator).exists():
            fail(f"Agnir memory locator does not resolve: {key} -> {locator}")

    criteria = (ROOT / "validation/SUCCESS_CRITERIA.md").read_text(encoding="utf-8")
    require_text(
        criteria,
        [
            "Cold-start recovery",
            "Credential-free VERIFY",
            "Protected DELIVER",
            "OBSERVE",
            "Static validation success",
            "End-to-end validation success",
            "must not be conflated",
        ],
        "success criteria",
    )

    adapter = json.loads((ROOT / "adapters/cloudflare-validation.json").read_text(encoding="utf-8"))
    if adapter.get("svif_adapter", {}).get("version") != "0.2":
        fail("Cloudflare validation adapter does not declare 0.2")
    metadata = adapter.get("adapter", {})
    if metadata.get("id") != "cloudflare.workers.validation":
        fail("unexpected validation adapter id")
    if set(metadata.get("kinds", [])) != {"delivery", "provider", "observation"}:
        fail("validation adapter kinds are incomplete")
    operations = {op.get("effect"): op for op in adapter.get("operations", [])}
    if not {"resolve", "actuate", "observe", "recover"} <= set(operations):
        fail("validation adapter is missing required semantic effects")
    actuate = operations["actuate"]
    if actuate.get("authority") != "protected-delivery":
        fail("validation actuation does not require protected-delivery authority")
    if "verification" not in actuate.get("input_record_kinds", []) or "delivery" not in actuate.get("output_record_kinds", []):
        fail("validation actuation does not preserve verification -> delivery evidence boundary")
    if "PROVENANCE_MISMATCH" not in actuate.get("failure_classes", []):
        fail("validation actuation does not expose provenance mismatch")
    observe = operations["observe"]
    if "delivery" not in observe.get("input_record_kinds", []) or "observation" not in observe.get("output_record_kinds", []):
        fail("validation observation does not preserve delivery -> observation evidence boundary")

    allowed_credential_keys = {"reference", "purpose", "minimum_scope", "value_transport"}
    for credential in adapter.get("credentials", []):
        if not set(credential) <= allowed_credential_keys:
            fail("validation adapter credential contains secret/unknown fields")
        if credential.get("value_transport") != "protected-store-only":
            fail("validation credential is not protected-store-only")
        if not str(credential.get("reference", "")).startswith("protected-store://"):
            fail("validation credential is not an opaque protected-store reference")

    workflow = (ROOT / ".github/workflows/svif-validation.yml").read_text(encoding="utf-8")
    if "\n  deploy-validation:" not in workflow:
        fail("validation workflow has no separate protected delivery job")
    verify_section, deliver_section = workflow.split("\n  deploy-validation:", 1)
    if "CLOUDFLARE_API_TOKEN" in verify_section or "CLOUDFLARE_ACCOUNT_ID" in verify_section:
        fail("credential-free verification section references protected Cloudflare credentials")
    require_text(
        verify_section,
        [
            "svif/cloudflare-validation",
            "Revision must be a full 40-character commit SHA",
            "ref: ${{ steps.candidate.outputs.sha }}",
            "python conformance/check_svif_validation.py",
            "pnpm install --frozen-lockfile",
            "pnpm run build",
            "./scripts/svif-render-config.sh",
            "wrangler-svif.generated.toml",
            "deploy --dry-run",
        ],
        "verification workflow",
    )
    require_text(
        deliver_section,
        [
            "vars.SVIF_ENABLE_VALIDATION_DELIVERY == 'true'",
            "environment: svif-validation",
            "secrets.CLOUDFLARE_API_TOKEN",
            "secrets.CLOUDFLARE_ACCOUNT_ID",
            "ref: ${{ needs.validate.outputs.sha }}",
            "CLOUDFLARE_ACCOUNT_ID must be exactly 32 hexadecimal characters",
            "SVIF_KV_NAME",
            "SVIF_D1_NAME",
            "cloudflare/wrangler-action@v4",
            "wrangler-svif.generated.toml",
            "/api/health",
            ".revision == $revision",
            ".checks.d1 == true",
            ".checks.kv == true",
            ".checks.assets == true",
            "grep -q 'id=\"app\"'",
        ],
        "protected delivery workflow",
    )

    script = (ROOT / "scripts/svif-render-config.sh").read_text(encoding="utf-8")
    require_text(
        script,
        [
            "wrangler-svif.toml",
            "wrangler-svif.generated.toml",
            '"SVIF_WORKER_NAME"',
            '"SVIF_D1_NAME"',
            '"SVIF_D1_ID"',
            '"SVIF_KV_ID"',
            '"SVIF_JWT_SECRET"',
            '"SVIF_REVISION"',
        ],
        "Svif config renderer",
    )

    wrangler = (ROOT / "mail-worker/wrangler-svif.toml").read_text(encoding="utf-8")
    require_text(
        wrangler,
        [
            '${SVIF_WORKER_NAME}',
            '${SVIF_D1_NAME}',
            '${SVIF_D1_ID}',
            '${SVIF_KV_ID}',
            '${SVIF_JWT_SECRET}',
            'zerolocal_revision = "${SVIF_REVISION}"',
        ],
        "Svif validation Wrangler template",
    )

    worker = (ROOT / "mail-worker/src/index.js").read_text(encoding="utf-8")
    require_text(worker, ["/api/health", "env.zerolocal_revision", "checks.d1", "checks.kv", "assets: Boolean(env.assets)"], "Cloud Mail health hook")

    state = (ROOT / ".agnir/state.md").read_text(encoding="utf-8")
    require_text(
        state,
        [
            "non-founding validation case",
            "svif/cloudflare-validation",
            "Provider/action success alone is not sufficient",
            "33050376135",
            "98449843043",
        ],
        "Agnir state",
    )

    print("PASS: Cloud Mail non-founding Svif 0.2 + Agnir 0.1 static validation contract")


if __name__ == "__main__":
    main()
