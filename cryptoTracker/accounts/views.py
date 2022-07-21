from rest_framework.generics import (
    CreateAPIView,
)
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': f" {request.user.username} logged out"}, status=status.HTTP_200_OK)

