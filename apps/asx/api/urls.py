from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.include_root_view = False

# reverse('api:company-list'), reverse('api:company-detail', kwargs={'pk': 1})
router.register(r'company', views.CompanyViewSet, base_name='company')

urlpatterns = [

]

urlpatterns += router.urls
