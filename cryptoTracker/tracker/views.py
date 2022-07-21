from rest_framework.views import (
    APIView
)
from .models import Order, ActiveTrackingUser
from .serializers import PositionTrackingSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import api_kucoin

class OpenPositionsAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        endpoint = '/api/v1/orders?status=active'
        api_key = request.user.api_key
        api_secret = request.user.secret_key
        api_passphrase = request.user.api_passphrase
        status_code, response = api_kucoin(api_key, api_secret, api_passphrase, endpoint)
        return Response(data=response, status=status_code)

class PositionTrackingAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    
    # get user's positions from kucoin
    def _get_position_data(self, user):
        endpoint = '/api/v1/orders'
        api_key = user.api_key
        api_secret = user.secret_key
        api_passphrase = user.api_passphrase
        try:
            status_code, response = api_kucoin(api_key, api_secret, api_passphrase, endpoint)
            return status_code, response
        except:
            pass

    # save positions for all users that requested for position tracking 
    def save_position_data(self):
        active_tracking_users = ActiveTrackingUser.objects.filter(track=True)
        for activ_user in active_tracking_users:
            user = activ_user.user
            status_code, response = self._get_position_data(user)
            if len(response['data']['items']) > 0:
                for item in response['data']['items']:
                    Order.objects.create(
                        user=user, order_id=item['id'], symbol=item['id'],
                        opType=item['opType'], type=item['type'],
                        side=item['side'], price=item['price'],
                        size=item['size'], fee=item['fee'],
                        isActive=item['isActive'], order_createdAt=item['createdAt'],
                        )

    # get user's positions
    def get(self, request):
        user_orders = Order.objects.filter(user=request.user).values()
        return Response(user_orders, status=200)

    # Set position tracking flag (track=True for start and track = False for stop tracking)
    def post(self, request):
        serializer = PositionTrackingSerializer(data=request.data)
        if serializer.is_valid():
            user = ActiveTrackingUser.objects.update_or_create(
                user=request.user,
                defaults={'track':request.data['track']}
                )
            if request.data['track'] == 'True':
                message = f'start tracking {request.user}\'s posisions'
            else:
                message = f'stop tracking {request.user}\'s posisions'
            return Response({'message': message})
        else:
            return Response(serializer.errors)