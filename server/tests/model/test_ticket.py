import unittest
from cartaro.model.ticket import Ticket

class TicketTest(unittest.TestCase):

    def _gen_ticket(self, count):
        tickets = []
        for i in range(0,count):
            tickets.append(Ticket(
                key=F"CNC-{i:04}",
                summary=F"Grok the Answer: {i*i}",
                type="Story" if i % 3 == 0 else "Bug",
                status="In Progress" if i % 2 == 0 else "Open",
                link=F"https://jira.example.com/browse/CNC-{i:04}"
            ))
        return tickets

    def setUp(self):
        sub_tasks = self._gen_ticket(5)

        self.ticket = Ticket(
            key="CNC-42",
            summary="Grok the Answer",
            type="Task",
            status="In Progress",
            link="https://jira.example.com/browse/CNC-42"
        )
        for task in sub_tasks:
            self.ticket.add_sub_task(task)

    def test_basics(self):
        # sub-tasks
        self.assertEqual(len(self.ticket.sub_tasks), 5)
        self.assertIsInstance(self.ticket.sub_tasks[0], Ticket)

    def test_serialize(self):
        data = self.ticket.serialize(inc_subtasks=True)

        self.assertEqual(self.ticket.key, data['key'])
        self.assertEqual(self.ticket.summary, data['summary'])
        self.assertEqual(self.ticket.type, data['type'])
        self.assertEqual(self.ticket.status, data['status'])
        self.assertEqual(self.ticket.link, data['link'])

        for i in range(0, len(self.ticket.sub_tasks)):
            task = self.ticket.sub_tasks[i]
            self.assertDictEqual(task.serialize(), data['sub_tasks'][i], F"sub_task #{i}")











#
