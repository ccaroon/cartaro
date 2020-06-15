import arrow
import inflector
import itertools
import json
import os
import re

from abc import ABC, abstractmethod
from datetime import datetime
from tinydb import TinyDB, Query
import tinydb.operations as tyops
# ------------------------------------------------------------------------------
# Configure JSONEncoder to look for "serialize" method when serializing classes
# ------------------------------------------------------------------------------
def __class_encoder(self, obj):
    return getattr(obj.__class__, "serialize", __class_encoder.default)(obj)

__class_encoder.default = json.JSONEncoder().default
json.JSONEncoder.default = __class_encoder
# ------------------------------------------------------------------------------
# IMPORTANT NOTES:
# 1. `id` is not stored in the database as part of the record. It is "external"
#     metadata: db = {"1": { rec1 }, "2": { rec2 }, ...  }
# 2. Datetime fields are assumed to be Arrow instances in code and epoch timestamps when serialized.
# ------------------------------------------------------------------------------
class Base(ABC):
    # TODO: Don't hard-code TZ
    # TOOD: Use UTC
    TIMEZONE = 'US/Eastern'
    
    __DATABASE = None

    def __init__(self, id=None, **kwargs):
        kwargs['id'] = id
        self.__unserialize(kwargs)

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
            inflect = inflector.Inflector()

            env = os.environ.get("CARTARO_ENV", "dev")
            doc_dir = os.environ.get("CARTARO_DOC_PATH", ".")

            db_name = inflect.pluralize(cls.__name__)
            if (env != "prod"):
                db_name += F"-{env}"

            cls.__DATABASE = TinyDB(F"{doc_dir}/{db_name}.json")

        return cls.__DATABASE

    def _date_setter(self, date_value, null_ok=False):
        new_date = None

        if isinstance(date_value, arrow.Arrow):
            new_date = date_value
        elif isinstance(date_value, int):
            new_date = self._epoch_to_date_obj(date_value)
        elif not date_value and null_ok:
            new_date = None
        else:
            raise TypeError(F"Date must be of type INT or Arrow; Got: {type(date_value)}")

        return new_date

    def _epoch_to_date_obj(self, ts):
        # Datetimes are assumed to be in UTC epoch format
        # Convert UTC timestamps to TZ specific Arrow instances
        # NOTE: ^^^^^ is that true? ^^^^^
        date_obj = arrow.get(datetime.fromtimestamp(ts), Base.TIMEZONE) if ts else None
        return date_obj

    def load(self):
        if self.id:
            data = self._database().get(doc_id=self.id)

            if data:
                data['id'] = data.doc_id
                self.__unserialize(data)
            else:
                raise ValueError(F"Record Not Found: [{self.id}]")
        else:
            raise ValueError(F"Valid Object ID required for loading: [{self.id}]")

    def _pre_save(self):
        pass

    def save(self):
        now = arrow.now()

        if self.deleted_at:
            raise RuntimeError(F"Can't Save ... Object deleted [{self.deleted_at.humanize()}].")

        # Pre Save
        self._pre_save()

        # Save
        if self.id:
            self.__updated_at = now
            self._database().update(self.serialize(omit_id=True), doc_ids=[self.id])
        else:
            self.__created_at = now
            self.__id = self._database().insert(self.serialize(omit_id=True))

        # Post Save
        self._post_save()

    def _post_save(self):
        pass

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
    def _serialize(self):
        raise NotImplementedError("_serialize is an Abstract Method and must be overridden")


    def serialize(self, omit_id=False):
        # Shared Fields
        data = {
            "created_at": self.created_at.timestamp if self.created_at else None,
            "updated_at": self.updated_at.timestamp if self.updated_at else None,
            "deleted_at": self.deleted_at.timestamp if self.deleted_at else None
        }

        if not omit_id:
            data['id'] = self.id

        data.update(self._serialize())
        
        return data

    @abstractmethod
    def update(self, date):
        raise NotImplementedError("update is an Abstract Method and must be overridden")

    def __unserialize(self, data):
        # Shared Attributes
        ## ID
        self.__id = data.get('id', None)

        ## Timestamps
        self.__created_at = self._epoch_to_date_obj(data.get('created_at', None))
        self.__updated_at = self._epoch_to_date_obj(data.get('updated_at', None))
        self.__deleted_at = self._epoch_to_date_obj(data.get('deleted_at', None))

        # Model Specific
        self.update(data)

        self._post_unserialize(data)

    def _post_unserialize(self, data):
        pass

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
    def purge(cls):
        cls._database().purge()

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
            if field == 'tags':
                # NOTE: Does not normalize tags for searching
                tags = value.replace(" ", "").split(',')
                query_parts.append(query_builder['tags'].any(tags))
            else:
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
