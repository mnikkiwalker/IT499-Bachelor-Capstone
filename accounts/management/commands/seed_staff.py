"""
seed_staff.py — creates a known staff account for demos (Team 2, CareConnectLite+)

Gives the team one reliable, shareable staff login so anyone can demo the
staff schedule without hand-making a superuser. Idempotent — re-running just
resets the account to the known password.

RUN (from repo root, next to manage.py):
    python manage.py seed_staff
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create or reset the demo staff account."

    # hardcoded demo credentials
    USERNAME = "staff"
    PASSWORD = "demo12345"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username=self.USERNAME)

        user.is_staff = True                 # this is what unlocks the staff schedule
        user.set_password(self.PASSWORD)     # always reset to the known password
        user.save()

        label = "Created" if created else "Reset existing"
        self.stdout.write(self.style.SUCCESS(
            f"{label} staff user '{self.USERNAME}' — password: {self.PASSWORD}"
        ))