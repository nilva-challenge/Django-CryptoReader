import re
from cryptography.fernet import Fernet
from decouple import config


def generate_key():
    """
    Generates a key and save it into a file
    """

    key = Fernet.generate_key()
    # with open("random-key.txt", "wb") as key_file:
    #     key_file.write(key)


def load_key():
    """
    Load the previously generated key
    """
    return config('key')


def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(bytes(message, encoding='utf8'))

    # print(encrypted_message.decode("utf-8"))
    return encrypted_message.decode("utf-8")


def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(bytes(encrypted_message, encoding='utf8'))
    # print(decrypted_message.decode("utf-8"))
    return decrypted_message.decode("utf-8")
