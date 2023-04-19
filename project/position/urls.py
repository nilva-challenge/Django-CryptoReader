from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('positions', views.PositionsListView, basename='positions')

urlpatterns = [
    path('position_tracking/<str:symbol_name>/', views.PositionTrackingView.as_view(), name='position_tracking'),
    path('position/<str:symbol_name>/', views.LastOpenPositionsView.as_view(), name='open_positions'),
    path('', include(router.urls)),
]
