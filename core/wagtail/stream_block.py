import json
import os

from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.widgets import AdminChooser
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.core.blocks import ChooserBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Collection
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.shortcuts import get_rendition_or_not_found
from wagtailstreamforms.blocks import WagtailFormBlock


class CustomStructBlock(blocks.StructBlock):
    """base custom block, add block_id,block_class,block_template for each"""

    template_path = 'includes/streamblocks'  # all templates for steam block under this path

    def get_template_path(self, filename):
        filename = os.path.basename(filename)
        return os.path.join(self.template_path, filename), filename

    def get_templates(self, kwargs):
        templates = kwargs.pop('templates', ())
        if isinstance(templates, str):
            filename = os.path.basename(templates)
            return [self.get_template_path(filename)]
        elif type(templates) in [list, tuple]:
            if not len(templates):
                raise Exception('Should provide at latest one templates')

            if isinstance(templates[0], str):
                return [self.get_template_path(t) for t in templates]
            return templates
        raise Exception('templates should be tuple, list or str.')

    def __init__(self, local_blocks=None, **kwargs):
        skip = kwargs.pop('skip', False)
        templates = self.get_templates(kwargs)
        if not skip:
            local_blocks = [('block_id', blocks.CharBlock(required=False)),
                            ('block_class', blocks.CharBlock(required=False)),
                            ('block_template', blocks.ChoiceBlock(choices=templates, default=templates[0][0],
                                                                  required=False))] + local_blocks

        super(CustomStructBlock, self).__init__(local_blocks, **kwargs)


new_table_options = {
    'colHeaders': False,
}
SUPER_STREAM_BLOCKS = [
    ('heading', blocks.StructBlock([
        ('heading_type', blocks.ChoiceBlock(choices=[
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
            ('h5', 'H5'),
            ('h6', 'H6'),
        ])),
        ('heading_text', blocks.CharBlock(required=True)),
    ], icon='title')),
    ('paragraph', blocks.RichTextBlock()),
    ('table', TableBlock(table_options=new_table_options)),
    ('embed', EmbedBlock()),
    ('button', blocks.StructBlock([
        ('button_name', blocks.CharBlock(required=True)),
        ('button_url', blocks.CharBlock(required=True)),
        ('button_color', blocks.ChoiceBlock(choices=[
            ('btn--green', 'Green'),
            ('btn--olive', 'Olive'),
            ('btn--dark-green', 'Dark green'),
            ('btn--lime', 'Lime'),
            ('btn--light-green', 'Light green'),
            ('btn--grey', 'Grey'),
        ], blank=False)),
    ], icon='form')),
    ('html', blocks.RawHTMLBlock()),
    ('image', blocks.StructBlock([
        ('image', ImageChooserBlock()),
        ('image_caption', blocks.CharBlock(required=False)),
        ('image_position', blocks.ChoiceBlock(choices=[
            ('center', 'Center'),
            ('left', 'Left'),
            ('right', 'Right'),
            ('full-width', 'Full width')
        ])),
    ], icon='image')),
    ('accordion', blocks.StructBlock([
        ('accordion_heading', blocks.CharBlock(required=True)),
        ('accordion_content', blocks.RichTextBlock()),
    ], icon='arrows-up-down')),
    ('quote', blocks.StructBlock([
        ('quote', blocks.RichTextBlock(required=False)),
    ], icon='openquote')),
    ('banner', CustomStructBlock([
        ('banner_heading', blocks.CharBlock(required=False)),
        ('banner_text', blocks.RichTextBlock(required=False)),
        ('banner_button_name', blocks.CharBlock(required=False)),
        ('banner_button_url', blocks.CharBlock(required=False)),
        ('banner_image', ImageChooserBlock(required=True)),
        ('banner_image_position', blocks.ChoiceBlock(choices=[
            ('bannerimage-bg', 'Image as background'),
            ('bannerimage-section', 'Image in a section')
        ])),
    ], icon='placeholder',
        templates=['streamblock_hero_banner.html']
    )),
    ('info_block', CustomStructBlock([
        ('info_block_heading', blocks.CharBlock(required=False)),
        ('info_block_text', blocks.RichTextBlock(required=False)),
        ('info_block_button_name', blocks.CharBlock(required=False)),
        ('info_block_button_url', blocks.CharBlock(required=False)),
        ('info_block_image', ImageChooserBlock(required=False)),
        ('info_block_image_position', blocks.ChoiceBlock(choices=[
            ('left', 'Image on the left'),
            ('right', 'Image on the right')
        ])),
        ('info_block_icon_section', blocks.ListBlock(blocks.StructBlock([
            ('info_block_icon_text', blocks.CharBlock(required=False)),
            ('info_block_icon_image', ImageChooserBlock(required=False)),
        ]))),
    ], icon='plus',
        templates=['streamblock_info_block.html']
    )),
    ('multi_blocks', CustomStructBlock([
        ('block_heading', blocks.CharBlock(required=False)),
        ('items_section', blocks.ListBlock(blocks.StructBlock([
            ('heading', blocks.CharBlock(required=False)),
            ('text', blocks.RichTextBlock(required=False)),
            ('image', ImageChooserBlock(required=False)),
            ('image_link', blocks.CharBlock(required=False)),
        ]))),
        ('block_url_text', blocks.CharBlock(required=False)),
        ('block_url', blocks.CharBlock(required=False)),
    ], icon='grip',
        templates=['streamblock_multi_blocks.html']
    )),
    ('info_banner', CustomStructBlock([
        ('info_banner_heading', blocks.CharBlock(required=False)),
        ('info_banner_text', blocks.RichTextBlock(required=False)),
        ('info_banner_button_name', blocks.CharBlock(required=False)),
        ('info_banner_button_url', blocks.CharBlock(required=False)),
    ], icon='plus-inverse',
        templates=['streamblock_info_banner.html'])),
    ('progress_steps', CustomStructBlock([
        ('progress_steps_image', ImageChooserBlock(required=False)),
        ('progress_steps_blocks', blocks.ListBlock(blocks.StructBlock([
            ('progress_steps_block_heading', blocks.CharBlock(required=False, label="Step Heading")),
            ('progress_steps_block_text', blocks.RichTextBlock(required=False, label="Step Text")),
            ('progress_steps_block_image', ImageChooserBlock(required=False, label="Step Image")),
        ]))),
    ], icon='order',
        templates=['streamblock_progress_steps.html'])),
    ('checklist', CustomStructBlock([
        ('checklist_heading', blocks.CharBlock(required=False)),
        ('checklist_image', ImageChooserBlock(required=False)),
        ('checklist_text', blocks.RichTextBlock(required=False)),
        ('checklist_lists', blocks.ListBlock(blocks.StructBlock([
            ('checklist_list', blocks.CharBlock(required=False, label="Checklist")),
        ]))),
        ('checklist_button_name', blocks.CharBlock(required=False)),
        ('checklist_button_url', blocks.CharBlock(required=False)),
        ('checklist_style', blocks.ChoiceBlock(choices=[
            ('full-checklist', 'Full checklist without image'),
            ('image-checklist', 'Image and checklist side by side'),
        ], blank=False)),
    ], icon='list-ul',
        templates=['streamblock_checklist.html'])),
    ('testimonial', CustomStructBlock([
        ('testimonial_image', ImageChooserBlock(required=False)),
        ('testimonial_text', blocks.RichTextBlock(required=False)),
        ('testimonial_name', blocks.CharBlock(required=False, label="Name")),
        ('testimonial_position', blocks.CharBlock(required=False, label="Position")),
    ], icon='user',
        templates=['streamblock_testimonial.html'])),
    ('multi_testimonials', CustomStructBlock([
        ('title', blocks.CharBlock(required=False)),
        ('testimonials', blocks.ListBlock(blocks.StructBlock([
            ('testimonial_image', ImageChooserBlock(required=False)),
            ('testimonial_text', blocks.RichTextBlock(required=False)),
            ('testimonial_name', blocks.CharBlock(required=False, label="Name")),
            ('testimonial_position', blocks.CharBlock(required=False, label="Position")),
        ]))),
    ], icon='user',
        templates=['streamblock_multi_testimonial.html'])),
    ('form', WagtailFormBlock()),
]



class CollectionChooser(AdminChooser):
    add_one_text = _('Add a collection')
    choose_one_text = _('Choose an collection')
    link_to_chosen_text = _('Edit this collection')

    def __init__(self, **kwargs):
        super(CollectionChooser, self).__init__(**kwargs)
        self.image_model = Collection

    def render_html(self, name, value, attrs):
        collections = Collection.objects.all()
        original_field_html = super(CollectionChooser, self).render_html(name, value, attrs)

        collection_items = []
        for collection in collections:
            if value == collection.id:
                collection_items.append(
                    '<option selected="true" value="%s">%s</option>' % (collection.id, collection.name))
            else:
                collection_items.append('<option value="%s">%s</option>' % (collection.id, collection.name))

        collection_selector = '''
        <select name="%s" id="%s_select" placeholder="%s">
            <option value="" selected="">---------</option>
                %s
        </select>
        ''' % (
            attrs['id'],
            attrs['id'],
            attrs['placeholder'],
            '\n'.join(collection_items)
        )

        return render_to_string("articles/widgets/collection_chooser.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'collection_selector': collection_selector,
        })

    def render_js_init(self, id_, name, value):
        return "createCollectionChooser({0});".format(json.dumps(id_))


class CollectionChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        return Collection

    @cached_property
    def widget(self):
        return CollectionChooser

    def render_basic(self, value, context=None):
        if value:
            return get_rendition_or_not_found(value, 'original').img_tag()
        else:
            return ''

    class Meta:
        icon = "folder-open-1"
