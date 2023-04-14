from rest_framework.generics import GenericAPIView
from kucoin.models import Order
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializers, TrackSerializers
from .utils import create_or_delete_celery_task, update_orders


class OpenPositions(GenericAPIView):
    '''
        Get and view open (active) positions. Orders save as objects in database with Order model and querying to get those.
    '''

    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializers

    def get(self, request) -> Response:
        user = request.user
        update_orders(user)
        orders = Order.objects.filter(user=user, isActive=True)
        data = OrderSerializers(orders, many=True).data or 'Empty'

        return Response(data, status=200)


class TrackPositions(GenericAPIView):
    '''
        Enable or disable tracking positions for each user & see list of tracking positions. enable/disable tracking using create/delete celery task. Get list of tracking positions using querying Order model.
    '''

    permission_classes = (IsAuthenticated,)
    serializer_class = TrackSerializers

    def post(self, request):
        user = request.user
        serializer = TrackSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        track = serializer.data['track']
        data = create_or_delete_celery_task(user, track)

        return Response(data, status=200)

    def get(self, request) -> Response:
        user = request.user
        orders = Order.objects.filter(user=user)
        data = OrderSerializers(orders, many=True).data or 'Empty'

        return Response(data, status=200)
