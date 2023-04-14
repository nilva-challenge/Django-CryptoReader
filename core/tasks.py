from celery import shared_task

from accounts.models import User
from core.updater import user_updater

@shared_task
def update_user_orders():
    """
    once each 30(can be modified in .env as SCHEDULE) seconds , updates the orders of the users with auto update enabled
    :return:
    """
    users = User.objects.filter(auto_update_orders=True)
    for user in users:
        user_updater.delay(user.username)
    return "Done"