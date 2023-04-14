from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.core.signing import Signer
from .encryption import encrypt, decrypt

signer = Signer()


def api_decryption(key, secret) -> tuple:
    return decrypt(key), decrypt(secret)


def api_encryption(key, secret) -> tuple:
    return encrypt(key), encrypt(secret)


class UserManager(BaseUserManager):

    def create_user(self, name, username, api_future_key, api_future_secret, api_spot_key, api_spot_secret, password=None):
        now = timezone.now()

        api_spot_key, api_spot_secret = api_encryption(api_spot_key, api_spot_secret)
        api_features_key, api_features_secret = api_encryption(api_future_key, api_future_secret)

        user = self.model(
            name=name, username=username, api_future_key=api_features_key, api_future_secret=api_future_secret,
            api_spot_key=api_spot_key, api_spot_secret=api_spot_secret, is_staff=False, is_active=True, is_superuser=False,
            date_joined=now)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, username, password=None):
        user = self.model(name=name, username=username)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
    name = models.CharField(_("name"), max_length=150)
    api_future_key = models.CharField(max_length=150, null=True)
    api_future_secret = models.CharField(max_length=150, null=True)
    api_spot_key = models.CharField(max_length=150, null=True)
    api_spot_secret = models.CharField(max_length=150, null=True)

    objects = UserManager()

    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.username
