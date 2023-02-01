from .utils import features_binance_api_list_of_orders, features_binance_api_list_of_positions, \
    features_binance_account_data, spot_binance_api_list_of_positions, spot_binance_api_list_of_orders, \
    spot_binance_account_data
from accounts.models import User
from .models import Order, Position, Binance_profile
from crypto_reader.celery import app
from datetime import datetime


@app.task(name='tracking')
def tracking(user_pk):
    user = User.objects.get(pk=user_pk)
    response_for_features_orders = features_binance_api_list_of_orders(user)
    response_for_features_positions = features_binance_api_list_of_positions(user)
    response_for_features_profile = features_binance_account_data(user)

    response_for_spot_orders = spot_binance_api_list_of_orders(user)
    response_for_spot_positions = spot_binance_api_list_of_positions(user)
    response_for_spot_profile = features_binance_account_data(user)

    open_orders_list = []
    for item in response_for_features_orders:
        Order.objects.update_or_create(
            user=user,
            market_type="features",
            side=item['side'],
            symbol=item['symbol'],
            type=item['type'],
            tradeType=item['origType'],
            isActive=not (item['closePosition']),
            time=datetime.fromtimestamp(item['time'] / 1000),
            price=item['price']
        )
        open_orders_dict = {
            "user_id": int(user_pk),
            "market_type": "features",
            "side": item["side"],
            "symbol": item["symbol"],
            "type": item["type"],
            "tradeType": item["origType"],
            "isActive": not (item['closePosition']),
            "price": float(item["price"])
        }
        open_orders_list.append(open_orders_dict)

    for obj in Order.objects.all().values():
        del obj["id"]
        del obj["time"]
        if obj not in open_orders_list:
            Order.objects.filter(**obj).delete()

    open_positions_list = []
    for item in response_for_features_positions:
        if item['entryPrice'] == "0.0":
            continue
        Position.objects.update_or_create(
            user=user,
            market_type="features",
            symbol=item['symbol'],
            entryPrice=item['entryPrice'],
            leverage=item['leverage'],
            time=datetime.fromtimestamp(item['updateTime'] / 1000),
        )

        open_positions_dict = {
            "user_id": int(user_pk),
            "market_type": "features",
            "symbol": item['symbol'],
            "entryPrice": item['entryPrice'],
            "leverage": item['leverage']
        }

        open_positions_list.append(open_positions_dict)

        for obj in Position.objects.all().values():
            del obj["id"]
            del obj["time"]
            if obj not in open_positions_list:
                Position.objects.filter(**obj).delete()

    for item in response_for_features_profile:
        profile = Binance_profile.objects.filter(user=user)
        market_type = "features"
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

