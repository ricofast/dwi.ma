from .base import *  # noqa
from .base import env

DEBUG = env.bool("DJANGO_DEBUG", False)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


OPENAI_KEY = env.str("DJANGO_OPENAI")
GEMINIAPI_KEY = env.str("DJANGO_GEMINIAPI")
ANTHROPIC_API_KEY = env.str("DJANGO_ANTHROPICAPI")