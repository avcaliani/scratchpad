#!/usr/bin/env bash
set -euo pipefail

APP_NAME="taxi-app"

echo "▶️  Starting $APP_NAME..."
databricks apps start "$APP_NAME"

# Pre-Configuration:
#   In Databricks UI, I've already configured the Git Repository
echo "🚀 Deploying $APP_NAME..."
databricks apps deploy "$APP_NAME" \
  --json '{"git_source": {"branch": "main", "source_code_path": "data/taxi-app"}}'

echo "✅ Done!"
