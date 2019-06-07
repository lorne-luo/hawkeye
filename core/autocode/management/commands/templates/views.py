VIEWS_HEADER = '''# coding=utf-8
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from .models import <% ALL_MODELS %>
from . import forms

'''

VIEWS_BODY = '''
class <% MODEL_NAME %>ListView(MultiplePermissionsRequiredMixin, ListView):
    """ List views for <% MODEL_NAME %> """
    model = <% MODEL_NAME %>
    template_name_suffix = '<% app_name %>/<% model_name %>_list.html'
    permissions = {
        "all": ("<% app_name %>.view_<% model_name %>",)
    }


class <% MODEL_NAME %>AddView(MultiplePermissionsRequiredMixin, CreateView):
    """ Add views for <% MODEL_NAME %> """
    model = <% MODEL_NAME %>
    form_class = forms.<% MODEL_NAME %>AddForm
    template_name = '<% app_name %>/<% model_name %>_form.html'
    permissions = {
        "all": ("<% app_name %>.add_<% model_name %>",)
    }


class <% MODEL_NAME %>UpdateView(MultiplePermissionsRequiredMixin, UpdateView):
    """ Update views for <% MODEL_NAME %> """
    model = <% MODEL_NAME %>
    form_class = forms.<% MODEL_NAME %>EditForm
    template_name = '<% app_name %>/<% model_name %>_form.html'
    permissions = {
        "all": ("<% app_name %>.change_<% model_name %>",)
    }


class <% MODEL_NAME %>DetailView(MultiplePermissionsRequiredMixin, UpdateView):
    """ Detail views for <% MODEL_NAME %> """
    model = <% MODEL_NAME %>
    form_class = forms.<% MODEL_NAME %>ViewForm
    template_name = '<% app_name %>/<% model_name %>_detail.html'
    permissions = {
        "all": ("<% app_name %>.view_<% model_name %>",)
    }

'''
