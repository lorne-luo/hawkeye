from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.utils.html import format_html, format_html_join
from taggit.models import Tag
from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdmin
from core.wagtail.permission import OwnerPermissionHelper
from .models import ArticlePage, Category


class ArticlePageAdmin(ModelAdmin):
    list_per_page = 15
    allowed_lookup = []
    model = ArticlePage
    menu_label = 'Article page'  # d itch this to use verbose_name_plural from model
    menu_icon = 'form'
    menu_order = 230
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'slug', 'owner', 'live', 'last_published_at')
    list_filter = ['sectors']
    search_fields = ['title', 'slug']
    permission_helper_class = OwnerPermissionHelper

    def get_queryset(self, request):
        qs = super(ArticlePageAdmin, self).get_queryset(request)
        if request.user.is_admin():
            if 'owner' not in self.list_filter:
                self.list_filter += ['owner']
            return qs
        else:
            return qs.filter(owner=request.user)


modeladmin_register(ArticlePageAdmin)


class CategoryPageAdmin(ModelAdmin):
    list_per_page = 15
    allowed_lookup = []
    model = Category
    menu_label = 'Category'  # d itch this to use verbose_name_plural from model
    menu_icon = 'list-ul'
    menu_order = 200
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'slug', 'show_in_menus')
    list_filter = ('show_in_menus',)
    search_fields = ('name', 'slug')


modeladmin_register(CategoryPageAdmin)


class TagAdmin(ModelAdmin):
    list_per_page = 15
    allowed_lookup = []
    model = Tag
    menu_label = 'Tags'  # d itch this to use verbose_name_plural from model
    menu_icon = 'tag'
    menu_order = 220
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'slug')
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')


modeladmin_register(TagAdmin)
