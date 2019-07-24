from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

# from cms.search import views as search_views
# from cms.articles.api import urls as article_api_urls

# REST API
api_v1_urlpatterns = [
    path(r'api/v1/asx/', include('apps.asx.api.urls', namespace='api')),
]

urlpatterns = api_v1_urlpatterns + [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'', include('autocode.urls', namespace='autocode')),

    url(r'^', include('apps.prediction.urls', namespace='prediction')),
    url(r'^', include('apps.recommendation.urls', namespace='recommendation')),

    # url(r'^search/$', search_views.search, name='search'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    # url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
