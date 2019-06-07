from __future__ import absolute_import, unicode_literals

from .base import *

SECRET_KEY = env('SECRET_KEY')

try:
    from .local import *
except ImportError:
    pass
