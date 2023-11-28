import asyncio
import os
import threading
import time

from django.apps import AppConfig
from djTBotCore.manager import TBotManager


class djTBotCore__Config(AppConfig):
    name = 'djTBotCore';

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  # Prevent double run
            tbot_manager: TBotManager = TBotManager.get_manager()
            tbot_manager.start()
            pass
