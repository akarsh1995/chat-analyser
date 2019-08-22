import unittest
from parsers.whatsapp import WhatsappParser
from datetime import datetime


class WhatsappTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        wp = WhatsappParser('./data/whatsapp.txt')
        wp.populate_conversations()
        conversation = wp.conversations[0]
        cls.conversation = conversation

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.messages = self.conversation._messages

    def tearDown(self) -> None:
        pass

    def test_word_count(self):
        self.assertEqual(self.messages[0].text.get_word_count(), 9)

    def test_letter_count(self):
        self.assertEqual(self.messages[1].text.get_char_count(), 19)

    def test_date(self):
        self.assertEqual(self.messages[3].date_time, datetime.strptime('26/12/18, 1:59 am', '%d/%m/%y, %I:%M %p'))
