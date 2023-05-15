from rest_framework import mixins, viewsets, permissions
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()

class UserCreateView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()

class UserGetView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.id)