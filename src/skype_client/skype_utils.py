from skpy import Skype

class SkypeClient(Skype):
    def __init__(self, sk_account, sk_password):
        super().__init__(sk_account, sk_password)

    @staticmethod
    def __is_group(target_id):
        return target_id[:2] == '19'
    
    def __get_contact_chat(self, target_id, is_group):
        if is_group:
            return self.chats[target_id]
        return self.contacts[target_id].chat
    
    def __get_contact_name(self, target_id, is_group):
        if is_group:
            return 'Team'
        return str(self.contacts[target_id].name)
    
    def get_contact(self, target_id):
        is_group = self.__is_group(target_id)
        contact_chat = self.__get_contact_chat(target_id, is_group)
        contact_name = self.__get_contact_name(target_id, is_group)
        return SkypeContact(contact_chat, contact_name)


class SkypeContact():
    def __init__(self, contact_chat, contact_name):
        self.chat = contact_chat
        self.name = contact_name

    def __str__(self):
        return f"SkypeContact(chat={self.chat}, name={self.name})"
    
    def __eq__(self, other):
        if not isinstance(other, SkypeContact):
            return False
        return (self.chat == other.chat and self.name == other.name)
    
    def __repr__(self):
        return self.__str__()

    def send_message(self, alert_message):
        msg = 'Hi, ' + self.name + '\n' + alert_message
        self.chat.sendMsg(msg)

    def send_csv(self, csv_path):
        self.chat.sendFile(open(csv_path, "rb"), csv_path)