from django.urls import path
from .views import OpenPositions, TrackPositions, UpdateOpenPositions

app_name = "kucoin"

urlpatterns = [
    path('open_positions/', OpenPositions.as_view(), name='open_positions'),  # see list of current open positions
    path('open_positions/update/', UpdateOpenPositions.as_view(),
         name='update_open_positions'),  # update list of current open positions
    path('tracking/', TrackPositions.as_view(), name='tracking'),  # enable or disable tracking position
]
