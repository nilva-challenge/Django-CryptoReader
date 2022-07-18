from config.settings.base import *


INSTALLED_APPS += [
    "rest_framework",
    "cryptoreader.accounts.apps.AccountsConfig",
    "cryptoreader.api.apps.ApiConfig",
]

ROOT_URLCONF = "config.urls.dev"
