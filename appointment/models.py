"""
this is where mapping for database objects goes
each entity is built as a class with attributes that will
become our fields with django magic
"""

from django.db import models
import uuid

# Create your models here.
class Appointment(models.Model):

    appt_ID = models.UUIDField(default = uuid.uuid4)
    appt_date = models.DateField()
    appt_time = models.TimeField()
    time_slot_span = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    

   

class Timeslot(models.Model):

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("checked_in", "Checked In"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("no_show", "No Show"),
    ]

    date = models.DateField()
    start_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    booked_appt_id = models.CharField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    def __str__(self):
        return f"{self.date} — {self.start_time}"

class IntakeForm(models.Model):

    # ties this intake to the booked slot it belongs to — one form per appointment
    timeslot = models.OneToOneField(
        Timeslot,
        on_delete=models.CASCADE,
        related_name="intake_form",
    )

    reason_for_visit = models.CharField(max_length=200)
    symptoms = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    consent = models.BooleanField(default=False)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Intake for slot {self.timeslot_id}"