import unittest
import faker
from cartaro.model.ticket import Ticket

class TicketTest(unittest.TestCase):

    FAKER = faker.Faker()

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

    def _gen_jira_issue(self, key_prefix='CNC'):
        key = self.FAKER.random_int()
        issue = {
            'key': F"{key_prefix}-{key:04}",
            'fields': {
                'summary': self.FAKER.sentence(),
                'issuetype': { 
                    'name': self.FAKER.random_element(elements=('Story','Task','Bug'))
                },
                'status': {
                    'name': self.FAKER.random_element(elements=('New', 'Open', 'In Progress', 'Closed'))
                },
                'subtasks': []
            }
        }
        return issue

    def _gen_jira_data(self, count):
        data = { 'issues': [] }

        for i in range(0, count):
            issue = self._gen_jira_issue()
            # Create `i` sub-tasks
            for j in range(0, i):
                sub_task = self._gen_jira_issue(key_prefix='SUB')
                issue['fields']['subtasks'].append(sub_task)
        
            data['issues'].append(issue)

        return data

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

    def test_parse_jira(self):
        jira_host = 'http://jira.simulcrum.com'
        jira_data = self._gen_jira_data(3)

        tickets = Ticket.parse_jira(jira_host, jira_data)

        self.assertEqual(len(tickets), len(jira_data['issues']))
        self.assertIsInstance(tickets[0], Ticket)

        # Test Fields
        self.assertEqual(tickets[0].key, jira_data['issues'][0]['key'])
        self.assertEqual(tickets[0].summary, jira_data['issues'][0]['fields']['summary'])
        self.assertEqual(tickets[0].type, jira_data['issues'][0]['fields']['issuetype']['name'])
        self.assertEqual(tickets[0].status, jira_data['issues'][0]['fields']['status']['name'])
        self.assertEqual(tickets[0].link, F"{jira_host}/browse/{jira_data['issues'][0]['key']}")

        # Sub-tasks
        self.assertEqual(len(tickets[2].sub_tasks), 2)
        self.assertIsInstance(tickets[2].sub_tasks[0], Ticket)
        self.assertRegex(tickets[2].sub_tasks[0].key, 'SUB-')












#
