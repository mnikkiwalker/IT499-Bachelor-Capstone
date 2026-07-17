from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta, date, time
from ...models import Timeslot

class Command(BaseCommand):

    def handle(self, **options):

        self.stdout.write("Generating timeslots...")

        population_days = 45

        #daily hour range in minutes
        start_time = 9.0
        end_time = 12.0

        timeslot_intervals = 0.5

        today = date.today()

        timeslots = []

        #for each day in the next 30 days
        for day in range(population_days):

            current_date = today + timedelta(days=day)

            current_time = start_time
            
            #for each hour within the allotted times

            while current_time < (end_time + timeslot_intervals) :

                start_h = int(current_time)
                start_m = int(((current_time % 1)*60))

                start = time(start_h, start_m)

                #add if not exists
                object, created = Timeslot.objects.get_or_create(
                    date=current_date,
                    start_time=start
                    )
                
                object.save()

                if created:
                    timeslot = {
                        "date": current_date,
                        "start_time": start
                    }

                    timeslots.append(timeslot)

                    self.stdout.write(f"Timeslot created: {timeslot.get('date')} {timeslot.get('start_time')}")

                #iterate up a half hour
                current_time += timeslot_intervals

            