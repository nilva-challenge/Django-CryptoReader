from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from .serializers import OpenOrderSerializer
from .models import Order
from .utils.utility import CallAPI
from account.models import User
from rest_framework.exceptions import NotFound


class OpenOrderView(ModelViewSet):

    def get_queryset(self):
        return Order.objects.filter(isOpen=True)

    def get_serializer_class(self):
        if self.action in ['create']:
            return OpenOrderSerializer

    def perform_create(self, serializer):
        # data = self.request.data
        user = self.request.user
        data = CallAPI(user, '/api/v1/positions', 'GET', None, True)
        data.create_request()

        if data:
            serializer = serializer.save(data=data)
            # return serializer
            return Response('done', status=HTTP_200_OK)
        return Response('error')
