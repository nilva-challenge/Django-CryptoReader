# tasks.py
import re
import requests
import time
import hmac
import hashlib
import base64
from dataclasses import dataclass
import pprint
from .serializers import TrackingPositionSerializer
from celery import shared_task

from django.core.cache import cache
from datetime import timedelta


@dataclass
class Utility:
    camel_pat = re.compile(r'([A-Z])')
    under_pat = re.compile(r'_([a-z])')
    serializer = None
    serializer = TrackingPositionSerializer

    symbol_name: str = 'XBTUSDM'
    context: dict = None
    api_key: str = None
    api_secret: str = None
    api_passphrase: str = None
    user: dict = None
    output: dict = None
    data: dict = None

    def __post_init__(self):
        self.api_key = self.api_key or self.user.get('kucoin_api_key')
        self.api_secret = self.api_secret or self.user.get('kucoin_api_secret')
        self.api_passphrase = self.api_passphrase or self.user.get('kucoin_passphrase')
        self.output = self.get_positions()
        #
        self.data = self.serializing_output()

    def serializing_output(self):
        s = self.serializer(data=self.output, context=self.context)
        s.is_valid(raise_exception=True)
        s.save()
        return s.data

    def _camel_to_underscore(self, name: str) -> str:
        return self.camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)

    def _internal_value(self, data: dict) -> dict:
        return {self._camel_to_underscore(k): v for k, v in data.items()}

    def get_positions(self) -> dict:
        url = f'https://api-futures.kucoin.com/api/v1/position?symbol={self.symbol_name}'
        now = int(time.time() * 1000)
        str_to_sign = str(now) + 'GET' + f'/api/v1/position?symbol={self.symbol_name}'
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
        # pprint.pprint(response.json())
        return self._internal_value(data=response.json()['data'])


@shared_task
def tracking_task(user, context):
    print("Tracking task---------> START")
    Utility(user=user, context=context)
    print("Tracking task---------> Done")

# if __name__ == '__main__':
#     output = Utility(api_key="643ac410317fa70001647b44",
#                      api_secret="ffe1e63c-1467-405b-99d4-6c59b491755c",
#                      api_passphrase="9219474").output
#     pprint.pprint(output)
#     #
#     # print({camel_to_underscore(k): v for k, v in data.items()})
