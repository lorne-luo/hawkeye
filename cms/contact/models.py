from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, MultiFieldPanel
from core.wagtail.stream_block import SUPER_STREAM_BLOCKS
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailstreamforms.blocks import WagtailFormBlock



class ContactPage(Page):
    banner_text = models.CharField(max_length=250, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+',

    )

    contact_description = RichTextField(blank=True)
    address = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)

    content = StreamField([('form', WagtailFormBlock())])

    content_panels = Page.content_panels + [

        MultiFieldPanel(
            [
                FieldPanel('banner_text', classname="full"),
                ImageChooserPanel('banner_image'),
            ],
            heading="Page Banner",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('contact_description', classname="full"),
                FieldPanel('address'),
                FieldPanel('phone'),
                FieldPanel('email'),
            ],
            heading="Contact Details",
            classname="collapsible"
        ),
        StreamFieldPanel('content'),
    ]

