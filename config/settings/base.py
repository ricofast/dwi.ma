import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="unsafe-default-key")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = [host.strip() for host in env("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",

    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    # "allauth.socialaccount.providers.apple",
    # "allauth.socialaccount.providers.facebook",
    # "allauth.socialaccount.providers.google",
    # "allauth.socialaccount.providers.twitter",
    # "allauth.socialaccount.providers.instagram",
    # "allauth.socialaccount.providers.telegram",
    "crispy_forms",
    "crispy_bootstrap5",
    "apps.accounts",
    "apps.wallet",
    "apps.payments",
    "apps.whatsapp",
    "apps.documents",
    "apps.audio",
    "apps.assistant",
    "apps.notifications",
    "apps.core",
    "django_celery_results",
    "django_celery_beat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "allauth.account.middleware.AccountMiddleware",
]
ADMIN_URL = env.str("DJANGO_ADMIN_URL")
ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.credit_balance",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

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

# DATABASES = {
#     "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
# }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    # "allauth.account.auth_backends.AuthenticationBackend",
)

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# ACCOUNT_EMAIL_VERIFICATION = "optional"

SITE_ID = 1

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_BROKER_URL = REDIS_URL
CCELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
# Add a one-minute timeout to all Celery tasks.
# CELERYD_TASK_SOFT_TIME_LIMIT = 55
CELERY_TASK_ALWAYS_EAGER = False

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "Africa/Casablanca"

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 10 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60

CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True



DEFAULT_FREE_CREDITS = env.int("DEFAULT_FREE_CREDITS", default=3)

DOCUMENT_MAX_UPLOAD_MB = env.int("DOCUMENT_MAX_UPLOAD_MB", default=10)
ALLOWED_DOCUMENT_EXTENSIONS = [e.strip() for e in env.str("ALLOWED_DOCUMENT_EXTENSIONS", default="pdf,jpg,jpeg,png,webp").split(",") if e.strip()]

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "landing"

TEXT_EXPLANATION_MAX_CHARS = int(os.getenv("TEXT_EXPLANATION_MAX_CHARS", "12000"))

WHATSAPP_PROVIDER = env.str("WHATSAPP_PROVIDER", default="mock")
WHATSAPP_VERIFY_TOKEN = env.str("WHATSAPP_VERIFY_TOKEN", default="")
WHATSAPP_ACCESS_TOKEN = env.str("WHATSAPP_ACCESS_TOKEN", default="")
WHATSAPP_PHONE_NUMBER_ID = env.str("WHATSAPP_PHONE_NUMBER_ID", default="")
WHATSAPP_BUSINESS_ACCOUNT_ID = env.str("WHATSAPP_BUSINESS_ACCOUNT_ID", default="")
WHATSAPP_APP_SECRET = env.str("WHATSAPP_APP_SECRET", default="")
WHATSAPP_API_VERSION = env.str("WHATSAPP_API_VERSION", default="v23.0")
WHATSAPP_DEFAULT_COUNTRY_CODE = env.str("WHATSAPP_DEFAULT_COUNTRY_CODE", default="212")
SITE_URL = env.str("SITE_URL", default="http://localhost:8000")

AUDIO_MAX_UPLOAD_MB = env.int("AUDIO_MAX_UPLOAD_MB", default=15)
ALLOWED_AUDIO_EXTENSIONS = [e.strip() for e in env.str("ALLOWED_AUDIO_EXTENSIONS", default="mp3,mp4,m4a,wav,webm,ogg,opus").split(",") if e.strip()]
TRANSCRIPTION_PROVIDER = env.str("TRANSCRIPTION_PROVIDER", default="mock")
TRANSCRIPTION_MODEL = env.str("TRANSCRIPTION_MODEL", default="mock-transcribe")
OPENAI_API_KEY = env.str("DJANGO_OPENAI", default="")
ANTHROPIC_API_KEY = env.str("DJANGO_ANTHROPICAPI", default="")
GEMINI_API_KEY = env.str("DJANGO_GEMINIAPI", default="")
DEFAULT_LLM_PROVIDER = env.str("DEFAULT_LLM_PROVIDER", default="mock")
DEFAULT_LLM_MODEL = env.str("DEFAULT_LLM_MODEL", default="mock-1")


PAYMENT_PROVIDER = env.str("PAYMENT_PROVIDER", default="mock")
DIGITAL_VIRGO_API_BASE_URL = env.str("DIGITAL_VIRGO_API_BASE_URL", default="")
DIGITAL_VIRGO_MERCHANT_ID = env.str("DIGITAL_VIRGO_MERCHANT_ID", default="")
DIGITAL_VIRGO_API_KEY = env.str("DIGITAL_VIRGO_API_KEY", default="")
DIGITAL_VIRGO_WEBHOOK_SECRET = env.str("DIGITAL_VIRGO_WEBHOOK_SECRET", default="")
DIGITAL_VIRGO_CALLBACK_URL = env.str("DIGITAL_VIRGO_CALLBACK_URL", default="")
DIGITAL_VIRGO_RETURN_URL = env.str("DIGITAL_VIRGO_RETURN_URL", default="")
PAYMENT_TRANSACTION_EXPIRY_MINUTES = env.int("PAYMENT_TRANSACTION_EXPIRY_MINUTES", default=30)


DOCUMENT_ORIGINAL_RETENTION_DAYS = env.int("DOCUMENT_ORIGINAL_RETENTION_DAYS", default=30)
AUDIO_ORIGINAL_RETENTION_DAYS = env.int("AUDIO_ORIGINAL_RETENTION_DAYS", default=30)
DELETE_EXTRACTED_TEXT_ON_DOCUMENT_DELETE = env.bool("DELETE_EXTRACTED_TEXT_ON_DOCUMENT_DELETE", default=True)
DELETE_TRANSCRIPT_ON_AUDIO_DELETE = env.bool("DELETE_TRANSCRIPT_ON_AUDIO_DELETE", default=True)
DELETE_AI_RESULTS_ON_SOURCE_DELETE = env.bool("DELETE_AI_RESULTS_ON_SOURCE_DELETE", default=False)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}

# Required credits per operation
CREDITS_COST_DOCUMENT_EXPLANATION = 2
CREDITS_COST_MESSAGE_GENERATION = 1
CREDITS_COST_TEXT_EXPLANATION = 1
CREDITS_COST_VOICE_MESSAGE = 1

