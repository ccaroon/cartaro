import unittest

from cartaro.utils.crypto import Crypto
class CryptoTest(unittest.TestCase):

    def setUp(self):
        pass

    # def test_gen_key(self):
    #     key = Crypto.generate_key()
    #     self.assertIsNotNone(key)

    def test_construct(self):
        with self.assertRaisesRegex(ValueError, "'password' cannot be empty or None"):
            Crypto(None)

    def test_encrypt_decrypt(self):
        crypto = Crypto("7h3-7ru7h")

        msg = "Hello, World!"
        secret = crypto.encrypt(msg)
        self.assertIsNotNone(secret)
        self.assertNotEqual(msg, secret)

        clear_text = crypto.decrypt(secret)
        self.assertIsNotNone(clear_text)
        self.assertEqual(msg, clear_text)









# 
