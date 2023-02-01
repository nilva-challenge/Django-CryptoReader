from django.contrib import admin

from binance_handler.models import Binance_profile, Order, Position

admin.site.register(Binance_profile)
admin.site.register(Order)
admin.site.register(Position)
