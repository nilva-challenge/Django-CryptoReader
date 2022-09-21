from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('sign-up/', RegisterView.as_view()),
    path('sign-in/', LoginView.as_view()),
]
