import unittest
from unittest.mock import MagicMock, patch

from skype_client import SkypeClient, SkypeContact

class MockSkypeClient(SkypeClient):
    def __init__(self):
        self.personal_contact = MagicMock()
        self.personal_contact.chat = 'personal_chat'
        self.personal_contact.name = 'Jeff Hsu'
        self.contacts = {'jeff': self.personal_contact}
        self.chats = {'19:group': 'group_chat'}

class TestSkypeClient(unittest.TestCase):
    def setUp(self):
        self.skype_client = MockSkypeClient()
        self.personal_target_id = 'jeff'
        self.group_target_id = '19:group'

    def test_get_contact(self):
        personal_contact = self.skype_client.get_contact(self.personal_target_id)
        self.assertEqual(
            SkypeContact('personal_chat', 'Jeff Hsu'),
            personal_contact
        )
        group_contact = self.skype_client.get_contact(self.group_target_id)
        self.assertEqual(
            SkypeContact('group_chat', 'Team'),
            group_contact
        )

class TestSkypeContact(unittest.TestCase):
    def setUp(self):
        self.contact_chat = MagicMock()
        self.contact_name = 'Jeff'
        self.skype_contact = SkypeContact(self.contact_chat, self.contact_name)
        self.alert_message = 'Test Alert'
        self.csv_path = 'path/to/csv'

    def test_send_message(self):
        self.skype_contact.send_message(self.alert_message)
        self.contact_chat.sendMsg.assert_called_once_with(
            f"Hi, {self.contact_name}\n{self.alert_message}"
        )

    def test_send_csv(self):
        with patch('builtins.open', new_callable=MagicMock) as mock_open:
            self.skype_contact.send_csv(self.csv_path)
            mock_open.assert_called_with(self.csv_path, "rb")
            self.contact_chat.sendFile.assert_called_once_with(
                mock_open(self.csv_path, "rb"), 
                self.csv_path
            )