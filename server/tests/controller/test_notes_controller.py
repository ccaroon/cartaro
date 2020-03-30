import unittest
import cartaro
import faker

from cartaro.model.note import Note
# ------------------------------------------------------------------------------
class NotesControllerTest(unittest.TestCase):

    FAKER = faker.Faker()

    def __gen_notes(self, count, ts='', cs=''):
        for i in range(0, count):
            note = Note(title=F"{self.FAKER.name()} - {ts}", content=F"{self.FAKER.text()} - {cs}")
            note.save()

    def setUp(self):
        # New Note for testing
        self.note = Note(title=self.FAKER.name(), content=self.FAKER.text())
        self.note.save()

        # Setup Flask Testing
        cartaro.flask_app.config['TESTING'] = True
        self.client = cartaro.flask_app.test_client()

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

    def test_find_pagination(self):
        # Create a bunch of notes
        self.__gen_notes(50)

        # Page 1, Default PP
        r = self.client.get('/notes/')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 10)
        self.assertGreaterEqual(data['total'], 50)

        notes = data['notes']
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 10)

        # Page 1, 25 PP
        r = self.client.get('/notes/?pp=25')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 25)
        self.assertGreaterEqual(data['total'], 50)

        notes = data['notes']
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 25)

        # Save to compare below
        note_1 = notes[0]
        note_10 = notes[9]
        
        # Default: page 3, pp 10
        r = self.client.get('/notes/?page=3&pp=10')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 3)
        self.assertEqual(data['per_page'], 10)
        self.assertGreaterEqual(data['total'], 50)

        notes = data['notes']
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 10)
        self.assertNotEqual(notes[0]['id'], note_1['id'])
        self.assertNotEqual(notes[9]['id'], note_10['id'])

        # Bad page specifier - str instead of int
        r = self.client.get('/notes/?page=one')
        data = r.get_json()
        self.assertEqual(r.status_code, 500)
        self.assertRegexpMatches(data['error'], "invalid literal for int\(\) with base 10: 'one'")

    def test_find_search(self):
        self.__gen_notes(15)
        self.__gen_notes(8, ts="Astrium")
        self.__gen_notes(7, cs="Xenomorph")

        # Single Param Search - 1
        r = self.client.get('/notes/?title=Astrium')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 10)
        self.assertEqual(data['total'], 8)

        notes = data['notes']
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 8)

        # Single Param Search - 2
        r = self.client.get('/notes/?content=Xenomorph')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 10)
        self.assertEqual(data['total'], 7)

        notes = data['notes']
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 7)

        # Mult Param Search - 1
        r = self.client.get('/notes/?title=Astrium&content=Xenomorph&pp=25')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 25)
        self.assertEqual(data['total'], 15)

        notes = data['notes']
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 15)

        # Mult Param Search - 2
        r = self.client.get('/notes/?title=Astrium&content=Xenomorph&page=2&pp=12')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['per_page'], 12)
        self.assertEqual(data['total'], 15)

        notes = data['notes']
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 3)

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

    def test_delete(self):
        note = Note(title=self.FAKER.name(), content=self.FAKER.text())
        note.save()

        # Safe Delete
        r = self.client.delete(F"/notes/{note.id}?safe=1")
        self.assertEqual(r.status_code, 200)

        r_data = r.get_json()
        self.assertIsNotNone(r_data.get('id', None))
        self.assertEqual(note.id, r_data.get('id', None))

        del_note = Note(id=note.id)
        del_note.load()
        self.assertIsNotNone(del_note.deleted_at)

        # Real Delete
        r = self.client.delete(F"/notes/{note.id}")
        self.assertEqual(r.status_code, 200)

        r_data = r.get_json()
        self.assertIsNotNone(r_data.get('id', None))
        self.assertEqual(note.id, r_data.get('id', None))

        del_note = Note(id=note.id)
        with self.assertRaisesRegex(ValueError, F'Record Not Found: \[{note.id}\]'):
            del_note.load()

        # Non-existent
        r = self.client.delete("/notes/777777")
        self.assertEqual(r.status_code, 404)

        r_data = r.get_json()
        self.assertIsNotNone(r_data.get('error', None))
        self.assertRegexpMatches(r_data['error'], "Not Found")
