from django.conf.urls import url, include
# from rest_framework import routers

from . import views

# router = routers.DefaultRouter()

urlpatterns = (
    # urls for Plan
    url(r'^prediction/$', views.WeeklyPredictionListView.as_view(), name='prediction_list'),
    url(r'^prediction/(?P<week>[\d]+)/$', views.WeeklyPredictionListView.as_view(), name='prediction_list'),
)
