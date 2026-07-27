"""
seed_patients.py — synthetic test data for CareConnectLite+ (Team 2)

Loads fake Students/Patients (demographics) into the DB, matching the
Patient model in accounts/models.py. Intake/medical data is written to a
separate CSV (for the Intake Form work next week), NOT to the patient table.

WHERE THIS GOES:
    accounts/management/commands/seed_patients.py
    (create accounts/management/ and accounts/management/commands/, each with
     an empty __init__.py — same structure appointment/ already has)

RUN (from the repo root, next to manage.py):
    pip install Faker
    python manage.py seed_patients --count 25
    python manage.py seed_patients --count 25 --clear          # wipe + reseed
    python manage.py seed_patients --count 25 --intake-csv     # also write intake_sample.csv

All data is 100% synthetic (Faker). Non-EHR mock project — no real patient info.
"""

import csv
import random
from django.core.management.base import BaseCommand
from accounts.models import Patient          # Patient lives in accounts/models.py

try:
    from faker import Faker
except ImportError:
    raise SystemExit("Faker isn't installed. Run:  pip install Faker")

fake = Faker("en_US")

# Intake pools — for the Intake Form (next week), NOT the Patient table.
ALLERGIES   = ["None", "Penicillin", "Peanuts", "Tree nuts", "Latex",
               "Bee stings", "Shellfish", "Sulfa drugs", "Seasonal / pollen", "Dairy"]
CONDITIONS  = ["None", "Asthma", "Seasonal allergies", "Anxiety", "Depression",
               "ADHD", "Type 1 diabetes", "Migraines", "Hypertension", "Eczema"]
MEDICATIONS = ["None", "Albuterol inhaler", "Sertraline 50mg", "Adderall XR",
               "Ibuprofen as needed", "Loratadine", "Oral contraceptive",
               "Metformin", "Lisinopril", "Daily multivitamin"]
REASONS     = ["Cold / flu symptoms", "Sports injury", "Mental health check-in",
               "Flu shot / vaccination", "Prescription refill", "Annual physical",
               "Sore throat", "Sprained ankle", "Allergy consultation", "STI screening"]


class Command(BaseCommand):
    help = "Seed Students/Patients with synthetic demographics for testing."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=25,
                            help="How many patients to create (default 25).")
        parser.add_argument("--clear", action="store_true",
                            help="Delete existing patients before seeding.")
        parser.add_argument("--intake-csv", action="store_true",
                            help="Also write intake_sample.csv for the Intake Form work.")

    def handle(self, *args, **options):
        count = options["count"]

        if options["clear"]:
            Patient.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing patient records."))

        intake_rows = []
        created = 0
        for i in range(count):
            first = fake.first_name()
            last  = fake.last_name()
            email = f"{first.lower()}.{last.lower()}{i}@campus.edu"   # i keeps it unique

            # Students/Patients: demographics only (matches accounts.models.Patient)
            Patient.objects.create(
                first_name=first,
                last_name=last,
                email=email,
                phone_number=fake.numerify("(###) ###-####"),
                address=fake.address().replace("\n", ", "),
                date_of_birth=fake.date_of_birth(minimum_age=17, maximum_age=35),
            )
            created += 1

            # Intake Form data — for next week, written to CSV, not the DB
            intake_rows.append({
                "patient_email": email,          # link key until real FK exists
                "reason_for_visit": random.choice(REASONS),
                "allergies": random.choice(ALLERGIES),
                "chronic_conditions": random.choice(CONDITIONS),
                "current_medications": random.choice(MEDICATIONS),
                "emergency_contact_name": fake.name(),
                "emergency_contact_phone": fake.numerify("(###) ###-####"),
            })

        self.stdout.write(self.style.SUCCESS(f"Created {created} patients."))

        if options["intake_csv"]:
            with open("intake_sample.csv", "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(intake_rows[0].keys()))
                writer.writeheader()
                writer.writerows(intake_rows)
            self.stdout.write(self.style.SUCCESS(
                f"Wrote intake_sample.csv ({len(intake_rows)} rows)."))
