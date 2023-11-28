import threading
import asyncio
from asgiref.sync import sync_to_async, async_to_sync

from telebot.async_telebot import AsyncTeleBot

from django.conf import settings


class TBotManager:
    __slots__ = (
        '__BOT',
        '__TELEGRAM_BOT_TOKEN',
        '__handlers_menu',
    )

    def get_handler_menu(self):
        return self.__handlers_menu

    def get_token(self):
        return self.__TOKEN

    def __init__(self, TELEGRAM_TOKEN):
        self.__BOT = None
        self.__TELEGRAM_BOT_TOKEN = TELEGRAM_TOKEN
        self.__handlers_menu = {}
        pass

    @staticmethod
    def get_manager():
        if settings.TBOT_MANAGER is None:
            settings.TBOT_MANAGER = TBotManager(TELEGRAM_TOKEN=settings.TELEGRAM_BOT_TOKEN)

        return settings.TBOT_MANAGER

    def reg_handler(self, menu_text, handler):
        self.__handlers_menu[menu_text] = handler

    def send_broadcast_message(self, tbo_message):
        from telegram import Bot

        # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

        # application = Application.builder().token("TOKEN").build()

        # on different commands - answer in Telegram
        # application.add_handler(CommandHandler("start", start))
        # application.add_handler(CommandHandler("help", help_command))

        # on non command i.e message - echo the message on Telegram

        # Run the bot until the user presses Ctrl-C
        # application.run_polling(allowed_updates=Update.ALL_TYPES)

        from users.models import User
        res1 = User.objects.get_all()
        # TODO Create async call
        for cur_user in res1:
            bot_info = Bot(settings.TELEGRAM_BOT_TOKEN)
            asyncio.run(bot_info.send_message(text=tbo_message.text, chat_id=cur_user['telegram_id']))
            # await self.__BOT.send_message(cur_user['telegram_id'], "OOOO")

    async def chat_handler_menu(self, message, handler):
        async_handler = asyncio.to_thread(handler, message)
        return_message = await async_handler

        if return_message.is_broadcast:
            from users.models import User

            res1 = await sync_to_async(User.objects.get_all, thread_sensitive=True)()
            # TODO Create async call
            for cur_user in res1:
                await self.__BOT.send_message(cur_user['telegram_id'], return_message.text)
        else:
            await self.__BOT.send_message(message.chat.id, return_message)

    async def chat_send_message(self, chat_id = None, text: str = None):
        await self.__BOT.send_message(chat_id, text)

    async def dispatcher(self, message):
        text_message = message.json['text']
        if text_message[0:1] == "/":
            handler_menu = self.get_handler_menu()
            menu_name = text_message[1:]
            if menu_name in handler_menu:
                handler = handler_menu[menu_name]

                await self.chat_handler_menu(
                    handler=handler,
                    message=message)
            else:
                await self.chat_send_message(message.chat.id, f"Menu {menu_name} does not available")
                # TODO Save log (incorrect menu name)
        else:
            # TODO Dialogue Processing
            pass

        await self.chat_send_message(message.chat.id, "Check OK")

    def start(self):
        def worker():
            self.__BOT = AsyncTeleBot(self.__TELEGRAM_BOT_TOKEN)
            self.__BOT.register_message_handler(self.dispatcher)
            asyncio.run(self.__BOT.polling())

        # async def start_executor(message):
        #     await bot.send_message(message.chat.id, 'Async')
        #     result = await asyncio.to_thread(message_execution, bot, message)
        #     await bot.send_message(message.chat.id, result)
        #     # await print(result)
        #     # await threading.Thread(target=message_execution, daemon=True, args=(bot,message,)).start()
        #     pass

        # bot.register_message_handler(start_executor, commands=['start'])

        threading.Thread(target=worker, daemon=True).start()
        pass
