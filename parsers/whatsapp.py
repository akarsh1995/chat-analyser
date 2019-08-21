from parsers.parser import Parser
from message.message import Message
from conversation.conversation import Conversation
import pandas as pd


class WhatsappParser(Parser):
    conversations = []

    def __init__(self, filepath, *args, **kwargs):
        super().__init__(filepath, *args, **kwargs)
        self.chat_df = self.set_parsed_df()

    def populate_conversations(self):
        messages = []
        for index, (date_time, sender, text) in self.chat_df.iterrows():
            m = Message.from_args(date_time, sender, text)
            if '<Media omitted>' in text:
                m.set_media()
            messages.append(m)
        self.conversations += [Conversation(messages)]

    def set_parsed_df(self):
        chat_df = pd.read_csv(self.filepath, sep='\n', header=None)
        chat_df['is_date'] = chat_df[0].str.contains(r'^\d?\d/\d?\d').cumsum()
        chat_df = chat_df.groupby('is_date')[[0]].sum()
        chat_df = chat_df[0].str.split(' - ', 1, expand=True)
        chat_df = pd.concat([chat_df[0], chat_df[1].str.split(':', 1, expand=True)], axis=1)
        chat_df.columns = ['date_time', 'sender', 'text']
        chat_df['date_time'] = pd.to_datetime(chat_df['date_time'])
        return chat_df
