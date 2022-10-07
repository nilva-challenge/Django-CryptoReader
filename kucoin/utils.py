import time
import base64
import hashlib
import hmac
import time
import json
import requests
from accounts.encryption import decrypt
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import Order

schedule, created = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS,)


def kucoin_api(key, secret, passphrase, endpoint) -> tuple:
    '''
        Get data from kucoin with specefic header
    '''

    url = 'https://api.kucoin.com' + endpoint

    # decrypt data
    key = decrypt(key)
    secret = decrypt(secret)
    passphrase = decrypt(passphrase)

    # create signature
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + endpoint
    signature = base64.b64encode(
        hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(
        hmac.new(secret.encode('utf-8'),
                 passphrase.encode('utf-8'),
                 hashlib.sha256).digest())

    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }

    response = requests.request('get', url, headers=headers)
    return response.status_code, response.json()


def create_or_delete_celery_task(user, track):
    '''
        Create or delete celery task based on track field
    '''

    if track:
        PeriodicTask.objects.get_or_create(interval=schedule, name=f"User({user.pk})",
                                           task='kucoin.tasks.tracking_position_per_user',
                                           args=json.dumps([f"{user.pk}"]),)

        return {'message': 'Tracking Enabled'}

    PeriodicTask.objects.filter(name=f"User({user.pk})").delete()

    return {'message': 'Tracking Disabled'}


def update_orders(user):
    '''
        Update order objects for user
    '''

    status, response = kucoin_api(user.kucoin_key, user.kucoin_secret,
                                  user.kucoin_passphrase, '/api/v1/orders')

    if response.get('code') == '200000':
        items = response['data']['items']

        for item in items:
            Order.objects.update_or_create(
                user=user, clientOid=item['clientOid'],
                side=item['side'],
                symbol=item['symbol'],
                type=item['type'],
                remark=item['remark'],
                stp=item['stp'],
                tradeType=item['tradeType'], isActive=item['isActive'])
