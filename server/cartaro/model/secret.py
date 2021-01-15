from .base import Base
from .taggable import Taggable

class Secret(Taggable, Base):

    TYPE_USER_PASS  = 'user-pass'
    TYPE_TOKEN      = 'token'
    TYPE_KEY_SECRET = 'key-secret'

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
        self.data = None
        self.note = None

        super().__init__(id=id, **kwargs)

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

    def _serialize(self):
        data =  {
            'name': self.name,
            'system': self.system,
            'sub_system': self.sub_system,
            'type': self.type,
            'data': self.data,
            'note': self.note
        }

        # Tags
        data.update(super()._serialize())

        return data

    def update(self, data):
        self.name = data.get('name', self.name)
        self.system = data.get('system', self.system)
        self.sub_system = data.get('sub_system', self.sub_system)
        self.type = data.get('type', self.type)
        self.data = data.get('data', self.data)
        self.note = data.get('note', self.note)

        if self.data is None:
            self.data = Secret.forge(self.type, **data)

    def _post_unserialize(self, data):
        # Tags
        super()._unserialize(data)
