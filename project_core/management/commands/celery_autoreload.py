from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run Celery worker with autoreload in development."

    def handle(self, *args, **options):  # type: ignore[override]
        self.stdout.write("Starting Celery worker with --autoreload")
        cmd = [sys.executable, "-m", "celery", "-A", "project_core.celery", "worker", "-l", "info", "--autoreload"]
        subprocess.call(cmd)


