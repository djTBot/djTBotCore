from djTBotCore import TBotMessage


class TBotUpdate:
    __slots__ = (
        '__handler'
    )

    def __init__(self, handler):
        self.__handler = handler

    def message_handler(self, message, *args, **kwargs):
        from users.models import User
        tbot_message = TBotMessage(message)
        user_entry = User.get_user(tbot_message)
        pass
        return self.__handler(tbot_message)
        # return f'ПРИВІТ! Працює!!!! ID:{message.chat.id}'