import unittest
import cartaro
import faker

# ------------------------------------------------------------------------------
class Snippet(cartaro.model.base.Base):
    def __init__(self, id=None, **kwargs):
        self.title = None
        self.content = None
        super().__init__(id=id, **kwargs)

    def update(self, data):
        self.title = data.get('title', self.title)
        self.content = data.get('content', self.content)

    def _serialize(self):
        data =  {
            "title": self.title,
            "content": self.content
        }
        return data
# ------------------------------------------------------------------------------
class BaseControllerTest(unittest.TestCase):

    FAKER = faker.Faker()

    def __gen_snippets(self, count, ts='', cs=''):
        for i in range(0, count):
            snippet = Snippet(title=F"{self.FAKER.name()} - {ts}", content=F"{self.FAKER.text()} - {cs}")
            snippet.save()

    @classmethod
    def setUpClass(cls):
        # Setup Flask Testing
        snippets = cartaro.controller.base.create_controller("snippets", Snippet)
        cartaro.flask_app.register_blueprint(snippets, url_prefix="/snippets")
        cartaro.flask_app.config['TESTING'] = True

    def setUp(self):
        Snippet.purge()
        # New Snippet for testing
        self.snippet = Snippet(title=self.FAKER.name(), content=self.FAKER.text())
        self.snippet.save()

        self.client = cartaro.flask_app.test_client()

    def test_create(self):
        data = {
            'title': self.FAKER.name(),
            'content': self.FAKER.text()
        }

        r = self.client.post('/snippets/', json=data)
        self.assertEqual(r.status_code, 201)

        r_data = r.get_json()
        self.assertIsNotNone(r_data['id'])

        r = self.client.get(F"/snippets/{r_data['id']}")
        self.assertEqual(r.status_code, 200)

        snippet = r.get_json()
        self.assertEqual(snippet['id'], r_data['id'])
        self.assertEqual(snippet['title'], data['title'])
        self.assertEqual(snippet['content'], data['content'])

    def test_retrieve(self):
        # Normal
        r = self.client.get(F'/snippets/{self.snippet.id}')
        self.assertEqual(r.status_code, 200)

        snippet = r.get_json()
        self.assertIsNone(snippet.get('error', None))

        self.assertEqual(snippet.get('title', None), self.snippet.title)
        self.assertEqual(snippet.get('content', None), self.snippet.content)

        # Non-existent snippet
        r = self.client.get('/snippets/9999999')
        self.assertEqual(r.status_code, 404)

        snippet = r.get_json()
        self.assertIsNotNone(snippet.get('error', None))
        self.assertRegexpMatches(snippet['error'], "Not Found")

    def test_find_pagination(self):
        # Create a bunch of snippets
        self.__gen_snippets(50)

        # Page 1, Default PP
        r = self.client.get('/snippets/')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 10)
        self.assertGreaterEqual(data['total'], 50)

        snippets = data['snippets']
        self.assertIsInstance(snippets, list)
        self.assertEqual(len(snippets), 10)

        # Page 1, 25 PP
        r = self.client.get('/snippets/?pp=25')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 25)
        self.assertGreaterEqual(data['total'], 50)

        snippets = data['snippets']
        self.assertIsInstance(snippets, list)
        self.assertEqual(len(snippets), 25)

        # Save to compare below
        note_1 = snippets[0]
        note_10 = snippets[9]
        
        # Default: page 3, pp 10
        r = self.client.get('/snippets/?page=3&pp=10')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 3)
        self.assertEqual(data['per_page'], 10)
        self.assertGreaterEqual(data['total'], 50)

        snippets = data['snippets']
        self.assertIsInstance(snippets, list)
        self.assertEqual(len(snippets), 10)
        self.assertNotEqual(snippets[0]['id'], note_1['id'])
        self.assertNotEqual(snippets[9]['id'], note_10['id'])

        # Bad page specifier - str instead of int
        r = self.client.get('/snippets/?page=one')
        data = r.get_json()
        self.assertEqual(r.status_code, 500)
        self.assertRegexpMatches(data['error'], "invalid literal for int\(\) with base 10: 'one'")

    def test_find_search(self):
        self.__gen_snippets(15)
        self.__gen_snippets(8, ts="Astrium")
        self.__gen_snippets(7, cs="Xenomorph")

        # Single Param Search - 1
        r = self.client.get('/snippets/?title=Astrium')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 10)
        self.assertEqual(data['total'], 8)

        snippets = data['snippets']
        self.assertIsInstance(snippets, list)
        self.assertEqual(len(snippets), 8)

        # Single Param Search - 2
        r = self.client.get('/snippets/?content=Xenomorph')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 10)
        self.assertEqual(data['total'], 7)

        snippets = data['snippets']
        self.assertIsInstance(snippets, list)
        self.assertEqual(len(snippets), 7)

        # Mult Param Search - 1
        r = self.client.get('/snippets/?title=Astrium&content=Xenomorph&pp=25')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 25)
        self.assertEqual(data['total'], 15)

        snippets = data['snippets']
        self.assertIsInstance(snippets, list)
        self.assertEqual(len(snippets), 15)

        # Mult Param Search - 2
        r = self.client.get('/snippets/?title=Astrium&content=Xenomorph&page=2&pp=12')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['per_page'], 12)
        self.assertEqual(data['total'], 15)

        snippets = data['snippets']
        self.assertIsInstance(snippets, list)
        self.assertEqual(len(snippets), 3)

    def test_update(self):
        data = {
            'title': self.FAKER.name(),
            'content': self.FAKER.text()
        }

        self.assertNotEqual(self.snippet.title, data['title'])
        self.assertNotEqual(self.snippet.content, data['content'])

        r = self.client.put(F"/snippets/{self.snippet.id}", json=data)
        self.assertIsNone(r.get_json().get('error', None))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(F"/snippets/{self.snippet.id}")
        self.assertEqual(r.status_code, 200)

        snippet = r.get_json()
        self.assertEqual(snippet['title'], data['title'])
        self.assertEqual(snippet['content'], data['content'])

        # Update Non-Existent Snippet
        r = self.client.put("/snippets/999999999999", json={'title': 'Nothing Nobody None'})
        self.assertEqual(r.status_code, 404)

        r_data = r.get_json()
        self.assertIsNotNone(r_data.get('error', None))
        self.assertRegexpMatches(r_data['error'], "Not Found")

    def test_delete(self):
        snippet = Snippet(title=self.FAKER.name(), content=self.FAKER.text())
        snippet.save()

        # Safe Delete
        r = self.client.delete(F"/snippets/{snippet.id}?safe=1")
        self.assertEqual(r.status_code, 200)

        r_data = r.get_json()
        self.assertIsNotNone(r_data.get('id', None))
        self.assertEqual(snippet.id, r_data.get('id', None))

        del_note = Snippet(id=snippet.id)
        del_note.load()
        self.assertIsNotNone(del_note.deleted_at)

        # Real Delete
        r = self.client.delete(F"/snippets/{snippet.id}")
        self.assertEqual(r.status_code, 200)

        r_data = r.get_json()
        self.assertIsNotNone(r_data.get('id', None))
        self.assertEqual(snippet.id, r_data.get('id', None))

        del_note = Snippet(id=snippet.id)
        with self.assertRaisesRegex(ValueError, F'Record Not Found: \[{snippet.id}\]'):
            del_note.load()

        # Non-existent
        r = self.client.delete("/snippets/777777")
        self.assertEqual(r.status_code, 404)

        r_data = r.get_json()
        self.assertIsNotNone(r_data.get('error', None))
        self.assertRegexpMatches(r_data['error'], "Not Found")
