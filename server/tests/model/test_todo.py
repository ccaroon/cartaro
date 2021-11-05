import arrow
import unittest

from cartaro.model.todo import Todo
from cartaro.model.tag import Tag
class TodoTest(unittest.TestCase):

    def setUp(self):
        self.todo = Todo(
            title="Fix the drive plate on deck C", 
            description="Replace with new ones if necessary.",
            priority=1,
            repeat=0,
            due_at=arrow.now().shift(days=+7),
            is_completed=True,
            completed_at=arrow.now(),
        )

    def test_serialize(self):
        data = self.todo.serialize()

        self.assertEqual(self.todo.title, data['title'])
        self.assertEqual(self.todo.description, data['description'])

        self.assertEqual(self.todo.priority, data['priority'])
        self.assertEqual(self.todo.repeat, data['repeat'])
        self.assertEqual(self.todo.due_at.int_timestamp, data['due_at'])

        self.assertEqual(self.todo.is_complete, data['is_complete'])
        self.assertEqual(self.todo.completed_at.int_timestamp, data['completed_at'])


    def test_tagging(self):
        self.assertIsNotNone(self.todo.tags)
        self.assertIsInstance(self.todo.tags, set)
        self.assertEqual(len(self.todo.tags), 0)

        self.todo.tag("maintenance")
        self.todo.tag("deckc")
        self.assertEqual(len(self.todo.tags), 2)
        self.assertIsInstance(list(self.todo.tags)[0], Tag)

        self.todo.save()

        note2 = Todo(id=self.todo.id)
        note2.load()
        self.assertIsNotNone(note2.tags)
        self.assertIsInstance(note2.tags, set)
        self.assertEqual(len(note2.tags), 2)
        self.assertIsInstance(list(note2.tags)[0], Tag)

        self.assertTrue(Tag(name="maintenance") in note2.tags)
