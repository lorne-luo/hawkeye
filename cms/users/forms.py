from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    pass


class CustomUserEditForm(UserEditForm):
    pass
