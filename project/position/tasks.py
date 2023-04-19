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
from datetime import timedelta
from django.conf import settings
from django_redis import get_redis_connection


@dataclass
class Utility:
    """
    This class implements some functionalities that can be used in
    tracking task in tracking_task function and caching
    """
    camel_pat = re.compile(r'([A-Z])')
    serializer = TrackingPositionSerializer
    domain = 'https://api-futures.kucoin.com'

    redis_conn: object
    symbol_name: str = 'XBTUSDM'
    context: dict = None
    api_key: str = None
    api_secret: str = None
    api_passphrase: str = None
    user: dict = None
    output: dict = None  # data is fetched from KuCoins
    data: dict = None

    def __post_init__(self):
        self.api_key = self.api_key or self.user.get('kucoin_api_key')
        self.api_secret = self.api_secret or self.user.get('kucoin_api_secret')
        self.api_passphrase = self.api_passphrase or self.user.get('kucoin_passphrase')
        self.output = self.get_positions()
        #
        self._validated_data = self.serializing_output()

    def _set_cache(self) -> None:
        if self.output:
            _user_id = self.context.get("user_id")

            # the structure of cache key is `cache_key_{symbol_name}_{user_id}`
            self.redis_conn.set(f'cache_key_{self.symbol_name}_{_user_id}', json.dumps(self.output))
            self.redis_conn.expire(f'cache_key_{_user_id}', timedelta(seconds=settings.INTERVAL - 5))

    def serializing_output(self):
        if self.output is not None:
            s = self.serializer(data=self.output, context=self.context)
            s.is_valid(raise_exception=True)
            s.save()
            # Set cache
            self._set_cache()
            return s.data
        return None

    def _camel_to_underscore(self, name: str) -> str:
        return self.camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)

    def _internal_value(self, data: dict) -> dict:
        return {self._camel_to_underscore(k): v for k, v in data.items()}

    def get_positions(self) -> dict | None:
        # For position details
        url = f'{self.domain}/api/v1/position?symbol={self.symbol_name}'

        now = int(time.time() * 1000)
        # For position details
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
        response = requests.request('get', url, headers=headers).json()
        data = response.get('data')
        if data:
            return self._internal_value(data=data)
        else:
            print(response)
            return None


@shared_task
def tracking_task(user, context):
    redis_conn = get_redis_connection("default")
    print("Tracking task---------> START")
    Utility(user=user, context=context, redis_conn=redis_conn)
    print("Tracking task---------> Done")
