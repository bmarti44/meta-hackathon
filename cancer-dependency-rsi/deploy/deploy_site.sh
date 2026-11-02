#!/usr/bin/env bash
# Deploys the static site to S3 + CloudFront, and the AI Lambda code.
# Refuses to deploy if anything that looks like an API key is in the site bundle.
set -euo pipefail
cd "$(dirname "$0")/.."
BUCKET=itsthemedium-site-087630439073
DIST=E25F95NV3DTSL4
# 1. secret scan: no bearer tokens / key-looking strings / muse auth file contents in what we ship
if grep -rIlE "(Bearer [A-Za-z0-9._-]{20,}|sk-[A-Za-z0-9]{20,}|META_API_KEY|muse-api-key|api\.meta\.ai)" site deploy/lambda >/dev/null 2>&1; then
  hits=$(grep -rIlE "(Bearer [A-Za-z0-9._-]{20,}|sk-[A-Za-z0-9]{20,}|META_API_KEY)" site deploy/lambda || true)
  if [[ -n "$hits" ]]; then echo "Refusing to deploy, possible secret in: $hits"; exit 1; fi
fi
if grep -rIl "api.meta.ai\|muse-api-key" site >/dev/null 2>&1; then echo "Refusing: site bundle references the upstream API or key name"; exit 1; fi
# 2. lambda code
./deploy/build_lambda.sh
aws lambda update-function-code --function-name itsthemedium-muse --zip-file fileb://deploy/lambda.zip --query LastUpdateStatus --output text
aws lambda wait function-updated --function-name itsthemedium-muse
# 3. static site
aws s3 sync site "s3://$BUCKET" --delete --exclude "apex_redirect.js" --exclude ".DS_Store" \
  --exclude "index.html" --cache-control "public, max-age=3600"
aws s3 cp site/index.html "s3://$BUCKET/index.html" --content-type "text/html; charset=utf-8" --cache-control "public, max-age=60"
aws cloudfront create-invalidation --distribution-id "$DIST" --paths "/index.html" "/" "/assets/*" "/data/*" --query Invalidation.Id --output text
echo "deployed"
