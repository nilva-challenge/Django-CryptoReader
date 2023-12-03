import base64
import hashlib
import hmac
import time


def get_nonce():
    return str(int(time.time() * 1000))


def create_signature(endpoint, nonce, secret):
    message = f'{endpoint}/{nonce}'
    signature = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature


def kucoin_api(user, endpoint):
    user_kucoin_data = user.decrypt_kucoin_data()
    api_key = user_kucoin_data['api_key']
    api_secret = user_kucoin_data['api_secret']
    api_passphrase = user_kucoin_data['api_passphrase']

    nonce = get_nonce()
    signature = create_signature(endpoint, nonce, api_secret)

    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), signature.encode('utf-8'), hashlib.sha256).digest())

    passphrase = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())

    headers = {
        'KC-API-SIGN': signature,
        'KC-API-TIMESTAMP': nonce,
        'KC-API-KEY': api_key,
        'KC-API-PASSPHRASE': passphrase,
        'KC-API-KEY-VERSION': '2'
    }

    return headers


def get_open_orders(user):
    endpoint = '/api/v1/orders'
    return kucoin_api(user, endpoint)
