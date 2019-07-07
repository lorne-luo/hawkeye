from datetime import datetime

from dateutil.relativedelta import relativedelta, FR
from django.core.exceptions import ImproperlyConfigured


class WeekViewMixin:

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

    def get_query_week(self):
        return self.kwargs.get('week') or self.request.GET.get('week') or self.get_weeks()[0]

    def get_weeks(self):
        return [x.week for x in self.model.objects.all().distinct('week').order_by('-week')]

    def get_context_data(self, *, object_list=None, **kwargs):
        week = self.get_query_week()
        weeks = self.get_weeks()

        context = super(WeekViewMixin, self).get_context_data(object_list=object_list, **kwargs)
        context['all_weeks'] = weeks
        context['week'] = int(week)
        return context
