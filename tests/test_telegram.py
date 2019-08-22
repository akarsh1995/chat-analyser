import unittest
from parsers.telegram import TelegramParser
from datetime import datetime


class TelegramTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        wp = TelegramParser('./data/telegram.json')
        wp.populate_conversations()
        cls.conversation1 = wp.conversations[0]
        cls.conversation2 = wp.conversations[1]
        cls.conversation1.populate_senders()
        cls.conversation2.populate_senders()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_word_count(self):
        self.assertEqual(self.conversation1._messages[0].text.get_word_count(), 5)

    def test_letter_count(self):
        self.assertEqual(self.conversation1._messages[0].text.get_char_count(), 19)

    def test_date(self):
        self.assertEqual(self.conversation1._messages[0].date_time, datetime.fromisoformat('2019-02-11T21:49:13'))
        self.assertEqual(self.conversation2._messages[1].date_time, datetime.fromisoformat('2019-02-11T21:49:15'))
