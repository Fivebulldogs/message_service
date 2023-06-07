from django.test import Client, TestCase
from appmessages.models import Message


class MessageFetchNewMessagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MessageFetchNewMessagesTest, cls).setUpClass()
        cls.client = Client()

    def test_fetch_new_messages(self):
        # create two new messages
        Message.objects.create(recipient="apansson", text="Hej!")
        Message.objects.create(recipient="bepansson", text="Hoj!")

        # fetch new messages
        response = self.client.get(
            path="/api/messages/new",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        self.assertEqual(len(response_dict), 2)
        self.assertEqual(response_dict[0]["recipient"], "bepansson")
        self.assertEqual(response_dict[0]["is_new"], True)
        self.assertEqual(response_dict[0]["text"], "Hoj!")
        self.assertEqual(response_dict[1]["recipient"], "apansson")
        self.assertEqual(response_dict[1]["is_new"], True)
        self.assertEqual(response_dict[1]["text"], "Hej!")

        # fetch new messages again, no messages should be returned
        response = self.client.get(
            path="/api/messages/new",
            content_type="application/json",
        )
        response_dict = response.json()
        self.assertEqual(len(response_dict), 0)

    def test_fetch_new_messages_after_fetch_all_messages(self):
        # create two new messages
        Message.objects.create(recipient="apansson", text="Hej!")
        Message.objects.create(recipient="bepansson", text="Hoj!")

        # fetch "all" messages, but only the last one via start/stop index
        response = self.client.get(
            path="/api/messages?start=1&stop=2",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        self.assertEqual(len(response_dict), 1)
        self.assertEqual(response_dict[0]["recipient"], "apansson")
        self.assertEqual(response_dict[0]["is_new"], True)
        self.assertEqual(response_dict[0]["text"], "Hej!")

        # fetch new messages, only one messages should be returned
        response = self.client.get(
            path="/api/messages/new",
            content_type="application/json",
        )
        response_dict = response.json()
        self.assertEqual(len(response_dict), 1)

        self.assertEqual(response_dict[0]["recipient"], "bepansson")
        self.assertEqual(response_dict[0]["is_new"], True)
        self.assertEqual(response_dict[0]["text"], "Hoj!")
