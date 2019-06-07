from rest_framework.routers import DefaultRouter
from .views import ArticlePageViewSet

router = DefaultRouter()
router.register(r'article_page', ArticlePageViewSet, base_name='article_page')
urlpatterns = router.urls
