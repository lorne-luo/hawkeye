from django.core.management.base import BaseCommand

from apps.asx.models import Company
from apps.prediction.models import WeeklyPrediction
from apps.recommendation.strategy import ReturnRiskRank


class Command(BaseCommand):
    help = 'Load prediction by week.'

    def add_arguments(self, parser):
        parser.add_argument('week', nargs='+', type=int)

    def handle(self, *args, **options):
        if not options.get('week'):
            print('Please enter week.')

        week = options['week'][0]
        counter = ReturnRiskRank().run(week)
        print(f'{counter} stocks recommended.')
