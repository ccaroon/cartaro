from .base import Base

class Tag(Base):

    _TAGGABLE = False

    def __init__(self, id=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self._instantiate(kwargs)

    @property
    def name(self):
        return self.__name

    def _instantiate(self, data):
        self.__name = data.get('name', None)

    def _for_json(self):
        return {
            "name": self.name
        }

    def __eq__(self, value):
        return self.name == value.name
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
