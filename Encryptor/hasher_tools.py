import base64
from typing import Union
import decouple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from decouple import config




def hasher(raw_content:Union[str,bytes]) -> bytes:
    """
    The main function to generate a kdf . hashes the given raw_content parameter
    :param raw_content: The raw byte or str we want to hash
    :return: hashed raw content
    """
    raw_content = raw_content if type(raw_content) == str else raw_content.decode('utf-8')
    try:
        salt = bytes(config("salt"), encoding='utf8')
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
        hashed_content = base64.urlsafe_b64encode(kdf.derive(bytes(raw_content,encoding='utf-8')))
    except decouple.UndefinedValueError:
        raise NotImplementedError({'salt': 'Not found'})
    except SyntaxError as e:
        raise SyntaxError(e)

    return hashed_content

def check_pass_phrase(user,pass_phrase:str) -> bool:
    """
    checks if the provided pass phrase is correct with hashing pass phrase and comparing it to the hashed pass phrase in db
    :param user:
    :param pass_phrase:
    :return:
    """
    hashed_pass = hasher(pass_phrase)
    return hashed_pass.decode('utf-8') == user.security_passphrase