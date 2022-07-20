from cryptoreader.accounts.serializers import (
    User,
    UserSerializer,
)
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Raise an error in the endpoint for invalid data
RAISE_ERROR_IF_INVALID = True


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        elif self.action in ["me", "update_me", "destroy_me"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary="get current user detail",
        parameters=None,
        responses={
            200: KucoinAccountSerializer(many=True),
            404: None,
        },
    )
    @action(methods=["GET"], detail=False)
    def me(self, request):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        summary="sign-up new user",
        parameters=None,
        request=UserSerializer,
        responses={
            200: UserSerializer(many=True),
            404: None,
        },
    )
    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(RAISE_ERROR_IF_INVALID):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

    @extend_schema(
        summary="updating current user",
        request=UserSerializer,
        responses={
            200: UserSerializer(),
            404: None,
        },
    )
    @me.mapping.put
    def update_me(self, request, partial=False):
        user = self.get_object()
        serializer = UserSerializer(user, request.data, partial=partial)
        if serializer.is_valid(RAISE_ERROR_IF_INVALID):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        summary="deleting current user",
        request=UserSerializer,
        responses={
            404: None,
        },
    )
    @me.mapping.delete
    def destroy_me(self, request):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Create your views here.
