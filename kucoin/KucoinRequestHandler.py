import base64
import hashlib
import hmac
import time
import urllib.parse
from abc import ABC, abstractmethod
import requests

from Encryptor.hasher_tools import hasher


def now_in_mili() -> int:
    """
    :return: timestamp of now
    """
    return int(time.time() * 1000)


class AbstractKucoin(ABC):

    @abstractmethod
    def header_maker(self):
        pass

    @abstractmethod
    def secret_revealed(self):
        pass

    @abstractmethod
    def url_maker(self):
        pass

    @abstractmethod
    def signature_generator(self):
        pass

    @abstractmethod
    def passphrase_generator(self):
        pass

    @abstractmethod
    def dispatcher(self):
        pass


class Kucoin(AbstractKucoin):
    user_secrets = None

    def __init__(self, user, endpoint: str, method: str, params: dict = None, sandbox: bool = False):
        """

        :param user: a user instance to get values like passphrase and uuid for decrypting secrets
        :param endpoint: used for calling the endpoint of kucoin apis
        :param method: The method we want to use to send request . also needed for creating api sign
        :param params: take any accepted parameter by the kucoin endpoint and sends with the request
        :param sandbox: to get the main url
        """
        self.user = user
        self.endpoint = endpoint
        self.params = params
        self.method = method
        self.sandbox_mode = sandbox
        self.secret_revealed()

    def secret_revealed(self) -> dict:
        """
        uses the 'decrypted_secrets_collection' method of User model to decrypt api key , secret key and pass phrase
        as mentioned before we hash uuid , concatenate it to hashed passphrase and hash it to generate our kdf in which we can decrypt with it

        this method is called upon instantiation , to set value for user_secrets variable
        :return:
        """
        hashed_uuid = hasher(str(self.user.id))
        decryption_kdf = hasher(self.user.security_passphrase + hashed_uuid.decode('utf-8'))
        secrets = self.user.decrypted_secrets_collection(decryption_kdf)
        self.user_secrets = secrets
        return secrets

    def url_maker(self) -> str:
        """
        provides the url we need to send request
        :return:
        """
        if self.sandbox_mode:
            return "https://openapi-sandbox.kucoin.com" + self.endpoint
        return "https://api.kucoin.com" + self.endpoint

    def signature_generator(self) -> bytes:
        """
        according to the kucoin docs , we need to generate a signature using endpoint,method,timestamp of now and params
        and hashing with encrypted secret key
        we add it to the request headers later as "KC-API-SIGN"
        :return:
        """
        api_secret = self.user_secrets.get('kc_secret')
        str_to_sign = str(now_in_mili()) + self.method + self.endpoint + '?' + urllib.parse.urlencode(self.params)
        signature = base64.b64encode(
            hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        return signature

    def passphrase_generator(self) -> bytes:
        """
        use the encrypted secret key and api pass phrase and generate a hashed passphrase
        we add it to the request headers later as "KC-API-PASSPHRASE"
        :return:
        """
        api_secret = self.user_secrets.get('kc_secret')
        api_passphrase = self.user_secrets.get('kc_pp')
        passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        return passphrase

    def header_maker(self) -> dict:
        """
        according to the docs of kucoin , this whole header is needed to be sent with request to authenticate
        :return:
        """
        return {
            "KC-API-SIGN": self.signature_generator(),
            "KC-API-TIMESTAMP": str(now_in_mili()),
            "KC-API-KEY": self.user_secrets.get('kc_apikey'),
            "KC-API-PASSPHRASE": self.passphrase_generator(),
            "KC-API-KEY-VERSION": "2"
        }

    def dispatcher(self) -> dict:
        """
        we dispatch the request with the generated credentials

        we use method variable to determine the method
        generate url by calling url_maker method
        add headers and params that we generated above
        :return:
        """
        response = requests.request(self.method, self.url_maker(), headers=self.header_maker(), params=self.params)
        if response.status_code != 200:
            raise Exception({'Error': response.json()})
        return response.json()
