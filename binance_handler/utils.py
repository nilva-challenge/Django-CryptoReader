import time
from binance import Client
import requests
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule

schedule, created = IntervalSchedule.objects.get_or_create(every=30, period=IntervalSchedule.SECONDS, )

base_url = "https://data.binance.com"


def binance_api_list_of_open_positions(key, secret):
   end_point = "/api/v3/openOrders"
   print("DISHDISH")
   return requests.get(base_url + end_point)
    #return client.futures_account()['positions']


def create_or_delete_celery_task(user, track):
    binance_api_list_of_open_positions(user.binance_key, user.binance_secret)
    if track:
        PeriodicTask.objects.get_or_create(interval=schedule, name=f"User({user.pk})",
                                           task='binance_handler.tasks.tracking_position_per_user',
                                           args=json.dumps([f"{user.pk}"]), )
        return {'message': 'Tracking Enabled'}

    PeriodicTask.objects.filter(name=f"User({user.pk})").delete()

    return {'message': 'Tracking Disabled'}
