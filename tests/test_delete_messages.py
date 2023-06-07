from django.test import Client, TestCase
from appmessages.models import Message


class MessageDeletionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MessageDeletionTest, cls).setUpClass()
        cls.client = Client()

    def test_delete_single_message(self):
        self.message = Message.objects.create(recipient="apansson", text="Hej!")
        message_id = self.message.id

        response = self.client.delete(
            path=f"/api/messages?id={self.message.id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("delete_count"), "1")
        self.assertEqual(Message.objects.filter(id=message_id).exists(), False)

    def test_delete_multiple_messages(self):
        self.message1 = Message.objects.create(recipient="apansson", text="Hej!")
        self.message2 = Message.objects.create(recipient="bepansson", text="Hoj!")
        message_ids = [self.message1.id, self.message2.id]

        response = self.client.delete(
            path=f"/api/messages?id={self.message1.id}&id={self.message2.id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("delete_count"), "2")
        self.assertEqual(Message.objects.filter(id__in=message_ids).exists(), False)

    def test_delete_no_ids_passed(self):
        response = self.client.delete(
            path="/api/messages",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_single_non_existing_message(self):
        response = self.client.delete(
            path="/api/messages?id=1",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("delete_count"), "0")

    def test_delete_multiple_non_existing_messages(self):
        response = self.client.delete(
            path="/api/messages?id=1&id=2",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("delete_count"), "0")

    def test_delete_existing_and_non_existing_messages(self):
        self.message = Message.objects.create(recipient="apansson", text="Hej!")
        message_id = self.message.id

        response = self.client.delete(
            path=f"/api/messages?id={message_id}&id={message_id+1}",
            content_type="application/json",
        )
        self.assertEqual(response.json().get("delete_count"), "1")
        self.assertEqual(response.status_code, 200)
