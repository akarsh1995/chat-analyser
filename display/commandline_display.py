from conversation.conversation import Conversation


def hash_print(func):
    def inner(*args):
        val = func(*args)
        print('')
        hashes = len(val) + 10
        print(''.center(hashes, '#'))
        print((' ' + str(val) + ' ').center(hashes, '#'))
        print(''.center(hashes, '#'))

    return inner


def dict_print(func):
    def _dict_print(*args):
        val = func(*args)
        val, title = val
        print('')
        print((' ' + title + ' ').center(40, '#'))
        for k, v in val.items():
            print(str(k).ljust(20) + str(v).rjust(20))
        print(''.center(40, '#'))

    return _dict_print


def days_hours_minutes(td):
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60


def make_plural(num):
    return 's' if num > 1 else ''


def h_m_s_convert(d, h, m):
    hs = f'{h} hr{make_plural(h)}' if h > 0 else ''
    ms = f'{m} min{make_plural(m)}' if m > 0 else ''
    return hs + (' ' if hs else '') + ms


class Display:

    def __init__(self, conversation: Conversation):
        if not isinstance(conversation, Conversation):
            raise TypeError(f"{type(conversation)} does not match {type(Conversation)}")
        self._conversation = conversation
        self.display_stats()

    def display_stats(self):
        """Displays the stats of your conversation"""
        self.display_title()
        self.display_message_count()
        self.display_media_count()
        self.display_words_per_message()
        self.display_character_count()
        self.display_most_active_day()
        self.display_longest_conversation()

    @hash_print
    def display_title(self):
        """Gets you the headline """
        return str(self._conversation)

    @dict_print
    def display_message_count(self, title='Message Count'):
        """Messages count of the individuals or group"""
        return self._conversation.message_count(), title

    @dict_print
    def display_media_count(self, title='Media Count'):
        """media count of the group"""
        return self._conversation.media_count(), title

    @dict_print
    def display_words_per_message(self, title='Words per Message'):
        """word count of each user"""
        return self._conversation.words_per_message(), title

    @dict_print
    def display_average_word_length(self):
        return self._conversation.avg_wordlength()

    @dict_print
    def display_character_count(self, title='Characters per message'):
        return self._conversation.characters_per_message(), title

    @dict_print
    def display_most_active_day(self, title='Most Active Day'):
        date, count = self._conversation.most_active_day()
        date = date.strftime('%a, %b %e, %Y')
        return {date: count}, title

    @hash_print
    def display_longest_conversation(self):
        starts_at, ends_at, message_count = self._conversation.longest_continue_conversation(6)
        d, h, m = days_hours_minutes(ends_at - starts_at)
        starts_at, ends_at = map(lambda date_time: date_time.strftime("%b %e, %y at%l:%M %p"), [starts_at, ends_at])
        return (f"The longest conversation starts {starts_at} and ends {ends_at}, duration: "
                f"{h_m_s_convert(d, h, m)}")
