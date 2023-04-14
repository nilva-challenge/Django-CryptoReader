import binascii
from typing import Union
from cryptography.fernet import Fernet
from abc import ABC , abstractmethod


class AbsSymmetric(ABC):

    @abstractmethod
    def encrypt(self,to_encrypt):
        pass

    @abstractmethod
    def decrypt(self,to_decrypt):
        pass


class SymmetricEncryptor(AbsSymmetric):
    """
    Upon instantiating we store the kdf which is needed to encrypt and decrypt secrets
    """

    def __init__(self,kdf:bytes):
        self.__kdf = kdf


    def encrypt(self,to_encrypt : str) -> Union[str,bool]:
        """
        uses the kdf and encrypts the provided 'to_encrypt' parameter

        :param to_encrypt: the raw data that we want to encrypt like api key etc ...
        :return:
        """
        try:
            f = Fernet(self.__kdf)
            must_kept_secret = f.encrypt(bytes(to_encrypt,encoding='utf8'))
        except binascii.Error:
            return False
        except TypeError:
            return False
        return must_kept_secret.decode("utf-8")

    def decrypt(self,to_decrypt:str) -> Union[str,bool]:
        """
        uses the kdf and decrypts the provided 'to_encrypt' parameter
        :param to_decrypt: the raw data that we want to decrypt like encrypted api key etc ...
        :return:
        """
        try:
            f = Fernet(self.__kdf)
            revealed_secret = f.decrypt(bytes(to_decrypt,encoding='utf8'))
        except binascii.Error:
            return False
        except TypeError:
            return False
        return revealed_secret.decode("utf-8")