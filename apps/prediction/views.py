from datetime import datetime

from dateutil.relativedelta import relativedelta, FR
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.views.generic import ListView, RedirectView
from django_filters.views import FilterView

from apps.prediction.models import WeeklyPrediction
from asx import get_last_friday


class WeeklyPredictionRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        week = WeeklyPredictionListView.get_get_last_friday()
        return reverse('prediction:prediction_list_week', args=[week])


class WeeklyPredictionListView(FilterView, ListView):
    model = WeeklyPrediction
    paginate_by = 20
    template_name_suffix = '_list'

    def get_filterset_kwargs(self, filterset_class):
        week = self.get_query_week()

        kwargs = {
            'data': {'week': week},
            'request': self.request,
        }
        try:
            kwargs.update({
                'queryset': self.get_queryset(),
            })
        except ImproperlyConfigured:
            # ignore the error here if the filterset has a model defined
            # to acquire a queryset from
            if filterset_class._meta.model is None:
                msg = ("'%s' does not define a 'model' and the view '%s' does "
                       "not return a valid queryset from 'get_queryset'.  You "
                       "must fix one of them.")
                args = (filterset_class.__name__, self.__class__.__name__)
                raise ImproperlyConfigured(msg % args)
        return kwargs

    @classmethod
    def get_get_last_friday(self):
        friday = get_last_friday()
        return friday.year * 10000 + friday.month * 100 + friday.day

    def get_query_week(self):
        return self.kwargs.get('week') or self.request.GET.get('week') or self.get_get_last_friday()

    def get_week_options(self, first_week, last_week):
        weeks = [first_week]
        start_date = datetime.strptime(str(first_week), '%Y%m%d')
        friday = start_date
        while (True):
            friday += relativedelta(weekday=FR(2))
            number = friday.year * 10000 + friday.month * 100 + friday.day
            if number > int(last_week):
                break
            weeks.append(number)

        return weeks

    def get_context_data(self, *, object_list=None, **kwargs):
        week = self.get_query_week()
        first_week = WeeklyPrediction.objects.all().order_by('week').first().week
        last_week = WeeklyPrediction.objects.all().order_by('week').last().week
        weeks = self.get_week_options(first_week, last_week)

        context = super(WeeklyPredictionListView, self).get_context_data(object_list=object_list, **kwargs)
        context['all_weeks'] = weeks
        context['week'] = int(week)
        return context
