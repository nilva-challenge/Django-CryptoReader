# tasks.py
import re
import requests
import time
import hmac
import hashlib
import base64
from dataclasses import dataclass
import pprint
from django.core.cache import cache
from datetime import timedelta


# from django.contrib.auth import get_user_model
#
# User = get_user_model()


# from celery import shared_task

#
# # @shared_task
# def track_positions(user_id):
#     # get user details from the database
#     user = CustomUser.objects.get(id=user_id)
#
#     # connect to KuCoin API
#     client = kucoin.client.User(api_key=user.kucoin_api_key, api_secret=user.kucoin_api_secret)
#
#     # track positions every 30 seconds
#     while True:
#         # get open positions
#         positions = client.get_open_positions()
#
#         # update cache with positions data
#         cache_key = f'user_{user_id}_positions'
#         cache.set(cache_key, positions, timeout=timedelta(seconds=30))
#
#         # sleep for 30 seconds
#         time.sleep(30)

@dataclass
class Utility:
    camel_pat = re.compile(r'([A-Z])')
    under_pat = re.compile(r'_([a-z])')

    api_key: str = None
    api_secret: str = None
    api_passphrase: str = None
    user: object = None
    output: dict = None

    def __post_init__(self):
        self.api_key = self.api_key or self.user.kucoin_api_key
        self.api_secret = self.api_secret or self.user.kucoin_api_secret
        self.api_passphrase = self.api_passphrase or self.user.kucoin_passphrase
        self.output = self.get_positions()

    def _camel_to_underscore(self, name: str) -> str:
        return self.camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)

    def _internal_value(self, data: dict) -> dict:
        return {self._camel_to_underscore(k): v for k, v in data.items()}

    def get_positions(self) -> dict:
        url = 'https://api-futures.kucoin.com/api/v1/position?symbol=XBTUSDM'
        now = int(time.time() * 1000)
        str_to_sign = str(now) + 'GET' + '/api/v1/position?symbol=XBTUSDM'
        signature = base64.b64encode(
            hmac.new(self.api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(
            hmac.new(self.api_secret.encode('utf-8'), self.api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2"
        }
        response = requests.request('get', url, headers=headers)
        pprint.pprint(response.status_code)
        pprint.pprint(response.json())
        return self._internal_value(data=response.json()['data'])


if __name__ == '__main__':
    output = Utility(api_key="643ac410317fa70001647b44",
                     api_secret="ffe1e63c-1467-405b-99d4-6c59b491755c",
                     api_passphrase="9219474").output
    pprint.pprint(output)
    #
    # print({camel_to_underscore(k): v for k, v in data.items()})
