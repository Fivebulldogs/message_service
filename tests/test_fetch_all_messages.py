from django.test import Client, TestCase
from appmessages.models import Message


class MessageFetchAllMessagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MessageFetchAllMessagesTest, cls).setUpClass()
        cls.client = Client()

    def setUp(self) -> None:
        # create a number of messages (some new, some old)
        Message.objects.create(recipient="apansson", text="Hej!")
        Message.objects.create(recipient="bepansson", text="Hoj!", is_new=False)
        Message.objects.create(recipient="cepansson", text="Haj!")
        Message.objects.create(recipient="depansson", text="Huj!", is_new=False)

    def test_fetch_all_messages_no_indices(self):
        # fetch all messages, both messages should be returned although they are old
        response = self.client.get(
            path="/api/messages",
            content_type="application/json",
        )
        response_dict = response.json()

        self.assertEqual(len(response_dict), 4)
        self.assertEqual(response_dict[0]["recipient"], "depansson")
        self.assertEqual(response_dict[0]["is_new"], False)
        self.assertEqual(response_dict[0]["text"], "Huj!")

        self.assertTrue(response_dict[0]["id"] > response_dict[1]["id"])

        self.assertEqual(response_dict[1]["recipient"], "cepansson")
        self.assertEqual(response_dict[1]["is_new"], True)
        self.assertEqual(response_dict[1]["text"], "Haj!")

        self.assertTrue(response_dict[1]["id"] > response_dict[2]["id"])

        self.assertEqual(response_dict[2]["recipient"], "bepansson")
        self.assertEqual(response_dict[2]["is_new"], False)
        self.assertEqual(response_dict[2]["text"], "Hoj!")

        self.assertTrue(response_dict[2]["id"] > response_dict[3]["id"])

        self.assertEqual(response_dict[3]["recipient"], "apansson")
        self.assertEqual(response_dict[3]["is_new"], True)
        self.assertEqual(response_dict[3]["text"], "Hej!")

    def test_fetch_all_messages_by_start_and_stop_index_in_middle(self):
        # fetch messages with start and stop indices for the two "middle" messages
        response = self.client.get(
            path="/api/messages?start=1&stop=3",
            content_type="application/json",
        )
        response_dict = response.json()
        self.assertEqual(len(response_dict), 2)
        self.assertTrue(response_dict[0]["id"] > response_dict[1]["id"])
        self.assertEqual(response_dict[0]["recipient"], "cepansson")
        self.assertEqual(response_dict[0]["is_new"], True)
        self.assertEqual(response_dict[0]["text"], "Haj!")
        self.assertEqual(response_dict[1]["recipient"], "bepansson")
        self.assertEqual(response_dict[1]["is_new"], False)
        self.assertEqual(response_dict[1]["text"], "Hoj!")

    def test_fetch_all_messages_by_start_and_stop_index_all(self):
        # fetch messages with start and stop indices to include all messages
        response = self.client.get(
            path="/api/messages?start=0&stop=4",
            content_type="application/json",
        )
        response_dict = response.json()
        self.assertEqual(len(response_dict), 4)
        self.assertTrue(response_dict[0]["id"] > response_dict[1]["id"])
        self.assertEqual(response_dict[0]["recipient"], "depansson")
        self.assertEqual(response_dict[0]["is_new"], False)
        self.assertEqual(response_dict[0]["text"], "Huj!")

        self.assertTrue(response_dict[1]["id"] > response_dict[2]["id"])
        self.assertEqual(response_dict[1]["recipient"], "cepansson")
        self.assertEqual(response_dict[1]["is_new"], True)
        self.assertEqual(response_dict[1]["text"], "Haj!")

        self.assertTrue(response_dict[2]["id"] > response_dict[3]["id"])
        self.assertEqual(response_dict[2]["recipient"], "bepansson")
        self.assertEqual(response_dict[2]["is_new"], False)
        self.assertEqual(response_dict[2]["text"], "Hoj!")

        self.assertEqual(response_dict[3]["recipient"], "apansson")
        self.assertEqual(response_dict[1]["is_new"], True)
        self.assertEqual(response_dict[3]["text"], "Hej!")

    def test_fetch_all_messages_by_start_and_stop_index_first_only(self):
        response = self.client.get(
            path="/api/messages?start=0&stop=1",
            content_type="application/json",
        )
        response_dict = response.json()
        self.assertEqual(len(response_dict), 1)
        self.assertEqual(response_dict[0]["recipient"], "depansson")
        self.assertEqual(response_dict[0]["is_new"], False)
        self.assertEqual(response_dict[0]["text"], "Huj!")

    def test_fetch_all_messages_by_start_and_stop_index_last_only(self):
        # fetch messages with same start and stop index = 3
        response = self.client.get(
            path="/api/messages?start=3&stop=4",
            content_type="application/json",
        )
        response_dict = response.json()
        self.assertEqual(len(response_dict), 1)
        self.assertEqual(response_dict[0]["recipient"], "apansson")
        self.assertEqual(response_dict[0]["is_new"], True)
        self.assertEqual(response_dict[0]["text"], "Hej!")

    def test_fetch_all_messages_by_start_index_only(self):
        response = self.client.get(
            path="/api/messages?start=1",
            content_type="application/json",
        )
        response_dict = response.json()
        self.assertEqual(len(response_dict), 3)

        self.assertTrue(response_dict[0]["id"] > response_dict[1]["id"])
        self.assertEqual(response_dict[0]["recipient"], "cepansson")
        self.assertEqual(response_dict[0]["is_new"], True)
        self.assertEqual(response_dict[0]["text"], "Haj!")

        self.assertTrue(response_dict[1]["id"] > response_dict[2]["id"])
        self.assertEqual(response_dict[1]["recipient"], "bepansson")
        self.assertEqual(response_dict[1]["is_new"], False)
        self.assertEqual(response_dict[1]["text"], "Hoj!")

        self.assertEqual(response_dict[2]["recipient"], "apansson")
        self.assertEqual(response_dict[2]["is_new"], True)
        self.assertEqual(response_dict[2]["text"], "Hej!")

    def test_fetch_all_messages_by_stop_index_only(self):
        response = self.client.get(
            path="/api/messages?stop=3",
            content_type="application/json",
        )
        response_dict = response.json()
        self.assertEqual(len(response_dict), 3)
        self.assertTrue(response_dict[0]["id"] > response_dict[1]["id"])
        self.assertEqual(response_dict[0]["recipient"], "depansson")
        self.assertEqual(response_dict[0]["is_new"], False)
        self.assertEqual(response_dict[0]["text"], "Huj!")

        self.assertTrue(response_dict[1]["id"] > response_dict[2]["id"])
        self.assertEqual(response_dict[1]["recipient"], "cepansson")
        self.assertEqual(response_dict[1]["is_new"], True)
        self.assertEqual(response_dict[1]["text"], "Haj!")

        self.assertEqual(response_dict[2]["recipient"], "bepansson")
        self.assertEqual(response_dict[2]["is_new"], False)
        self.assertEqual(response_dict[2]["text"], "Hoj!")
