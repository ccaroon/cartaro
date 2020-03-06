import unittest
import cartaro
import faker

from cartaro.model.note import Note
# ------------------------------------------------------------------------------
class NotesControllerTest(unittest.TestCase):

    FAKER = faker.Faker()

    def setUp(self):        
        # New Note for testing
        self.note = Note(title=self.FAKER.name(), content=self.FAKER.text())
        self.note.save()
        
        # Setup Flask Testing
        cartaro.flask_app.config['TESTING'] = True
        self.client = cartaro.flask_app.test_client()

    def test_retrieve(self):
        # Normal
        r = self.client.get(F'/notes/{self.note.id}')
        self.assertEqual(r.status_code, 200)
        
        note = r.get_json()
        self.assertIsNone(note.get('error', None))
        
        self.assertEqual(note.get('title', None), self.note.title)
        self.assertEqual(note.get('content', None), self.note.content)

        # Non-existent note
        r = self.client.get('/notes/9999999')
        self.assertEqual(r.status_code, 404)
        
        note = r.get_json()
        self.assertIsNotNone(note.get('error', None))
        self.assertRegexpMatches(note['error'], "Not Found")

    def test_create(self):
        data = {
            'title': self.FAKER.name(),
            'content': self.FAKER.text(),
            'is_favorite': True
        }

        r = self.client.post('/notes/', json=data)
        self.assertEqual(r.status_code, 201)

        r_data = r.get_json()
        self.assertIsNotNone(r_data['id'])

        r = self.client.get(F"/notes/{r_data['id']}")
        self.assertEqual(r.status_code, 200)

        note = r.get_json()
        self.assertEqual(note['id'], r_data['id'])
        self.assertEqual(note['title'], data['title'])
        self.assertEqual(note['content'], data['content'])
        self.assertEqual(note['is_favorite'], data['is_favorite'])


    def test_update(self):
        data = {
            'title': self.FAKER.name(),
            'content': self.FAKER.text(),
            'is_favorite': not self.note.is_favorite
        }

        self.assertNotEqual(self.note.title, data['title'])
        self.assertNotEqual(self.note.content, data['content'])
        self.assertNotEqual(self.note.is_favorite, data['is_favorite'])

        r = self.client.put(F"/notes/{self.note.id}", json=data)
        self.assertEqual(r.status_code, 200)

        r = self.client.get(F"/notes/{self.note.id}")
        self.assertEqual(r.status_code, 200)

        note = r.get_json()
        self.assertEqual(note['title'], data['title'])
        self.assertEqual(note['content'], data['content'])
        self.assertEqual(note['is_favorite'], data['is_favorite'])

        # Update Non-Existent Note
        r = self.client.put("/notes/999999999999", json={'title': 'Nothing Nobody None'})
        self.assertEqual(r.status_code, 404)

        r_data = r.get_json()
        self.assertIsNotNone(r_data.get('error', None))
        self.assertRegexpMatches(r_data['error'], "Not Found")












# 
