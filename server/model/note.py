from .base import Base

class Note(Base):
    def __init__(self, id=None, title=None, content=None):
        super().__init__(id)
        self._instantiate(title=title, content=content)

    def _instantiate(self, **data):
        self.title = data.get('title', None)
        self.content = data.get('content', None)
        self.is_favorite = data.get('is_favorite', False)
        self.__is_encrypted = data.get('is_encrypted', False)

    @property
    def is_encrypted(self):
        return self.__is_encrypted

    # TODO: implement
    def encrypt(self):
        self.__is_encrypted = True

    # TODO: implement
    def decrypt(self):
        self.__is_encrypted = False

    def to_json(self):
        data = super().to_json()
        data.update({
            "title": self.title,
            "content": self.content,
            "is_favorite": self.is_favorite,
            "is_encrypted": self.__is_encrypted
        })
        return (data)
