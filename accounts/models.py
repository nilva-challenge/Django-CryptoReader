from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.core.signing import Signer
from .encryption import encrypt, decrypt

signer = Signer()


class UserManager(BaseUserManager):
    '''
        UserManager to create user and encrypts kucoin details and save to the database.
    '''

    def encryption(self, key, secret, passphrase) -> tuple:
        '''
            Encrypt key, secret & passphrase
        '''

        return encrypt(key), encrypt(secret), encrypt(passphrase)

    def create_user(self, name, username, kucoin_key, kucoin_secret, kucoin_passphrase, password=None):

        now = timezone.now()

        kucoin_key, kucoin_secret, kucoin_passphrase = self.encryption(kucoin_key, kucoin_secret, kucoin_passphrase)

        user = self.model(
            name=name, username=username, kucoin_key=kucoin_key, kucoin_secret=kucoin_secret,
            kucoin_passphrase=kucoin_passphrase, is_staff=False, is_active=True, is_superuser=False, date_joined=now,
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
    '''
        User model with name, username & kucoin details    
    '''

    name = models.CharField(_("name"), max_length=150)
    kucoin_key = models.CharField(max_length=200)
    kucoin_secret = models.CharField(max_length=200)
    kucoin_passphrase = models.CharField(max_length=200)

    objects = UserManager()

    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.username

    def decryption(self, key, secret, passphrase) -> tuple:
        '''
            Decrypt kucoin details of the user
        '''

        return decrypt(key),  decrypt(secret),  decrypt(passphrase)
