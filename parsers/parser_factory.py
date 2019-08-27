# In serializers.py
from parsers.telegram import TelegramParser
from parsers.whatsapp import WhatsAppParser
from settings.config import IMConfig
import re


class ParserFactory:

    def __init__(self):
        self._creators = {}

    def register_parser(self, _format, creator):
        self._creators[_format] = creator

    def get_parser(self, _format):
        creator = self._creators.get(_format)
        if not creator:
            raise ValueError(_format)
        return creator


factory = ParserFactory()
factory.register_parser('WhatsApp', WhatsAppParser)
factory.register_parser('Telegram', TelegramParser)


class ChatFileParser:

    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.file_text = f.read(100)

    def parse_conversations(self):
        parser = factory.get_parser(self.im)
        parser_obj = parser(self.filepath)
        parser_obj.populate_conversations()
        return parser_obj.conversations

    @property
    def im(self):
        for im, hooks in IMConfig.HOOKS.items():
            if re.match('|'.join(['(' + x + ')' for x in hooks]), self.file_text):
                return im
