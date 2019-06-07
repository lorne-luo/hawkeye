from rest_framework import serializers

from .models import ArticlePage


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    sectors = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    media_type_display = serializers.SerializerMethodField()
    thumbnail_image_url = serializers.SerializerMethodField()
    last_published_at = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_media_type_display(self, obj):
        return obj.media_type.name if obj.media_type else None

    def get_thumbnail_image_url(self, obj):
        return obj.thumbnail_image.file.url if obj.thumbnail_image else None

    def get_last_published_at(self, obj):
        if obj.last_published_at:
            return '%s %s' % (obj.last_published_at.day, obj.last_published_at.strftime("%b %Y"))
        else:
            return None

    def get_url(self, obj):
        return obj.get_url()

    class Meta:
        model = ArticlePage
        fields = (
            'id', 'thumbnail_image', 'promotion_image', 'media_type_display', 'thumbnail_image_url', 'view_count',
            'tags', 'short_description', 'media_type', 'title', 'slug', 'owner', 'last_published_at', 'url')
