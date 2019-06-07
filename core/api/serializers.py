from django.core.urlresolvers import reverse
from rest_framework import serializers


class URLModelSerializerMixin(object):
    """ output edit_url and view_url for model obj, use with DRF ModelSerializer """
    edit_url = serializers.SerializerMethodField()
    view_url = serializers.SerializerMethodField()

    def get_view_url(self, obj):
        app_label = self.Meta.model._meta.app_label
        model_name = self.Meta.model._meta.model_name

        if self.has_perm('view'):
            url_tag = '%s:%s_view' % (app_label, model_name)
            return reverse(url_tag, args=[obj.id])
        return None

    def get_edit_url(self, obj):
        app_label = self.Meta.model._meta.app_label
        model_name = self.Meta.model._meta.model_name

        if self.has_perm('change'):
            url_tag = '%s:%s_edit' % (app_label, model_name)
            return reverse(url_tag, args=[obj.id])
        return None

    def has_perm(self, perm):
        user = self.context['request'].user
        app_label = self.Meta.model._meta.app_label
        model_name = self.Meta.model._meta.model_name
        perm_str = '%s.%s_%s' % (app_label, perm, model_name)
        return user.has_perm(perm_str)
