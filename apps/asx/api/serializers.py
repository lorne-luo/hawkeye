from rest_framework.serializers import ModelSerializer

from ..models import Company


# Serializer for address
class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['pk', 'code', 'name', 'last_price_date', 'last_price', 'asx_200', 'daily_volume', 'last_csv_path',
                  'this_week_csv']
        read_only_fields = ['pk']
