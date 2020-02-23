# TinyDB Questions
# * Does it handle create, update, delete dates?
# * Object serialization or do I need to implement `to_json`

class Base:
    def __init__(self, id=None):
        print(F"Base init: {id}")
        self._instantiate(id=id)

    @property
    def id(self):
        return self.__id

    @property
    def created_at(self):
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    @property
    def deleted_at(self):
        return self.__deleted_at

    def _instantiate(self, **data):
        print(F"Base INST: {data.get('id', 'X')}")
        self.__id = data.get('id', None)

        self.__created_at = data.get('created_at', None)
        self.__updated_at = data.get('updated_at', None)
        self.__deleted_at = data.get('deleted_at', None)

    def load(self):
        # error if not self.__id
        # figure out database name
        # select data
        data = {
            'title': "How To Kung-Fu",
            'created_at': "C",
            'updated_at': "U",
            'deleted_at': "D"
        }
        self._instantiate(**data)

    def save(self):
        pass

    def delete(self):
        pass
