from io import BytesIO

import matplotlib.pyplot as plt
from django.db.models import Max, Min
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, RedirectView
from django_filters.views import FilterView

from apps.recommendation.models import WeeklyRecommendation
from apps.utils.helper import return_percent
from core.django.views import WeekViewMixin


class WeeklyRecommendationRedirectView(WeekViewMixin, RedirectView):
    model = WeeklyRecommendation

    def get_redirect_url(self, *args, **kwargs):
        week = self.get_weeks()[-1]
        return reverse('recommendation:recommendation_list', args=[week])


class WeeklyRecommendationListView(WeekViewMixin, FilterView, ListView):
    model = WeeklyRecommendation
    paginate_by = 20
    template_name_suffix = '_list'
    ordering = '-rank'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WeeklyRecommendationListView, self).get_context_data(object_list=object_list, **kwargs)
        recommendations = context.get('object_list')

        next_week_counter = 0
        next_month_counter = 0
        next_week_return = 0
        next_month_return = 0
        for rec in recommendations:
            next_week = rec.prediction.next(1)
            next_month = rec.prediction.next(4)
            if next_week:
                print(next_week.code, return_percent(next_week.current_price, rec.prediction.current_price))
                next_week_counter += 1
                next_week_return += return_percent(next_week.current_price, rec.prediction.current_price)
            if next_month:
                next_month_counter += 1
                next_month_return += return_percent(next_month.current_price, rec.prediction.current_price)

        if next_week_counter:
            context['avg_week_return'] = round(next_week_return / next_week_counter, 3)
        if next_month_counter:
            context['avg_month_return'] = round(next_month_return / next_month_counter, 3)

        page = self.request.GET.get('page')
        page = int(page) if page else 1
        context['start'] = (page - 1) * self.paginate_by
        return context


def top_rank_scatter(request, week):
    items = WeeklyRecommendation.objects.filter(week=week)
    if not items:
        return None

    plt.figure(figsize=(16, 8))
    plt.ylim(bottom=60, top=100)
    plt.xlim(left=0, right=35)

    vol = items.aggregate(Max('prediction__volume_mean'), Min('prediction__volume_mean'))
    minm = float(vol.get('prediction__volume_mean__min'))
    maxm = vol.get('prediction__volume_mean__max')

    for item in items:
        code = item.code
        return_rank = float(item.prediction.return_rank)
        risk_rank = float(item.prediction.risk_rank)
        volume_mean = float(item.prediction.volume_mean)
        size = volume_mean / minm * 5
        plt.scatter(risk_rank, return_rank, s=size, alpha=0.4)
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

    io = BytesIO()
    plt.savefig(io, format='png')
    plt.clf()
    plt.cla()
    plt.close()
    io.seek(0)

    return HttpResponse(io.read(), content_type="image/png")
