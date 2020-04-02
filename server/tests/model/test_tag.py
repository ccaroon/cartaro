import unittest

from cartaro.model.tag import Tag
class TagTest(unittest.TestCase):

    def setUp(self):
        self.tag = Tag(name="Urgent")

    def test_for_json(self):
        data = self.tag.for_json()

        self.assertEqual(self.tag.name, data['name'])

    def test_immutable(self):
        self.assertEqual(self.tag.name, "Urgent")

        with self.assertRaisesRegex(AttributeError, "can't set attribute"):
            self.tag.name = "Not So Urgent"

        self.assertEqual(self.tag.name, "Urgent")

    def test_str__repr(self):
        self.assertEqual(str(self.tag), self.tag.name)
        self.assertEqual(repr(self.tag), self.tag.name)

    def test_eq(self):
        tag2 = Tag(name=self.tag.name)

        self.assertEqual(self.tag, tag2)

    def test_tagability(self):
        # Tags should not be taggable
        self.tag.tag("fish")
        print(self.tag.tags)
        

        # from db
        # ...
