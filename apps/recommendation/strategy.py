from django.db.models import F, Q

from apps.asx.models import Company
from apps.prediction.models import WeeklyPrediction
from apps.recommendation.models import WeeklyRecommendation


class Strategy:
    count = 20

    @property
    def name(self):
        return self.__class__.__name__

    def run(self, week):
        raise NotImplementedError


class ReturnRiskRank(Strategy):
    count = 40

    @property
    def name(self):
        return self.__class__.__name__

    def run(self, week):
        WeeklyRecommendation.objects.filter(week=week, strategy=self.name).delete()
        value_company = Company.exclude_trash(10)
        predictions = WeeklyPrediction.objects.week(week).filter(
            code__in=value_company.values_list('code', flat=True)).exclude(
            Q(return_rank__isnull=True) | Q(risk_rank__isnull=True))
        ranked_queryset = predictions.annotate(rank=F('return_rank') - F('risk_rank')).order_by('-rank')
        recommendations = ranked_queryset[:self.count]

        for rec in recommendations:
            WeeklyRecommendation.objects.update_or_create(week=week, strategy=self.name, prediction=rec,
                                                          defaults={'rank': rec.rank})
        return recommendations
