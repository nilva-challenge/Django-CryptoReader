from .utils import kucoin_api
from accounts.models import User
from .models import Order
from crypto_reader.celery import app


@app.task(name='kucoin.tasks.tracking_position_per_user')
def tracking(user_pk):
    '''
        Tracking position of each user every 30 seconds
    '''

    user = User.objects.get(pk=user_pk)
    status, response = kucoin_api(user.kucoin_key, user.kucoin_secret,
                                  user.kucoin_passphrase, '/api/v1/orders')

    if response['code'] == '200000':
        items = response['items']

        for item in items:
            Order.objects.update_or_create(
                user=user, clientOid=item['clientOid'],
                side=item['side'],
                symbol=item['symbol'],
                type=item['type'],
                remark=item['remark'],
                stp=item['stp'],
                tradeType=item['tradeType'], isActive=item['isActive'])
