from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .routers import router


urlpatterns = [
    path('login/token/', TokenObtainPairView.as_view(), name='api-token_obtain'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='api-token_refresh'),
]

urlpatterns += router.urls