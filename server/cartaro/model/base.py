import arrow
import itertools
import json
import os
import re

from abc import ABC, abstractmethod
from datetime import datetime
from tinydb import TinyDB, Query
import tinydb.operations as tyops
# ------------------------------------------------------------------------------
# Configure JSONEncoder to look for "for_json" method when serializing classes
# ------------------------------------------------------------------------------
def __class_encoder(self, obj):
    return getattr(obj.__class__, "for_json", __class_encoder.default)(obj)

__class_encoder.default = json.JSONEncoder().default
json.JSONEncoder.default = __class_encoder
# ------------------------------------------------------------------------------
# IMPORTANT NOTES:
# 1. `id` is not stored in the database as part of the record. It is "external"
#     metadata: db = {"1": { rec1 }, "2": { rec2 }, ...  }
# 2. Datetime fields are assumed to be Arrow instances in code and epoch timestamps when serialized.
# ------------------------------------------------------------------------------
class Base(ABC):
    __DATABASE = None

    def __init__(self, id=None, **kwargs):
        kwargs['id'] = id
        self.__base_instantiate(kwargs)

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

    @classmethod
    def _database(cls):
        if not cls.__DATABASE:
            env = os.environ.get("CARTARO_ENV", "dev")
            doc_dir = os.environ.get("CARTARO_DOC_PATH", ".")

            db_name = cls.__name__
            if (env != "prod"):
                db_name += F"-{env}"

            cls.__DATABASE = TinyDB(F"{doc_dir}/{db_name}.json")

        return cls.__DATABASE

    def __base_instantiate(self, data):
        self.__id = data.get('id', None)

        # Shared Attributes
        ## Timestamps
        created_at = data.get('created_at', None)
        updated_at = data.get('updated_at', None)
        deleted_at = data.get('deleted_at', None)

        # Datetimes are assumed to be in UTC epoch format
        # Convert UTC timestamps to TZ specific Arrow instances
        # NOTE: ^^^^^ is that true? ^^^^^
        # TODO: Don't hard-code TZ
        tz = 'US/Eastern'
        self.__created_at = arrow.get(datetime.fromtimestamp(created_at), tz) if created_at else None
        self.__updated_at = arrow.get(datetime.fromtimestamp(updated_at), tz) if updated_at else None
        self.__deleted_at = arrow.get(datetime.fromtimestamp(deleted_at), tz) if deleted_at else None

    @abstractmethod
    def _instantiate(self, data):
        raise NotImplementedError("_instantiate is an Abstract Method and must be overridden")

    def load(self):
        if self.id:
            data = self._database().get(doc_id=self.id)

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
            self._database().update(self.for_json(omit_id=True), doc_ids=[self.id])
        else:
            self.__created_at = now
            self.__id = self._database().insert(self.for_json(omit_id=True))

    def delete(self, safe=False):
        if self.id:
            now = arrow.now()
            self.__deleted_at = now

            try:
                if safe:
                    # Mark as deleted by setting the `deleted_at` date instead of
                    # actually removing the record.
                    self._database().update(tyops.set('deleted_at', self.__deleted_at.timestamp), doc_ids=[self.id])
                else:
                    self._database().remove(doc_ids=[self.id])

                self.__id = None
            except KeyError as ke:
                raise ValueError(F"Record Not Found: [{self.id}]")
        else:
            raise ValueError(F"Valid Object ID required for deletion: [{self.id}]")

    @abstractmethod
    def _for_json(self):
        raise NotImplementedError("_for_json is an Abstract Method and must be overridden")

    def _base_for_json(self, omit_id=False):
        data = {
            "created_at": self.created_at.timestamp if self.created_at else None,
            "updated_at": self.updated_at.timestamp if self.updated_at else None,
            "deleted_at": self.deleted_at.timestamp if self.deleted_at else None
        }

        if not omit_id:
            data['id'] = self.id

        return data

    def for_json(self, omit_id=False):
        data = self._base_for_json(omit_id)
        data.update(self._for_json())
        return data

    @classmethod
    def fetch(cls, offset=0, count=None):
        docs = []
        
        # Want ALL docs
        if offset == 0 and count is None:
            docs = cls._database().all()
        else:
            if count is None:
                end = None
            else:
                end = offset + count

            db_iter = iter(cls._database())
            docs = itertools.islice(db_iter, offset, end)

        objs = []
        for doc in docs:
            objs.append(cls(id=doc.doc_id, **doc))

        return objs

    @classmethod
    def count(cls):
        return len(cls._database())

    # NOTE:
    # Currently only supports searching string fields
    # TODO:
    # - intelligent searching based on type
    @classmethod
    def find(cls, op="or", **kwargs):
        query_parts = []
        query_builder = Query()
        
        for (field, value) in kwargs.items():
            query_parts.append(query_builder[field].search(value, flags=re.IGNORECASE))

        query = query_parts[0]
        if op == "or":
            for qp in query_parts:
                query |= qp
        elif op == "and":
            for qp in query_parts:
                query &= qp

        docs = cls._database().search(query)

        objs = []
        for doc in docs:
            objs.append(cls(id=doc.doc_id, **doc))

        return objs






#
