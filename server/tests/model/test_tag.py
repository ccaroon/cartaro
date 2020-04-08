import unittest

from cartaro.model.tag import Tag
class TagTest(unittest.TestCase):

    def setUp(self):
        self.tag = Tag(name="Urgent")

    def test_basics(self):
        # Tag name should be normalized when constructed
        tag = Tag(name="Hack-A-Thon 2020")
        self.assertEqual(tag.name, "hack-a-thon-2020")

    def test_serialize(self):
        data = self.tag.serialize()

        self.assertEqual(self.tag.name, data['name'])

    def test_immutable(self):
        self.assertEqual(self.tag.name, "urgent")

        with self.assertRaisesRegex(AttributeError, "can't set attribute"):
            self.tag.name = "Not So Urgent"

        self.assertEqual(self.tag.name, "urgent")

    def test_str__repr(self):
        self.assertEqual(str(self.tag), self.tag.name)
        self.assertEqual(repr(self.tag), self.tag.name)

    def test_eq(self):
        tag2 = Tag(name=self.tag.name)

        self.assertEqual(self.tag, tag2)

    def test_normalize(self):
        tests = [
            ('HELLO',                       'hello'),
            ('Hello.World',                 'hello.world'),
            ('HELLO_wOrLd',                 'hello_world'),
            ('Hello, World!',               'hello-world'),
            ('  hello,world!!',             'hello-world'),
            ('helloWorld',                  'helloworld'),
            ('   hello,,,,,   world!!!   ', 'hello-world'),
            ('###  ! Hello World @ Large ! ###', 'hello-world-large')
        ]

        for tset in tests:
            self.assertEqual(Tag.normalize(tset[0]), tset[1], tset[0])









# 
