import unittest
import cartaro
import faker

# ------------------------------------------------------------------------------
class Snippet(cartaro.model.taggable.Taggable, cartaro.model.base.Base):
    def __init__(self, id=None, **kwargs):
        self.title = None
        self.content = None
        super().__init__(id=id, **kwargs)

    def update(self, data):
        self.title = data.get('title', self.title)
        self.content = data.get('content', self.content)
        self.tags = data.get('tags', self.tags)

    def _serialize(self):
        data =  {
            "title": self.title,
            "content": self.content
        }
        # Tags
        data.update(super()._serialize())

        return data
# ------------------------------------------------------------------------------
class BaseControllerTest(unittest.TestCase):

    FAKER = faker.Faker('en_US')

    def __gen_snippets(self, count, title=None, ts='', cs=''):
        for i in range(0, count):
            the_title = title if title else self.FAKER.name()
            if ts:
                the_title += F" - {ts}"

            snippet = Snippet(
                title=the_title,
                content=F"{self.FAKER.text()} - {cs}"
            )
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
        # self.snippet = Snippet(
        #     title=self.FAKER.name(),
        #     content=self.FAKER.text(),
        #     tags=['thing-1', 'thing-2']
        # )
        # self.snippet.save()

        self.client = cartaro.flask_app.test_client()

#     def test_create(self):
#         data = {
#             'title': self.FAKER.name(),
#             'content': self.FAKER.text(),
#             'tags': ['tag-1', 'tag-2']
#         }

#         r = self.client.post('/snippets/', json=data)
#         self.assertEqual(r.status_code, 201)

#         r_data = r.get_json()
#         self.assertIsNotNone(r_data['id'])

#         r = self.client.get(F"/snippets/{r_data['id']}")
#         self.assertEqual(r.status_code, 200)

#         snippet = r.get_json()
#         self.assertEqual(snippet['id'], r_data['id'])
#         self.assertEqual(snippet['title'], data['title'])
#         self.assertEqual(snippet['content'], data['content'])
#         self.assertEqual(len(snippet['tags']), 2)
#         self.assertIn('tag-1', snippet['tags'])
#         self.assertIn('tag-2', snippet['tags'])

#     def test_retrieve(self):
#         a_snippet = Snippet(
#             title=self.FAKER.name(),
#             content=self.FAKER.text(),
#             tags=['thing-1', 'thing-2']
#         )
#         a_snippet.save()

#         # Normal
#         r = self.client.get(F'/snippets/{a_snippet.id}')
#         self.assertEqual(r.status_code, 200)

#         snippet = r.get_json()
#         self.assertIsNone(snippet.get('error', None))

#         self.assertEqual(snippet.get('title', None), a_snippet.title)
#         self.assertEqual(snippet.get('content', None), a_snippet.content)
#         self.assertEqual(len(snippet['tags']), len(a_snippet.tags))
#         self.assertIn('thing-1', snippet['tags'])
#         self.assertIn('thing-2', snippet['tags'])

#         # Non-existent snippet
#         r = self.client.get('/snippets/9999999')
#         self.assertEqual(r.status_code, 404)

#         snippet = r.get_json()
#         self.assertIsNotNone(snippet.get('error', None))
#         self.assertRegexpMatches(snippet['error'], "Not Found")

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
        r = self.client.get('/snippets/?meta=pp=25')
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
        r = self.client.get('/snippets/?meta=page=3:pp=10')
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
        r = self.client.get('/snippets/?meta=page=one')
        data = r.get_json()
        self.assertEqual(r.status_code, 500)
        self.assertRegexpMatches(data['error'], "invalid literal for int\(\) with base 10: 'one'")

#     def test_find_search(self):
#         self.__gen_snippets(15)
#         self.__gen_snippets(8, ts="Astrium")
#         self.__gen_snippets(7, cs="Xenomorph")

#         # Single Param Search - 1
#         r = self.client.get('/snippets/?title=Astrium')
#         self.assertEqual(r.status_code, 200)

#         data = r.get_json()
#         self.assertEqual(data['page'], 1)
#         self.assertEqual(data['per_page'], 10)
#         self.assertEqual(data['total'], 8)

#         snippets = data['snippets']
#         self.assertIsInstance(snippets, list)
#         self.assertEqual(len(snippets), 8)

#         # Single Param Search - 2
#         r = self.client.get('/snippets/?content=Xenomorph')
#         self.assertEqual(r.status_code, 200)

#         data = r.get_json()
#         self.assertEqual(data['page'], 1)
#         self.assertEqual(data['per_page'], 10)
#         self.assertEqual(data['total'], 7)

#         snippets = data['snippets']
#         self.assertIsInstance(snippets, list)
#         self.assertEqual(len(snippets), 7)

#         # Mult Param Search - 1
#         r = self.client.get('/snippets/?title=Astrium&content=Xenomorph&pp=25')
#         self.assertEqual(r.status_code, 200)

#         data = r.get_json()
#         self.assertEqual(data['page'], 1)
#         self.assertEqual(data['per_page'], 25)
#         self.assertEqual(data['total'], 15)

#         snippets = data['snippets']
#         self.assertIsInstance(snippets, list)
#         self.assertEqual(len(snippets), 15)

#         # Mult Param Search - 2
#         r = self.client.get('/snippets/?title=Astrium&content=Xenomorph&page=2&pp=12')
#         self.assertEqual(r.status_code, 200)

#         data = r.get_json()
#         self.assertEqual(data['page'], 2)
#         self.assertEqual(data['per_page'], 12)
#         self.assertEqual(data['total'], 15)

#         snippets = data['snippets']
#         self.assertIsInstance(snippets, list)
#         self.assertEqual(len(snippets), 3)

#     def test_find_group_by(self):
#         self.__gen_snippets(8, title='MurderOfCrows')
#         self.__gen_snippets(5, title='HerdOfCattle')

#         r = self.client.get('/snippets/?group_by=title')
#         self.assertEqual(r.status_code, 200)

#         data = r.get_json()
#         self.assertEqual(data['page'], 1)
#         self.assertEqual(data['per_page'], 10)
#         self.assertEqual(data['total'], 13)

#         snippets = data['snippets']
#         self.assertIsInstance(snippets, dict)
#         self.assertEqual(len(snippets), 2)
#         self.assertEqual(len(snippets['MurderOfCrows']), 8)
#         self.assertEqual(len(snippets['HerdOfCattle']), 2)

#     def test_update(self):
#         a_snippet = Snippet(
#             title=self.FAKER.name(),
#             content=self.FAKER.text(),
#             tags=['thing-1', 'thing-2']
#         )
#         a_snippet.save()

#         data = {
#             'title': self.FAKER.name(),
#             'content': self.FAKER.text(),
#             'tags': ['ghoti-1', 'ghoti-2', 'ghoti-3']
#         }

#         self.assertNotEqual(a_snippet.title, data['title'])
#         self.assertNotEqual(a_snippet.content, data['content'])
#         self.assertNotEqual(a_snippet.tags, data['tags'])

#         r = self.client.put(F"/snippets/{a_snippet.id}", json=data)
#         self.assertIsNone(r.get_json().get('error', None))
#         self.assertEqual(r.status_code, 200)

#         r = self.client.get(F"/snippets/{a_snippet.id}")
#         self.assertEqual(r.status_code, 200)

#         snippet = r.get_json()
#         self.assertEqual(snippet['id'], a_snippet.id)
#         self.assertEqual(snippet['title'], data['title'])
#         self.assertEqual(snippet['content'], data['content'])
#         self.assertIn(data['tags'][0], snippet['tags'])
#         self.assertIn(data['tags'][1], snippet['tags'])
#         self.assertIn(data['tags'][2], snippet['tags'])
#         self.assertEqual(len(snippet['tags']), len(data['tags']))

#         # Update Non-Existent Snippet
#         r = self.client.put("/snippets/999999999999", json={'title': 'Nothing Nobody None'})
#         self.assertEqual(r.status_code, 404)

#         r_data = r.get_json()
#         self.assertIsNotNone(r_data.get('error', None))
#         self.assertRegexpMatches(r_data['error'], "Not Found")

#     def test_delete(self):
#         snippet = Snippet(title=self.FAKER.name(), content=self.FAKER.text())
#         snippet.save()

#         # Safe Delete
#         r = self.client.delete(F"/snippets/{snippet.id}?safe=1")
#         self.assertEqual(r.status_code, 200)

#         r_data = r.get_json()
#         self.assertIsNotNone(r_data.get('id', None))
#         self.assertEqual(snippet.id, r_data.get('id', None))

#         del_note = Snippet(id=snippet.id)
#         del_note.load()
#         self.assertIsNotNone(del_note.deleted_at)

#         # Real Delete
#         r = self.client.delete(F"/snippets/{snippet.id}")
#         self.assertEqual(r.status_code, 200)

#         r_data = r.get_json()
#         self.assertIsNotNone(r_data.get('id', None))
#         self.assertEqual(snippet.id, r_data.get('id', None))

#         del_note = Snippet(id=snippet.id)
#         with self.assertRaisesRegex(ValueError, F'Record Not Found: \[{snippet.id}\]'):
#             del_note.load()

#         # Non-existent
#         r = self.client.delete("/snippets/777777")
#         self.assertEqual(r.status_code, 404)

#         r_data = r.get_json()
#         self.assertIsNotNone(r_data.get('error', None))
#         self.assertRegexpMatches(r_data['error'], "Not Found")

#     def test_undelete(self):
#         snippet = Snippet(title=self.FAKER.name(), content=self.FAKER.text())
#         snippet.save()

#         # Safe Delete
#         r = self.client.delete(F"/snippets/{snippet.id}?safe=1")
#         self.assertEqual(r.status_code, 200)

#         r_data = r.get_json()
#         self.assertIsNotNone(r_data.get('id', None))
#         self.assertEqual(snippet.id, r_data.get('id', None))

#         del_note = Snippet(id=snippet.id)
#         del_note.load()
#         self.assertIsNotNone(del_note.deleted_at)

#         # UnDelete
#         r = self.client.put(F"/snippets/undelete/{del_note.id}")
#         self.assertEqual(r.status_code, 200)

#         r_data = r.get_json()
#         self.assertIsNotNone(r_data.get('id', None))
#         self.assertEqual(del_note.id, r_data.get('id', None))

#         undel_note = Snippet(id=del_note.id)
#         undel_note.load()
#         self.assertIsNone(undel_note.deleted_at)
#         self.assertEqual(undel_note.title, snippet.title)
#         self.assertEqual(undel_note.content, snippet.content)

#     def test_undelete_nonexistent(self):
#         r = self.client.put(F"/snippets/undelete/77998800")
#         self.assertEqual(r.status_code, 404)








# #
