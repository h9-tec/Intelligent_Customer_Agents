#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=project_core.settings.dev
python manage.py runserver 0.0.0.0:8000


