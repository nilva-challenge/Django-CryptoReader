from .utils import binance_api_list_of_orders, binance_api_list_of_positions, \
    binance_account_data
from accounts.models import User
from .models import Order, Position, Wallet
from crypto_reader.celery import app
from datetime import datetime


@app.task(name='tracking')
def tracking(user_pk):
    user = User.objects.get(pk=user_pk)
    response_for_features_orders = binance_api_list_of_orders(user, "features")
    response_for_features_positions = binance_api_list_of_positions(user, "features")
    response_for_features_profile = binance_account_data(user, "features")

    response_for_spot_orders = binance_api_list_of_orders(user, "spot")
    response_for_spot_profile = binance_account_data(user, "spot")

    print(response_for_features_orders)
    print("YA")

    open_orders_list = []
    for item in response_for_features_orders:
        _, created = Order.objects.update_or_create(
            customer=user,
            market_type="features",
            side=item['side'],
            symbol=item['symbol'],
            type=item['type'],
            isActive=not (item['closePosition']),
            created_time=datetime.fromtimestamp(item['time'] / 1000),
            price=item['price'],
            amount=item['origQty'],
        )
        if created is False:
            Order.objects.filter(
                customer=user,
                market_type="features",
                side=item['side'],
                symbol=item['symbol'],
                type=item['type'],
                isActive=not (item['closePosition']),
                created_time=datetime.fromtimestamp(item['time'] / 1000),
                price=item['price'],
                amount=item['origQty'],
            ).update(update_time=datetime.now())
        open_orders_dict = {
            "user_id": int(user_pk),
            "market_type": "features",
            "side": item["side"],
            "symbol": item["symbol"],
            "type": item["type"],
            "isActive": not (item['closePosition']),
            "price": float(item["price"]),
        }
        open_orders_list.append(open_orders_dict)

    for obj in Order.objects.filter(market_type="features").values():
        del obj["id"]
        del obj["created_time"]
        del obj["amount"]
        if obj not in open_orders_list and obj["user_id"] in open_orders_list:
            Order.objects.filter(**obj).delete()

    open_positions_list = []
    for item in response_for_features_positions:
        if item['entryPrice'] == "0.0":
            continue
        _, created = Position.objects.update_or_create(
            customer=user,
            market_type="features",
            symbol=item['symbol'],
            entryPrice=item['entryPrice'],
            leverage=item['leverage'],
            created_time=datetime.fromtimestamp(item['time'] / 1000),
            update_time=datetime.fromtimestamp(item['updateTime'] / 1000),
            amount=item["positionAmt"],
        )
        Position.objects.filter(
            customer=user,
            market_type="features",
            symbol=item['symbol'],
            entryPrice=item['entryPrice'],
            leverage=item['leverage'],
            update_time=datetime.fromtimestamp(item['updateTime'] / 1000),
            amount=item["positionAmt"],
        ).update(pnl=item['unRealizedProfit'])

        open_positions_dict = {
            "user_id": int(user_pk),
            "market_type": "features",
            "symbol": item['symbol'],
            "entryPrice": item['entryPrice'],
            "leverage": item['leverage'],
            # "amount": item['positionAmt'],
            # "pnl": item['unRealizedProfit'],
        }

        open_positions_list.append(open_positions_dict)

    for obj in Position.objects.filter(market_type="features").values():
        del obj["id"]
        del obj["created_time"]
        del obj["update_time"]
        del obj["pnl"]
        del obj["amount"]

        if obj not in open_positions_list and obj["user_id"] in open_positions_list:
            Position.objects.filter(**obj).delete()

    for item in response_for_features_profile:
        wallet = Wallet.objects.filter(customer=user, market_type="features")
        if wallet.exists():
            wallet.update(update_time=datetime.now())
            wallet.futures_conis[item['asset']] = item['balance']
            if item['balance'] is '0.0':
                wallet.futures_coins.pop(item['asset'])
            wallet.save()
        else:
            Wallet.objects.create(customer=user, market_type="features", created_time=datetime.now())
            wallet.futures_conis[item['asset']] = item['balance']
            wallet.save()

    open_orders_list = []
    for item in response_for_spot_orders:
        _, created = Order.objects.update_or_create(
            customer=user,
            market_type="spot",
            side=item['side'],
            symbol=item['symbol'],
            type=item['type'],
            isActive=item['isWorking'],
            created_time=datetime.fromtimestamp(item['time'] / 1000),
            price=item['price'],
            amount=item['origQty'],
        )
        if created is False:
            Order.objects.filter(
                customer=user,
                market_type="spot",
                side=item['side'],
                symbol=item['symbol'],
                type=item['type'],
                isActive=item['isWorking'],
                created_time=datetime.fromtimestamp(item['time'] / 1000),
                price=item['price'],
                amount=item['origQty'],
            ).update(update_time=datetime.now())
        open_orders_dict = {
            "user_id": int(user_pk),
            "market_type": "spot",
            "side": item["side"],
            "symbol": item["symbol"],
            "type": item["type"],
            "isActive": item['isWorking'],
            "price": float(item["price"]),
            "amount": item["origQty"]
        }
        open_orders_list.append(open_orders_dict)

    for obj in Order.objects.filter(market_type="spot").values():
        del obj["id"]
        del obj["created_time"]

        if obj not in open_orders_list:
            Order.objects.filter(**obj).delete()

    for item in response_for_spot_profile["balances"]:
        wallet = Wallet.objects.filter(customer=user, market_type="spot")
        if wallet.exists():
            wallet.update(update_time=datetime.now())
            wallet.futures_conis[item['asset']] = item['free']
            if item['balance'] is '0.0':
                wallet.futures_coins.pop(item['asset'])
            wallet.save()
        else:
            Wallet.objects.create(customer=user, market_type="spot", created_time=datetime.now())
            wallet.futures_conis[item['asset']] = item['free']
            wallet.save()
