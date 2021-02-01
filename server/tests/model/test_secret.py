import json
import unittest

from cartaro.model.secret import Secret
from cartaro.model.tag import Tag
from cartaro.utils.crypto import Crypto
class SecretTest(unittest.TestCase):

    def setUp(self):
        self.encryption_key = '0000000'
        Secret.ENCRYPTION_KEY = self.encryption_key
        self.crypto = Crypto(self.encryption_key)

    def test_missing_encryption_key(self):
        Secret.ENCRYPTION_KEY = None

        with self.assertRaisesRegex(Exception, "Secret - Encryption Key not set"):
            secret = Secret(name="bad wolf")

    def test_construction(self):
        # Set secret 'data' directly
        secret = Secret(
            name="LEGO",
            system="www.lego.com",
            sub_system="UI",
            type=Secret.TYPE_USER_PASS,
            data={'username': 'hob-goblin', 'password': '0xDeadbeeF'}
        )

        self.assertDictEqual(secret.data, {
            'username': 'hob-goblin',
            'password': '0xDeadbeeF'
        })

        # "Forge" secret 'data' from kwargs
        secret = Secret(
            name="LEGO",
            system="api.lego.com",
            sub_system="REST API",
            type=Secret.TYPE_KEY_SECRET,
            key="4c1300c900d1af3de0e67560f542090b",
            secret="bWluaS1maWcK"
        )

        self.assertDictEqual(secret.data, {
            'key': "4c1300c900d1af3de0e67560f542090b",
            'secret': "bWluaS1maWcK"
        })

    def test_forge(self):
        # user-pass
        secret = Secret.forge(
            Secret.TYPE_USER_PASS,
            username="bugbear",
            password="s3kR37"
        )

        self.assertDictEqual(secret, {
            'username': "bugbear",
            'password': "s3kR37"
        })

        # token
        secret = Secret.forge(
            Secret.TYPE_TOKEN,
            token="0xDEADBEEF"
        )

        self.assertDictEqual(secret, {'token': "0xDEADBEEF"})

        # key-secret
        secret = Secret.forge(
            Secret.TYPE_KEY_SECRET,
            key="abc12377x",
            secret="frog blast the vent core"
        )

        self.assertDictEqual(secret, {
            'key': "abc12377x",
            'secret': "frog blast the vent core"
        })

    def test_forge_invalid_type(self):
        with self.assertRaisesRegex(TypeError, "Invalid Secret Type: 'base64-encoded-string'"):
            Secret.forge('base64-encoded-string', string="deciduous manifestations")

    def test_forge_missing_args(self):
        with self.assertRaisesRegex(ValueError, "Missing Required Value: 'username'"):
            Secret.forge(
                Secret.TYPE_USER_PASS,
                password="h0lyc0W"
            )

    def test_encryption(self):
        Secret.purge()

        stype = Secret.TYPE_USER_PASS
        username = 'rufus42'
        password = 'y5kqyRrPXUUjS4DM'
        secret = Secret(
            name="My Email Account",
            system="email.com",
            sub_system="UI",
            type=stype,
            data={'username': username, 'password': password},
            note="Personal Email **ONLY**"
        )

        self.assertEqual(secret.data['username'], username)
        self.assertEqual(secret.data['password'], password)

        secret.save()

        with open('tests/tmp/Secrets-test.json') as file:
            raw_data = json.load(file).get('_default', {}).get('1', {}).get('data')

        self.assertNotEqual(raw_data['username'], secret.data['username'])
        self.assertNotEqual(raw_data['password'], secret.data['password'])

        self.assertEqual(self.crypto.decrypt(raw_data['username']), secret.data['username'])
        self.assertEqual(self.crypto.decrypt(raw_data['password']), secret.data['password'])

        self.assertEqual(secret.data['username'], username)
        self.assertEqual(secret.data['password'], password)

        # Load and check stuff
        secret2 = Secret(id=1)
        secret2.load()

        self.assertEqual(secret2.type, stype)
        self.assertEqual(secret2.data['username'], username)
        self.assertEqual(secret2.data['password'], password)


    def test_serialize(self):
        # set data directly
        secret = Secret(
            name="My Email Account",
            system="email.com",
            sub_system="UI",
            type=Secret.TYPE_USER_PASS,
            data={'username': 'rufus42', 'password': 'y5kqyRrPXUUjS4DM'},
            note="Personal Email **ONLY**"
        )

        data = secret.serialize()

        self.assertEqual(secret.name, "My Email Account")
        self.assertEqual(secret.system, "email.com")
        self.assertEqual(secret.sub_system, "UI")
        self.assertEqual(secret.type, Secret.TYPE_USER_PASS)
        self.assertEqual(secret.data['username'], "rufus42")
        self.assertEqual(secret.data['password'], "y5kqyRrPXUUjS4DM")
        self.assertEqual(secret.note, "Personal Email **ONLY**")

        # forge data directly
        secret = Secret(
            name="My Email Account",
            system="email.com",
            sub_system="UI",
            type=Secret.TYPE_USER_PASS,
            username='rufus007',
            password='y5kqyRrXPXUUjS4DM',
            note="Personal Email **ONLY**"
        )

        data = secret.serialize()

        self.assertEqual(secret.name, "My Email Account")
        self.assertEqual(secret.system, "email.com")
        self.assertEqual(secret.sub_system, "UI")
        self.assertEqual(secret.type, Secret.TYPE_USER_PASS)
        self.assertEqual(secret.data['username'], "rufus007")
        self.assertEqual(secret.data['password'], "y5kqyRrXPXUUjS4DM")
        self.assertEqual(secret.note, "Personal Email **ONLY**")

    def test_tagging(self):
        # Basic instance
        secret = Secret(
            name="LEGO",
            system="www.lego.com",
            sub_system="UI",
            type=Secret.TYPE_USER_PASS,
            data={'username': 'hob-goblin', 'password': '0xDeadbeeF'},
        )
        self.assertIsNotNone(secret.tags)
        self.assertIsInstance(secret.tags, set)
        self.assertEqual(len(secret.tags), 0)

        # Create with Tags
        secret.tag("lego")
        secret.tag("brick-by-brick")
        self.assertEqual(len(secret.tags), 2)
        self.assertIsInstance(list(secret.tags)[0], Tag)
        secret.save()

        # Retrieve has Tags
        secret2 = Secret(id=secret.id)
        secret2.load()
        self.assertIsNotNone(secret2.tags)
        self.assertIsInstance(secret2.tags, set)
        self.assertEqual(len(secret2.tags), 2)
        self.assertIsInstance(list(secret2.tags)[0], Tag)
        self.assertTrue(Tag(name="lego") in secret2.tags)

        # Update tags
        secret2.tag("studs-r-us")
        self.assertEqual(len(secret2.tags), 3)
        self.assertIsInstance(list(secret2.tags)[2], Tag)

        secret2.save()

        secret3 = Secret(id=secret2.id)
        secret3.load()
        self.assertIsNotNone(secret3.tags)
        self.assertIsInstance(secret3.tags, set)
        self.assertEqual(len(secret3.tags), 3)

        self.assertTrue(Tag(name="lego") in secret3.tags)
        self.assertTrue(Tag(name="brick-by-brick") in secret3.tags)
        self.assertTrue(Tag(name="studs-r-us") in secret3.tags)
