from django.db import models
from django.contrib.auth import get_user_model
import random
User = get_user_model()

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    id = models.CharField(max_length=512, null=False, blank=False, unique=True)
    currency = models.CharField(max_length=10, null=False, blank=False)
    type = models.CharField(max_length=6, null=False, blank=False)
    balance = models.DecimalField(max_digits=20, decimal_places=6)
    available = models.DecimalField(max_digits=20, decimal_places=6)
    holds = models.DecimalField(max_digits=20, decimal_places=6)

    id_field = models.AutoField(primary_key=True)
    
    class Meta:
        unique_together = ('user', 'id',)

    def __str__(self) -> str:
        return f'{self.id} - user:{self.user.id}'