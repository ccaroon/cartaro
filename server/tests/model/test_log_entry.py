import arrow
import datetime
import unittest

from cartaro.model.log_entry import LogEntry
from cartaro.model.taggable import Taggable
from cartaro.model.ticket import Ticket

class LogEntryTest(unittest.TestCase):

    def setUp(self):
        self.ticket = Ticket(
            key="CNC-42", 
            summary="Grok the Answer", 
            type="Task", 
            status="In Progress",
            link="https://jira.example.com/browse/CNC-42"
        )

        self.entry = LogEntry(
            logged_at=datetime.datetime.now().timestamp(),
            subject="Just Another Day",
            content="Just another day at sea. Lost. Hopeless.",
            category="Mourning Update",
            ticket=self.ticket
        )

    def test_basics(self):
        self.assertIsInstance(self.entry, Taggable)
        self.assertIsInstance(self.entry.logged_at, arrow.Arrow)
        self.assertIsInstance(self.entry.ticket, Ticket)

    def test_construction(self):
        # logged_at should default to now
        entry = LogEntry(
            subject="Just Another Day",
            content="Just another day at sea. Lost. Hopeless.",
            category="Mourning Update"
        )
        self.assertIsNotNone(entry.logged_at)
        self.assertAlmostEqual(entry.logged_at.timestamp, arrow.now().timestamp)

        # Ticket can be specified as a Ticket object, a dict or None
        # Test as Ticket
        entry = LogEntry(
            subject="Just Another Day",
            content="Just another day at sea. Lost. Hopeless.",
            category="Mourning Update",
            ticket=self.ticket
        )
        self.assertIsInstance(entry.ticket, Ticket)

        # Test as dict
        entry = LogEntry(
            subject="Just Another Day",
            content="Just another day at sea. Lost. Hopeless.",
            category="Mourning Update",
            ticket={'key': "BND-007", 'summary': "Bond. James Bond.", 'type': "Story", 'status': "Open", 'link': "https://jira.example.com/browse/BND-007"}
        )
        self.assertIsInstance(entry.ticket, Ticket)

        # Test as None
        entry = LogEntry(
            subject="Just Another Day",
            content="Just another day at sea. Lost. Hopeless.",
            category="Mourning Update",
            ticket=None
        )
        self.assertEqual(entry.ticket, None)

        # Test invalid type
        with self.assertRaisesRegex(TypeError, "'ticket' must be of type `Ticket`, `dict` or `None`."):
            entry = LogEntry(
                subject="Just Another Day",
                content="Just another day at sea. Lost. Hopeless.",
                category="Mourning Update",
                ticket="BND-007"
            )

    def test_serialize(self):
        data = self.entry.serialize()

        self.assertEqual(self.entry.logged_at.timestamp, data['logged_at'])
        self.assertEqual(self.entry.subject, data['subject'])
        self.assertEqual(self.entry.content, data['content'])
        self.assertEqual(self.entry.category, data['category'])

        ticket_data = self.entry.ticket.serialize()
        self.assertDictEqual(ticket_data, data['ticket'])












# 
