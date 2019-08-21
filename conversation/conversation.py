from message.message import Message, Sender
from statistics import mean
from collections import Counter, defaultdict
import numpy as np
from NLP.cleaning import WordCloudGenerate
import pandas as pd
from settings.config import IMConfig
import re


class Conversation:
    _messages = []
    _senders = []
    _senders_message_list: dict

    def __init__(self, messages, *args, **kwargs):
        if not isinstance(messages, list):
            messages += [messages]
        if all([isinstance(msg, Message) for msg in messages]):
            self._messages = messages
        else:
            raise TypeError(f'Not all the messages is the instance of {type(Message)}')
        self.populate_senders()

    def message_count(self):
        message_count = {}
        for sender, messages in self.messages_by_sender().items():
            if messages:
                message_count[sender] = len(messages)
        return message_count

    def words_per_message(self):
        words_per_message = {}
        for sender, messages in self.messages_by_sender().items():
            if messages:
                average = mean([message.text.get_word_count() for message in messages])
                words_per_message[sender] = round(average, 2)
        return words_per_message

    def avg_wordlength(self):
        msg_by_sender = self.messages_by_sender()
        # total chars / total words
        count_chars = lambda text: len(re.findall(IMConfig().char_regex, text))
        count_words = lambda text: len(re.findall(IMConfig().word_regex, text))

        for k, v in msg_by_sender.items():
            re.findall()

    def characters_per_message(self):
        characters_per_message = {}
        for sender, messages in self.messages_by_sender().items():
            if messages:
                average = mean([message.text.get_char_count() for message in messages])
                characters_per_message[sender] = round(average, 2)
        return characters_per_message

    def media_count(self):
        msg_by_sender = self.messages_by_sender()
        media_count = lambda msgs: sum([m.is_media for m in msgs])
        return {k: media_count(v) for k, v in msg_by_sender.items()}

    def top_frequency_words(self, n) -> dict:
        """
        returns: dictionary
        """
        top_frequency_words = {}
        for sender, messages in self.messages_by_sender().items():
            counter = Counter()
            if messages:
                for message in messages:
                    counter.update(message.text.get_words())
                top_frequency_words[sender] = counter.most_common(n)
        return top_frequency_words

    def weekdaywise_count(self):
        counter = Counter()
        if self._messages_are_present:
            for message in self._messages:
                counter.update([message.date_time.strftime("%A")])
        return counter

    def hourwise_count(self):
        counter = Counter()
        if self._messages_are_present:
            for message in self._messages:
                counter.update([message.date_time.hour])
        return counter

    def add_message(self, message: Message):
        if message:
            self._messages.append(message)

    def populate_senders(self):
        senders = []
        if self._messages_are_present:
            for message in self._messages:
                if not message.sender in senders:
                    senders += [message.sender]
            self._senders = senders
        else:
            raise Exception('Messages are not present in conversation object.')

    def delete_messages(self, range):
        pass

    def get_messages(self, sender):
        if isinstance(sender, Sender):
            sender = sender.name
        if isinstance(sender, str):
            if sender in self._senders:
                return self.messages_by_sender()[sender]
            else:
                raise Exception(f"No sender exist by the name {sender}: try names {[s.name for s in self._senders]}")
        else:
            raise TypeError(f"Check the type {type(sender)} should be either {type(str)} or {type(Sender)}")

    def change_sender_name(self, sender=None, to_name=None):
        if sender:
            if sender in self._senders:
                if to_name:
                    if self._messages_are_present:
                        for message in self._messages:
                            if sender == message.sender:
                                message.add_sender(to_name)
                        self.populate_senders()
        else:
            sender, to_name = self._sender_name_input()
            self.change_sender_name(sender, to_name)

    def _sender_name_input(self):
        senders_available = [s.name for s in self._senders]
        if senders_available:
            print('Which sender you want to change the name of:')
            for i, s in enumerate(senders_available):
                print(str(i + 1) + ':', s)
            ip = int(input())
            sender_name_change = senders_available[ip - 1]
            if sender_name_change:
                print('What name do you want to set ?')
                ip_name = input()
                if ip_name:
                    return sender_name_change, ip_name
                else:
                    self._sender_name_input()
        else:
            raise Exception('No participants are present in the conversation.')

    def messages_by_sender(self) -> dict:
        if hasattr(self, '_senders_message_list'):
            return self._senders_message_list

        senders_message_list = defaultdict(list)
        if self._messages_are_present:
            for message in self._messages:
                senders_message_list[message.sender.name].append(message)
        self._senders_message_list = senders_message_list
        return senders_message_list

    def save_wordcloud(self):
        import uuid
        text = ' '.join([m.text.text for m in self._messages])
        WordCloudGenerate(text).save_wordcloud(str(uuid.uuid4()) + '.png')

    def conversation_type(self):
        # self.populate_senders()
        if self._senders:
            return 'group' if len(self._senders) > 2 else 'personal'

    def get_convo_df(self):
        m_dict = defaultdict(list)
        if self._messages_are_present:
            for message in self._messages:
                if not message.is_media:
                    m_dict['date_time'] += [message.date_time]
                    m_dict['sender'] += [message.sender]
                    m_dict['text'] += [message.text]
        return pd.DataFrame(m_dict)

    @property
    def _messages_are_present(self):
        return bool(self._messages)

    def most_active_day(self):
        counter = Counter()
        if self._messages_are_present:
            for message in self._messages:
                counter.update([message.date_time.date()])
        return (
            counter.most_common(1)[0][0],
            counter.most_common(1)[0][1]
        )

    def longest_continue_conversation(self, timegap):
        timegap = np.timedelta64(timegap, 'm')
        date_times = []
        for message in self._messages:
            date_times.append(message.date_time)
        date_times = np.array(date_times, dtype=np.datetime64)
        date_times = date_times.astype('datetime64[m]')
        consecutive_difference = date_times[2:] - date_times[1:-1]
        split_at = consecutive_difference >= timegap
        split_at = np.insert(split_at, 0, True if split_at[0] else False)
        split_slices = np.where(split_at)
        date_times = np.split(date_times, split_slices[0] + 1)
        conversation_stretch = []
        for date_time_set in date_times:
            conversation_stretch.append(date_time_set[-1] - date_time_set[0])
        max_conversation_stretch = max(conversation_stretch)
        idx = conversation_stretch.index(max_conversation_stretch)
        max_datetime = date_times[idx]
        message_count = len(max_datetime)
        starts_at, ends_at = max_datetime[0].item(), max_datetime[-1].item()
        # starts_at, ends_at = max_datetime[0].item().strftime("%b%e, %y at%l:%M %p"), max_datetime[-1].item().strftime("%b%e, %y at%l:%M %p")

        # d, h, m = Conversation.days_hours_minutes(max_datetime[-1]-max_datetime[0])
        # print(f"The longest converstaion starts {starts_at} and ends {ends_at}, duration: "
        #       f"{str(d)+' days' if d else ''}{str(h)+' hrs' if h else ''}{str(m)+' mins' if m else ''}")
        return starts_at, ends_at, message_count

    @staticmethod
    def days_hours_minutes(td):
        td = td.item()
        return td.days, td.seconds // 3600, (td.seconds // 60) % 60

    def __str__(self):
        # self.populate_senders()
        if len(self._senders) > 2:
            return f"Group Conversation between {len(self._senders)} people."
        elif len(self._senders) == 2:
            person1 = self._senders[0]
            person2 = self._senders[1]
            return f"Personal Conversation between {person1} and {person2}."
        else:
            return f"No sender exist in the conversation."

    def __repr__(self):
        return self.__str__()
