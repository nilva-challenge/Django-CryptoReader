from rest_framework.generics import GenericAPIView
from kucoin.models import Order
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializers, TrackSerializers
from .utils import create_or_delete_celery_task


class OpenPositions(GenericAPIView):
    '''
        Get and view open (active) positions. 
    '''

    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializers

    def get(self, request) -> Response:
        user = request.user
        orders = Order.objects.filter(user=user, isActive=True)
        data = OrderSerializers(orders, many=True).data

        return Response(data, status=200)


class TrackPositions(GenericAPIView):
    '''
        Enable or disable Tracking positions for each user
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
