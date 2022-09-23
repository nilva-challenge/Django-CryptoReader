from django.urls import path, include
from .views import OpenOrderView

urlpatterns = [
    path('open-position/',
         OpenOrderView.as_view({'post': 'create', 'get': 'list'})),
    # path('list-order/', OrderView.as_view({'post': 'create', 'get': 'list'})),

]
