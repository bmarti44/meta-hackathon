#!/usr/bin/env bash
# Packages the AI Lambda with the current gene tables. No secrets are bundled.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf build && mkdir build
cp lambda/index.mjs build/
cp ../site/data/genes.json ../site/data/stats.json build/
(cd build && zip -qr ../lambda.zip .)
echo "built deploy/lambda.zip"
