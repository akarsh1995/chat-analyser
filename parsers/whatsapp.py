from parsers.parser import Parser
from message.message import Message
from conversation.conversation import Conversation
import pandas as pd


def get_parsed_df(file_path):
    chat_df = pd.read_csv(file_path, sep='\n', header=None)
    chat_df['is_date'] = chat_df[0].str.contains(r'^\d?\d/\d?\d').cumsum()
    chat_df = chat_df.groupby('is_date')[[0]].agg(lambda x: '\n'.join(x))
    chat_df = chat_df[0].str.split(' - ', 1, expand=True)
    chat_df = pd.concat([chat_df[0], chat_df[1].str.split(r': ', 1, expand=True)], axis=1)
    chat_df.columns = ['date_time', 'sender', 'text']
    chat_df['date_time'] = pd.to_datetime(chat_df['date_time'])
    return chat_df


def get_conversation(df):
    messages = []
    for index, (date_time, sender, text) in df.iterrows():
        m = Message.from_args(date_time, sender, text)
        if '<Media omitted>' in text:
            m.set_media()
        messages.append(m)
    return Conversation(messages)


class WhatsAppParser(Parser):
    conversations = []
    chat_dfs: list = []

    def __init__(self, file_paths, *args, **kwargs):
        super().__init__(file_paths, *args, **kwargs)
        self.populate_dfs()

    def populate_conversations(self):
        for df in self.chat_dfs:
            self.conversations.append(get_conversation(df))

    def populate_dfs(self):
        self.chat_dfs = [get_parsed_df(file_path) for file_path in self.file_paths]
