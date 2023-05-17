from celery.utils.log import get_task_logger
from celery import shared_task
from django.contrib.auth import get_user_model
from multiprocessing.dummy import Pool as ThreadPool
from django.conf import settings

from utils.cache import write_positions_in_cache

logger = get_task_logger(__name__)
User = get_user_model()

@shared_task
def cache_positions_all_users():
    """
        Caches all Users positions in redis if service is active.
        Function implements multi-thread processing to boost speed of caching process.
    """
    users = User.objects.all()
    pool = ThreadPool(settings.THREAD_POOL)
    params = list(users)
    results = pool.map(write_positions_in_cache, params)
    