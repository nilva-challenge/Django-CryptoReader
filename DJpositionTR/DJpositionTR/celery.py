import os
from datetime import timedelta
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DJpositionTR.settings")

app = Celery("DJpositionTR")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"


app.conf.beat_schedule = {
    'read-open-positions-every-30-sec': {
        'task': 'DjReader.tasks.trackPositions',
        'schedule': timedelta(seconds=30),
    },
}