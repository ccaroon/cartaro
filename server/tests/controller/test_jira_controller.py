import unittest
import cartaro

# ------------------------------------------------------------------------------
class JiraControllerTest(unittest.TestCase):
    def setUp(self):
        # Setup Flask Testing
        cartaro.flask_app.config['TESTING'] = True
        self.client = cartaro.flask_app.test_client()

    def test_search(self):
        r = self.client.get('/search')
        # self.assertEqual(r.status_code, 200)

        data = r.get_json()
        print(data)
        # tags = data.get('tags', [])
        # self.assertEqual(len(tags), 40)
