from .utils import binance_api_list_of_orders, binance_api_list_of_positions
from accounts.models import User
from .models import Order, Position
from binance_handler.celery import app


@app.task(name='dish')
def tracking(user_pk):
    print("hello")
    user = User.objects.get(pk=user_pk)
    response_for_orders = binance_api_list_of_orders(user)
    response_for_posistions = binance_api_list_of_positions(user)

    for item in response_for_orders:
        Order.objects.update_or_create(
            user=user,
            clientOid=item['clientOrderId'],
            side=item['side'],
            symbol=item['symbol'],
            type=item['type'],
            tradeType=item['origType'],
            isActive=not(item['closePosition'])
        )

    for item in response_for_posistions:
        Position.objects.update_or_create(
            user=user,
            clientOid=item['clientOrderId'],
            side=item['side'],
            symbol=item['symbol'],
            type=item['type'],
            tradeType=item['origType'],
            isActive=not(item['closePosition'])
        )
