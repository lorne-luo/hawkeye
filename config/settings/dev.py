from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='27ccw6=vv%*m=0+u)duq4rda3tbyd6!nzw$f(l7v(!in1hxm129)+du')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '.luotao.net', ])

INSTALLED_APPS += ['django_extensions']

try:
    from .local import *
except ImportError:
    pass

try:
    # declare DEV_APPS in local.py if you have extra apps personally
    INSTALLED_APPS += DEV_APPS
except NameError:
    pass
