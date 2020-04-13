from cartaro.model.note import Note
import cartaro.controller.base as base

# NOTE: Currently does not support/surface the Note classes encryption ability
notes = base.create_controller("notes", Note)

# ------------------------------------------------------------------------------
# CLI commands
# ------------------------------------------------------------------------------
# NOTE: Don't really need this anymore. Leaving as documentation on HOWTO
#       add a command-line action.
# import click
# import faker
# FAKER = faker.Faker()

# @notes.cli.command('bulk-create')
# @click.option('-c', '--count', default=25)
# def create(count):
#     """Create a bunch of fake notes in the database"""

#     for i in range(0, count):
#         note = Note(
#             title=FAKER.sentence(),
#             content='\n'.join(FAKER.paragraphs(nb=5)),
#             is_favorite=FAKER.boolean(chance_of_getting_true=25)
#         )
#         note.save()

#         print(F"Created {i+1}/{count}", end='\r')

#     print("\nDone.")
