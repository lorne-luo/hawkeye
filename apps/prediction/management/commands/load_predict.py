from django.core.management.base import BaseCommand

from apps.asx.models import Company
from apps.prediction.models import WeeklyPrediction


class Command(BaseCommand):
    help = 'Load prediction by week.'

    def add_arguments(self, parser):
        parser.add_argument('week', nargs='+', type=int)

    def handle(self, *args, **options):
        if not options.get('week'):
            print('Please enter week.')

        week = options['week'][0]
        WeeklyPrediction.process_csv(week)
