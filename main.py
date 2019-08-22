import sys
from display.commandline_display import Display
from parsers.parser_factory import ChatFileParser


args = sys.argv
args.pop(0)

if __name__ == '__main__':
    filepath = args[0]
    w = ChatFileParser(filepath)
    conversations = w.parse_conversations()
    conversation = conversations[0]
    Display(conversation)
