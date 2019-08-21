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
        self.message = message
        if not self.is_bad():
            self.add_date_time(self.get_date_time())
            self.add_sender(self.get_sender())
            self.add_text(self.get_text())
            self.set_media()

    def is_bad(self):
        return self.get_type() in self._bad_types

    def get_id(self):
        return self.message.get('id')

    def get_type(self):
        return self.message.get('type')

    def get_date_time(self):
        from datetime import datetime
        return datetime.fromisoformat(self.message.get('date'))

    def get_sender(self):
        return self.message.get('from')

    def from_id(self):
        return self.message.get('from_id')

    def get_text(self):
        return Text(self.message.get('text')).get_text()

    def set_media(self):
        self.is_media = bool(self.get_media_type())

    def get_media_type(self):
        return self.message.get('media_type')


class TelegramTextMessageObject(TelegramMessageObject):
    pass


class TelegramConversationObject(Conversation):

    def __init__(self, conversation_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversation_dict = conversation_dict
        self.populate_messages()

    @property
    def conversation_type(self):
        return self.conversation_dict['type']

    def conversation_id(self):
        return self.conversation_dict['id']

    def populate_messages(self):
        messages = self.conversation_dict["messages"]
        messages = [TelegramTextMessageObject(message) for message in messages]
        messages = [message for message in messages if not message.is_bad()]
        self.messages = messages

    @property
    def is_personal(self):
        return self.conversation_type == 'personal_chat'

    @property
    def name(self):
        return self.conversation_dict["name"]

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        message = self.messages[self.counter]
        self.counter += 1
        return message

    def filter(self):
        pass


class TelegramParser(Parser):

    def __init__(self, filepath, *args, **kwargs):
        super().__init__(filepath, *args, **kwargs)
        self.parsed_file = json.loads(self.file_text)

    def populate_conversations(self):
        if self.conversations:
            print('Already parsed.')
        conversations = self.parsed_file['chats']['list']
        if conversations:
            self.conversations += [TelegramConversationObject(conversation) for conversation in conversations]

    @property
    def conversations_are_present(self):
        if not self.conversations:
            print("Maybe the file does not contain any conversation.")
        return bool(self.conversations)
