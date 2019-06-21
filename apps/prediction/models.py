from __future__ import absolute_import, unicode_literals

import csv
import os
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.manager import Manager
from django.utils.functional import cached_property

from apps.asx.models import Company
from core.django.models import WeeklyModel


class WeeklyPredictionManager(Manager):
    def week(self, week):
        return super().get_queryset().filter(week=week)


class WeeklyPrediction(WeeklyModel):
    """
    ['code', 'last_date', 'start price', 'sim_mean', 'sim_diff', 'VaR 99%', 'VaR 99% Percent','volume_mean',
    'return_mean', 'return_sigma', 'percent99', 'percent90', 'percent80', 'percent70', 'percent60'])
    """
    code = models.CharField('code', max_length=80, blank=False, null=False)
    last_price_date = models.DateField('last price date', blank=True, null=True)
    current_price = models.DecimalField('current price', max_digits=10, decimal_places=4, blank=True, null=True)
    sim_mean = models.DecimalField('sim mean', max_digits=10, decimal_places=4, blank=True, null=True)
    sim_diff = models.DecimalField('sim return', max_digits=10, decimal_places=4, blank=True, null=True)
    var_99 = models.DecimalField('var 99%', max_digits=10, decimal_places=4, blank=True, null=True)
    var_99_percent = models.DecimalField('var 99% perent', max_digits=10, decimal_places=4, blank=True, null=True)
    volume_mean = models.DecimalField('volume mean', max_digits=12, decimal_places=4, blank=True, null=True)
    return_mean = models.DecimalField('return mean', max_digits=12, decimal_places=9, blank=True, null=True)
    return_sigma = models.DecimalField('return sigma', max_digits=12, decimal_places=9, blank=True, null=True)
    confidence_99 = models.DecimalField('confidence 99%', max_digits=10, decimal_places=4, blank=True, null=True)
    confidence_90 = models.DecimalField('confidence 90%', max_digits=10, decimal_places=4, blank=True,
                                        null=True)
    confidence_80 = models.DecimalField('confidence 80%', max_digits=10, decimal_places=4, blank=True, null=True)
    confidence_70 = models.DecimalField('confidence 70%', max_digits=10, decimal_places=4, blank=True, null=True)
    confidence_60 = models.DecimalField('confidence 60%', max_digits=10, decimal_places=4, blank=True, null=True)
    # rank
    sim_return = models.DecimalField('simulate return', max_digits=10, decimal_places=4, blank=True, null=True)
    return_rank = models.DecimalField('return rank', max_digits=10, decimal_places=4, blank=True, null=True)
    risk_rank = models.DecimalField('risk rank', max_digits=10, decimal_places=4, blank=True, null=True)
    volume_rank = models.DecimalField('volume rank', max_digits=10, decimal_places=4, blank=True, null=True)
    return_mean_rank = models.DecimalField('return mean rank', max_digits=10, decimal_places=4, blank=True, null=True)
    return_sigma_rank = models.DecimalField('return sigma rank', max_digits=10, decimal_places=4, blank=True, null=True)

    # future changes
    next_week_price = models.DecimalField('next week price', max_digits=10, decimal_places=4, blank=True, null=True)
    next_month_price = models.DecimalField('next month price', max_digits=10, decimal_places=4, blank=True,
                                           null=True)
    csv_path = models.CharField('csv path', max_length=255, blank=True, null=False)

    objects = WeeklyPredictionManager()

    def __str__(self):
        return f'{self.code}@{self.week}'

    @cached_property
    def company(self):
        return Company.objects.filter(code=self.code).first()

    @property
    def next_week_return(self):
        previous=self.previous(1)
        if previous:
            next_week_return = (self.current_price - previous.current_price) / previous.current_price
            return round(next_week_return * 100, 3)

    def calculate_last(self):
        last_prediction = self.previous(1)
        if last_prediction:
            last_prediction.next_week_price = self.current_price
            last_prediction.save()

    @staticmethod
    def process_csv(week):
        result_csv = os.path.join(settings.BASE_DIR, 'data', str(week), 'result.csv')
        if not os.path.exists(result_csv):
            print(f'{result_csv} not exist.')
            return

        # ['code', 'last_date', 'start price', 'sim_mean', 'sim_diff', 'VaR 99%', 'VaR 99% Percent', 'volume_mean',
        #  'return_mean', 'return_sigma', 'percent99', 'percent90', 'percent80', 'percent70', 'percent60'])

        model_csv_map = {
            'last_price_date': 'last_date',
            'current_price': 'start price',
            'sim_mean': 'sim_mean',
            'sim_diff': 'sim_diff',
            'var_99': 'VaR 99%',
            'var_99_percent': 'VaR 99% Percent',
            'volume_mean': 'volume_mean',
            'return_mean': 'return_mean',
            'return_sigma': 'return_sigma',
            'confidence_99': 'percent99',
            'confidence_90': 'percent90',
            'confidence_80': 'percent80',
            'confidence_70': 'percent70',
            'confidence_60': 'percent60',
            'sim_return': 'return',
            'return_rank': 'return_rank',
            'risk_rank': 'risk_rank',
            'volume_rank': 'volume_rank',
            'return_mean_rank': 'return_mean_rank',
            'return_sigma_rank': 'return_sigma_rank',
        }
        counter = 0
        failed = 0
        with open(result_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                data = dict([(model_field, row[csv_field]) for model_field, csv_field in model_csv_map.items()])
                data['csv_path'] = result_csv
                try:
                    prediction, created = WeeklyPrediction.objects.update_or_create(code=row['code'], week=week,
                                                                                    defaults=data)
                    prediction.calculate_last()

                    # update last price and date
                    date = datetime.strptime(data['last_price_date'], '%Y-%m-%d').date()
                    com, created = Company.objects.get_or_create(code=row['code'])
                    if not com.last_price_date or com.last_price_date < date:
                        com.last_price = data['current_price']
                        com.last_price_date = date
                        com.daily_volume = Decimal(str(data['volume_mean']))
                        com.save()
                except Exception as ex:
                    failed += 1
                    print(row['code'], str(ex))
                    print(data)
                counter += 1
        print(f'{counter} records updated, {failed} failed.')

    @staticmethod
    def top_rank(week, limit=20):
        return WeeklyPrediction.objects.week(week).order_by('-sim_return')[:limit]

    @property
    def sim_pic_url(self):
        return '%s%s/pic/%s.png' % (settings.MEDIA_URL, self.week, self.code)

    @property
    def line_pic_url(self):
        return '%s%s/pic/%s_line.png' % (settings.MEDIA_URL, self.week, self.code)
