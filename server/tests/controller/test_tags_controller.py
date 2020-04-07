import unittest
import cartaro
import faker

from cartaro.model.tag import Tag
# ------------------------------------------------------------------------------
class TagsControllerTest(unittest.TestCase):

    FAKER = faker.Faker()

    def __gen_tags(self, count, prefix='', suffix=''):
        for i in range(0, count):
            tag = Tag(name=F"{prefix} {self.FAKER.word().capitalize()} {suffix}")
            tag.save()

    def setUp(self):
        # Setup Flask Testing
        cartaro.flask_app.config['TESTING'] = True
        self.client = cartaro.flask_app.test_client()

    def test_find_search(self):
        self.__gen_tags(25)
        self.__gen_tags(8, prefix="Super")
        self.__gen_tags(7, prefix="Hello", suffix="World")

        # Get All
        r = self.client.get('/tags/')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        tags = data.get('tags', [])
        self.assertEqual(len(tags), 40)

        # Search
        r = self.client.get('/tags/?name=Super')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        tags = data.get('tags', [])
        self.assertEqual(len(tags), 8)

        #  Search - 2
        r = self.client.get('/tags/?name=Hello.*world')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        tags = data.get('tags', [])
        self.assertEqual(len(tags), 7)










# 
