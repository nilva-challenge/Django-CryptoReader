from django.db import models
from accounts.models import User

MARKET_TYPE = (
    ("features", '1'),
    ("spot", 2)
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    side = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    tradeType = models.CharField(max_length=200)
    isActive = models.BooleanField(null=True)
    time = models.DateTimeField(null=True)
    # leverage = models.FloatField(null=True)
    price = models.FloatField(null=True)
    market_type = models.CharField(choices=MARKET_TYPE, max_length=10, null=True)


class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=100, null=True)
    entryPrice = models.CharField(max_length=100, null=True)
    leverage = models.IntegerField(null=True)
    time = models.DateTimeField(null=True)
    unRealizedProfit = models.FloatField(null=True)
    market_type = models.CharField(choices=MARKET_TYPE, max_length=10, null=True)


class Binance_profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    market_type = models.CharField(choices=MARKET_TYPE, max_length=10, null=True)
    BTC_wallet = models.FloatField(default=0)
    BNB_wallet = models.FloatField(default=0)
    ETH_wallet = models.FloatField(default=0)
    USDT_wallet = models.FloatField(default=0)
    USDC_wallet = models.FloatField(default=0)
    BUSD_wallet = models.FloatField(default=0)
