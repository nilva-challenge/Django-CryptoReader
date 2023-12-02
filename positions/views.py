from rest_framework import pagination, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .functions import cache_position
from .models import Order
from .serializers import OrderSerializers, SymbolTrackSerializers


class PositionPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class OpenPositionsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializers
    pagination_class = PositionPagination

    def get(self, request):
        orders = cache_position(request.user)
        data = OrderSerializers(orders, many=True).data

        paginator = PositionPagination()
        result_page = paginator.paginate_queryset(data, request)
        return paginator.get_paginated_response(result_page)


class TrackPositions(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SymbolTrackSerializers
    queryset = Order.objects.all()

    def post(self, request):
        serializer = SymbolTrackSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        track = serializer.data['track']
        order_obj = Order.objects.filter(user=request.user, symbol=track).first()
        if not order_obj:
            return Response({'message': 'symbol not found in tracking position'}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderSerializers(instance=order_obj).data, status=status.HTTP_200_OK)
