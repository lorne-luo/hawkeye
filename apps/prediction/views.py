from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views.generic import ListView, RedirectView
from django_filters.views import FilterView
from pandas.plotting import register_matplotlib_converters

from apps.prediction.models import WeeklyPrediction
from core.django.views import WeekViewMixin
from core.matplotlib import add_arrow


class WeeklyPredictionRedirectView(WeekViewMixin, RedirectView):
    model = WeeklyPrediction

    def get_redirect_url(self, *args, **kwargs):
        week = self.get_weeks()[0]
        return reverse('prediction:prediction_list', args=[week])


class WeeklyPredictionListView(WeekViewMixin, FilterView, ListView):
    model = WeeklyPrediction
    paginate_by = 20
    template_name_suffix = '_list'
    ordering = '-return_rank'

    def get_queryset(self):
        code = self.request.GET.get('q')
        if code:
            return WeeklyPrediction.objects.filter(code=code)
        else:
            return super(WeeklyPredictionListView, self).get_queryset()


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
    next_pre = prediction.get_next(4) or prediction.get_next(3) or prediction.get_next(2) or prediction.get_next(
        1) or None
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


def rank_trend_image2(request, code):
    register_matplotlib_converters()

    weeks_age = datetime.now() - relativedelta(weeks=8)  # past 1 year
    week_number = int(weeks_age.strftime('%Y%m%d'))
    predictions = WeeklyPrediction.objects.filter(code=code.upper(), week__gte=week_number).order_by('week')

    factor = 400 / max(predictions.values_list('volume_mean', flat=True))
    previous_pred = None

    max_risk = float(max(predictions.values_list('var_99_percent', flat=True)))
    max_return = float(max(predictions.values_list('sim_return', flat=True)))
    plt.ylim(bottom=0, top=max_return + 0.1)
    plt.xlim(left=0, right=max_risk + 0.1)

    for pred in predictions:
        # size = float(pred.volume_mean * factor)
        # plt.scatter(pred.var_99_percent, pred.sim_return, s=size, alpha=0.4)
        plt.annotate(str(pred.week)[4:],
                     xy=(pred.var_99_percent, pred.sim_return),
                     xytext=(0, -20),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')

        plt.title(f"# Return vs Risk vs Volume trend for {code}")
        plt.xlabel("RISK")
        plt.ylabel("RETURN")

        if previous_pred:
            x1, y1 = [previous_pred.var_99_percent, pred.var_99_percent], [previous_pred.sim_return, pred.sim_return]
            line = plt.plot(x1, y1, marker='o')[0]
            add_arrow(line)
        previous_pred = pred

    io = BytesIO()
    plt.savefig(io, format='png')
    plt.clf()
    plt.cla()
    plt.close()
    io.seek(0)

    return HttpResponse(io.read(), content_type="image/png")
