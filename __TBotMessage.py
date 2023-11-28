class TBotMessage:
    __slots__ = (
        'user',
        'chat'
    )

    def __init__(self, message):
        self.user = message.from_user
        self.chat = message.chat
        pass