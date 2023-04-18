# tasks.py
import re
import requests
import time
import hmac
import hashlib
import base64
from dataclasses import dataclass
import json
import pprint
from .serializers import TrackingPositionSerializer
from celery import shared_task

from django.core.cache import cache



@dataclass
class Utility:
    camel_pat = re.compile(r'([A-Z])')
    under_pat = re.compile(r'_([a-z])')
    serializer = TrackingPositionSerializer

    symbol_name: str = 'XBTUSDM'  # or 'XBTUSDT'
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
        self._validated_data = self.serializing_output()

    def _set_cache(self) -> None:
        if self._validated_data:
            _user_id = self.context.get("user_id")
            cache.set(f'cache_key_{_user_id}', json.dumps(self.output), timeout=300)

    def serializing_output(self):
        if self.output is not None:
            s = self.serializer(data=self.output, context=self.context)
            s.is_valid(raise_exception=True)
            s.save()

            # self._set_cache()
            return s.data
        return None

    def _camel_to_underscore(self, name: str) -> str:
        return self.camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)

    def _internal_value(self, data: dict) -> dict:
        return {self._camel_to_underscore(k): v for k, v in data.items()}

    def get_positions(self) -> dict | None:
        # For position details
        url = f'https://api-futures.kucoin.com/api/v1/position?symbol={self.symbol_name}'
        # For positions (list of positions)
        # url = f'https://api-futures.kucoin.com/api/v1/positions'

        now = int(time.time() * 1000)
        # For position details
        str_to_sign = str(now) + 'GET' + f'/api/v1/position?symbol={self.symbol_name}'

        # For positions (list of positions)
        # str_to_sign = str(now) + 'GET' + f'/api/v1/positions'

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

        res = response.json()
        data = res.get('data')
        if data:
            return self._internal_value(data=data)
        else:
            print(res)
            return None

@shared_task
def tracking_task(user, context):
    print("Tracking task---------> START")
    Utility(user=user, context=context)
    print("Tracking task---------> Done")

# if __name__ == '__main__':
    # output = Utility(api_key="643ac410317fa70001647b44",
    #                  api_secret="ffe1e63c-1467-405b-99d4-6c59b491755c",
    #                  api_passphrase="9219474").output
    # output = Utility(api_key="643e5c90d3b4b7000149c88c",
    #                  api_secret="2e03da19-254e-4556-8055-553c62b4d44c",
    #                  api_passphrase="9219474").output
    # pprint.pprint(output)
    #
#     # print({camel_to_underscore(k): v for k, v in data.items()})
