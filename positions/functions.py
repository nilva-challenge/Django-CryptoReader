import aiohttp
from django.conf import settings
from django.db import transaction

from positions.models import Order
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
