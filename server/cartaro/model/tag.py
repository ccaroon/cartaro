import re
from tinydb import where

from .base import Base

class Tag(Base):
    def __init__(self, id=None, **kwargs):
        super().__init__(id=id, **kwargs)

    @property
    def name(self):
        return self.__name

    @classmethod
    def normalize(cls, name):
        norm_name = name.lower()
        norm_name = re.sub('^\W+|\W+$',      '',  norm_name)
        norm_name = re.sub('[^a-zA-Z0-9_\-.]', ' ', norm_name)
        norm_name = re.sub('\s+',            '-', norm_name)

        return norm_name

    @classmethod
    def exists(cls, name):
        return cls._database().contains(where('name') == cls.normalize(name))

    def _unserialize(self, data):
        self.__name = None
        
        tmp_name = data.get('name', None)
        if tmp_name:
            self.__name = self.normalize(tmp_name)

    def _serialize(self):
        return {
            "name": self.name
        }

    def __eq__(self, other_tag):
        return self.name == other_tag.name
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
