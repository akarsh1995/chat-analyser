import re
from datetime import datetime
from parsers.parser import Parser
from message.message import Message
from conversation.conversation import Conversation
from settings.config import IMConfig


class WhatsAppConfig(IMConfig):

    def __init__(self):
        self.date_pattern = '\d?\d/\d\d/\d\d, \d\d:\d\d'

    def __str__(self):
        return f"WhatsApp Generated File Configuration"

    @property
    def IM_thread_pattern(self):
        return r'(^{})(?: - )(.*?)(?:: )(.+(?:(.*\n)*?))'.format(self.date_pattern)

    @property
    def IM_text_split_at(self):
        return r'\n(?={} - )'.format(self.date_pattern)

class WhatsappParser(Parser):

    def __init__(self, filepath, *args, **kwargs):
        super().__init__(filepath, *args, **kwargs)
        self.config = WhatsAppConfig()
        self.set_date_format()

    @staticmethod
    def get_date_time(match_obj, date_time_fmt):
        date = match_obj.group(1)
        parsed_date_time = datetime.strptime(date, date_time_fmt)
        return parsed_date_time

    @staticmethod
    def get_sender(match_obj):
        return match_obj.group(2)

    @staticmethod
    def get_text(match_obj):
        return match_obj.group(3)

    def populate_conversations(self):
        splitted_texts = self.get_splitted_texts()
        messages = []
        for text in splitted_texts:
            match_obj = re.match(self.config.IM_thread_pattern, text)
            if match_obj:
                date_time = WhatsappParser.get_date_time(match_obj, self.config.date_strptime_fmt)
                sender = WhatsappParser.get_sender(match_obj)
                text = WhatsappParser.get_text(match_obj)
                m = Message.from_args(date_time, sender, text)
                if '<Media omitted>' in text:
                    m.set_media()
                messages.append(m)
        self.conversations = [Conversation(messages)]

    def get_splitted_texts(self):
        if hasattr(self, '_splitted_texts'):
            return self._splitted_texts
        pattern = self.config.IM_text_split_at
        self._splitted_texts = re.split(pattern, self.file_text)
        return self._splitted_texts

    def set_date_format(self):
        pattern = r'^(?:\d?\d)\/(\d+)\/'
        month_deciding_range = [int(re.match(pattern, text).group(1)) for text in self.get_splitted_texts()]
        if max(month_deciding_range) > 12:
            f = '%m/%d/%y, %H:%M'
            self.config.date_strptime_fmt = f
