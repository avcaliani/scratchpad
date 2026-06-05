#!/usr/bin/env bash
set -euo pipefail

APP_NAME="nyctaxi"

uv export --no-dev --no-hashes -o requirements.txt
databricks apps deploy "$APP_NAME"
