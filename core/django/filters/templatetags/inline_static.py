import os
import base64
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from django import template
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import StaticNode
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='file_exists')
def file_exists(filepath):
    if default_storage.exists(filepath):
        return True
    return False


@register.filter(name='file_to_base64')
def file_to_base64(file_instance):
    """convert image field into base64
    Usage::
        <img src="data:image;base64,{{ object.image|file_to_base64 }}"/>
    """
    if file_instance and os.path.exists(file_instance.file.path):
        file_instance = file_instance.file.file
        encoded_string = base64.b64encode(file_instance.read())
        return encoded_string
    return ''


@register.simple_tag
def base64_static(path):
    """convert relative static url to base64
    Usage::
        <img src="data:image;base64,{% base64_static 'img/img.png' %}" />
    """
    file_path = staticfiles_storage.path(path)

    if os.path.exists(file_path):
        with open(file_path, "rb") as file_data:
            encoded_string = base64.b64encode(file_data.read())
            encoded_string = encoded_string.decode("utf-8")
            return encoded_string
    return ''


class InlineStaticNode(StaticNode):
    def render(self, context):
        path = self.path.resolve(context)
        file_path = staticfiles_storage.path(path)

        if os.path.exists(file_path):
            with open(file_path, "rb") as file_data:
                return file_data.read()
        return ''


@register.tag
def inline_static(parser, token):
    """read content from file and render it as inline, this one can't use `simple_tag` as it always apply autoescape
    Usage::
        <style type="text/css">
            {% inline_static 'css/style.css' %}
        </style>
    """
    return InlineStaticNode.handle_token(parser, token)


@register.filter(name='inline_img')
def inline_img(stream_block, site):
    """replace local image in <img> with base64 encoding
    Usage::
        {% autoescape off %}
            {{ content|inline_img:request.site }}
        {% endautoescape %}
    """
    html = str(stream_block.value)  # to html snippet
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        src = img['src']
        url = urlparse(src)
        try:
            if url.path.startswith(settings.MEDIA_URL) and (url.hostname == site.hostname or not url.hostname):
                # local pic link
                file_path = os.path.join(settings.MEDIA_ROOT, src[len(settings.MEDIA_URL):])
                if os.path.exists(file_path):
                    with open(file_path, "rb") as file_data:
                        encoded_string = base64.b64encode(file_data.read())
                        encoded_string = encoded_string.decode("utf-8")
                        img['src'] = 'data:image;base64,%s' % encoded_string
            else:
                # external pic
                r = requests.get(url, stream=True)
                r.raw.decode_content = True
                encoded_string = base64.b64encode(r.raw.data)
                encoded_string = encoded_string.decode("utf-8")
                img['src'] = 'data:image;base64,%s' % encoded_string
        except:
            # ignore
            img['src'] = ''

    result = mark_safe(str(soup))  # avoid escape for base64 encoding
    return result
