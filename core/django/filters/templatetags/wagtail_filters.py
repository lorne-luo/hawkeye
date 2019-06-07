from django import template
from wagtail.images.models import Image

register = template.Library()


@register.assignment_tag
def gellary(collection):
    return Image.objects.filter(collection=collection)
