from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from account.models import User
from .models import OrderDetail
from celery import shared_task
from utils.utility import CallAPI


@shared_task
def refresh_orders():
    """ 
    Just track active order 
    """
    users = User.objects.all()
    for user in users:
        obj = OrderDetail()
        try:
            active_orders = CallAPI(
                (user, '/api/v1/positions', 'GET', {'status': 'active'}, True))
            active_order_response = active_orders.create_request()
            obj.id = active_order_response['id']
            obj.symbol = active_order_response['symbol']
            obj.save()
        except Exception as e:
            raise Exception(e)
