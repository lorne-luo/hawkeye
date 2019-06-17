from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.prediction.models import WeeklyPrediction


class WeeklyPredictionView(ListView):
    model = WeeklyPrediction
    paginate_by = 20
    template_name_suffix = '_list'
