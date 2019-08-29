from settings import config
import re

# a function input file path and return parser object


class Parser:
    group_conversations = []
    personal_conversations = []
    conversations = []
    im: str

    def __init__(self, file_paths, *args, **kwargs):
        if not isinstance(file_paths, list):
            file_paths = [file_paths]
        self.file_paths = file_paths
        self.file_texts = self.read_files()

    def read_files(self):
        file_texts = []
        for file_path in self.file_paths:
            with open(file_path, 'r') as chat_file:
                file_texts.append(chat_file.read())
        return file_texts

    def populate_conversations(self):
        pass

    def __str__(self):
        return f"Parser Object"

    def __repr__(self):
        return f"Parser({self.file_paths})"
