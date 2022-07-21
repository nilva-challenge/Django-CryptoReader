from celery import Celery
from celery.utils.log import get_task_logger

# setup django env
import init_django

from cryptoreader.accounts import models, serializers
from django.http import HttpRequest

from third_party_sdks.sdk_api import fetch_accounts

app = Celery("tasks", broker="redis://localhost:6379/2")
logger = get_task_logger(__name__)


def load_accounts_from_kucoin_by_user(user) -> dict:
    login_info = user.get_key(), user.get_secret(), user.get_passphrase()
    accounts = fetch_accounts(*login_info)
    return accounts


@app.task
def update_kucoin_account(username):
    """fetch kucoin accounts and insert data
    to DB

    Args:
        username (str): username of user (Model User)
    """

    try:
        user = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
        logger.debug("user not found")
        return

    try:
        account = load_accounts_from_kucoin_by_user(user)
    except Exception as error:
        logger.debug(error)
        return

    request = HttpRequest()
    request.user = user
    context = {"request": request}
    serializer = serializers.KucoinAccountSerializer(
        data=account, many=True, context=context
    )

    try:
        serializer.is_valid(True)
        serializer.save()
        logger.info(serializer.data)
    except Exception as error:
        logger.debug(error)

    return None


@app.task
def update_all_user_kucoin_account():
    """fetch all avilable users and run a task for each"""

    users = models.User.objects.all()
    for user in users:
        update_kucoin_account.delay(user.username)
