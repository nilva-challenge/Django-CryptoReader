from django.urls import path

from binance_handler.views import all_orders, TrackPositions, all_positions,  TotalWalletBalance

app_name = "binance_handler"

urlpatterns = [
    path('all_orders/', all_orders.as_view(), name='all_orders'),
    path('all_positions/', all_positions.as_view(), name='all_positions'),
    path('total_wallet_balance/', TotalWalletBalance.as_view(), name='TotalWalletBalance'),
    path('tracking/', TrackPositions.as_view(), name='tracking'),
]
