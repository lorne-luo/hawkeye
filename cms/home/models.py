from __future__ import absolute_import, unicode_literals

from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField

from wagtail.core.models import Page

from core.wagtail.page import StreamPage
from core.wagtail.stream_block import SUPER_STREAM_BLOCKS


class HomePage(StreamPage):
    content = StreamField(SUPER_STREAM_BLOCKS, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]

