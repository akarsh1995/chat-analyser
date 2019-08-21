import json
from parsers.parser import Parser
from message.message import Message
from conversation.conversation import Conversation
# exclude message forwarded from
# exclude type == service message


class Text:
    _bad_text_types = ['phone', 'hashtag', 'pre']

    def __init__(self, message_texts):

        if not self._is_list(message_texts):
            self.message_text = message_texts
        else:
            self.message_texts = message_texts
            self.message_text = self._get_text()

    def get_text(self):
        return self.message_text

    def _get_text(self):
        temp_text = ''
        for text in self.message_texts:
            text_type, t_text = self._get_type_and_text(text)
            if text_type not in self._bad_text_types:
                temp_text += t_text
        return temp_text

    def _get_type_and_text(self, text):
        if self._is_normal_text(text):
            return 'text', text
        return text["type"], text["text"]

    def _is_normal_text(self, text):
        return not isinstance(text, dict)

    def _is_list(self, obj):
        return isinstance(obj, list)


class TelegramMessageObject(Message):

    _bad_types = ['service']

    def __init__(self, message: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.t_message_dict = message
        if not self.is_bad():
            self.add_date_time(self.get_date_time())
            self.add_sender(self.get_sender())
            self.add_text(self.get_text())
            self.set_media()

    def is_bad(self):
        return self.get_type() in self._bad_types

    def get_id(self):
        return self.t_message_dict.get('id')

    def get_type(self):
        return self.t_message_dict.get('type')

    def get_date_time(self):
        from datetime import datetime
        return datetime.fromisoformat(self.t_message_dict.get('date'))

    def get_sender(self):
        return self.t_message_dict.get('from')

    def from_id(self):
        return self.t_message_dict.get('from_id')

    def get_text(self):
        return Text(self.t_message_dict.get('text')).get_text()

    def set_media(self):
        self.is_media = bool(self.get_media_type())

    def get_media_type(self):
        return self.t_message_dict.get('media_type')


class TelegramTextMessageObject(TelegramMessageObject):
    pass


class TelegramConversationObject(Conversation):

    def __init__(self, conversation_dict, *args, **kwargs):
        self.conversation_dict = conversation_dict
        messages = self.extract_messages()
        if messages:
            super().__init__(messages)

    @property
    def conversation_type(self):
        return self.conversation_dict['type']

    def conversation_id(self):
        return self.conversation_dict['id']

    def extract_messages(self):
        messages = self.conversation_dict["messages"]
        messages = [TelegramTextMessageObject(message) for message in messages]
        messages = [message for message in messages if not message.is_bad()]
        return messages

    @property
    def is_personal(self):
        return self.conversation_type == 'personal_chat'

    @property
    def name(self):
        return self.conversation_dict["name"]

    def filter(self):
        pass


class TelegramParser(Parser):
    conversations = []

    def __init__(self, filepath, *args, **kwargs):
        super().__init__(filepath, *args, **kwargs)
        self.parsed_file = json.loads(self.file_text)

    def populate_conversations(self):
        if self.conversations:
            print('Already parsed.')
        conversations = self.parsed_file['chats']['list']
        if conversations:
            for conversation in conversations:
                conversation_obj = TelegramConversationObject(conversation)
                if conversation_obj.messages_are_present:
                    self.conversations.append(conversation_obj)

    @property
    def conversations_are_present(self):
        if not self.conversations:
            print("Maybe the file does not contain any conversation.")
        return bool(self.conversations)
