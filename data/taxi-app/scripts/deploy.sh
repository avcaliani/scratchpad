#!/usr/bin/env bash
set -euo pipefail

APP_NAME="nyctaxi"

databricks apps deploy "$APP_NAME"
