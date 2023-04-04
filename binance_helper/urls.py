from django.urls import path

from binance_helper.views import CurrentFutureOrders, CurrentFuturePositions, CurrentFutureWallet, \
                                  CurrentSpotOrders, CurrentSpotWallet,\
                                  TrackPositions

app_name = "binance_helper"

urlpatterns = [
    path('current_future_orders/', CurrentFutureOrders.as_view(), name='current_orders'),
    path('current_future_positions/', CurrentFuturePositions.as_view(), name='current_positions'),
    path('current_future_wallet/', CurrentFutureWallet.as_view(), name='TotalWalletBalance'),
    path('current_spot_orders/', CurrentSpotOrders.as_view(), name='TotalSpotOrders'),
    path('current_spot_wallet', CurrentSpotWallet.as_view(), name='TotalSpotWalletBalance'),
    path('tracking/', TrackPositions.as_view(), name='tracking'),
]
