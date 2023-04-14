from django.db import models
from accounts.models import User


class Order(models.Model):
    '''
        save kucoin orders as objects of Order model
    '''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clientOid = models.CharField(max_length=200)
    side = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    remark = models.CharField(max_length=200)
    stp = models.CharField(max_length=200)
    tradeType = models.CharField(max_length=200)
    isActive = models.BooleanField()
