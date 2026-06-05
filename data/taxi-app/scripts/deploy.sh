#!/usr/bin/env bash
set -euo pipefail

APP_NAME="taxi-app"

echo "▶️  Starting $APP_NAME..."
databricks apps start "$APP_NAME"

echo "🔗 Linking $APP_NAME to GitHub..."
databricks apps create-update "$APP_NAME" \
  --json '{"update_mask": "git_repository", "git_repository": {"url": "https://github.com/avcaliani/scratchpad", "provider": "gitHub"}}'

echo "🚀 Deploying $APP_NAME..."
databricks apps deploy "$APP_NAME" \
  --json '{"git_source": {"branch": "databricks/first-app", "source_code_path": "data/taxi-app"}}'

echo "✅ Done!"
