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
    "apps.accounts",
    "apps.wallet",
    "apps.payments",
    "apps.whatsapp",
    "apps.documents",
    "apps.audio",
    "apps.assistant",
    "apps.notifications",
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_ALWAYS_EAGER = False

DEFAULT_FREE_CREDITS = env.int("DEFAULT_FREE_CREDITS", default=3)

DOCUMENT_MAX_UPLOAD_MB = env.int("DOCUMENT_MAX_UPLOAD_MB", default=10)
ALLOWED_DOCUMENT_EXTENSIONS = [e.strip() for e in env.str("ALLOWED_DOCUMENT_EXTENSIONS", default="pdf,jpg,jpeg,png,webp").split(",") if e.strip()]

LOGIN_URL = "login"
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
OPENAI_API_KEY = env.str("OPENAI_API_KEY", default="")


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
