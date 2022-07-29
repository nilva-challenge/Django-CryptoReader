from django.urls import path
from .views import RegisterUserAPIView , LoginAPIView

app_name = 'Accounts'

urlpatterns = [
    path('register', RegisterUserAPIView.as_view(), name='Register'),
    path('login', LoginAPIView.as_view(), name='Login')
]
