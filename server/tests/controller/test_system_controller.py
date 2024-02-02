import re
import sys
import unittest
import cartaro

# ------------------------------------------------------------------------------
class SystemControllerTest(unittest.TestCase):
    def setUp(self):
        # Setup Flask Testing
        cartaro.flask_app.config['TESTING'] = True
        self.client = cartaro.flask_app.test_client()

    def test_ping(self):
        r = self.client.get('/sys/ping')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        sys_ver = re.escape(sys.version)
        self.assertRegex(data, fr'^pong - {sys_ver}')

    # def test_backup(self):
    #     r = self.client.post('/sys/backup')
    #     self.assertEqual(r.status_code, 201)

    #     data = r.get_json()
    #     self.assertRegex(data['message'], "Data in")
