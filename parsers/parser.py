from settings import config
import re

# a function input file path and return parser object


class Parser:
    group_conversations = []
    personal_conversations = []
    conversations = []
    im: str

    def __init__(self, filepath, *args, **kwargs):
        self.filepath = filepath
        self.file_text = self.read_file()

    def read_file(self):
        with open(self.filepath, 'r') as chat_file:
            file_text = chat_file.read()
        return file_text

    def populate_conversations(self):
        pass

    def __str__(self):
        return f"{self.guess_im} Parser Object"

    def __repr__(self):
        return f"Parser('{self.filepath}')"
