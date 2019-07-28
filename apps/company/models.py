from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.functional import cached_property


class Company(models.Model):
    code = models.CharField('code', max_length=80, blank=False, null=False)
    name = models.CharField('name', max_length=80, blank=False, null=False)
    country = models.CharField('country', max_length=80, blank=True, null=False)
    total_value = models.DecimalField('total value', max_digits=12, decimal_places=4, blank=True,
                                      null=True)  # billion usd
    currency = models.CharField('currency', max_length=80, blank=True, null=False)
