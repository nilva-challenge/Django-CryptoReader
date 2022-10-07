from django.urls import path

from .views import OpenPositions

app_name = "kucoin"

urlpatterns = [
    path('open_positions/', OpenPositions.as_view(), name='open_positions'),  # see list of current open positions
]
