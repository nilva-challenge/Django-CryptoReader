from django.db import models
from accounts.models import CustomUser

# we just add some fields of a real position. other fields can added in the same way    
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    symbol = models.CharField(max_length=50)
    opType = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    side = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    fee = models.CharField(max_length=20)
    isActive = models.CharField(max_length=20)
    order_createdAt = models.IntegerField()    

# check user must be tracked or not
class ActiveTrackingUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    track = models.BooleanField(default=False)
