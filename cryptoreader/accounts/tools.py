import base64

from cryptography.fernet import Fernet

from django.conf import settings


def encrypt(pas):
    try:
        pas = str(pas)
        cipher_pass = Fernet(settings.SECRET_KEY)
        encrypt_pass = cipher_pass.encrypt(pas.encode("ascii"))
        encrypt_pass = base64.urlsafe_b64encode(encrypt_pass).decode("ascii")
        return encrypt_pass
    except Exception as e:
        return None


def decrypt(pas):
    try:
        pas = base64.urlsafe_b64decode(pas)
        cipher_pass = Fernet(settings.SECRET_KEY)
        decod_pass = cipher_pass.decrypt(pas).decode("ascii")
        return decod_pass
    except Exception as e:
        return None
