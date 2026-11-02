#!/usr/bin/env bash
# Packages the AI Lambda with the current gene tables and its one runtime dependency (Meta's SAM output parser).
# No secrets are bundled. The AWS SDK comes from the Lambda runtime.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf build && mkdir build
cp lambda/index.mjs lambda/package.json build/
cp ../site/data/genes.json ../site/data/stats.json build/
(cd build && npm install --omit=dev --ignore-scripts --no-audit --no-fund --silent)
(cd build && zip -qr ../lambda.zip .)
echo "built deploy/lambda.zip"
