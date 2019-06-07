from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from core.constants import AU_CITY_CHOICES, AU_STATE_CHOICES
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


@register_setting(icon='form')
class ContactUs(BaseSetting):
    name = models.CharField(_('name'), max_length=255, blank=True, help_text='contactor name')
    address1 = models.CharField(_('address1'), max_length=255, blank=True, help_text='address1')
    address2 = models.CharField(_('address2'), max_length=255, blank=True, help_text='address2')
    city = models.CharField(_('city'), choices=AU_CITY_CHOICES, max_length=255, blank=True, help_text='city')
    state = models.CharField(_('state'), choices=AU_STATE_CHOICES, max_length=255, blank=True, help_text='state')
    postcode = models.CharField(_('postcode'), max_length=32, blank=True, help_text='postcode')
    phone = models.CharField(_('phone'), max_length=32, blank=True, help_text='phone')
    email = models.EmailField(_('email'), max_length=255, blank=True, help_text='email')

    class Meta:
        verbose_name = 'contact us'


@register_snippet
class Link(models.Model):
    name = models.CharField(_('name'), max_length=255, blank=False, help_text='Partner name')
    link = models.URLField(_('link'), blank=True, help_text='Partner link')
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    class_name = models.CharField(_('styling class name'), max_length=64, blank=True, help_text='styling class name')

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
        FieldPanel('link'),
        FieldPanel('class_name'),
    ]

    def __str__(self):
        return self.name
