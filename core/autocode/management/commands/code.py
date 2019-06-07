import os
import sys
import types
import inspect
from django.db import models
from django.core import management
from django.utils.module_loading import import_string
from django.core.management.base import BaseCommand

from .templates.urls import URLS_HEADER, URLS_BODY, URLS_FOOTER
from .templates.views import VIEWS_HEADER, VIEWS_BODY
from .templates.forms import FORMS_HEADER, FORMS_BODY
from .templates.api_serializers import SERIALIZERS_HEADER, SERIALIZERS_BODY
from .templates.api_urls import API_URLS_HEADER, API_URLS_BODY, API_URLS_FOOTER
from .templates.api_views import API_VIEWS_HEADER, API_VIEWS_BODY


class Command(BaseCommand):
    help = ''' Create code

    Usage: ./manage.py code [--overwrite] <module_name>

    Example:

        ./manage.py code apps.product

        ./manage.py code -o apps.product.models.Product

        ./manage.py code apps/product/

    '''

    args = "app folder path or models.py path"
    module = None
    model_list = []
    is_overwrite = False

    def add_arguments(self, parser):
        parser.add_argument("--overwrite", "-o", action="store_true", dest="is_overwrite", default=False,
                            help="Overwrite all files.")
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        params = options.get("path")
        if len(params) < 1:
            self.stderr.write(self.help)
            return
        self.is_overwrite = options.get("is_overwrite")

        path = params[0]
        self.module_str = path.replace('.py', '').replace('/', '.').strip('.')
        self.module_str = self.module_str if '.models' in self.module_str else self.module_str + '.models'

        try:
            self.scan_models(self.module_str)
        except AttributeError as e:
            self.stdout.write("Error: %s" % e)
            return

        self.stdout.write('\n############################## info ##############################')
        self.stdout.write(self.module_str)
        self.stdout.write(self.app_str)
        self.stdout.write(str(self.module))
        self.stdout.write(self.app_name)
        # self.stdout.write('%s.%s' % (self.model.__module__, self.model.__name__))
        self.stdout.write(self.module_file)
        self.stdout.write(self.module_folder)
        self.stdout.write(self.js_folder)
        self.stdout.write(self.templates_folder)
        self.stdout.write(self.urls_file)

        self.stdout.write('\n############################## models ##############################')
        for md in self.model_list:
            self.stdout.write(md.__module__ + '.' + md.__name__)

        self.run()

    def scan_models(self, name):
        mod = import_string(name)
        if isinstance(mod, types.ModuleType):
            self.module = mod
            self.import_model(mod)
        elif issubclass(mod, models.Model):
            self.model_list.append(mod)
            self.module = sys.modules[mod.__module__]
        else:
            raise AttributeError('%s is not a model or module' % name)

        if not len(self.model_list):
            raise AttributeError('Found no model in %s' % name)

        self.app_name = self.model_list[0]._meta.app_label
        self.app_str = self.module_str[:self.module_str.find('.models')]
        self.module_file = self.module.__file__[:-1]
        self.module_folder = os.path.dirname(self.module.__file__)
        self.serializers_file = os.path.join(self.module_folder, 'api', 'serializers.py')
        self.api_urls_file = os.path.join(self.module_folder, 'api', 'urls.py')
        self.api_views_file = os.path.join(self.module_folder, 'api', 'views.py')
        self.views_file = os.path.join(self.module_folder, 'views.py')
        self.urls_file = os.path.join(self.module_folder, 'urls.py')
        self.forms_file = os.path.join(self.module_folder, 'forms.py')
        self.js_folder = os.path.join(self.module_folder, 'static', 'js', self.app_name, '%s_list.js')
        self.templates_folder = os.path.join(self.module_folder, 'templates', self.app_name, '%s_list.html')
        self.all_models_str = ', '.join([md.__name__ for md in self.model_list])

    def get_fields_and_titles(self, model):
        titles = []
        fields = []

        # normal fields + many-to-many fields
        meta_fields = model._meta.fields + model._meta.many_to_many
        for mf in meta_fields:
            if mf.name == 'id':
                continue
            elif isinstance(mf, models.fields.DateTimeField):
                if mf.auto_now_add or mf.auto_now:
                    continue
            fields.append(mf.name)
            title = mf.verbose_name
            if title and title[0].islower():
                title = title.title()
            titles.append(title)
        return fields, titles

    def get_chinese_titles(self, titles):
        result = ''
        for t in titles:
            if u'\u4e00' <= t <= u'\u9fff':
                item = "u'%s'" % t.encode('gb2312')
            else:
                item = "'%s'" % t.encode('gb2312')

            if result:
                result = ', '.join([result, item])
            else:
                result = item
        result = '[%s]' % result
        return result.decode('gbk')

    def import_model(self, mod):
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if obj.__module__.startswith(self.module_str):
                if issubclass(obj, models.Model) and not obj._meta.abstract:
                    self.model_list.append(obj)

    def make_folder(self, path):
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

    def create_file(self, file_path, content):
        if os.path.isfile(file_path) and not self.is_overwrite:
            file_path += '.code'

        base_dir = os.path.dirname(file_path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        with open(file_path, 'w+') as f:
            f.write(content)

    def append_file(self, file_path, content):
        with open(file_path, 'w+') as f:
            f.write(content)

    # ============= generate content ==============
    def render_content(self, content, model=None):
        content = content.replace('<% module_str %>', self.module_str). \
            replace('<% app_name %>', self.app_name). \
            replace('<% App_name %>', self.app_name.title()). \
            replace('<% ALL_MODELS %>', self.all_models_str)
        if model:
            fields, titles = self.get_fields_and_titles(model)
            content = content.replace('<% MODEL_NAME %>', model.__name__). \
                replace('<% model_name %>', model.__name__.lower()). \
                replace('<% fields %>', str(fields)). \
                replace('<% titles %>', self.get_chinese_titles(titles))
        return content

    def get_urls_content(self):
        content = URLS_HEADER
        for model in self.model_list:
            content += self.render_content(URLS_BODY, model)
        content += URLS_FOOTER
        self.stdout.write(content)
        return content

    def get_views_content(self):
        content = self.render_content(VIEWS_HEADER)
        for model in self.model_list:
            content += self.render_content(VIEWS_BODY, model)
        self.stdout.write(content)
        return content

    def get_forms_content(self):
        content = self.render_content(FORMS_HEADER)
        for model in self.model_list:
            content += self.render_content(FORMS_BODY, model)
        self.stdout.write(content)
        return content

    def get_api_serializers_content(self):
        content = self.render_content(SERIALIZERS_HEADER)
        for model in self.model_list:
            content += self.render_content(SERIALIZERS_BODY, model)
        self.stdout.write(content)
        return content

    def get_api_urls_content(self):
        content = self.render_content(API_URLS_HEADER)
        for model in self.model_list:
            content += self.render_content(API_URLS_BODY, model)
        content += API_URLS_FOOTER
        self.stdout.write(content)
        return content

    def get_api_views_content(self):
        content = self.render_content(API_VIEWS_HEADER)
        for model in self.model_list:
            content += self.render_content(API_VIEWS_BODY, model)
        self.stdout.write(content)
        return content

    def get_reverse_js(self):
        management.call_command('js_reverse')
        management.call_command('collectstatic_js_reverse')

    def run(self):
        self.stdout.write('\n######### %s #########' % self.urls_file)
        self.create_file(self.urls_file, self.get_urls_content())
        self.stdout.write('\n######### %s #########' % self.forms_file)
        self.create_file(self.forms_file, self.get_forms_content())
        self.stdout.write('\n######### %s #########' % self.views_file)
        self.create_file(self.views_file, self.get_views_content())

        # api
        self.create_file(os.path.join(self.module_folder, 'api', '__init__.py'), '')
        self.stdout.write('\n######### %s #########' % self.serializers_file)
        self.create_file(self.serializers_file, self.get_api_serializers_content())
        self.stdout.write('\n######### %s #########' % self.api_urls_file)
        self.create_file(self.api_urls_file, self.get_api_urls_content())
        self.stdout.write('\n######### %s #########' % self.api_views_file)
        self.create_file(self.api_views_file, self.get_api_views_content())

        self.get_reverse_js()
        self.stdout.write('')
        self.stdout.write('')
        self.stderr.write('# Still need to add some codes manually:')
        self.stdout.write('')
        self.stderr.write(" * Add 'url(r'^', include('%s.urls', namespace='%s')),' into super urls.py" % (
            self.app_str, self.app_name))
        self.stdout.write('')
        self.stderr.write(" * Add 'url(r'^%s/', include('%s.api.urls')),' into super urls.py" % (
            self.app_name, self.app_str))
        self.stdout.write('')
        self.stderr.write(
            " * Add '{% include \"" + self.app_name + "/_menu.html\" %}' into core/adminlte/templates/adminlte/includes/menu.html")
        self.stdout.write('')
