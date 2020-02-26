import arrow
import json
import os

from abc import ABC, abstractmethod
from tinydb import TinyDB, Query

# ------------------------------------------------------------------------------
# Configure JSONEncoder to look for "to_json" method when serializing classes
# ------------------------------------------------------------------------------
# def __class_encoder(self, obj):
#     return getattr(obj.__class__, "to_json", __class_encoder.default)(obj)
# 
# __class_encoder.default = json.JSONEncoder().default
# json.JSONEncoder.default = __class_encoder
# ------------------------------------------------------------------------------
# IMPORTANT NOTES:
# 1. `id` is not stored in the database as part of the record. It is "external"
#     metadata: db = {"1": { rec1 }, "2": { rec2 }, ...  }
# ------------------------------------------------------------------------------
class Base(ABC):
    def __init__(self, id=None):
        self.__base_instantiate(id=id)
        
        # Construct DB name
        db_name = type(self).__name__
        env = os.environ.get("CARTARO_ENV", "dev")
        if (env != "prod"):
            db_name += F"-{env}"

        doc_dir = os.environ.get("CARTARO_DOC_PATH", ".")
        # TODO: DB should be a CLASS property
        self.__db_path = F"{doc_dir}/{db_name}.json"
        self.__db = TinyDB(self.__db_path)

    def __base_instantiate(self, **data):
        self.__id = data.get('id', None)

        self.__created_at = data.get('created_at', None)
        self.__updated_at = data.get('updated_at', None)
        self.__deleted_at = data.get('deleted_at', None)

    @abstractmethod
    def _instantiate(self, **data):
        pass

    @property
    def id(self):
        is_valid = False
        if self.__id and isinstance(self.__id, int) and self.__id > 0:
            is_valid = True

        return self.__id if is_valid else None

    @property
    def created_at(self):
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    @property
    def deleted_at(self):
        return self.__deleted_at

    def load(self):
        if self.id:
            data = self.__db.get(doc_id=self.id)

            if data:
                data['id'] = data.doc_id
                self.__base_instantiate(**data)
                self._instantiate(**data)
            else:
                raise ValueError(F"Record Not Found: [{self.id}]")
        else:
            raise ValueError(F"Valid Object ID required for loading: [{self.id}]")

    def save(self):
        now = arrow.now()

        if self.id:
            self.__updated_at = now
            self.__db.update(self.to_json(), doc_ids=[self.id])
        else:
            self.__created_at = now
            self.__id = self.__db.insert(self.to_json())

    # TODO: Support *marked deletion*
    def delete(self):
        if self.id:
            Obj = Query()
            self.__db.remove(Obj.id == self.id)
            self.__id = None
        else:
            raise ValueError(F"Valid Object ID required for deletion: [{self.id}]")

    # TODO: make abstract
    def to_json(self):
        return {
            # "id": self.id,
            "created_at": self.created_at.timestamp if self.created_at else None,
            "updated_at": self.updated_at.timestamp if self.updated_at else None,
            "deleted_at": self.deleted_at.timestamp if self.deleted_at else None
        }

    @classmethod
    def find(cls, **kwargs):
        pass







# 
