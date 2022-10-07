from django.urls import path
from .views import OpenPositions, TrackPositions

app_name = "kucoin"

urlpatterns = [
    path('open_positions/', OpenPositions.as_view(), name='open_positions'),  # see list of current open positions
    path('tracking/', TrackPositions.as_view(), name='tracking'),  # enable or disable tracking position
]
