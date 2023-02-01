from .utils import binance_api_list_of_orders, binance_api_list_of_positions, binance_account_data
from accounts.models import User
from .models import Order, Position, Binance_profile
from crypto_reader.celery import app
from datetime import datetime


@app.task(name='tracking')
def tracking(user_pk):
    user = User.objects.get(pk=user_pk)
    response_for_orders = binance_api_list_of_orders(user)
    response_for_posistions = binance_api_list_of_positions(user)
    response_for_profile = binance_account_data(user)

    for item in response_for_orders:

        Order.objects.update_or_create(
            user=user,
            side=item['side'],
            symbol=item['symbol'],
            type=item['type'],
            tradeType=item['origType'],
            isActive=not (item['closePosition']),
            time=datetime.fromtimestamp(item['time'] / 1000),
            price=item['price']
        )

    for item in response_for_posistions:
        if item['entryPrice'] == "0.0":
            continue
        Position.objects.update_or_create(
            user=user,
            symbol=item['symbol'],
            entryPrice=item['entryPrice'],
            leverage=item['leverage'],
            time=datetime.fromtimestamp(item['updateTime'] / 1000),
        )

    for item in response_for_profile:
        profile = Binance_profile.objects.filter(user=user)
        if item['asset'] == 'BTC':
            if profile.exists():
                profile.update(BTC_wallet=item['balance'])
            else:
                Binance_profile.objects.create(user=user, BTC_wallet=item['balance'])

        if item['asset'] == 'BNB':
            if profile.exists():
                profile.update(BNB_wallet=item['balance'])

            else:
                Binance_profile.objects.create(user=user, BNB_wallet=item['balance'])

        if item['asset'] == 'ETH':
            if profile.exists():
                profile.update(ETH_wallet=item['balance'])
            else:
                Binance_profile.objects.create(user=user, ETH_wallet=item['balance'])

        if item['asset'] == 'USDT':
            if profile.exists():
                profile.update(USDT_wallet=item['balance'])
            else:
                Binance_profile.objects.create(user=user, USDT_wallet=item['balance'])

        if item['asset'] == 'USDC':
            if profile.exists():
                profile.update(USDC_wallet=item['balance'])
            else:
                Binance_profile.objects.create(user=user, USDC_wallet=item['balance'])

        if item['asset'] == 'BUSD':
            if profile.exists():
                profile.update(BUSD_wallet=item['balance'])
            else:
                Binance_profile.objects.create(user=user, BUSD_wallet=item['balance'])