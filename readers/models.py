from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_id = models.CharField(max_length=512, null=False, blank=False)
    currency = models.CharField(max_length=10, null=False, blank=False)
    account_type = models.CharField(max_length=6, null=False, blank=False)
    balance = models.DecimalField(max_digits=20, decimal_places=6)
    available = models.DecimalField(max_digits=20, decimal_places=6)
    holds = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        unique_together = ('user', 'account_id',)

    def __str__(self) -> str:
        return f'{self.account_id} - user:{self.user.id}'