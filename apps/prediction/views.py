import os
from datetime import datetime
from io import StringIO, BytesIO

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views.generic import ListView, RedirectView
from django_filters.views import FilterView

from apps.prediction.models import WeeklyPrediction
from core.django.views import WeekViewMixin


class WeeklyPredictionRedirectView(WeekViewMixin, RedirectView):
    model = WeeklyPrediction

    def get_redirect_url(self, *args, **kwargs):
        week = self.get_weeks()[-1]
        return reverse('prediction:prediction_list', args=[week])


class WeeklyPredictionListView(WeekViewMixin, FilterView, ListView):
    model = WeeklyPrediction
    paginate_by = 20
    template_name_suffix = '_list'


def line_image(request, week, code):
    prediction = WeeklyPrediction.objects.get(week=week, code=code.upper())

    parser = lambda date: pd.datetime.strptime(date, '%Y-%m-%d')
    df = pd.read_csv(prediction.code_csv_path, index_col='date', parse_dates=[0], date_parser=parser)
    df = df.dropna()
    df.drop(index=df[df['1. open'] == 0].index, inplace=True)

    plt.plot(df.index, df['4. close'])
    plt.legend([prediction.code], loc='upper left')
    plt.title(f"{prediction.code} price movement.", weight='bold')
    # plt.axvline(x=prediction.week_date, linewidth=1, color='r')
    ax = plt.gca()
    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=20))
    ax.xaxis.set_label_text('')
    # for tick in ax.get_xticklabels():
    #     tick.set_rotation(90)
    # plt.xlabel('xlabel', fontsize=5)
    io = BytesIO()
    plt.savefig(io, format='png')
    plt.clf()
    plt.cla()
    plt.close()
    io.seek(0)

    return HttpResponse(io.read(), content_type="image/png")


def future_image(request, week, code):
    prediction = WeeklyPrediction.objects.get(week=week, code=code.upper())
    next_pre = prediction.next(4) or prediction.next(3) or prediction.next(2) or prediction.next(1) or None
    if not next_pre:
        raise Http404

    parser = lambda date: pd.datetime.strptime(date, '%Y-%m-%d')
    df = pd.read_csv(next_pre.code_csv_path, index_col='date', parse_dates=[0], date_parser=parser)
    df = df.dropna()
    df.drop(index=df[df['1. open'] == 0].index, inplace=True)

    plt.plot(df.index, df['4. close'])
    plt.legend([next_pre.code], loc='upper left')
    plt.title(f"{next_pre.code} price movement.", weight='bold')
    plt.axvline(x=prediction.week_date, linewidth=1, color='r')
    ax = plt.gca()
    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=20))
    ax.xaxis.set_label_text('')
    # for tick in ax.get_xticklabels():
    #     tick.set_rotation(90)
    # plt.xlabel('xlabel', fontsize=5)
    io = BytesIO()
    plt.savefig(io, format='png')
    plt.clf()
    plt.cla()
    plt.close()
    io.seek(0)

    return HttpResponse(io.read(), content_type="image/png")


def rank_trend_image(request, code):
    register_matplotlib_converters()

    weeks_age = datetime.now() - relativedelta(weeks=53)
    week_number = int(weeks_age.strftime('%Y%m%d'))
    predictions = WeeklyPrediction.objects.filter(code=code.upper(), week__gte=week_number).order_by('week')

    x = [str(x) for x in predictions.values_list('week', flat=True)]
    plt.plot(x, predictions.values_list('return_rank', flat=True), label="Return Rank")

    plt.plot(x, predictions.values_list('risk_rank', flat=True), label="Risk Rank")

    # plt.legend(['Return Rank', 'Risk Rank'], loc='mid left')
    plt.legend(loc='center left')
    plt.title(f"{code} price movement.", weight='bold')
    ax = plt.gca()
    ax.xaxis.set_label_text('')
    io = BytesIO()
    plt.savefig(io, format='png')
    plt.clf()
    plt.cla()
    plt.close()
    io.seek(0)

    return HttpResponse(io.read(), content_type="image/png")
