from __future__ import absolute_import, unicode_literals

from .base import *

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['.luotao.net', ])

try:
    from .local import *
except ImportError:
    pass
