from django.conf import settings
from cryptography.fernet import Fernet
import base64
import logging
import traceback

# get the key from settings
f = Fernet(settings.ENCRYPTION_KEY)

def encrypt(raw_txt):
    """
        Function to encrypt raw text using Fernet class
    """
    try:
        # convert integer etc to string first
        txt = str(raw_txt)
        #input should be byte, so convert the text to byte
        encrypted_text = f.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii") 
        return encrypted_text
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(encrypted_txt):
    """
        Function to decrypt encrypted text using Fernet class
    """
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(encrypted_txt)
        # decryption
        decoded_text = f.decrypt(txt).decode("ascii")     
        return decoded_text
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None

