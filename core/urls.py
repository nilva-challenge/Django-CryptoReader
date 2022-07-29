from django.urls import path
from .views import kucoin_orders_api_view , enable_disable_auto_update

app_name = 'Core'

urlpatterns = [
    path('orders', kucoin_orders_api_view, name='Orders'),
    path('auto_updater', enable_disable_auto_update, name='Auto Updater'),
]
