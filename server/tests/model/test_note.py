import unittest

from cartaro.model.note import Note
from cartaro.model.tag import Tag
class NoteTest(unittest.TestCase):

    def setUp(self):
        self.note = Note(title="Say Hi", content="Hello, World!")

    def test_serialize(self):
        data = self.note.serialize()

        self.assertEqual(self.note.title, data['title'])
        self.assertEqual(self.note.content, data['content'])
        self.assertEqual(self.note.is_favorite, data['is_favorite'])
        self.assertEqual(self.note.is_encrypted, data['is_encrypted'])

    # encrypt -> decrypt in memory
    def test_encrypt_decrypt(self):
        passwd = "frog blast the vent core"
        orig_content = self.note.content        

        self.note.encrypt(passwd)
        self.assertTrue(self.note.is_encrypted)
        self.assertNotEqual(self.note.content, orig_content)

        self.note.decrypt(passwd)
        self.assertFalse(self.note.is_encrypted)
        self.assertEqual(self.note.content, orig_content)

    # Test encrypt -> save -> load -> decrypt
    def test_encrypt_decrypt2(self):
        passwd = "7ru7h"
        orig_content = self.note.content

        self.note.encrypt(passwd)
        self.assertNotEqual(self.note.content, orig_content)
        self.note.save()

        note2 = Note(id=self.note.id)
        note2.load()
        self.assertEqual(note2.title, self.note.title)
        self.assertEqual(note2.content, self.note.content)
        self.assertNotEqual(note2.content, orig_content)

        note2.decrypt(passwd)
        self.assertEqual(note2.content, orig_content)

    def test_encrypt_error(self):
        orig_content = self.note.content
        self.assertFalse(self.note.is_encrypted)
        
        # invalid password
        with self.assertRaisesRegex(RuntimeError, "Failed to encrypt: 'password' cannot be empty or None"):
            self.note.encrypt("")

        self.assertFalse(self.note.is_encrypted)
        self.assertEqual(self.note.content, orig_content)

    def test_decrypt_error(self):
        orig_content = self.note.content
        self.assertFalse(self.note.is_encrypted)

        self.note.encrypt("bannana")
        self.assertTrue(self.note.is_encrypted)
        self.assertNotEqual(self.note.content, orig_content)
        
        # wrong password
        with self.assertRaisesRegex(RuntimeError, "Failed to decrypt"):
            self.note.decrypt("penquin")

        self.assertTrue(self.note.is_encrypted)
        self.assertNotEqual(self.note.content, orig_content)

    def test_tagging(self):
        self.assertIsNotNone(self.note.tags)
        self.assertIsInstance(self.note.tags, set)
        self.assertEqual(len(self.note.tags), 0)

        self.note.tag("Hello")
        self.note.tag("World")
        self.assertEqual(len(self.note.tags), 2)
        self.assertIsInstance(list(self.note.tags)[0], Tag)

        self.note.save()

        note2 = Note(id=self.note.id)
        note2.load()
        self.assertIsNotNone(note2.tags)
        self.assertIsInstance(note2.tags, set)
        self.assertEqual(len(note2.tags), 2)
        self.assertIsInstance(list(note2.tags)[0], Tag)

        self.assertTrue(Tag(name="Hello") in note2.tags)











# 
