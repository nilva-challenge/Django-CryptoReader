from .utils import update_orders
from accounts.models import User
from crypto_reader.celery import app


@app.task(name='kucoin.tasks.tracking_position_per_user')
def tracking(user_pk):
    '''
        Tracking position of each user every 30 seconds
    '''

    user = User.objects.get(pk=user_pk)
    update_orders(user)
