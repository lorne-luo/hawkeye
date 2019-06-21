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

    @property
    def next_month_date(self):
        if self.week_date.weekday() == 4:
            return self.week_date + relativedelta(weekday=FR(5))
        else:
            return self.week_date + relativedelta(weekday=FR(4))

    @cached_property
    def last(self):
        last_week = date_to_int(self.last_week_date)
        return self.__class__.objects.filter(code=self.code, week=last_week).first()

    @cached_property
    def next(self):
        next_week = date_to_int(self.next_week_date)
        return self.__class__.objects.filter(code=self.code, week=next_week).first()
