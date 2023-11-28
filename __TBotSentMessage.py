class TBotSentMessage:
    __slots__ = (
        'text',
        '__broadcast',
    )

    def __init__(self, text=None, broadcast=False):
        self.text = text
        self.__broadcast = broadcast
        pass

    def set_broadcast(self, broadcast=True):
        self.__broadcast = broadcast

    @property
    def is_broadcast(self):
        return self.__broadcast