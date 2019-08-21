from conversation.conversation import Conversation


def hash_print(func):
    def inner(*args):
        val = func(*args)
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
        self.avg_words_per_message()
        self.display_character_count()
        self.display_most_active_day()

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
    def display_word_count(self, title='Word Count'):
        """word count of each user"""
        pass

    @dict_print
    def display_letter_count(self):
        """letter count of an individual"""
        pass

    def avg_letters_per_message(self):
        """average letters per message"""
        pass

    @dict_print
    def avg_words_per_message(self, title='Words per message'):
        """avg words per message"""
        return self._conversation.words_per_message(), title

    def display_average_word_length(self):
        pass

    @dict_print
    def display_character_count(self, title='Characters per message'):
        return self._conversation.characters_per_message(), title

    @dict_print
    def display_most_active_day(self, title='Most Active Day'):
        date, count = self._conversation.most_active_day()
        date = date.strftime('%a, %b %e, %Y')
        return {date: count}, title
