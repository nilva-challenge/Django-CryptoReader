from cryptoreader.accounts.serializers import (
    KucoinAccount,
    KucoinAccountSerializer,
    User,
    UserSerializer,
)
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from third_party_sdks.sdk_api import fetch_accounts

# Raise an error in the endpoint for invalid data
RAISE_ERROR_IF_INVALID = True
CACHE_TTL_ACCOUNTS = 30


def load_accounts_from_kucoin_by_user(user: User) -> dict:
    login_info = user.get_key(), user.get_secret(), user.get_passphrase()
    accounts = fetch_accounts(*login_info)
    return accounts


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
    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
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


class KucoinAccountViewSet(viewsets.ViewSet):
    queryset = KucoinAccount.objects.all()
    serializer_class = KucoinAccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_object(self, id):
        account = KucoinAccount.objects.filter(user=self.request.user, id=id).last()
        if account:
            return account
        raise Http404

    @extend_schema(
        summary="create a new account",
        request=KucoinAccountSerializer,
        responses={
            200: KucoinAccountSerializer,
            404: None,
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = KucoinAccountSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(RAISE_ERROR_IF_INVALID):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

    @extend_schema(
        summary="get the list of accounts specified with the ID ",
        responses={
            200: KucoinAccountSerializer,
            404: None,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        account = self.get_object(kwargs.setdefault("id", None))
        serializer = KucoinAccountSerializer(account)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        summary="get the all available accounts",
        responses={
            200: KucoinAccountSerializer(many=True),
            404: None,
        },
    )
    @method_decorator(cache_page(CACHE_TTL_ACCOUNTS))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def list(self, request, *args, **kwargs):
        user = user = self.request.user
        accounts = KucoinAccount.objects.filter(user=user)
        serializer = KucoinAccountSerializer(accounts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        summary="get the open accounts",
        responses={
            200: KucoinAccountSerializer(many=True),
            404: None,
        },
    )
    @action(detail=False, methods=("GET",))
    @method_decorator(cache_page(CACHE_TTL_ACCOUNTS))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def list_current(self, request, *args, **kwargs):
        """fetch last avilable accounts form kucoin and instert to db"""
        
        user = self.request.user
        accounts = load_accounts_from_kucoin_by_user(user)
        serializer = KucoinAccountSerializer(
            data=accounts, many=True, context={"request": request}
        )

        if serializer.is_valid(RAISE_ERROR_IF_INVALID):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
