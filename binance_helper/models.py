from django.db import models
from accounts.models import User

MARKET_TYPE = (
    ("futures", 'futures'),
    ("spot", 'spot')
)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    side = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    isActive = models.BooleanField()
    created_time = models.DateTimeField()
    update_time = models.DateTimeField()
    price = models.FloatField()
    amount = models.FloatField()
    market_type = models.CharField(choices=MARKET_TYPE, max_length=10)


class Position(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=100)
    entryPrice = models.FloatField()
    leverage = models.FloatField()
    created_time = models.DateTimeField()
    update_time = models.DateTimeField()
    pnl = models.FloatField()
    market_type = models.CharField(choices=MARKET_TYPE, max_length=10)
    amount = models.FloatField()


class Wallet(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    futures_coins = models.JSONField()
    spot_coins = models.JSONField()
    update_time = models.DateTimeField(null=True)
    created_time = models.DateTimeField(null=True)
