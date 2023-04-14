from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCryptoReader.settings')

app = Celery('DjangoCryptoReader')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update_orders': {
        'task': 'core.tasks.update_user_orders',
        'schedule': int(config('SCHEDULE')),
    },

}

app.autodiscover_tasks()
