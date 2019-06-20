from datetime import datetime

from dateutil.relativedelta import relativedelta, FR
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.views.generic import ListView, RedirectView
from django_filters.views import FilterView

from apps.recommendation.models import WeeklyRecommendation
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

