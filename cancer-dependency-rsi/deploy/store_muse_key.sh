#!/usr/bin/env bash
# Stores the Muse Code API key in AWS SSM Parameter Store (SecureString).
# The key is never echoed, written to disk, or placed in shell history.
# Usage: bash deploy/store_muse_key.sh [--from-login]
#   - paste a key when prompted, or press Enter to reuse the key from your `muse login`.
set -euo pipefail
PARAM="/itsthemedium/muse-api-key"
KEY=""
# Interactive terminal: offer to paste a key. Non-interactive (e.g. Claude Code's "!" prefix) or --from-login: use the muse login.
if [[ "${1:-}" != "--from-login" && -t 0 ]]; then
  printf 'Paste Muse API key (input hidden), or press Enter to use your muse login: '
  IFS= read -rs KEY || KEY=""; echo
fi
if [[ -z "$KEY" ]]; then
  KEY="$(python3 - <<'PY'
import json, os, re
d = json.load(open(os.path.expanduser("~/.config/muse/auth.json")))
best = None
def walk(x, path=""):
    global best
    if isinstance(x, dict):
        for k, v in x.items(): walk(v, path + "." + k.lower())
    elif isinstance(x, list):
        for v in x: walk(v, path)
    elif isinstance(x, str) and re.search(r"(api_?key|access_?token|key|token)", path) and "refresh" not in path and 20 <= len(x) <= 400:
        if best is None or "key" in path: best = x
walk(d)
print(best or "")
PY
)"
fi
[[ -n "$KEY" ]] || { echo "No key found."; exit 1; }
printf '%s' "$KEY" | aws ssm put-parameter --name "$PARAM" --type SecureString --overwrite \
  --value "file:///dev/stdin" --region us-east-1 >/dev/null
unset KEY
echo "Stored in SSM as $PARAM (SecureString). Only the itsthemedium Lambda role can read it."
