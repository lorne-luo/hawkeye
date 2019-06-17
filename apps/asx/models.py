from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.functional import cached_property

from asx import get_asx_df, get_asx_200_list


class Industry(models.Model):
    name = models.CharField('name', max_length=80, blank=False, null=False)

    @cached_property
    def company_count(self):
        return self.company_set.count()


class Company(models.Model):
    """Company name,ASX code,GICS industry group"""
    name = models.CharField('name', max_length=80, blank=False, null=False)
    code = models.CharField('code', max_length=10, blank=False, null=False, unique=True)
    industry = models.ForeignKey(Industry, blank=True, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    asx_200 = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code}'

    @staticmethod
    def update():
        df = get_asx_df()
        counter = 0
        for i in range(len(df)):
            name, code, industry_name = df.iloc[i]['Company name'], df.iloc[i]['ASX code'], df.iloc[i][
                'GICS industry group']
            industry, create = Industry.objects.get_or_create(name=industry_name)
            Company.objects.get_or_create(code=code, name=name, defaults={'industry': industry, 'is_active': True})
            counter += 1

        print(f'{counter} companies updated.')
        asx_200 = get_asx_200_list()
        counter = Company.objects.filter(code__in=asx_200).update(asx_200=True)
        print(f'{counter} ASX 200 companies updated.')
