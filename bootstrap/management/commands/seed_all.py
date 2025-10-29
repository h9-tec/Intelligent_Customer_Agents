from __future__ import annotations

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed all demo data."

    def handle(self, *args, **options):  # type: ignore[override]
        call_command("seed_brandkit")
        call_command("seed_inventory")
        call_command("seed_helpdesk")
        call_command("seed_orders")
        self.stdout.write(self.style.SUCCESS("All seeders executed."))


