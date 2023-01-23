from .utils import binance_api_list_of_open_positions
from accounts.models import User
from .models import Order
from crypto_reader.celery import app


@app.task(name='tracking_position_per_user')
def tracking(user_pk):
    user = User.objects.get(pk=user_pk)
    response = binance_api_list_of_open_positions(user.binance_key, user.binance_secret)

    for item in response:
        Order.objects.update_or_create(
            user=user,
            clientOid=item['clientOrderId'],
            side=item['side'],
            symbol=item['symbol'],
            type=item['type'],
            tradeType=item['origType'],
            isActive=not(item['closePosition'])
        )
