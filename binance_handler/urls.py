from django.urls import path

from .views import OpenPositions

app_name = "binance_handler"

urlpatterns = [
    path('open_positions/', OpenPositions.as_view(), name='open_positions'),
]