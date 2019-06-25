from django.conf.urls import url, include
# from rest_framework import routers

from . import views

# router = routers.DefaultRouter()

urlpatterns = (
    # urls for Plan
    url(r'^$', views.WeeklyRecommendationRedirectView.as_view(), name='recommendation_index'),
    url(r'^(?P<week>[\d]+)/$', views.WeeklyRecommendationListView.as_view(), name='recommendation_list'),
)
