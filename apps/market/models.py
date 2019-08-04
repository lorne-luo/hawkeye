from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.functional import cached_property


class Market(models.Model):
    code = models.CharField('code', max_length=80, blank=False, null=False)
    name = models.CharField('name', max_length=80, blank=False, null=False)
    region = models.CharField('region', max_length=80, blank=True, null=False)
    total_value = models.DecimalField('total value', max_digits=12, decimal_places=4, blank=True,
                                      null=True)  # billion usd
    currency = models.CharField('currency', max_length=80, blank=True, null=False)
    open_time = models.SmallIntegerField('open time', blank=True, null=True)  # utc time
    close_time = models.SmallIntegerField('close time', blank=True, null=True)  # utc

    @cached_property
    def company_count(self):
        return self.company_set.count()
