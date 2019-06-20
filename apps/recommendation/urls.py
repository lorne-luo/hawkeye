from django.conf.urls import url, include
# from rest_framework import routers

from . import views

# router = routers.DefaultRouter()

urlpatterns = (
    # urls for Plan
    url(r'^recommendation/$', views.WeeklyRecommendationRedirectView.as_view(), name='recommendation_index'),
    url(r'^recommendation/(?P<week>[\d]+)/$', views.WeeklyRecommendationListView.as_view(), name='recommendation_list'),
)
