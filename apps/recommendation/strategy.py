from django.db.models import F

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
    count = 20

    @property
    def name(self):
        return self.__class__.__name__

    def run(self, week):
        ranked_queryset = WeeklyPrediction.objects.week(week).annotate(rank=F('return_rank') - F('risk_rank')).order_by(
            '-rank')
        recommendations = ranked_queryset[:self.count]

        for rec in recommendations:
            WeeklyRecommendation.objects.update_or_create(week=week, strategy=self.name, prediction=rec,
                                                          defaults={'rank': rec.rank})
        WeeklyRecommendation.generate_scatter(week)
        return recommendations
