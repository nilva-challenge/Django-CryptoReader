from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Position
from .serializers import PositionSerializer, TrackingPositionSerializer
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .tasks import Utility, tracking_task
from datetime import datetime, timedelta
import json


class PositionTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, symbol_name='XBTUSDM'):
        # code to start position tracking for the authenticated user

        # tracking_task.delay(user=user_kucoin_secret_items,
        #                     context={'user_id': user.pk})
        # tracking_task.apply_async(kwargs=dict(user=user_kucoin_secret_items,
        #                                       context={'user_id': user.pk}), countdown=3, expires=3600)
        #
        # tracking_task.apply_async(kwargs=dict(user=user_kucoin_secret_items,
        #                                       context={'user_id': user.pk}), eta=datetime.now() + timedelta(seconds=3))
        user = request.user
        user_kucoin_secret_items = {'kucoin_api_key': user.kucoin_api_key,
                                    'kucoin_api_secret': user.kucoin_api_secret,
                                    'kucoin_passphrase': user.kucoin_passphrase}


        MY_APP_NAME = 'position'

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )

        PeriodicTask.objects.create(
            interval=schedule,  # we created this above.
            name=f'{user.id}_{symbol_name}',  # simply describes this periodic task. (unique)
            task=f'{MY_APP_NAME}.tasks.tracking_task',  # name of task.
            kwargs=json.dumps(dict(user=user_kucoin_secret_items, context={'user_id': user.pk})),
            expires=datetime.utcnow() + timedelta(seconds=3600)  # expire time
        )

        return Response({'detail': 'Position tracking started.', 'symbol': symbol_name})


class OpenPositionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        positions = Position.objects.filter(user=user)
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)
