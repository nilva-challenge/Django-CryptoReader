import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.functions import encrypt, decrypt


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.api_key = encrypt(extra_fields.get('api_key'))
        user.api_secret = encrypt(extra_fields.get('api_secret'))
        user.api_passphrase = encrypt(extra_fields.get('api_passphrase'))
        user.save()

        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Please assign is_staff=True for superuser')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Please assign is_superuser=True for superuser')
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    # Add additional fields for KuCoin details
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    api_passphrase = models.CharField(max_length=255)

    EMAIL_FIELD = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def decrypt_kucoin_data(self):
        return {'api_key': decrypt(self.api_key), 'api_secret': decrypt(self.api_secret),
                'api_passphrase': decrypt(self.api_passphrase)}

    def __str__(self):
        return str(self.id)
