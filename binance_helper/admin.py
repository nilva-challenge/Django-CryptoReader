from django.contrib import admin

from binance_helper.models import Wallet, Order, Position

admin.site.register(Wallet)
admin.site.register(Order)
admin.site.register(Position)
