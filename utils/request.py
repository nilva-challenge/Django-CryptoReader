from kucoin.client import User as KuUser
from django.contrib.auth import get_user_model

from .encryption import decrypt

User = get_user_model()

def get_account_for_user(user:User) -> list:
    client = KuUser(decrypt(user.api_key), decrypt(user.api_secret), decrypt(user.api_passphrase))
    # Request for accounts using Kucoin SDK
    account_list = client.get_account_list()
    # Transaction success
    if account_list['code'] == '200000':
        return account_list['data']
    else:
        raise Exception('Error connecting to Kucoin server')
