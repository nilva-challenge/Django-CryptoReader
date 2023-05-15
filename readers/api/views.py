from rest_framework import viewsets, permissions, mixins
from readers.models import Account
from .serializers import AccountSerializer

from utils.request import update_positions_for_user

class AccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated,]
    
    def get_queryset(self):
        account = self.request.user.accounts.all()
        if account:
            return account
        else:
            return Account.objects.none()

    def list(self, request, *args, **kwargs):
        update_positions_for_user(request.user)
        return super().list(request, *args, **kwargs)