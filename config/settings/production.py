from .base import *  # noqa
from .base import env

DEBUG = env.bool("DJANGO_DEBUG", False)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


