import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class Crypto:
    def __init__(self, password):
        if not password:
            raise ValueError("'password' cannot be empty or None")

        key = self.__password_to_key(password)
        self.__fernet = Fernet(key)

    # @classmethod
    # def generate_key(cls):
    #     return Fernet.generate_key()

    @classmethod
    def __password_to_key(cls, password):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(password, 'utf-8'))
        return base64.urlsafe_b64encode(digest.finalize())

    def encrypt(self, plain_text):
        cipher_text = self.__fernet.encrypt(bytes(plain_text, "utf-8"))
        return cipher_text.decode("utf-8")

    def decrypt(self, cipher_text):
        clear_text = self.__fernet.decrypt(bytes(cipher_text, "utf-8"))
        return clear_text.decode("utf-8")
