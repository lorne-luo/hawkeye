from django.conf.urls import url, include
# from rest_framework import routers

from . import views

# router = routers.DefaultRouter()

app_name = 'perdiction'
urlpatterns = (
    # urls for Plan
    url(r'^prediction/$', views.WeeklyPredictionRedirectView.as_view(), name='prediction_index'),
    url(r'^prediction/(?P<week>[\d]+)/$', views.WeeklyPredictionListView.as_view(), name='prediction_list'),
    url(r'^prediction/(?P<week>[\d]+)/(?P<code>[\w]+)_line.png', views.line_image, name='prediction_line_image'),
    url(r'^prediction/(?P<week>[\d]+)/(?P<code>[\w]+)_future.png', views.future_image, name='prediction_future_image'),
    url(r'^prediction/(?P<code>[\w]+)_rank_trend.png', views.rank_trend_image2, name='rank_trend_image'),
)
