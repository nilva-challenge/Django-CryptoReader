from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import User
from django.contrib.auth import login
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED , HTTP_202_ACCEPTED
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.exceptions import NotFound


class RegisterView(ModelViewSet):

    def get_queryset(self):
        try:
            user = User.objects.get(username=self.request.user.username)
        except User.DoesNotExist:
            raise NotFound('User not found.')

    def get_serializer_class(self):
        if self.action in ['create']:
            return RegisterSerializer

    def perform_create(self, serializer):
        serializer = serializer.save(data=self.request.data)
        return serializer




class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    # permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=HTTP_202_ACCEPTED)
