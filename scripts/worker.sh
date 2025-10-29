#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate
celery -A project_core.celery worker -l info


