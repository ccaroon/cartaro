import unittest

from server.model.note import Note
class NoteTest(unittest.TestCase):

    def setUp(self):
        self.note = Note(title="Say Hi", content="Hello, World!")

    def test_for_json(self):
        data = self.note.for_json()

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
