#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="/tmp/bjp_deploy.log"

# cPanel puts the virtualenv at ~/virtualenv/{app_root_name}/{python_version}/
# Fall back to a local venv/ for local dev environments.
_activate_venv() {
    local app_name
    app_name=$(basename "$REPO_DIR")
    local cpanel_activate
    cpanel_activate=$(find "$HOME/virtualenv/$app_name" -name "activate" -path "*/bin/activate" 2>/dev/null | head -1)

    if [ -n "$cpanel_activate" ]; then
        source "$cpanel_activate"
    elif [ -f "$REPO_DIR/venv/bin/activate" ]; then
        source "$REPO_DIR/venv/bin/activate"
    else
        echo "ERROR: No virtualenv found. Looked in $HOME/virtualenv/$app_name and $REPO_DIR/venv"
        exit 1
    fi
}

{
    echo "=== Deploy started $(date) ==="
    cd "$REPO_DIR"
    _activate_venv
    git pull origin main
    pip install -r requirements.txt --quiet
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput --clear
    mkdir -p tmp
    touch tmp/restart.txt
    echo "=== Deploy finished $(date) ==="
} >> "$LOG" 2>&1
