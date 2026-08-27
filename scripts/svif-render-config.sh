#!/usr/bin/env bash
set -euo pipefail

TEMPLATE="${1:-mail-worker/wrangler-svif.toml}"
OUTPUT="${2:-mail-worker/wrangler-svif.generated.toml}"

python3 - "$TEMPLATE" "$OUTPUT" <<'PY'
import os
import pathlib
import sys

template = pathlib.Path(sys.argv[1])
output = pathlib.Path(sys.argv[2])
required = [
    "SVIF_WORKER_NAME",
    "SVIF_D1_NAME",
    "SVIF_D1_ID",
    "SVIF_KV_ID",
    "SVIF_JWT_SECRET",
    "SVIF_REVISION",
]
missing = [name for name in required if not os.environ.get(name)]
if missing:
    raise SystemExit("missing required Svif validation config values: " + ", ".join(missing))

text = template.read_text()
for name in required:
    text = text.replace("${" + name + "}", os.environ[name])

if "${SVIF_" in text:
    raise SystemExit("unresolved Svif placeholder remains in rendered Wrangler config")

output.write_text(text)
PY
