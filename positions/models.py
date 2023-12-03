from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=128)
    side = models.CharField(max_length=128)
    symbol = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    remark = models.CharField(max_length=128)
    stp = models.CharField(max_length=128)
    trade_type = models.CharField(max_length=128)

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.symbol}'
