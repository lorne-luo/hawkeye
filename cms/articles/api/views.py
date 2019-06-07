from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from ..models import ArticlePage
from .serializers import ArticlePageSerializer


class ArticlePageViewSet(ViewSet):
    def list(self, request):
        ids = request.GET.getlist('id')
        queryset = ArticlePage.objects.live().filter(id__in=ids) if ids else ArticlePage.objects.none()
        serializer = ArticlePageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ArticlePage.objects.live()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ArticlePageSerializer(user)
        return Response(serializer.data)
