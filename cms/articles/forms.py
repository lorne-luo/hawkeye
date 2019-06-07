from wagtail.admin.forms import WagtailAdminPageForm


class ArticleWagtailAdminModelForm(WagtailAdminPageForm):
    class Media:
        js = (
            'js/collection-chooser.js',
            'vendor/jquery_chosen/chosen.jquery.min.js'
        )
        css = {
            'all': ('vendor/jquery_chosen/chosen.min.css',)
        }
