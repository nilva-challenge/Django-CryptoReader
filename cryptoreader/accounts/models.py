from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from . import tools

User = get_user_model()


class KucoinAccountManager(models.Manager):
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


class KucoinAccount(models.Model):
    user = models.OneToOneField(
        User,
        models.CASCADE,
        related_name="kuicon_account",
    )
    key = models.CharField(max_length=248)
    secret = models.CharField(max_length=248)
    passphrase = models.CharField(max_length=558)

    # change the default model manager
    objects = KucoinAccountManager()
    _objects = models.Manager()

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
