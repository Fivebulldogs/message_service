from django.test import Client, TestCase
from appmessages.models import Message


class MessageCreationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MessageCreationTest, cls).setUpClass()
        cls.client = Client()

    def test_create_message(self):
        response = self.client.post(
            path="/api/messages",
            data={"recipient": "apansson", "text": "Hej!"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        message = Message.objects.get(
            id=response_dict.get("id"), recipient="apansson", text="Hej!"
        )
        self.assertEqual(message.id, response_dict.get("id"))
        self.assertEqual(message.recipient, response_dict.get("recipient"))
        self.assertEqual(message.text, response_dict.get("text"))
        self.assertEqual(message.is_new, True)

    def test_create_message_without_recipient(self):
        response = self.client.post(
            path="/api/messages",
            data={"text": "Hej!"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)

    def test_create_message_without_text(self):
        response = self.client.post(
            path="/api/messages",
            data={"text": "Hej!"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)
