#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
  .venv/bin/python -m pip install -r requirements.txt
fi
.venv/bin/python scripts/init_local.py
.venv/bin/python manage.py migrate --noinput
exec .venv/bin/python manage.py runserver "127.0.0.1:${PORT:-8001}"
