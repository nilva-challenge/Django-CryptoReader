from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .models import Position
from .serializers import PositionSerializer, TrackingPositionSerializer
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import status, mixins
from django.conf import settings
from django_redis import get_redis_connection
from .pagination import CustomPagination
import json


class PositionTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, symbol_name='XBTUSDM'):
        # code to start position tracking for the authenticated user
        user = request.user
        user_kucoin_secret_items = {'kucoin_api_key': user.kucoin_api_key,
                                    'kucoin_api_secret': user.kucoin_api_secret,
                                    'kucoin_passphrase': user.kucoin_passphrase}

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=settings.INTERVAL,
            period=IntervalSchedule.SECONDS,
        )
        try:
            PeriodicTask.objects.create(
                interval=schedule,  # we created this above.
                name=f'{user.id}_{symbol_name}',  # simply describes this periodic task. (unique)
                task=f'{settings.TARGET_SCHEDULE_APP_NAME}.tasks.tracking_task',  # name of task.
                kwargs=json.dumps(dict(user=user_kucoin_secret_items, context={'user_id': user.pk})),
                expires=settings.EXPIRE_TIME  # expire time
            )
        except Exception as err:
            return Response({"message": f"Maybe you already set up tracking for symbol = {symbol_name}"},
                            status=status.HTTP_409_CONFLICT)

        return Response({'message': f'Position tracking started symbol {symbol_name}'}, status=status.HTTP_201_CREATED)


class LastOpenPositionsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PositionSerializer

    def get(self, request, symbol_name='XBTUSDM'):
        user = request.user
        # Check if the data is already cached
        cached_data = self.get_results_from_redis(user=user, symbol=symbol_name)
        if cached_data:
            serializer = self.serializer_class(data=json.loads(cached_data))
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Fetch data from database.
        positions = Position.objects.filter(user=user).filter(symbol=symbol_name).order_by('created_at').last()
        serializer = self.serializer_class(positions, many=True)
        return Response(serializer.data)

    def get_results_from_redis(self, user, symbol):
        result = None
        try:
            self.redis_conn = get_redis_connection("default")
            result = self.redis_conn.get(f'cache_key_{symbol}_{user.id}')
        except Exception as e:
            # Logger exception
            pass
        return result


class PositionsListView(mixins.ListModelMixin,
                        GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PositionSerializer
    pagination_class = CustomPagination

    def get(self, request, **kwargs):
        user = request.user
        positions = Position.objects.filter(user=user).order_by('created_at').all()
        serializer = self.serializer_class(positions, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        target_symbol = self.kwargs.get('symbol')
        queryset = Position.objects.filter(user=self.request.user).order_by('created_at').all()
        if target_symbol:
            queryset = queryset.filter(symbol=target_symbol)
        return queryset
