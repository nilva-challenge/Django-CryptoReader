from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from . import tools
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create(self, **kwargs):
        """encrtept data"""
        are_args_complete = all(
            [
                kwargs.setdefault("key", False),
                kwargs.setdefault("secret", False),
                kwargs.setdefault("passphrase", False),
            ],
        )

        if not are_args_complete:
            raise FieldError("pass all args [ key, secret, passphrase ]")

        kwargs["key"] = tools.encrypt(kwargs["key"])
        kwargs["secret"] = tools.encrypt(kwargs["secret"])
        kwargs["passphrase"] = tools.encrypt(kwargs["passphrase"])

        return super().create(**kwargs)


class User(AbstractUser):
    key = models.CharField(max_length=248)
    secret = models.CharField(max_length=248)
    passphrase = models.CharField(max_length=558)
    is_active = models.BooleanField(default=True)

    # change the default model manager
    objects = CustomUserManager()
    _objects = UserManager()

    def __str__(self) -> str:
        return str(self.username)

    def set_key(self, key):
        self.key = tools.encrypt(key)

    def get_key(self):
        return tools.decrypt(self.key)

    def set_secret(self, secret):
        self.secret = tools.encrypt(secret)

    def get_secret(self):
        return tools.decrypt(self.secret)

    def set_passphrase(self, passphrase):
        self.passphrase = tools.encrypt(passphrase)

    def get_passphrase(self):
        return tools.decrypt(self.passphrase)


class KucoinAccount(models.Model):
    class TypeAccount(models.TextChoices):
        main = "main", "Main"
        trade = "trade", "Trade"
        margin = "margain", "Margin"

    pk_uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
    )

    user = models.ForeignKey(
        User,
        models.CASCADE,
    )
    id = models.CharField(max_length=24)  # accountId
    type = models.CharField(
        max_length=7,
        choices=TypeAccount.choices,
        default=TypeAccount.main,
    )
    currency = models.CharField(max_length=24)  # Currency
    balance = models.DecimalField(
        max_digits=20, decimal_places=10
    )  # Total assets of a currency
    available = models.DecimalField(
        max_digits=20, decimal_places=10
    )  # Available assets of a currency
    holds = models.DecimalField(
        max_digits=20, decimal_places=10
    )  # Hold assets of a currency

    def __str__(self) -> str:
        return str(self.kucoin_api)
