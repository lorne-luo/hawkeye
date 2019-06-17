from datetime import datetime

import django_filters
from dateutil.relativedelta import relativedelta, FR
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView
from django_filters.views import FilterView

from apps.prediction.models import WeeklyPrediction
from asx import get_last_friday


#
# class AccountPlatformFilter(Filter):
#     def filter(self, qs, value):
#         if value:
#             return qs.filter(week=value)
#         return qs


class WeeklyPredictionFilter(django_filters.FilterSet):
    # week = WeeklyPredictionFilter(field_name='platform_id')

    class Meta:
        model = WeeklyPrediction
        fields = ['week']


class WeeklyPredictionListView(FilterView, ListView):
    model = WeeklyPrediction
    paginate_by = 20
    template_name_suffix = '_list'

    def get_filterset_kwargs(self, filterset_class):
        week = self.kwargs.get('week') or self.get_get_last_friday()

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

    def get_get_last_friday(self):
        friday = get_last_friday()
        return friday.year * 10000 + friday.month * 100 + friday.day

    def get_week_options(self, first_week, last_week):
        weeks = [first_week]
        start_date = datetime.strptime(str(first_week), '%Y%m%d')
        while (True):
            friday = start_date + relativedelta(weekday=FR(2))
            number = friday.year * 10000 + friday.month * 100 + friday.day
            if number > int(last_week):
                break
            weeks.append(number)

        return weeks

    def get_context_data(self, *, object_list=None, **kwargs):
        week = self.kwargs.get('week') or self.get_get_last_friday()
        first_week = WeeklyPrediction.objects.all().order_by('week').first().week
        weeks = self.get_week_options(first_week, week)

        context = super(WeeklyPredictionListView, self).get_context_data(object_list=object_list, **kwargs)
        context['all_weeks'] = weeks
        context['week'] = week
        return context
