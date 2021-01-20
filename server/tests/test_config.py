import unittest

from cartaro.config import Config
class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.config = Config.initialize('tests/data/CartaroCfg.json')

    def test_basic(self):
        self.assertIsInstance(self.config, Config)
        self.assertEqual(self.config.get('CARTARO:encryption_password'), '42')

    


















    # 
