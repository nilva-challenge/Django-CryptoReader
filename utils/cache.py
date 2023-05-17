from readers.models import Account
from django.contrib.auth import get_user_model

import redis
import pickle

from utils.request import get_account_for_user

User = get_user_model()

def write_positions_in_cache(user:User) -> None:
    """
        Handles caching positions in redis
        If redis was down it will call another function to store data in DB.
        params:
            user : user
    """
    account_list = get_account_for_user(user)
    try:
        client = redis.Redis('localhost', port=6379, db=0)
        client.set(f'user_{user.id}', pickle.dumps(account_list))
    except redis.exceptions.ConnectionError: # Rides down store in DB
        write_to_db(user, account_list)

def read_positions_from_cache(user:User) -> list:
    """
        Reads all positions in account of user
        params:
            - user : user
    """
    try:
        client = redis.Redis('localhost', port=6379, db=0)
        account_list = client.get(f'user_{user.id}') # returns pickled
        if account_list:
            return pickle.loads(account_list)
        else:
            return list()
    except redis.exceptions.ConnectionError: # Rides down store in DB
        return 'DB' # View handles reading from DB if necessary


def write_to_db(user:User, account_list:list) -> None:
    """
        Function to replace storing positions in DB
        params:
            user : user
            account_list : list of position (returned by Kucoin)
    """
    bulk_accounts = []
    for item in account_list:
        print(item)
        account = Account(**item)
        account.user = user
        bulk_accounts.append(account)
    # Won't work on Oracle and SQLite < 3.24 because of update_conflicts feature
    Account.objects.bulk_create(
        bulk_accounts, update_conflicts=True,
        update_fields=['type', 'balance', 'available', 'holds'],
        unique_fields=['id']
    )
