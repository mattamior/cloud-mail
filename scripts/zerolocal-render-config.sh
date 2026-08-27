#!/usr/bin/env bash
set -euo pipefail

TEMPLATE="${1:-mail-worker/wrangler-zerolocal.toml}"
OUTPUT="${2:-mail-worker/wrangler-zerolocal.generated.toml}"

python3 - "$TEMPLATE" "$OUTPUT" <<'PY'
import os
import pathlib
import sys

template = pathlib.Path(sys.argv[1])
output = pathlib.Path(sys.argv[2])
required = [
    "ZEROLOCAL_WORKER_NAME",
    "ZEROLOCAL_D1_NAME",
    "ZEROLOCAL_D1_ID",
    "ZEROLOCAL_KV_ID",
    "ZEROLOCAL_JWT_SECRET",
    "ZEROLOCAL_REVISION",
]
missing = [name for name in required if not os.environ.get(name)]
if missing:
    raise SystemExit("missing required ZeroLocal config values: " + ", ".join(missing))

text = template.read_text()
for name in required:
    text = text.replace("${" + name + "}", os.environ[name])

if "${ZEROLOCAL_" in text:
    raise SystemExit("unresolved ZeroLocal placeholder remains in rendered Wrangler config")

output.write_text(text)
PY
