
from django.db import models
import uuid


class Order(models.Model):
    """ 
    based on this docs: just define some fileds not all of them
    https://docs.kucoin.com/futures/#get-position-list
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    symbol = models.CharField(max_length=64, null=True,blank=True, verbose_name='symbol')
    autoDeposit = models.BooleanField(default=False, verbose_name='auto deposit ?')
    isOpen = models.BooleanField(default=False, verbose_name='is open ?')

    def __str__(self) -> str:
        return f'id = {self.id} , symbol = {self.symbol}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


