from django.urls import path

from binance_handler.views import current_orders, current_positions, TrackPositions,  TotalWalletBalance

app_name = "binance_handler"

urlpatterns = [
    path('current_orders/', current_orders.as_view(), name='current_orders'),
    path('current_positions/', current_positions.as_view(), name='current_positions'),
    path('total_wallet_balance/', TotalWalletBalance.as_view(), name='TotalWalletBalance'),
    path('tracking/', TrackPositions.as_view(), name='tracking'),
]
