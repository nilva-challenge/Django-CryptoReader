from django.urls import path, include
from .views import OrderView

urlpatterns = [
    path('order-list/', OrderView.as_view({'post': 'create', 'get': 'list'})),
]
