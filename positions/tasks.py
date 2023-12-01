import asyncio

from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from positions.functions import fetch_all_users_order, update_orders

logger = get_task_logger(__name__)
User = get_user_model()


@shared_task
async def tracking_positions():
    """
         Tracking position of each user every 30 seconds
    """
    users = User.objects.filter(is_active=True).all()
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(fetch_all_users_order(users))
    update_orders(results)
