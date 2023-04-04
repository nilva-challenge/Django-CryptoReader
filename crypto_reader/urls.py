from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('binance_helper/', include('binance_helper.urls')),
    path('kocoin/', include('kocoin.urls')),
]
