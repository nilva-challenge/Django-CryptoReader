from datetime import datetime, timezone, timedelta
import hmac, hashlib
import requests
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from accounts.encryption import decrypt
from crypto_reader.settings import features_base_url, spot_base_url

schedule, created = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS, )


# key = "5009ff8d1413839c0b3af0e097a04a5d26d80f74d3b47939923799cff6439b8d"
# secret = "2d237c8829b1568504af754d014064c0262060cc3926fa7f07e0f0aca161eb11"


def create_query_string():
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
    posix_timestamp_millis = posix_timestamp_micros // 1000
    queryString = "&timestamp=" + str(posix_timestamp_millis)
    return queryString


def create_signature(user):
    queryString = create_query_string()
    secret = decrypt(user.binance_secret)
    signature = hmac.new(secret.encode(), queryString.encode(), hashlib.sha256).hexdigest()
    return signature


def features_binance_api_list_of_orders(user):
    query_string = create_query_string()
    signature = create_signature(user)
    end_point = "/fapi/v1/openOrders"
    url = features_base_url + end_point
    url = url + f"?{query_string}&signature={signature}"

    key = decrypt(user.binance_key)
    return requests.get(url, headers={'X-MBX-APIKEY': key}).json()


def features_binance_api_list_of_positions(user):
    query_string = create_query_string()
    signature = create_signature(user)
    end_point = "/fapi/v2/positionRisk"
    url = features_base_url + end_point
    url = url + f"?{query_string}&signature={signature}"
    key = decrypt(user.binance_key)
    data = requests.get(url, headers={'X-MBX-APIKEY': key}).json()
    return data


def features_binance_account_data(user):
    query_string = create_query_string()
    signature = create_signature(user)
    end_point = "/fapi/v2/balance"
    url = features_base_url + end_point
    url = url + f"?{query_string}&signature={signature}"
    key = decrypt(user.binance_key)
    data = requests.get(url, headers={'X-MBX-APIKEY': key}).json()
    return data


def spot_binance_api_list_of_orders(user):
    query_string = create_query_string()
    signature = create_signature(user)
    end_point = "/sapi/v1/openOrders"
    url = spot_base_url + end_point
    url = url + f"?{query_string}&signature={signature}"

    key = decrypt(user.binance_key)
    return requests.get(url, headers={'X-MBX-APIKEY': key}).json()


def spot_binance_api_list_of_positions(user):
    query_string = create_query_string()
    signature = create_signature(user)
    end_point = "/sapi/v1/capital/config/getall"
    url = spot_base_url + end_point
    url = url + f"?{query_string}&signature={signature}"
    key = decrypt(user.binance_key)
    data = requests.get(url, headers={'X-MBX-APIKEY': key}).json()
    return data


def spot_binance_account_data(user):
    query_string = create_query_string()
    signature = create_signature(user)
    end_point = "/sapi/v2/balance"
    url = spot_base_url + end_point
    url = url + f"?{query_string}&signature={signature}"
    key = decrypt(user.binance_key)
    data = requests.get(url, headers={'X-MBX-APIKEY': key}).json()
    return data


def create_or_delete_celery_task(user, track):
    schedule, created = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS, )

    if track:
        PeriodicTask.objects.get_or_create(interval=schedule, name=f"User({user.pk})",
                                           start_time=datetime.now(timezone.utc),
                                           task='tracking',
                                           args=json.dumps([f"{user.pk}"]), )
        return {'message': 'Tracking Enabled'}

    PeriodicTask.objects.all().delete()
    return {'message': 'Tracking Disabled'}
