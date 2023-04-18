from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django_cryptography.fields import encrypt

# provide name, username & kucoin details
class User(AbstractUser):
    kucoin_api_key = encrypt(models.CharField(max_length=255, null=True, blank=True))
    kucoin_api_secret = encrypt(models.CharField(max_length=255, null=True, blank=True))
    kucoin_passphrase = encrypt(models.CharField(max_length=255, blank=True, null=True))
    email = models.EmailField(_('email address'), unique=True)
