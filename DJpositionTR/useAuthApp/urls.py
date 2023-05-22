from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path, include
from . import views



urlpatterns = [
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('tst',views.my_view),
    path('register/', views.UserRegistrationView.as_view(), name ='register'),
    path('logout/', views.LogoutView.as_view(), name ='logout'),

    
]