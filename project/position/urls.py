from django.urls import path
from . import views

urlpatterns = [
    path('position_tracking/', views.PositionTrackingView.as_view(), name='position_tracking'),
    path('position/', views.OpenPositionsView.as_view(), name='open_positions'),

]
