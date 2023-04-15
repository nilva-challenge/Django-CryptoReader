from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


# provide name, username & kucoin details
class User(AbstractUser):
    kucoin_api_key = models.CharField(max_length=255, null=True, blank=True)
    kucoin_api_secret = models.CharField(max_length=255, null=True, blank=True)
    kucoin_passphrase = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
