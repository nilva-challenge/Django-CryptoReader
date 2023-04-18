from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Position
from .serializers import PositionSerializer, TrackingPositionSerializer
from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from django.core.cache import cache
# from django.core.cache import cache

# from django_redis.cache import cache
from rest_framework import status
from datetime import datetime, timedelta
import json

from django_redis import get_redis_connection


class PositionTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, symbol_name='XBTUSDM'):
        # code to start position tracking for the authenticated user
        user = request.user
        user_kucoin_secret_items = {'kucoin_api_key': user.kucoin_api_key,
                                    'kucoin_api_secret': user.kucoin_api_secret,
                                    'kucoin_passphrase': user.kucoin_passphrase}

        my_app_name = 'position'
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=30,
            period=IntervalSchedule.SECONDS,
        )
        try:
            PeriodicTask.objects.create(
                interval=schedule,  # we created this above.
                name=f'{user.id}_{symbol_name}',  # simply describes this periodic task. (unique)
                task=f'{my_app_name}.tasks.tracking_task',  # name of task.
                kwargs=json.dumps(dict(user=user_kucoin_secret_items, context={'user_id': user.pk})),
                expires=datetime.utcnow() + timedelta(seconds=3600*24*10)  # expire time
            )
        except Exception as err:
            return Response({"message": f"Maybe you already set up tracking for symbol = {symbol_name}"},
                            status=status.HTTP_409_CONFLICT)

        return Response({'message': f'Position tracking started symbol {symbol_name}'}, status=status.HTTP_201_CREATED)


class OpenPositionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        self._get_redis_conn()
        user = request.user
        # Check if the data is already cached

        cached_data = self.redis_conn.get(f'cache_key_{user.id}')
        if cached_data:
            return Response(cached_data)

        positions = Position.objects.filter(user=user).order_by('created_at')
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)

    def _get_redis_conn(self):
        self.redis_conn = get_redis_connection("default")