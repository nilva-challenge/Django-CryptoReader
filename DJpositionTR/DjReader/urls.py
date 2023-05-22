from django.urls import path
from . import views


urlpatterns = [
    path('activePositionTracking/',views.activePositionTracking),
    path('positions/',views.positions),

]