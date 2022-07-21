from symtable import Symbol
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from cryptography.fernet import Fernet
from django.conf import settings
from fernet_fields import EncryptedCharField
from django.contrib.auth.models import UserManager

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    api_key = EncryptedCharField(max_length=200)
    secret_key = EncryptedCharField(max_length=200)
    api_passphrase = EncryptedCharField(max_length=200)

