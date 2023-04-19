from django.conf import settings
from django.db import models


class Position(models.Model):
    """
    This model is created based partial received data from following api
    https://api-futures.kucoin.com/api/v1/position?symbol={symbol_name}
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10, default='XBTUSDM')
    created_at = models.DateTimeField(auto_now_add=True)
    mark_price = models.FloatField(max_length=2,null=True)
    mark_value = models.FloatField(max_length=2, null=True)
    risk_limit = models.IntegerField(null=True)
