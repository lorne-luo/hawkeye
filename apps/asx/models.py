from __future__ import absolute_import, unicode_literals

import csv
import os

from dateutil.relativedelta import relativedelta, FR
from django.conf import settings
from django.db import models
from django.db.models.manager import Manager
from django.utils.functional import cached_property

from apps.utils.helper import date_to_int
from asx import get_asx_df, get_asx_200_list


class Industry(models.Model):
    name = models.CharField('name', max_length=80, blank=False, null=False)

    @cached_property
    def company_count(self):
        return self.company_set.count()


class CompanyManager(Manager):
    def dead(self):
        return super().get_queryset().filter(last_price__isnull=True)

    def avtive(self):
        return super().get_queryset().filter(is_active=True)

    def non_trash(self):
        return super().get_queryset().filter(is_trash=False)

    def trash(self):
        return super().get_queryset().filter(is_trash=True)


class Company(models.Model):
    """Company name,ASX code,GICS industry group"""
    name = models.CharField('name', max_length=80, blank=False, null=False)
    code = models.CharField('code', max_length=10, blank=False, null=False, unique=True)
    industry = models.ForeignKey(Industry, blank=True, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    asx_200 = models.BooleanField(blank=False, null=False, default=False)
    last_price_date = models.DateField('last price date', auto_now_add=False, auto_now=False, editable=True, blank=True,
                                       null=True)
    last_price = models.DecimalField('last price', max_digits=10, decimal_places=4, blank=True, null=True)
    daily_volume = models.DecimalField('daily volume', max_digits=14, decimal_places=4, blank=True, null=True)
    create_at = models.DateTimeField('create at', auto_now_add=True, auto_now=False)
    is_trash = models.BooleanField(blank=False, null=False, default=False)

    objects = CompanyManager()

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code}'

    @staticmethod
    def sync():
        df = get_asx_df()
        counter = 0
        for i in range(len(df)):
            name, code, industry_name = df.iloc[i]['Company name'], df.iloc[i]['ASX code'], df.iloc[i][
                'GICS industry group']
            industry, create = Industry.objects.get_or_create(name=industry_name)
            Company.objects.update_or_create(code=code, name=name, defaults={'industry': industry, 'is_active': True})
            counter += 1

        inactived = Company.objects.exclude(code__in=list(df['ASX code'])).update(is_active=False)

        print(f'{counter} companies updated, {inactived} inacitived')
        asx_200 = get_asx_200_list()
        counter = Company.objects.filter(code__in=asx_200).update(asx_200=True)
        print(f'{counter} ASX 200 companies updated.')

    @cached_property
    def week(self):
        return self.last_price_date + relativedelta(weekday=FR(-1))

    @cached_property
    def industry_name(self):
        return self.industry.name if self.industry else ''

    @cached_property
    def week_number(self):
        return date_to_int(self.week)

    @property
    def simulation_pic_url(self):
        return '%s%s/pic/%s.png' % (settings.MEDIA_URL, self.week_number, self.code)

    @property
    def line_pic_url(self):
        return '%s%s/pic/%s_line.png' % (settings.MEDIA_URL, self.week_number, self.code)

    @staticmethod
    def export_csv():
        path = os.path.join(settings.BASE_DIR, 'data', 'asx.csv')
        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ['code', 'name', 'industry', 'last_date', 'last_price', 'volume', 'asx_200'])
            for com in Company.objects.all():
                writer.writerow(
                    [com.code, com.name, com.industry_name, com.last_price_date, com.last_price, com.daily_volume,
                     com.asx_200])
