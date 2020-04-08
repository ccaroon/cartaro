from .base import Base
from .taggable import Taggable
from cartaro.utils.crypto import Crypto

class Note(Taggable, Base):
    def __init__(self, id=None, **kwargs):
        super().__init__(id=id, **kwargs)

    def _unserialize(self, data):
        self.title = data.get('title', None)
        self.content = data.get('content', None)
        self.is_favorite = data.get('is_favorite', False)
        self.__is_encrypted = data.get('is_encrypted', False)

        # Tags
        super()._unserialize(data)

    @property
    def is_encrypted(self):
        return self.__is_encrypted

    def encrypt(self, passwd):
        orig_content = self.content
        try:
            cryer = Crypto(passwd)
            self.content = cryer.encrypt(orig_content)
            self.__is_encrypted = True
        except Exception as e:
            self.__is_encrypted = False
            self.content = orig_content
            raise RuntimeError(F"Failed to encrypt: {e}")

    def decrypt(self, passwd):
        orig_content = self.content
        try:
            cryer = Crypto(passwd)
            self.content = cryer.decrypt(self.content)
            self.__is_encrypted = False
        except Exception as e:
            self.__is_encrypted = True
            self.content = orig_content
            raise RuntimeError(F"Failed to decrypt: <{e}>")

    def _serialize(self):
        data = {
            "title": self.title,
            "content": self.content,
            "is_favorite": self.is_favorite,
            "is_encrypted": self.__is_encrypted
        }
        # Tags
        data.update(super()._serialize())
        
        return data







# 
