from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from accounts.models import User
from kucoin.KucoinRequestHandler import Kucoin
from celery import shared_task



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@shared_task
def user_updater(username) -> None:
    """
    fetches the active/done orders of each individual user , using the same kdf , encrypt , decrypt functionality
    caches the response data with the key format like username_active/done_orders
    :param username:
    :return:
    """
    user = User.objects.get(username=username)
    try:
        active_orders_obj = Kucoin(method='GET', endpoint='/api/v1/orders', sandbox=True, params={'status': 'active'}, user=user)
        active_order_response = active_orders_obj.dispatcher()
        done_orders_obj = Kucoin(method='GET', endpoint='/api/v1/orders', sandbox=True, params={'status': 'done'}, user=user)
        done_order_response = done_orders_obj.dispatcher()
    except Exception as e:
        raise Exception(e)
    else:
        active_orders = active_order_response['data']['items']
        done_orders = done_order_response['data']['items']
        active_orders_key = f'{user.username}_active_orders'
        done_orders_key = f'{user.username}_done_orders'
        cache.set(active_orders_key, active_orders, timeout=CACHE_TTL)
        cache.set(done_orders_key, done_orders, timeout=CACHE_TTL)

    return
