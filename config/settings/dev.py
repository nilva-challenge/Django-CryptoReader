from config.settings.base import *

import environ
import os

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR / "config/django.dev.env"))

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = str(env("ALLOWED_HOSTS")).strip('"').strip().split()
APPEND_SLASH = env("APPEND_SLASH")

# encrypt key for encrypting and decrypting data
# generated with cryptography.fernet.Fernet.generate_key()
ENCRYPT_KEY = env("ENCRYPT_KEY")
# ENCRYPT_KEY = b"f7DwTK5K6EwmA30THAxnXgBKy_v969ItANlVGhi4C-0="

INSTALLED_APPS += [
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "cryptoreader.accounts",
    "cryptoreader.api",
]


ROOT_URLCONF = "config.urls.dev"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": "5432",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "django_",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Crypto Rader ",
    "DESCRIPTION": "Crypot Reader Challnge From Nilva Co",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "statics"
STATICFILES_DIRS = []
