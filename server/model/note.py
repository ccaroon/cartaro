from .base import Base

class Note(Base):
    def __init__(self, id=None, title=None, content=None):
        # self.title = title
        # self.content = content
        # self.is_favorite = False
        # self.__is_encrypted = False
        print(F"Calling super init with {id}")
        super().__init__(id)
        self._instantiate(id=id, title=title, content=content)

    def _instantiate(self, **data):
        super()._instantiate(**data)

        self.title = data.get('title', None)
        self.content = data.get('content', None)
        self.is_favorite = data.get('is_favorite', False)
        self.__is_encrypted = data.get('is_encrypted', False)

    # TODO: implement
    def encrypt(self):
        self.__is_encrypted = True

    # TODO: implement
    def decrypt(self):
        self.__is_encrypted = False

    # @classmethod
    # def find(cls,)

# note = Note(id=12)
# note.load()
