from django.shortcuts import render
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data='registeration done successfully.',
            status=HTTP_201_CREATED
        )


class LoginView(APIView):
    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #     return {
    #         'username': self.request.data['username'],
    #         'password': self.request.data['password'],
    #     }

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            data='login done successfully.',
            status=HTTP_200_OK
        )
