import arrow
import random
import unittest

from cartaro.model.base import Base
# ------------------------------------------------------------------------------
# Since cartaro.model.base.Base is an Abstract Class we have to create a concrete
# class for testing purposes.
# ------------------------------------------------------------------------------
class Ticket(Base):    
    def __init__(self, id=None, **kwargs):
        self.name = None
        self.desc = None
        self.use_count = 0
        self.active = False

        super().__init__(id=id, **kwargs)

    @classmethod
    def purge(cls):
        cls._database().purge()
    
    def update(self, data):
        self.name = data.get('name', self.name)
        self.desc = data.get('desc', self.desc)
        self.use_count = data.get('use_count', self.use_count)
        self.active = data.get('active', self.active)

    def _serialize(self):
        return {
            'name': self.name,
            'desc': self.desc,
            'use_count': self.use_count,
            'active': self.active
        }

# ------------------------------------------------------------------------------
class BaseTest(unittest.TestCase):

    def setUp(self):
        # Delete all records
        Ticket.purge()

    def test_abstractness(self):
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class Base with abstract methods"):
            obj = Base()

        with self.assertRaisesRegex(NotImplementedError, "update is an Abstract Method and must be overridden"):
            Base.update(None, {})

        with self.assertRaisesRegex(NotImplementedError, "_serialize is an Abstract Method and must be overridden"):
            Base._serialize(None)

    def test_id(self):
        # Valid
        obj = Ticket(id=42)
        self.assertIsNotNone(obj.id)

        # Invalid - Not an INT
        obj = Ticket(id=42.7)
        self.assertIsNone(obj.id)

        # Invalid - Not an INT
        obj = Ticket(id="77")
        self.assertIsNone(obj.id)

        # Invalid - Zero (0)
        obj = Ticket(id=0)
        self.assertIsNone(obj.id)

        # Invalid - falsy
        obj = Ticket(id=False)
        self.assertIsNone(obj.id)

        # Invalid - falsy
        obj = Ticket(id="")
        self.assertIsNone(obj.id)

        # Invalid - True (Not an INT)
        obj = Ticket(id=False)
        self.assertIsNone(obj.id)

    def test_serialize(self):
        obj = Ticket(id=42, name="Water Usage", desc="Turn off the water", active=False)

        # With ID
        data = obj.serialize()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.id, data['id'])
        self.assertEqual(obj.name, data['name'])
        self.assertEqual(obj.desc, data['desc'])
        self.assertEqual(obj.active, data['active'])

        # W/O ID
        data = obj.serialize(omit_id=True)
        self.assertIsNotNone(obj.id)
        self.assertIsNone(data.get('id', None), None)
        self.assertEqual(obj.name, data['name'])
        self.assertEqual(obj.desc, data['desc'])
        self.assertEqual(obj.active, data['active'])

    def test_save(self):
        # Create
        obj = Ticket(name="Grow Veges", desc="Plant a garden. Eat it's bounty.")
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
        obj.name = "Buy Local Produce"
        obj.desc = "You don't have to grow; Buy Local!!"

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
        obj = Ticket(name="Smile", desc="Brush your teeth. Keep them pearlies white.")

        obj.save()
        self.assertIsNotNone(obj.id)

        obj2 = Ticket(id=obj.id)
        self.assertIsNone(obj2.name)

        obj2.load()
        self.assertEquals(obj2.id, obj.id)
        self.assertEquals(obj2.name, obj.name)
        self.assertEquals(obj2.desc, obj.desc)
        self.assertEquals(obj2.active, obj.active)
        self.assertEqual(type(obj2.created_at), arrow.Arrow)

        # Fail - Bad ID
        obj = Ticket(id="cupcake")
        with self.assertRaisesRegex(ValueError, 'Valid Object ID required for loading'):
            obj.load()

        # Fail - No record with ID
        obj = Ticket(id=999999999)
        with self.assertRaisesRegex(ValueError, 'Record Not Found: \[999999999\]'):
            obj.load()

    def test_delete_safe(self):
        obj = Ticket(name="Silly Putty", desc="All work and no play makes Jack a dull boy.")

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
        obj2 = Ticket(id=obj_id)
        obj2.load()
        self.assertEqual(obj2.name, obj.name)
        self.assertIsNotNone(obj2.deleted_at)

    def test_delete(self):
        obj = Ticket(name="Flutterby", desc="Start a butterfly collection.")

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
        obj2 = Ticket(id=obj_id)
        with self.assertRaisesRegex(ValueError, F"Record Not Found: \[{obj_id}\]"):
            obj2.load()

    def test_delete_nonexistent(self):
        obj = Ticket(id=77777, name="No Running", desc="Fix the toilet. It's running.")

        with self.assertRaisesRegex(ValueError, F"Record Not Found: \[{obj.id}\]"):
            obj.delete()

    def test_fetch(self):
        # Create a bunch of new records
        record_count = 50
        for i in range(0, record_count):
            d = Ticket(name=F"Ticket #{i+1}", desc=F"Step #{i}")
            d.save()

        # Load All
        objs = Ticket.fetch()
        self.assertEqual(len(objs), record_count)
        self.assertIsInstance(objs[0], Ticket)
        self.assertEqual(objs[49].id, 50)

        # Limit - First 5
        offset = 0
        count = 5
        objs = Ticket.fetch(offset, count)
        self.assertEqual(len(objs), count)
        for i in range(1, count):
            self.assertEqual(objs[i-1].id, i + offset)

        # Limit - Second 5
        offset = 5
        count = 5
        objs = Ticket.fetch(offset, count)
        self.assertEqual(len(objs), count)
        for i in range(1, count):
            self.assertEqual(objs[i-1].id, i + offset)

        # Limit - Last 2
        count = 2
        offset = record_count - count
        objs = Ticket.fetch(offset, count)
        self.assertEqual(len(objs), count)
        self.assertEqual(objs[0].id, 49)
        self.assertEqual(objs[1].id, 50)

        # Limit - Last 5
        offset = record_count - 5
        objs = Ticket.fetch(offset)
        self.assertEqual(len(objs), 5)
        self.assertEqual(objs[0].id, 46)
        self.assertEqual(objs[1].id, 47)
        self.assertEqual(objs[2].id, 48)
        self.assertEqual(objs[3].id, 49)
        self.assertEqual(objs[4].id, 50)

    def test_count(self):
        # Create a bunch of new records
        record_count = random.randint(1, 100)
        for i in range(0, record_count):
            d = Ticket(name=F"Ticket #{i+1}", desc=F"{i} / {record_count}")
            d.save()

        count = Ticket.count()
        self.assertIsNotNone(count)
        self.assertEqual(count, record_count)

    def test_find(self):
        # Create a couple objs
        obj1 = Ticket(name="Xenomorph - 42", desc="Weyland-Yutani Specimen #42")
        obj1.save()

        obj2 = Ticket(name="Xenomorph - 88", desc="Weyland-Yutani Specimen #88")
        obj2.save()

        obj3 = Ticket(name="BOB - ID#7", desc="Marathon - Born on Board - #7")
        obj3.save()

        # Find #1 - OR
        things = Ticket.find(name="Xeno|BOB")
        self.assertEquals(len(things), 3)

        self.assertEqual(things[0].id, obj1.id)
        self.assertEqual(things[0].name, obj1.name)

        self.assertEqual(things[1].id, obj2.id)
        self.assertEqual(things[1].name, obj2.name)

        self.assertEqual(things[2].id, obj3.id)
        self.assertEqual(things[2].name, obj3.name)

        # Find #2 - OR
        things = Ticket.find(name="88", desc="Born on Board")
        self.assertEquals(len(things), 2)

        self.assertEqual(things[0].id, obj2.id)
        self.assertEqual(things[0].name, obj2.name)

        self.assertEqual(things[1].id, obj3.id)
        self.assertEqual(things[1].name, obj3.name)

        # Find #3 - AND - 0 hits
        things = Ticket.find("and", name="BOB", desc="Green Suit Scaredie Cats")
        self.assertEquals(len(things), 0)

        # Find #4 - AND
        things = Ticket.find("and", name="Xeno", desc="Specimen #88")
        self.assertEquals(len(things), 1)

        self.assertEqual(things[0].id, obj2.id)
        self.assertEqual(things[0].name, obj2.name)
