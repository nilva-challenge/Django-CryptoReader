from celery.utils.log import get_task_logger
from celery import shared_task
from django.contrib.auth import get_user_model
from multiprocessing.dummy import Pool as ThreadPool

from utils.request import cache_position_in_redis

logger = get_task_logger(__name__)
User = get_user_model()

@shared_task
def cach_positions_all_users():
    users = User.objects.all()
    pool = ThreadPool(4)
    params = list(users)
    results = pool.map(cache_position_in_redis, params)
    