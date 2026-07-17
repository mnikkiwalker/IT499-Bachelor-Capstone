from django.core.management.base import BaseCommand, CommandError
from ...models import Timeslot


class Command(BaseCommand):

    def handle(self, **options):
        Timeslot.objects.all().delete()