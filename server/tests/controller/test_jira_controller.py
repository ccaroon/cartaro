import unittest
import unittest.mock as mock
import cartaro

# ------------------------------------------------------------------------------
class JiraControllerTest(unittest.TestCase):
    def setUp(self):
        # Setup Flask Testing
        cartaro.flask_app.config['TESTING'] = True
        self.client = cartaro.flask_app.test_client()
        # Backup Jira config
        self._cfg_jira = cartaro.flask_app.config['CARTARO']['jira'].copy()

    def tearDown(self):
        # Restore Jira config
        cartaro.flask_app.config['CARTARO']['jira']['host'] = self._cfg_jira['host']
        cartaro.flask_app.config['CARTARO']['jira']['token'] = self._cfg_jira['token']

    def __set_cfg_jira(self, host, token):
        cartaro.flask_app.config['CARTARO']['jira']['host'] = host
        cartaro.flask_app.config['CARTARO']['jira']['token'] = token
    
    def test_cfg_missing_host(self):
        self.__set_cfg_jira(None, 'TOKEN')
        r = self.client.get('/jira/search')
        
        self.assertEqual(r.status_code, 500)

        body = r.get_json()
        self.assertTrue('error' in body)
        self.assertRegexpMatches(body['error'], 'Jira Connection Not Properly Configured')

    def test_cfg_missing_token(self):
        self.__set_cfg_jira('HOST', None)

        cartaro.flask_app.config['CARTARO']['jira']['token'] = None
        r = self.client.get('/jira/search')
        
        self.assertEqual(r.status_code, 500)

        body = r.get_json()
        self.assertTrue('error' in body)
        self.assertRegexpMatches(body['error'], 'Jira Connection Not Properly Configured')

    @mock.patch('requests.get')
    def test_search(self, mock_get):
        jira_data = {
            'issues': [
                {
                    'key': 'CNC-0001',
                    'fields': {
                        'summary': 'hello-world',
                        'issuetype': { 'name': 'Bug'},
                        'status': { 'name': 'In Progress'}
                    }
                },
                {
                    'key': 'CNC-0002',
                    'fields': {
                        'summary': 'hello-sailor',
                        'issuetype': { 'name': 'Task'},
                        'status': { 'name': 'New'}
                    }
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock.Mock(return_value=jira_data)

        r = self.client.get('/jira/search')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertIn('jira', data)
        self.assertIn('jql', data)
        self.assertIn('search_name', data)

        tickets = data['jira']
        self.assertEqual(len(tickets), 2)

        tix1 = tickets[0]
        self.assertEqual(tix1['key'], 'CNC-0001')
        self.assertEqual(tix1['summary'], 'hello-world')
        self.assertEqual(tix1['type'], 'Bug')
        self.assertEqual(tix1['status'], 'In Progress')

        tix2 = tickets[1]
        self.assertEqual(tix2['key'], 'CNC-0002')
        self.assertEqual(tix2['summary'], 'hello-sailor')
        self.assertEqual(tix2['type'], 'Task')
        self.assertEqual(tix2['status'], 'New')

    @mock.patch('requests.get')
    def test_search_jira_err(self, mock_get):
        mock_get.return_value.status_code = 401

        r = self.client.get('/jira/search')
        self.assertEqual(r.status_code, 500)

        data = r.get_json()
        self.assertIn('error', data)
        self.assertRegexpMatches(data['error'], "Error Querying Jira: 401")

    def test_search_faker(self):
        self.__set_cfg_jira('http://jira.simulacrum.com', 'TOKEN')
        r = self.client.get('/jira/search')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        self.assertIn('jira', data)
        self.assertIn('jql', data)
        self.assertIn('search_name', data)

        tickets = data['jira']
        self.assertEqual(len(tickets), 0)
