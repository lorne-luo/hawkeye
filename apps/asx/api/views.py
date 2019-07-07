import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apps.asx.api.serializers import CompanySerializer
from ..models import Company

log = logging.getLogger(__name__)


class CompanyViewSet(viewsets.ModelViewSet):
    """api views for Company"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_fields = ['id', 'code']
    search_fields = ['name', 'code']
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('id', 'code')
    ordering = ('id',)
