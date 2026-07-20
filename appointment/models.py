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

    date = models.DateField()
    start_time = models.TimeField()
    # duration = models.FloatField()
    is_booked = models.BooleanField(default=False)
    booked_appt_id = models.CharField()

    def __str__(self):
        return f"{self.date} — {self.start_time}"
