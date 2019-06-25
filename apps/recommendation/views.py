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
        return context
