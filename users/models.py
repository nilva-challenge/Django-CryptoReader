from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    api_key = models.CharField(max_length=512, null=False, blank=False)
    api_secret = models.CharField(max_length=512, null=False, blank=False)
    api_passphrase = models.CharField(max_length=512, null=False, blank=False)
    
    def __str__(self) -> str:
        return f'{self.id}. {self.first_name} {self.last_name}'
