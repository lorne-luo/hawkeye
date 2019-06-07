FORMS_HEADER = '''# coding=utf-8
from django import forms
from .models import <% ALL_MODELS %>

'''
FORMS_BODY = '''
class <% MODEL_NAME %>AddForm(forms.ModelForm):
    """ Add form for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>ViewForm(forms.ModelForm):
    """ Detail form for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>EditForm(forms.ModelForm):
    """ Update form for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>

'''
