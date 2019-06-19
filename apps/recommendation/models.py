from __future__ import absolute_import, unicode_literals

from django.db import models
from django.db.models.manager import Manager
from django.utils.functional import cached_property

from apps.prediction.models import WeeklyPrediction


class WeeklyRecommendationManager(Manager):
    def week(self, week, strategy):
        return super().get_queryset().filter(week=week, strategy=strategy)


class WeeklyRecommendation(models.Model):
    strategy = models.CharField('strategy', max_length=80, blank=True, null=False)
    week = models.IntegerField('week', blank=False, null=False)
    code = models.ForeignKey(WeeklyPrediction, blank=True, null=True, on_delete=models.SET_NULL)
    rank = models.DecimalField('rank', max_digits=10, decimal_places=4, blank=True, null=True)
    future_week_price = models.DecimalField('future week price', max_digits=10, decimal_places=4, blank=True, null=True)
    future_week_return = models.DecimalField('future week return', max_digits=10, decimal_places=4, blank=True,
                                             null=True)
    future_month_price = models.DecimalField('future month price', max_digits=10, decimal_places=4, blank=True,
                                             null=True)
    future_month_return = models.DecimalField('future month return', max_digits=10, decimal_places=4, blank=True,
                                              null=True)

    objects = WeeklyRecommendationManager()

    def __str__(self):
        return f'{self.code}@{self.week}'

    @cached_property
    def company(self):
        return ''
