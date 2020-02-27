import arrow
import json
import os

from abc import ABC, abstractmethod
from datetime import datetime
from tinydb import TinyDB, Query
import tinydb.operations as tyops
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
    __DATABASE = None

    def __init__(self, id=None):
        self.__base_instantiate({'id': id})
        self.__open_db()

    @classmethod
    def __open_db(cls):
        if not cls.__DATABASE:
            env = os.environ.get("CARTARO_ENV", "dev")
            doc_dir = os.environ.get("CARTARO_DOC_PATH", ".")
            
            db_name = cls.__name__
            if (env != "prod"):
                db_name += F"-{env}"

            cls.__DATABASE = TinyDB(F"{doc_dir}/{db_name}.json")

    def __base_instantiate(self, data):
        self.__id = data.get('id', None)

        # Datetimes are assumed to be in UTC epoch format
        created_at = data.get('created_at', None)
        updated_at = data.get('updated_at', None)
        deleted_at = data.get('deleted_at', None)

        # Convert UTC timestamps to TZ specific Arrow instances
        # TODO: Don't hard-code TZ
        tz = 'US/Eastern'
        self.__created_at = arrow.get(datetime.fromtimestamp(created_at), tz) if created_at else None
        self.__updated_at = arrow.get(datetime.fromtimestamp(updated_at), tz) if updated_at else None
        self.__deleted_at = arrow.get(datetime.fromtimestamp(deleted_at), tz) if deleted_at else None

    @abstractmethod
    def _instantiate(self, data):
        raise NotImplementedError("_instantiate is an Abstract Method and must be overridden")

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
            data = self.__DATABASE.get(doc_id=self.id)

            if data:
                data['id'] = data.doc_id
                self.__base_instantiate(data)
                self._instantiate(data)
            else:
                raise ValueError(F"Record Not Found: [{self.id}]")
        else:
            raise ValueError(F"Valid Object ID required for loading: [{self.id}]")

    def save(self):
        now = arrow.now()

        if self.deleted_at:
            raise RuntimeError(F"Can't Save ... Object deleted [{self.deleted_at.humanize()}].")

        if self.id:
            self.__updated_at = now
            self.__DATABASE.update(self.for_json(), doc_ids=[self.id])
        else:
            self.__created_at = now
            self.__id = self.__DATABASE.insert(self.for_json())

    def delete(self, safe=False):
        if self.id:
            now = arrow.now()
            self.__deleted_at = now
            
            if safe:
                # Mark as deleted by setting the `deleted_at` date instead of
                # actually removing the record.
                self.__DATABASE.update(tyops.set('deleted_at', self.__deleted_at.timestamp), doc_ids=[self.id])
            else:
                self.__DATABASE.remove(doc_ids=[self.id])

            self.__id = None
        else:
            raise ValueError(F"Valid Object ID required for deletion: [{self.id}]")

    @abstractmethod
    def _for_json(self):
        raise NotImplementedError("_for_json is an Abstract Method and must be overridden")

    def _base_for_json(self):
        return {
            # "id": self.id,
            "created_at": self.created_at.timestamp if self.created_at else None,
            "updated_at": self.updated_at.timestamp if self.updated_at else None,
            "deleted_at": self.deleted_at.timestamp if self.deleted_at else None
        }

    def for_json(self):
        data = self._base_for_json()
        data.update(self._for_json())
        return data

    # @classmethod
    # def find(cls, **kwargs):
    #     pass







# 
