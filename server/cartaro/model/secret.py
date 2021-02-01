from .base import Base
from .taggable import Taggable
from cartaro.utils.crypto import Crypto

class Secret(Taggable, Base):

    TYPE_USER_PASS  = 'username-password'
    TYPE_TOKEN      = 'token'
    TYPE_KEY_SECRET = 'key-secret'
    ENCRYPTION_KEY  = None

    TEMPLATES = {
        TYPE_USER_PASS: {
            'username': None,
            'password': None
        },
        TYPE_TOKEN: {
            'token': None,
        },
        TYPE_KEY_SECRET: {
            'key': None,
            'secret': None
        }
    }

    def __init__(self, id=None, **kwargs):
        self.name = None
        self.system = None
        self.sub_system = None
        self.type = None
        self.__data = None
        self.note = None
        self.__encrypted = False

        # TODO: Find a better way to manage encryption key???
        if not self.ENCRYPTION_KEY:
            raise Exception("Secret - Encryption Key not set.")

        self.__cryer = Crypto(self.ENCRYPTION_KEY)

        super().__init__(id=id, **kwargs)

    @property
    def data(self):
        if self.__encrypted:
            self.__decrypt_data()
        return self.__data

    @data.setter
    def data(self, new_data):
        # Assume new_data is in clear text
        self.__data = new_data
        self.__encrypt_data()

    @classmethod
    def forge(cls, stype, **kwargs):
        template = cls.TEMPLATES.get(stype, None)
        if not template:
            raise TypeError(F"Invalid Secret Type: '{stype}'")

        secret = template.copy()
        for attr in secret.keys():
            if attr not in kwargs:
                raise ValueError(F"Secret.forge - Missing Required Value: '{attr}'")

            secret[attr] = kwargs.get(attr)

        return secret

    def __encrypt_data(self):
        if self.__data:
            enc_data = self.__data.copy()
            for attr in enc_data.keys():
                enc_data[attr] = self.__cryer.encrypt(enc_data[attr])

            self.__data = enc_data
            self.__encrypted = True

    def __decrypt_data(self):
        if self.__data:
            clear_data = self.__data.copy()
            for attr in clear_data.keys():
                clear_data[attr] = self.__cryer.decrypt(clear_data[attr])

            self.__data = clear_data
            self.__encrypted = False

    def _serialize(self):
        if not self.__encrypted:
            self.__encrypt_data()

        data =  {
            'name': self.name,
            'system': self.system,
            'sub_system': self.sub_system,
            'type': self.type,
            # MUST access via __data else it will be decrypted
            'data': self.__data,
            'note': self.note,
            '__encrypted': self.__encrypted
        }

        # Tags
        data.update(super()._serialize())

        return data

    def update(self, data):
        self.name = data.get('name', self.name)
        self.system = data.get('system', self.system)
        self.sub_system = data.get('sub_system', self.sub_system)
        self.type = data.get('type', self.type)
        # Access via __data so as to not change the underlying data
        self.__data = data.get('data', self.__data)
        self.note = data.get('note', self.note)
        self.__encrypted = data.get('__encrypted', self.__encrypted)
        self.tags = data.get('tags', self.tags)

        if self.type and self.data is None:
            self.data = Secret.forge(self.type, **data)




#
