from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .utils.cryptography import encrypt_message,decrypt_message


class CustomManager(BaseUserManager):
    def create_user(self, username, kucoin_pass_pharese, kucoin_api_key, kucoin_api_secret, password=None):
        if not username:
            raise ValueError("Username is Required.")
        user = self.model(
            username=username,
        )
        user.save(using=self._db)
        user.set_password(password)
        user.kucoin_pass_pharese = encrypt_message(kucoin_pass_pharese)
        user.kucoin_api_key = encrypt_message(kucoin_api_key)
        user.kucoin_api_secret = encrypt_message(kucoin_api_secret)
        user.save()
        return user

    def create_superuser(self, username, kucoin_pass_pharese, kucoin_api_key, kucoin_api_secret, password=None):
        if not username:
            raise ValueError("Username is required.")
        user = self.model(
            username=username,
        )
        user.save(using=self._db)
        user.set_password(password)
        user.kucoin_pass_pharese = encrypt_message(kucoin_pass_pharese)
        user.kucoin_api_key = encrypt_message(kucoin_api_key)
        user.kucoin_api_secret = encrypt_message(kucoin_api_secret)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    # base information
    username = models.CharField(
        max_length=64, unique=True, verbose_name='user name')
    name = models.CharField(max_length=64, null=True,
                            blank=True, verbose_name='name')

    # extra information
    last_login = models.DateTimeField(auto_now=True, verbose_name='update at')
    joined_at = models.DateTimeField(
        auto_now_add=True, verbose_name='joined at')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # kucoin details
    kucoin_pass_pharese = models.CharField(
        max_length=256, verbose_name='pass phrase')
    kucoin_api_key = models.CharField(max_length=256, verbose_name='api key')
    kucoin_api_secret = models.CharField(
        max_length=256, verbose_name='api secret')

    USERNAME_FIELD = 'username'

    objects = CustomManager()

    def __str__(self) -> str:
        return f'user name = {self.username}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
