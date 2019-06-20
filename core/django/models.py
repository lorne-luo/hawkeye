from __future__ import absolute_import, unicode_literals

from datetime import datetime

from dateutil.relativedelta import relativedelta, FR
from django.db import models
from django.utils.functional import cached_property


class WeeklyModel(models.Model):
    week = models.IntegerField('week', blank=False, null=False)

    class Meta:
        abstract = True

    @property
    def week_date(self):
        return datetime.strptime(str(self.week), '%Y%m%d')

    @property
    def last_week_date(self):
        if self.week_date.weekday() == 4:
            return self.week_date - relativedelta(weekday=FR(-2))
        else:
            return self.week_date - relativedelta(weekday=FR(-1))

    @property
    def next_week_date(self):
        if self.week_date.weekday() == 4:
            return self.week_date + relativedelta(weekday=FR(2))
        else:
            return self.week_date + relativedelta(weekday=FR(1))

    @cached_property
    def last(self):
        last_week_date = self.last_week_date
        last_week = last_week_date.year * 10000 + last_week_date.month * 100 + last_week_date.day
        return self.__class__.objects.filter(code=self.code, week=last_week).first()

    @cached_property
    def next(self):
        next_week_date = self.next_week_date
        next_week = next_week_date.year * 10000 + next_week_date.month * 100 + next_week_date.day
        return self.__class__.objects.filter(code=self.code, week=next_week).first()
