from cryptography.fernet import Fernet
import base64
from django.conf import settings


def encrypt(text):
    text = str(text)
    cipher_suite = Fernet(settings.ENCRYPT_KEY)
    encrypted_text = cipher_suite.encrypt(text.encode('ascii'))
    encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
    return encrypted_text


def decrypt(text):
    text = base64.urlsafe_b64decode(text)
    cipher_suite = Fernet(settings.ENCRYPT_KEY)
    decoded_text = cipher_suite.decrypt(text).decode("ascii")
    return decoded_text
