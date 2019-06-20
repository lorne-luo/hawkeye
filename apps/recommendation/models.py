from __future__ import absolute_import, unicode_literals

from django.db import models
from django.db.models.manager import Manager
from django.utils.functional import cached_property

from apps.asx.models import Company
from apps.prediction.models import WeeklyPrediction
from core.django.models import WeeklyModel


class WeeklyRecommendationManager(Manager):
    def week(self, week, strategy):
        return super().get_queryset().filter(week=week, strategy=strategy)


class WeeklyRecommendation(WeeklyModel):
    strategy = models.CharField('strategy', max_length=80, blank=True, null=False)
    prediction = models.ForeignKey(WeeklyPrediction, blank=True, null=True, on_delete=models.SET_NULL)
    rank = models.DecimalField('rank', max_digits=10, decimal_places=4, blank=True, null=True)

    objects = WeeklyRecommendationManager()

    def __str__(self):
        return f'{self.prediction.code}@{self.week}'

    @cached_property
    def company(self):
        return self.prediction.company
