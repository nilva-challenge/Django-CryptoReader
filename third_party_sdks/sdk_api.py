from third_party_sdks.kucoin import Kucoin


def fetch_accounts(key, secret, passphrase, id=None) -> dict:
    kucoin = Kucoin(True)
    kucoin.set_key(key)
    kucoin.set_secret(secret)
    kucoin.set_passphrase(passphrase)
    return kucoin.get_account(id)
