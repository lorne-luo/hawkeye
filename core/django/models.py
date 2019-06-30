from __future__ import absolute_import, unicode_literals

from datetime import datetime

from dateutil.relativedelta import relativedelta, FR
from django.db import models
from django.utils.functional import cached_property

from apps.utils.helper import date_to_int


class WeeklyModel(models.Model):
    week = models.IntegerField('week', blank=False, null=False)

    class Meta:
        abstract = True

    @property
    def week_date(self):
        return datetime.strptime(str(self.week), '%Y%m%d')

    def get_previous_week(self, number=1):
        if self.week_date.weekday() == 4:
            return self.week_date - relativedelta(weekday=FR(-1 - number))
        else:
            return self.week_date - relativedelta(weekday=FR(-1 * number))

    def get_next_week(self, number=1):
        if self.week_date.weekday() == 4:
            return self.week_date - relativedelta(weekday=FR(1 + number))
        else:
            return self.week_date - relativedelta(weekday=FR(number))

    def get_previous(self, number=1):
        last_week = date_to_int(self.get_previous_week(number))
        return self.__class__.objects.filter(code=self.code, week=last_week).first()

    @cached_property
    def previous(self):
        return self.get_previous(1)

    def get_next(self, number=1):
        next_week = date_to_int(self.get_next_week(number))
        return self.__class__.objects.filter(code=self.code, week=next_week).first()

    @cached_property
    def next(self):
        return self.get_next(1)

    def has_previous(self):
        return self.__class__.objects.filter(code=self.code, week__lt=self.week).exists()

    def has_next(self):
        return self.__class__.objects.filter(code=self.code, week__gt=self.week).exists()
