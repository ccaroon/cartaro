import unittest
import cartaro
import faker

from cartaro.model.note import Note
# ------------------------------------------------------------------------------
class NotesControllerTest(unittest.TestCase):

    FAKER = faker.Faker()

    def setUp(self):
        self.password = "fish"
        
        # New Note for testing
        self.note = Note(title=self.FAKER.name(), content=self.FAKER.text())
        self.note.save()

        # New Encrypted Note for testing
        self.secret_note = Note(title=self.FAKER.name(), content=self.FAKER.text())
        self.secret_note.encrypt(self.password)
        self.secret_note.save()
        self.secret_note.decrypt(self.password)
        
        # Setup Flask Testing
        cartaro.flask_app.config['TESTING'] = True
        self.client = cartaro.flask_app.test_client()

    def test_retrieve(self):
        # Un-encrypted
        r = self.client.get(F'/notes/{self.note.id}')
        self.assertEqual(r.status_code, 200)
        
        note = r.get_json()
        self.assertIsNone(note.get('error', None))
        
        self.assertEqual(note.get('title', None), self.note.title)
        self.assertEqual(note.get('content', None), self.note.content)

        # Encrypted
        r = self.client.get(F'/notes/{self.secret_note.id}')
        self.assertEqual(r.status_code, 200)
        
        secret_note = r.get_json()
        self.assertIsNone(secret_note.get('error', None))
        
        self.assertEqual(secret_note.get('title', None), self.secret_note.title)
        self.assertEqual(secret_note.get('content', None), self.secret_note.content)

        # Non-existent note
        r = self.client.get('/notes/9999999')
        self.assertEqual(r.status_code, 404)
        
        note = r.get_json()
        self.assertIsNotNone(note.get('error', None))
        self.assertRegexpMatches(note['error'], "Not Found")













# 
