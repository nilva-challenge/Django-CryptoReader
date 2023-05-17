from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from readers.models import Account
from .serializers import AccountSerializer
from utils.cache import read_positions_from_cache

class AccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        """
            List of request.user positions.
            This endpoint tries to populate AccountSerializer first using with redis cache.
            If redis service was down, it will populate serializer from DB.
        """
        accounts = read_positions_from_cache(user=request.user)
        if accounts == 'DB':
            qs = request.user.accounts.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        qs = []
        for account in accounts:
            qs.append(Account(**account)) 
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
