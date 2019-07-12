from rest_framework.routers import DefaultRouter

from apps.asx.api.views import CompanyViewSet

router = DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')

app_name = 'asx'
urlpatterns = [

]

urlpatterns += router.urls
