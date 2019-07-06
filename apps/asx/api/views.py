import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from ..models import Company
from . import serializers

log = logging.getLogger(__name__)


class CompanyViewSet(viewsets.ViewSet):
    """api views for Company"""
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer
    filter_fields = ['pk', 'code']
    search_fields = ['name', 'code']
    filter_backends = (DjangoFilterBackend,)
