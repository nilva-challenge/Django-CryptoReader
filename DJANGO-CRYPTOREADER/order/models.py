from asyncio.constants import ACCEPT_RETRY_DELAY
from django.db import models


class Order(models.Model):
    ACTIVE = 'active'
    DONE = 'done'
    ORDER_STATUS_CHOICES = (
        (ACTIVE, 'پرداخت نشده'),
        (DONE, 'در انتظار ایجاد محتوا'),
    )

    BUY = 'buy'
    SELL = 'sell'
    ORDER_SIDE_CHOICES = (
        (BUY, 'خرید'),
        (SELL, 'فروش'),
    )

    LIMIT = 'limit'
    MARKET = 'market'
    LIMIT_STOP = 'limit_stop'
    MARKET_STOP = 'market_stop'
    ORDER_TYPE_CHOICES = ((LIMIT, 'لیمیت'), (MARKET, 'مارکت'),
                          (MARKET_STOP, 'لیمیت استاپ'),
                          (LIMIT_STOP, 'مارکت استاپ'))

    TRADE = 'trades'
    MARGIN_TRADE = 'margin_trade'
    ORDER_TRADE_TYPE_CHOICES = ((TRADE, 'ترید'),
                                (MARGIN_TRADE, 'مارجین ترید'))

    status = models.CharField(
        verbose_name='وضعیت',
        max_length=64,
        choices=ORDER_STATUS_CHOICES,
        default=ACTIVE,
    )
    symbol = models.CharField(max_length=64, null=True,
                              blank=True, verbose_name='نام ارز')
    side = models.ChoiceField(
        verbose_name='وضعیت خرید',
        max_length=64,
        choices=ORDER_SIDE_CHOICES,
        default=BUY,
    )
    type = models.ChoiceField(
        verbose_name='نوع سفارش',
        max_length=64,
        choices=ORDER_TYPE_CHOICES,
        default=LIMIT,
    )
    tradeType = models.ChoiceField(
        verbose_name='نوع سفارش',
        max_length=64,
        choices=ORDER_TRADE_TYPE_CHOICES,
        default=TRADE,
    )
    startAt = models.DateTimeField(blank=True, null=True)
    endAt = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'symbol = {self.symbol}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
