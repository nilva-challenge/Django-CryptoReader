from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.views import get_user_model
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from accounts.serializers import RegisterSerializer
from core.serializers import KucoinOrderSerializer
from kucoin.KucoinRequestHandler import Kucoin

from .utils import custom_filter , convert

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

User = get_user_model()



@api_view(('POST',))
@permission_classes([IsAuthenticated])
def kucoin_orders_api_view(request) -> Response:
    """
    Everything ends up in here . the whole idea is to use redis cache to store the data provided by the kucoin api for each user
    We track the open/done orders of the user , save it to the cache and filter it inside the python but not the kucoin api
    the celery task updates the cached data once each 30 seconds

    the filtering provided here is just the same as kucoin using custom_filter function in utils

    if the user is asking for orders for the first time , we generate and save it to the cache
    after it , we just call the key in the cache , and celery updating goes on if user has turned auto update on
    :param request:
    :return:
    """
    data = request.data
    user = request.user
    serializer = KucoinOrderSerializer(data=data,context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    user_serializer = RegisterSerializer(user)
    filter_params , time_params = serializer.validated_data
    status = filter_params['status']
    key = f'{user.username}_{status}_orders'
    del filter_params['status']
    if key in cache:
        print('inja')
        orders = cache.get(key)
    else:
        print('anja')
        try:
            kucoin_obj = Kucoin(method='GET',endpoint='/api/v1/orders',sandbox=True,params={'status':status},user=user)
            resp = kucoin_obj.dispatcher()
        except Exception as e:
            raise Exception(e)
        else:
            orders = resp['data']['items']
            cache.set(key, orders, timeout=CACHE_TTL)

    if filter_params:
        filter_dict = convert(filter_params)
        orders = custom_filter(orders, filter_dict,time_params)
    result = {
        'user': user_serializer.data,
        'orders': orders
    }
    return Response(result, status=HTTP_200_OK)


@api_view(('POST',))
@permission_classes([IsAuthenticated])
def enable_disable_auto_update(request) -> Response:
    """
    An endpoint to enable disable auto update whenever it is called

    if auto update field is true , by calling this endpoint it gets disabled
    :param request:
    :return:
    """
    user = request.user
    if user.auto_update_orders:
        user.auto_update_orders = False
        user.save()
        return Response({'Order Auto Update':'Disabled'}, status=HTTP_200_OK)
    user.auto_update_orders = True
    user.save()
    return Response({'Order Auto Update': 'Enabled'}, status=HTTP_200_OK)
