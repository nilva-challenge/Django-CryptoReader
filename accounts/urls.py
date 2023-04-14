from django.urls import path
from .views import Register
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

app_name = "accounts"

urlpatterns = [
    path('register/', Register.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]