from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from readers.models import Account
from .serializers import AccountSerializer
from utils.cache import read_positions_from_cache

class AccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        accounts = read_positions_from_cache(user=request.user)
        if accounts == 'DB':
            qs = request.user.accounts.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        if accounts:
            serializer = self.get_serializer(accounts)
            return Response(serializer.data)
        return Response({})
