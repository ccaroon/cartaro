import unittest

from cartaro.config import Config
class ConfigTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.initialize('tests/data/CartaroCfg-test.json')

    def setUp(self):
        self.config = Config()

    def test_basic(self):
        self.assertIsInstance(self.config, Config)
        self.assertEqual(self.config.get('CARTARO:encryption_password'), '42')

    def test_get(self):
        # non-default
        port = self.config.get('CARTARO:server:port')
        self.assertEqual(port, 8888)

        # not found - return default
        foo = self.config.get('CARTARO:foo', 'bar')
        self.assertEqual(foo, 'bar')

    def test_get_all(self):
        data = self.config.get_all()
        self.assertIsInstance(data, dict)

        self.assertIn('CARTARO', data)
        self.assertIn('jira', data['CARTARO'])

    def test_set(self):
        extra = self.config.get('CARTARO:extra')
        self.assertIsNone(extra)

        passphrase = 'this is the way the world ends'
        self.config.set('CARTARO:extra:passphrase', passphrase)
        pp = self.config.get('CARTARO:extra:passphrase')
        self.assertEqual(pp, passphrase)

        extra = self.config.get('CARTARO:extra')
        self.assertIn('passphrase', extra)

        motd = "he's 0xdead, Jim!"
        self.config.set('CARTARO:extra:motd', motd)
        msg = self.config.get('CARTARO:extra:motd')
        self.assertEqual(msg,motd)

        extra = self.config.get('CARTARO:extra')
        self.assertIn('passphrase', extra)
        self.assertIn('motd', extra)
        self.assertDictEqual(extra, {'passphrase': passphrase, 'motd': motd})

        self.assertEqual(self.config.get('CARTARO:extra:passphrase'), passphrase)
        self.assertEqual(self.config.get('CARTARO:extra:motd'), motd)

    def test_force_reload(self):
        self.config.set('CARTARO:transient:foo', 'bar')
        self.assertEqual(self.config.get('CARTARO:transient:foo'), 'bar')

        self.config.force_reload()

        self.assertIsNone(self.config.get('CARTARO:transient:foo'))
