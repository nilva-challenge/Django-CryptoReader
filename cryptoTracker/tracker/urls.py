from django.urls import path
from tracker.views import (
    OpenPositionsAPIView,
    PositionTrackingAPIView
)

urlpatterns = [
    path('open-positions/', OpenPositionsAPIView.as_view()),
    path('position-tracking/', PositionTrackingAPIView.as_view()),
]
