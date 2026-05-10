from .base import *  # noqa
from .base import env

DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
print(env.str("DATABASE_NAME"))
print(env.str("DATABASE_USER_SNAME"))
print(env.str("DATABASE_PASS_WORD"))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str("DATABASE_NAME"),
        'USER': env.str("DATABASE_USER_SNAME"),
        'PASSWORD': env.str("DATABASE_PASS_WORD"),
        'HOST': env.str("DATABASE_HOST"),
        'PORT': '5432',
    }
}