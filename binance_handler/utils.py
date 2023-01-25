from datetime import datetime, timezone, timedelta
import hmac, hashlib
import requests
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from accounts.encryption import decrypt
from crypto_reader.settings import base_url

schedule, created = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS, )


def create_query_string():
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
    posix_timestamp_millis = posix_timestamp_micros // 1000
    queryString = "&timestamp=" + str(posix_timestamp_millis)
    return queryString


def create_signature(user):
    queryString = create_query_string()
    signature = hmac.new(user.binance_secret.encode(), queryString.encode(), hashlib.sha256).hexdigest()
    return signature


def binance_api_list_of_orders(user):
    key = decrypt(user.binance_key)
    query_string = create_query_string()
    signature = create_signature(user)
    end_point = ""
    url = base_url + end_point
    url = url + f"?{query_string}&signature={signature}"

    return requests.get(url, headers={'X-MBX-APIKEY': key})


def create_or_delete_celery_task(user, track):
    if track:
        PeriodicTask.objects.get_or_create(interval=schedule, name=f"User({user.pk})",
                                           task='binance_handler.tasks.tracking_orders_per_user',
                                           args=json.dumps([f"{user.pk}"]), )
        return {'message': 'Tracking Enabled'}

    PeriodicTask.objects.filter(name=f"User({user.pk})").delete()
    return {'message': 'Tracking Disabled'}
