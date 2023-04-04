from datetime import datetime, timezone, timedelta
import hmac, hashlib
import requests
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from accounts.encryption import decrypt
from crypto_reader.settings import FUTURE_BASE_URL, SPOT_BASE_URL, CELERY_PERIOD_TIME

schedule, created = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS, )
from rest_framework import status
from rest_framework.response import Response


# key = "5009ff8d1413839c0b3af0e097a04a5d26d80f74d3b47939923799cff6439b8d"
# secret = "2d237c8829b1568504af754d014064c0262060cc3926fa7f07e0f0aca161eb11"


def create_time_stamp():
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
    posix_timestamp_millis = posix_timestamp_micros // 1000
    time_stamp = "&timestamp=" + str(posix_timestamp_millis)
    return time_stamp


def create_signature(user, market_type):
    query_string = create_time_stamp()
    if market_type == "futures":
        secret = decrypt(user.api_future_secret)
    elif market_type == "spot":
        secret = decrypt(user.api_spot_secret)
    else:
        return Response("market_type is not valid", status=status.HTTP_404_NOT_FOUND)
    signature = hmac.new(query_string.encode(), secret.encode(), hashlib.sha256).hexdigest()
    return signature


def binance_api_list_of_orders(user, market_type):
    query_string = create_time_stamp()
    signature = create_signature(user, market_type)
    if market_type == "features":
        end_pint = "/fapi/v1/openOrders"
        url = FUTURE_BASE_URL + end_pint
        key = decrypt(user.api_future_key)
    elif market_type == "spot":
        end_pint = "/api/v3/openOrders"
        url = SPOT_BASE_URL + end_pint
        key = decrypt(user.api_spot_key)
    else:
        return Response("market_type is not valid", status=status.HTTP_404_NOT_FOUND)

    url = url + f"?{query_string}&signature={signature}"

    print(key)
    return requests.get(url, headers={'X-MBX-APIKEY': key}).json()


def binance_api_list_of_positions(user, market_type):
    query_string = create_time_stamp()
    signature = create_signature(user, market_type)
    if market_type == "features":
        end_point = "/fapi/v2/positionRisk"
        url = FUTURE_BASE_URL + end_point
        key = decrypt(user.api_future_key)
    else:
        return Response("market_type is not valid", status=status.HTTP_404_NOT_FOUND)
    url = url + f"?{query_string}&signature={signature}"
    data = requests.get(url, headers={'X-MBX-APIKEY': key}).json()
    return data


def binance_account_data(user, market_type):
    query_string = create_time_stamp()
    signature = create_signature(user, market_type)
    if market_type == "features":
        end_point = "/fapi/v2/balance"
        url = FUTURE_BASE_URL + end_point
        key = decrypt(user.api_future_key)
    elif market_type == "spot":
        end_point = "/api/v3/account"
        url = SPOT_BASE_URL + end_point
        key = decrypt(user.api_spot_key)
    else:
        return Response("market_type is not valid", status=status.HTTP_404_NOT_FOUND)
    url = url + f"?{query_string}&signature={signature}"
    data = requests.get(url, headers={'X-MBX-APIKEY': key}).json()
    return data


def create_or_delete_celery_task(user, track):
    schedule, created = IntervalSchedule.objects.get_or_create(every=CELERY_PERIOD_TIME, period=IntervalSchedule.SECONDS)

    if track:
        PeriodicTask.objects.get_or_create(interval=schedule, name=f"User({user.pk})",
                                           start_time=datetime.now(timezone.utc),
                                           task='tracking',
                                           args=json.dumps([f"{user.pk}"]), )
        return {'message': 'Tracking Enabled'}

    PeriodicTask.objects.all().delete()
    return {'message': 'Tracking Disabled'}
