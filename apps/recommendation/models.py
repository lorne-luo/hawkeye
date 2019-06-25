from __future__ import absolute_import, unicode_literals

import os
from io import BytesIO

import matplotlib.pyplot as plt
from django.conf import settings
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

    @cached_property
    def code(self):
        return self.prediction.code

    @staticmethod
    def generate_scatter(week, save=True):
        image_path = os.path.join(settings.MEDIA_ROOT, str(week), 'pic', 'top_rank_scatter.png')

        items = WeeklyRecommendation.objects.filter(week=week)
        plt.figure(figsize=(16, 8))
        plt.ylim(bottom=60, top=100)
        plt.xlim(left=0, right=35)

        for item in items:
            code = item.code
            return_rank = float(item.prediction.return_rank)
            risk_rank = float(item.prediction.risk_rank)
            volume_rank = float(item.prediction.volume_rank)
            plt.scatter(risk_rank, return_rank, s=volume_rank * 7, alpha=0.4)
            plt.annotate(code,
                         xy=(risk_rank, return_rank),
                         xytext=(20, 20),
                         textcoords='offset points',
                         ha='right',
                         va='bottom',
                         arrowprops=dict(arrowstyle='-', connectionstyle='arc3,rad=-0.3'))

        plt.title(f"{week} # Return vs Risk vs Volume for top rank")
        plt.xlabel("RISK")
        plt.ylabel("RETURN")
        if save:
            plt.savefig(image_path, format='png')
            return image_path
        else:
            io = BytesIO()
            plt.savefig(io, format='png')
            plt.clf()
            plt.cla()
            plt.close()
            io.seek(0)
            return io