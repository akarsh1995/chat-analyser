from settings.config import IMConfig
from datetime import datetime
import re

class Sender():
    name: str
    def __init__(self, name, *args, **kwargs):
        self.name = name.title()
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        return f"Sender('{self.name}')"
    
    def __eq__(self, value):
        if isinstance(value, str):
            return self.name == value
        elif issubclass(type(value), Sender):
            return self.name == value.name
        raise TypeError(f'{value} should either be an instance of str or Sender')
    

class Text():
    
    def __init__(self, text: str, *args, **kwargs):
        self.text = text
        self.config = IMConfig()
        
    def get_clean_text(self):
        pass
    
    def get_words(self):
        return re.findall(self.config.word_regex, self.text)

    
    def get_char_count(self):
        return len(re.findall(self.config.char_regex, self.text))
    
    def get_word_count(self):
        return len(self.get_words())

    def __str__(self):
        return f"{self.text}"
    
    def __repr__(self):
        return f"Text('{self.text}')"

class Message():

    date_time: datetime
    is_media: bool = False

    def __init__(self, *args, **kwargs):
        self.config = IMConfig()
        super(Message, self).__init__(*args, **kwargs)

    def __str__(self):
        date = self.date_time.strftime(self.config.date_strftime_fmt)
        time = self.date_time.strftime(self.config.time_strftime_fmt)
        return f"Message by {self.sender} on {date} at {time}"

    def __eq__(self, other):
        if not isinstance(other, Message):
            raise TypeError(f"Does {type(other)} is not a valid message type.")
        return self.sender == other.sender and \
               self.date_time == other.date_time and \
               self.text == other.text

    def add_date_time(self, date_time):
        if not isinstance(date_time, datetime):
            try:
                date_time = datetime.strptime(date_time, "%d/%m/%Y, %H:%M")
            except TypeError:
                print("Sorry the date provided should be the datetime object or in the format dd/mm/YYYY, H:M")
    #         parse datetime and store
        self.date_time = date_time

    def add_sender(self, sender):
        if issubclass(type(sender), Sender):
            self.sender = sender
        elif not isinstance(sender, Sender) and isinstance(sender, str):
            self.sender = Sender(sender)
        else:
            raise TypeError(f'{sender} is not instance of {str} or {Sender}')

    def add_text(self, text):
        if not isinstance(text, Text):
            text = Text(text)
        self.text = text

    def set_media(self):
        self.is_media = True

    def __repr__(self):
        date = self.date_time.strftime("%d/%m/%Y, %H:%M")
        return f"Message.from_args('{date}', '{self.sender.name}', '{self.text.text}')"

    @classmethod
    def from_args(cls, date_time, sender, text):
        m = cls()
        m.add_date_time(date_time=date_time)
        m.add_sender(sender=sender)
        m.add_text(text=text)
        return m
    