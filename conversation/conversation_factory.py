import conversation.conversation as conv


class ConversationFactory():
    def __init__(self):
        self._conversation_type = {
            'personal': conv.PersonalConversation,
            'group': conv.GroupConversation
        }

    def register_conversation(self, conv):
        pass

    def get_conversation_type(self, conversation_type):
        c_type = self._conversation_type[conversation_type]
        if not c_type:
            raise ValueError(conversation_type, f'Choose the correct conversation type '
                                                f'from {self._conversation_type.keys()}')
        return c_type
