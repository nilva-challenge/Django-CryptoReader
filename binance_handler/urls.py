from django.urls import path

from binance_handler.views import OpenPositions, TrackPositions

app_name = "binance_handler"

urlpatterns = [
    path('open_positions/', OpenPositions.as_view(), name='open_positions'),
    path('tracking/', TrackPositions.as_view(), name='tracking'),
]
