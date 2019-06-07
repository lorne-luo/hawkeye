from __future__ import absolute_import, unicode_literals

import json
from collections import OrderedDict
from django.db.models import Q

from django.utils import timezone
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.contrib.table_block.blocks import TableBlock
from django.template.defaultfilters import slugify

from cms.articles.forms import ArticleWagtailAdminModelForm
from core.wagtail.page import StreamPage
from core.wagtail.stream_block import CollectionChooserBlock, SUPER_STREAM_BLOCKS


class Category(ClusterableModel):
    name = models.CharField(
        max_length=80, unique=True, verbose_name=_('Category'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.'),
        on_delete=models.SET_NULL)
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            count = Category.objects.filter(slug=slug).count()
            if count > 0:
                slug = '{}-{}'.format(slug, count)
            self.slug = slug
        return super(Category, self).save(*args, **kwargs)


class ArticlePageTag(TaggedItemBase):
    """
    many-to-many relationship between the ArticlePage object and tags.
    """
    content_object = ParentalKey('ArticlePage', related_name='article_tags', on_delete=models.CASCADE)


class ArticlePage(StreamPage):
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    view_count = models.PositiveIntegerField('view count', blank=False, default=0)
    short_description = models.TextField(_('short description'), max_length=512, blank=True)
    category = ParentalKey('articles.Category', related_name='category_articles', blank=True, null=True,
                           on_delete=models.SET_NULL)

    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    parent_page_types = ['home.Homepage']
    base_form_class = ArticleWagtailAdminModelForm

    search_fields = Page.search_fields + [
        index.SearchField('content', partial_match=True),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('main_image'),
        FieldPanel('short_description'),
        StreamFieldPanel('content'),
    ]
    category_content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('category', widget=forms.Select),
            ],
            heading="Categories",
            classname="collapsible"
        ),
        InlinePanel('article_tags', label="Tags", classname="collapsible"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('owner'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(category_content_panels, heading='Categories'),
        ObjectList(Page.promote_panels, heading='SEO settings'),
        ObjectList(settings_panels, heading='Article settings', classname="settings"),
    ])

    def update_view_count(self):
        # total view counter
        self.view_count += 1

        self.save(update_fields=['view_count'])

    def serve(self, request, *args, **kwargs):
        self.update_view_count()
        return super(ArticlePage, self).serve(request, *args, **kwargs)
