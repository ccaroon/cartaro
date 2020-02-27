import arrow
import unittest

from server.model.base import Base

# ------------------------------------------------------------------------------
# Since server.model.base.Base is an Abstract Class we have to create a concrete
# class for testing purposes.
# ------------------------------------------------------------------------------
class DropDaBase(Base):
    def __init__(self, id=None, **kwargs):
        super().__init__(id)
        self._instantiate(kwargs)

    @property
    def state(self):
        return self.__state

    def analyze(self):
        if self.decibels >= 120:
            self.__state = 808
        else:
            self.__state = 0

    def _instantiate(self, data):
        self.name = data.get('name', None)
        self.decibels = data.get('decibels', 0)
        self.__state = data.get('state', 0)

    def _for_json(self):
        return {
            "name": self.name,
            "decibels": self.decibels,
            "state": self.state
        }
# ------------------------------------------------------------------------------
class BaseTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_abstractness(self):
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class Base with abstract methods"):
            obj = Base()

        with self.assertRaisesRegex(NotImplementedError, "_instantiate is an Abstract Method and must be overridden"):
            Base._instantiate(None, {})

        with self.assertRaisesRegex(NotImplementedError, "_for_json is an Abstract Method and must be overridden"):
            Base._for_json(None)

    def test_id(self):
        # Valid
        obj = DropDaBase(id=42)
        self.assertIsNotNone(obj.id)

        # Invalid - Not an INT
        obj = DropDaBase(id=42.7)
        self.assertIsNone(obj.id)

        # Invalid - Not an INT
        obj = DropDaBase(id="77")
        self.assertIsNone(obj.id)

        # Invalid - Zero (0)
        obj = DropDaBase(id=0)
        self.assertIsNone(obj.id)

        # Invalid - falsy
        obj = DropDaBase(id=False)
        self.assertIsNone(obj.id)

        # Invalid - falsy
        obj = DropDaBase(id="")
        self.assertIsNone(obj.id)

        # Invalid - True (Not an INT)
        obj = DropDaBase(id=False)
        self.assertIsNone(obj.id)

    def test_save(self):
        # Create
        obj = DropDaBase(name="Flux", decibels=120)
        self.assertIsNone(obj.id)
        self.assertIsNone(obj.created_at)
        self.assertIsNone(obj.updated_at)
        self.assertIsNone(obj.deleted_at)
        
        obj.save()
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.created_at)
        self.assertIsNone(obj.updated_at)
        self.assertIsNone(obj.deleted_at)
        
        now = arrow.now().timestamp
        self.assertTrue(now-5 <= obj.created_at.timestamp <= now)

        # Update
        id = obj.id
        created = obj.created_at
        obj.name = "DJ Magic Mike"
        obj.decibels = 180
        
        obj.save()

        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.id, id)
        self.assertEqual(obj.created_at, created)
        self.assertIsNotNone(obj.updated_at)
        self.assertIsNone(obj.deleted_at)

        now = arrow.now().timestamp
        self.assertTrue(now-5 <= obj.updated_at.timestamp <= now)

    def test_load(self):
        # Success
        obj = DropDaBase(name="The Punkins'", decibels=120)
        obj.analyze()
        
        obj.save()
        self.assertIsNotNone(obj.id)
        self.assertEquals(obj.state, 808)

        obj2 = DropDaBase(id=obj.id)
        self.assertIsNone(obj2.name)
        self.assertEquals(obj2.decibels, 0)
        self.assertEquals(obj2.state, 0)

        obj2.load()
        self.assertEquals(obj2.id, obj.id)
        self.assertEquals(obj2.name, obj.name)
        self.assertEquals(obj2.decibels, obj.decibels)
        self.assertEquals(obj2.state, obj.state)
        self.assertEqual(type(obj2.created_at), arrow.Arrow)

        # Fail - Bad ID
        obj = DropDaBase(id="cupcake")
        with self.assertRaisesRegex(ValueError, 'Valid Object ID required for loading'):
            obj.load()

        # Fail - No record with ID
        obj = DropDaBase(id=999999999)
        with self.assertRaisesRegex(ValueError, 'Record Not Found: \[999999999\]'):
            obj.load()

    def test_delete_safe(self):
        obj = DropDaBase(name="Silly Putty")
        
        obj.save()
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.created_at)
        self.assertIsNone(obj.deleted_at)

        obj_id = obj.id

        obj.delete(safe=True)
        self.assertIsNone(obj.id)
        self.assertIsNotNone(obj.deleted_at)

        now = arrow.now().timestamp
        self.assertTrue(now-5 <= obj.deleted_at.timestamp <= now)

        with self.assertRaisesRegex(ValueError, 'Valid Object ID required for loading'):
            obj.load()

        with self.assertRaisesRegex(RuntimeError, "Can't Save ... Object deleted"):
            obj.save()

        with self.assertRaisesRegex(ValueError, 'Valid Object ID required for deletion'):
            obj.delete()

        # Should still be able to load it via a new instance
        obj2 = DropDaBase(id=obj_id)
        obj2.load()
        self.assertEqual(obj2.name, obj.name)
        self.assertIsNotNone(obj2.deleted_at)

    def test_delete(self):
        obj = DropDaBase(name="Flutterby")
        
        obj.save()
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.created_at)
        self.assertIsNone(obj.deleted_at)

        obj_id = obj.id

        # REALLY delete
        obj.delete()
        self.assertIsNone(obj.id)
        self.assertIsNotNone(obj.deleted_at)
        
        now = arrow.now().timestamp
        self.assertTrue(now-5 <= obj.deleted_at.timestamp <= now)

        with self.assertRaisesRegex(ValueError, 'Valid Object ID required for loading'):
            obj.load()

        with self.assertRaisesRegex(RuntimeError, "Can't Save ... Object deleted"):
            obj.save()

        with self.assertRaisesRegex(ValueError, 'Valid Object ID required for deletion'):
            obj.delete()

        # Should NOT be able to load it
        obj2 = DropDaBase(id=obj_id)
        with self.assertRaisesRegex(ValueError, F"Record Not Found: \[{obj_id}\]"):
            obj2.load()











#