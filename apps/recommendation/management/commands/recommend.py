from datetime import datetime

from dateutil.relativedelta import relativedelta, FR
from django.core.management.base import BaseCommand

from apps.recommendation.strategy import ReturnRiskRank


class Command(BaseCommand):
    help = 'Load prediction by week.'

    def add_arguments(self, parser):
        parser.add_argument('week', nargs='?', type=int)

    def get_last_friday(self):
        dt = datetime.now() + relativedelta(weekday=FR(-1))
        return dt.strftime('%Y%m%d')

    def handle(self, *args, **options):
        if options.get('week'):
            week = options['week'][0]
        else:
            week = self.get_last_friday()

        counter = ReturnRiskRank().run(week)
        print(f'{counter} stocks recommended.')
