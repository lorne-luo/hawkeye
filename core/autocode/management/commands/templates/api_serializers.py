SERIALIZERS_HEADER = '''# coding=utf-8
from rest_framework import serializers
from ..models import <% ALL_MODELS %>

'''

SERIALIZERS_BODY = '''
class <% MODEL_NAME %>Serializer(serializers.BaseSerializer):
    """ Serializer for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = ['id', 'edit_url', 'detail_url'] + \\
                 <% fields %>
        read_only_fields = ['id']

'''
