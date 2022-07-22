from email.mime import base
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from cryptoreader.api.views import KucoinAccountViewSet, UserViewSet

router = routers.DefaultRouter()
router.register("kucoinaccount", KucoinAccountViewSet)
router.register("user", UserViewSet, "user")


app_name = "API/V1"
urlpatterns = [
    path("", include(router.urls)),
    # path("user", UserCreate.as_view(), name="user-create"),
    # path("user2", UserDetail.as_view(), name="user-detail"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
