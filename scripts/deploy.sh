#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="/tmp/bjp_deploy.log"

{
    echo "=== Deploy started $(date) ==="
    cd "$REPO_DIR"
    source venv/bin/activate
    git pull origin main
    pip install -r requirements.txt --quiet
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput --clear
    touch tmp/restart.txt
    echo "=== Deploy finished $(date) ==="
} >> "$LOG" 2>&1
