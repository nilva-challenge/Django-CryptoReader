from config.settings.base import *


INSTALLED_APPS += [
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "cryptoreader.accounts",
    "cryptoreader.api",
]

# encrypt key for encrypting and decrypting data
# generated with cryptography.fernet.Fernet.generate_key()
ENCRYPT_KEY = b"f7DwTK5K6EwmA30THAxnXgBKy_v969ItANlVGhi4C-0="

ROOT_URLCONF = "config.urls.dev"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
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
