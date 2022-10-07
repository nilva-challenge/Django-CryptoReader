from django.urls import path
from .views import OpenPositions, TrackPositions

app_name = "kucoin"

urlpatterns = [
    path('open_positions/', OpenPositions.as_view(), name='open_positions'),  # see list of current open positions

    # enable or disable tracking position & see list of tracking positions
    path('tracking_positions/', TrackPositions.as_view(), name='tracking_positions'),
]
