# django_celery/celery.py

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoCryptoReader.settings")
app = Celery("DjangoCryptoReader")
app.config_from_object(settings, namespace="CELERY")

app.conf.beat_schedule = {
    'track_order':{
        'task':'order.tasks.refresh_orders',
        'schedule':30,
    }
}
app.autodiscover_tasks()