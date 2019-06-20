from datetime import datetime

from dateutil.relativedelta import relativedelta, FR
from django.core.exceptions import ImproperlyConfigured
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
