import unittest

from cartaro.model.secret import Secret
class SecretTest(unittest.TestCase):

    def setUp(self):
        pass

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
