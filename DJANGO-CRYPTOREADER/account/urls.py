from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('sign-up/', RegisterView.as_view({'post': 'create'})),
    path('sign-in/', LoginView.as_view()),
]
