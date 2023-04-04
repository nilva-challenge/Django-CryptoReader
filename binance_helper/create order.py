from binance.spot import Spot

spot_base_url = "https://testnet.binance.vision"
key = "hi2TSZxdE8k66UBmQsc2LSouVngMtS0CuaiTc3u4MiLcfsJtM693riv6b4Cq5by3"
secret = "3qarC4gnuFWcjTBvxg1YjaRaOXaKetefvxGDD4os8McMzWy9NEd9BAainGL3xwqv"

cl = Spot(
    key,
    secret,
    base_url="https://testnet.binance.vision"
)

symbol = 'ETHUSDT'

r = cl.new_order(
    symbol=symbol,
    side="SELL",
    type="Market",
    timeInForce="GTC",
    quantity=10,
    price=1479
)

r = cl.get_open_orders()

print(r)
