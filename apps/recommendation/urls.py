from django.conf.urls import url

from . import views

# from rest_framework import routers

# router = routers.DefaultRouter()

app_name = 'recommendation'
urlpatterns = (
    # urls for Plan
    url(r'^$', views.WeeklyRecommendationRedirectView.as_view(), name='recommendation_index'),
    url(r'^(?P<week>[\d]+)/$', views.WeeklyRecommendationListView.as_view(), name='recommendation_list'),
    url(r'^(?P<week>[\d]+)/top_rank_scatter.png', views.top_rank_scatter, name='top_rank_scatter'),
)
