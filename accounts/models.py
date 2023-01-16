from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.core.signing import Signer
from .encryption import encrypt, decrypt

signer = Signer()


class UserManager(BaseUserManager):
    def encryption(self, key, secret) -> tuple:
        return encrypt(key), encrypt(secret)

    def create_user(self, name, username, binance_key, binance_secret, password=None):

        now = timezone.now()

        binance_key, binance_secret = self.encryption(binance_key, binance_secret)

        user = self.model(
            name=name, username=username, binance_key=binance_key, binance_secret=binance_secret,
            is_staff=False, is_active=True, is_superuser=False, date_joined=now,
            last_login=now,)
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
    binance_key = models.CharField(max_length=200)
    binance_secret = models.CharField(max_length=200)

    objects = UserManager()

    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.username

    def decryption(self, key, secret) -> tuple:
        return decrypt(key),  decrypt(secret)
