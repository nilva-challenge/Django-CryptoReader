from config.settings.base import *


INSTALLED_APPS += [
    "rest_framework",
    "cryptoreader.accounts.apps.AccountsConfig",
    "cryptoreader.api.apps.ApiConfig",
]

# encrypt key for encrypting and decrypting data
# generated with cryptography.fernet.Fernet.generate_key()
ENCRYPT_KEY = b"f7DwTK5K6EwmA30THAxnXgBKy_v969ItANlVGhi4C-0="

ROOT_URLCONF = "config.urls.dev"
