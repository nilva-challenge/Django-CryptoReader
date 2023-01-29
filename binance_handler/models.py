from django.db import models
from accounts.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clientOid = models.CharField(max_length=200)
    side = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    tradeType = models.CharField(max_length=200)
    isActive = models.BooleanField()


class Position(Order):
    open = models.BooleanField()


class Binance_profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_wallet_balance = models.CharField(max_length=10000)
