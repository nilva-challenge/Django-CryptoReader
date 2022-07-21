from django.urls import path
from .views import (
    RegisterAPIView,
    LogoutAPIView
)
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', view=obtain_auth_token),
    path('logout/', LogoutAPIView.as_view()),

]
