from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.functional import cached_property

from apps.market.models import Market


class Industry(models.Model):
    name = models.CharField('name', max_length=80, blank=False, null=False, unique=True)

    @cached_property
    def company_count(self):
        return self.company_set.count()

    def get_company_set(self, market):
        if isinstance(market, str):
            return self.company_set.filter(market__name=market)
        elif isinstance(market, Market):
            return self.company_set.filter(market=market)
        return Company.objects.none()


class Company(models.Model):
    code = models.CharField('code', max_length=80, blank=False, null=False)
    name = models.CharField('name', max_length=80, blank=False, null=False)
    country = models.CharField('country', max_length=80, blank=True, null=False)
    # billion usd
    total_value = models.DecimalField('total value', max_digits=12, decimal_places=4, blank=True, null=True)
    industry = models.ForeignKey(Industry, blank=True, null=True, on_delete=models.SET_NULL)
    market = models.ForeignKey(Market, blank=True, null=True, on_delete=models.SET_NULL)
    is_archived = models.BooleanField(blank=True, null=True, default=False)
    daily_volume = models.DecimalField('daily volume', max_digits=14, decimal_places=4, blank=True, null=True)
    create_at = models.DateTimeField('create at', auto_now_add=True, auto_now=False)
    last_price = models.DecimalField('last price', max_digits=10, decimal_places=4, blank=True, null=True)
    last_price_date = models.DateField('last price date', auto_now_add=False, auto_now=False, editable=True, blank=True,
                                       null=True)


class ASXCompany(models.Model):
    """Company"""
    is_asx_200 = models.BooleanField(blank=False, null=False, default=False)
