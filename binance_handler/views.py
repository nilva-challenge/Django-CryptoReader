from rest_framework.generics import GenericAPIView

from .serializers import OrderSerializers, TrackSerializers
from .utils import create_or_delete_celery_task
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order


class OpenPositions(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializers

    def get(self, request) -> Response:
        user = request.user
        orders = Order.objects.filter(user=user)
        data = OrderSerializers(orders, many=True).data
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
