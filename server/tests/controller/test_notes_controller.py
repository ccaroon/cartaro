# import unittest
# import cartaro
# import faker

# from cartaro.model.note import Note
# # ------------------------------------------------------------------------------
# class NotesControllerTest(unittest.TestCase):

#     FAKER = faker.Faker('en_US)

#     def __gen_notes(self, count, ts='', cs=''):
#         for i in range(0, count):
#             note = Note(title=F"{self.FAKER.name()} - {ts}", content=F"{self.FAKER.text()} - {cs}")
#             note.save()

#     def setUp(self):
#         # New Note for testing
#         self.note = Note(title=self.FAKER.name(), content=self.FAKER.text())
#         self.note.save()

#         # Setup Flask Testing
#         cartaro.flask_app.config['TESTING'] = True
#         self.client = cartaro.flask_app.test_client()
