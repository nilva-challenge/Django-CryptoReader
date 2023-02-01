from rest_framework.generics import GenericAPIView

from .serializers import OrderSerializers, TrackSerializers, PositionSerializers, BinanceProfileSerializers
from .utils import create_or_delete_celery_task
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, Position, Binance_profile


class all_orders(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializers

    def get(self, request) -> Response:
        user = request.user
        orders = Order.objects.filter(user=user)
        data = OrderSerializers(orders, many=True).data
        return Response(data, status=200)


class all_positions(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PositionSerializers

    def get(self, request) -> Response:
        user = request.user
        positions = Position.objects.filter(user=user)
        data = PositionSerializers(positions, many=True).data
        return Response(data, status=200)


class TotalWalletBalance(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BinanceProfileSerializers

    def get(self, request) -> Response:
        user = request.user
        total_wallet = Binance_profile.objects.filter(user=user)
        data = BinanceProfileSerializers(total_wallet, many=True).data
        return Response(data, status=200)


class TrackPositions(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrackSerializers

    def post(self, request):
        user = request.user
        serializer = TrackSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        track = serializer.data['track']
        data = create_or_delete_celery_task(user, track)

        return Response(data, status=200)
