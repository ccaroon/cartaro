import unittest

from server.model.note import Note
class NoteTest(unittest.TestCase):

    def setUp(self):
        self.note = Note(title="Say Hi", content="Hello, World!")

    def test_to_json(self):
        data = self.note.to_json()

        self.assertEqual(self.note.title, data['title'])
        self.assertEqual(self.note.content, data['content'])
        self.assertEqual(self.note.is_favorite, data['is_favorite'])
        self.assertEqual(self.note.is_encrypted, data['is_encrypted'])
