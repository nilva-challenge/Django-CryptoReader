from kucoin.client import User as KuUser
from django.contrib.auth import get_user_model
from readers.models import Account
import redis
import pickle

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
        raise Exception('Error connecting to server')

def update_positions_for_user(user:User) -> None:
    """
        Update all positions in account of user
        params:
            - user : user
    """
    account_list = get_account_for_user(user)
    bulk_accounts = []
    # make a bulk list to for create_bulk
    for item in account_list:
        account = Account(**item)
        account.user = user
        bulk_accounts.append(account)
    # Won't work on Oracle and SQLite < 3.24 because of update_conflicts feature
    Account.objects.bulk_create(bulk_accounts, update_conflicts=True, update_fields=['account_type', 'balance', 'available', 'holds'])

def load_positions_from_cach(user:User) -> None:
    """
        Reads all positions in account of user
        params:
            - user : user
    """
    # account_list = get_account_for_user(user)
    # bulk_accounts = []
    # # make a bulk list to for create_bulk
    # for item in account_list:
    #     account = Account(**item)
    #     account.user = user
    #     bulk_accounts.append(account)
    # # Won't work on Oracle and SQLite < 3.24 because of update_conflicts feature
    # Account.objects.bulk_create(bulk_accounts, update_conflicts=True, update_fields=['account_type', 'balance', 'available', 'holds'])

def cache_position_in_redis(user:User) -> None:
    """
        Handles caching positions in redis
    """
    account_list = get_account_for_user(user)
    client = redis.Redis('localhost', port=6379, db=0)
    client.set(f'user_{user.id}', pickle.dumps(account_list))
