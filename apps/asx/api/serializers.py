from rest_framework import serializers
from core.api.serializers import BaseSerializer
from ..models import Company


# Serializer for address
class CompanySerializer(BaseSerializer):
    class Meta:
        model = Company
        fields = ['pk', 'code', 'name'] + \
                 ['last_price_date', 'last_price', 'asx_200', 'daily_volume']
        read_only_fields = ['pk']
