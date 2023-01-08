"""
Django command to wait for the DB to be available
"""
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Entry point for command"""

        db_up = False
        self.stdout.write("Waiting for database...")

        while db_up is False:
            try:
                self.check(databases=["default"])  # type: ignore
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable waiting...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
