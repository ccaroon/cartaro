import unittest
import random

from cartaro.model.base import Base
from cartaro.model.taggable import Taggable

from cartaro.model.tag import Tag
# ------------------------------------------------------------------------------
# Since cartaro.model.base.Base is an Abstract Class we have to create a concrete
# class for testing purposes.
# ------------------------------------------------------------------------------
class Comment(Taggable, Base):
    def __init__(self, id=None, **kwargs):
        self.name = None
        self.message = None

        super().__init__(id=id, **kwargs)

    def update(self, data):
        self.name = data.get('name', self.name)
        self.message = data.get('message', self.message)
        self.tags = data.get('tags', self.tags)

    def _serialize(self):
        data =  {
            "name": self.name,
            "message": self.message,
        }
        data.update(super()._serialize())
        return data
# ------------------------------------------------------------------------------
class TaggableTest(unittest.TestCase):

    def setUp(self):
        # Delete all records
        Comment.purge()

    def test_tagging_basics(self):
        comment = Comment(name="Carlos Phisher", message="The world is borked!")

        #  No tags yet
        self.assertIsInstance(comment.tags, set)
        self.assertEqual(len(comment.tags), 0)

        # Add a tag
        comment.tag("Urgent")
        self.assertIsInstance(comment.tags, set)
        self.assertEqual(len(comment.tags), 1)
        self.assertIsInstance(list(comment.tags)[0], Tag)

        # Add the same tag == no change
        comment.tag("Urgent")
        self.assertIsInstance(comment.tags, set)
        self.assertEqual(len(comment.tags), 1)
        self.assertIsInstance(list(comment.tags)[0], Tag)

        # Add a few more tags
        comment.tag("Phone") # Add by string
        comment.tag("CommErr") # Add by string
        comment.tag(Tag(name="Slang")) # Add by Tag class
        self.assertEqual(len(comment.tags), 4)
        self.assertTrue(Tag(name="CommErr") in comment.tags)

        # Remove one - by string
        comment.remove_tag("Slang")
        self.assertEqual(len(comment.tags), 3)
        self.assertFalse(Tag(name="Slang") in comment.tags)

        # Remove another - by Tag
        comment.remove_tag(Tag(name="Phone"))
        self.assertEqual(len(comment.tags), 2)
        self.assertFalse(Tag(name="Phone") in comment.tags)

        # Add tags at instance creation
        comment2 = Comment(
            name="John Doe",
            message="Mice eat cheese!?",
            tags=['mice', 'food', 'dairy']
        )

        self.assertIsInstance(comment2.tags, set)
        self.assertEqual(len(comment2.tags), 3)
        self.assertIsInstance(list(comment.tags)[0], Tag)

    def test_tagging_advanced(self):
        comment = Comment(
            name="BOB",
            message="Frog blast the vent core.",
            tags=["Green", "Simulacrum", "Histeria"]
        )

        self.assertIsInstance(comment.tags, set)
        self.assertEqual(len(comment.tags), 3)

        comment.save()
        self.assertIsNotNone(comment.id)
        self.assertEqual(len(comment.tags), 3)
        self.assertIsInstance(comment.tags, set)

        comment2 = Comment(id=comment.id)
        comment2.load()
        self.assertIsInstance(comment2.tags, set)
        self.assertIsInstance(list(comment2.tags)[0], Tag)
        
        self.assertCountEqual(comment.tags, comment2.tags)

    def test_search_by_tag(self):
        for i in range(0, 10):
            comment = Comment(name=F"User {i}", message=F"Foo Bar {i}", tags=[F"Anonymous", F"Tag{i}", F"Tag{i*i}"])
            comment.save()
        
        comment = Comment(
            name="John Titor",
            message="I am from the future. I can prove it.",
            tags=['Steins;Gate', 'WW III', 'Future']
        )
        comment.save()

        results = Comment.find(tags="anonymous")
        self.assertEqual(len(results), 10)

        results = Comment.find(tags="future")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, comment.id)
        self.assertEqual(results[0].name, "John Titor")
        self.assertTrue(Tag(name="Steins;Gate") in results[0].tags)

    def test_errors(self):
        comment = Comment(name="Darth Vader", comment="I find your lack of faith disturbing.")
        
        with self.assertRaisesRegex(TypeError, "'tag' must be of type `str` or `Tag`"):
            comment.tag(123)

        with self.assertRaisesRegex(TypeError, "'tag' must be of type `str` or `Tag`"):
            comment.remove_tag(['this', 'that'])

    def test_tag_management(self):
        # Adding a new tag to an object (& saving) should also update the Tags db
        tags = [F'star wars {random.randint(0,9999)}', F'trapped {random.randint(0,9999)}']
        comment = Comment(
            name="Luke Skywalker", 
            comment="There's something alive in here!"
        )
        comment.save()

        comment2 = Comment(id=comment.id)
        comment2.load()
        self.assertEqual(len(comment2.tags), 0)

        for tag in tags:
            # Tag does not exist in Tag DB
            self.assertFalse(Tag.exists(tag), tag)
            # Add to object
            comment2.tag(tag)

        comment2.save()
        self.assertEqual(len(comment2.tags), len(tags))
        
        for tag in tags:
            # Tag should now exist in Tag db
            self.assertTrue(Tag.exists(tag), tag)










# 
