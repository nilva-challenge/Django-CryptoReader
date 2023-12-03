import pickle

import aiohttp
import redis
from django.conf import settings
from django.db import transaction

from positions.models import Order
from positions.serializers import OrderSerializers
from utils.ex_request import kucoin_api


def update_orders(results):
    if results:
        with transaction.atomic():
            for user, items in results.items():
                items = results['data']['items']
                for item in items:
                    Order.objects.update_or_create(
                        user=user,
                        client_id=item['clientOid'],
                        side=item['side'],
                        symbol=item['symbol'],
                        type=item['type'],
                        remark=item['remark'],
                        stp=item['stp'],
                        trade_type=item['tradeType'],
                        is_active=item['isActive'])


async def get_headers(users):
    endpoint = '/api/v1/orders'
    headers = {}
    for user in users:
        headers[user] = await kucoin_api(user, endpoint)
    return headers


async def fetch_all_users_order(users):
    tasks = {}
    headers = await get_headers(users)
    async with aiohttp.ClientSession() as session:
        url = settings.KUCOIN_API + '/api/v1/orders'
        for user, header in headers.items():
            async with session.get(url, headers=header) as resp:
                tasks[user] = await resp.json()
    return tasks


def generate_name(user):
    return f'position-{user.id}'


def cache_position(user):
    """
        Cache position in redis
    """
    name = generate_name(user)  # redis name
    redis_instance = settings.REDIS_INSTANCE
    try:
        data = redis_instance.get(name)  # get from redis
        if data:
            data = pickle.loads(data)
            return data

        orders = Order.objects.filter(user=user, is_active=True).all()
        redis_instance.set(name, pickle.dumps(orders), settings.POSITION_EXPIRE)  # set in redis

        return orders

    except (redis.TimeoutError, redis.ConnectionError):  # time out or connection error from redis
        orders = Order.objects.filter(user=user, is_active=True).all()
        return orders
