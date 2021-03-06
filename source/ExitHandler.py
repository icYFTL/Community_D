import os
from source.BotApi import BotApi
from Config import Config
import hues


class ExitHandler:
    @staticmethod
    def bye():
        try:
            BA = BotApi(Config.vk_community_token)
            BA.write_msg('Скрипт был аварийно остановлен.', None)
        except:
            pass

        hues.warn('Shutting down...')

        try:
            os.remove('source/tmp/img.jpg')
        except:
            pass

        try:
            os.remove('./source/tmp/result.png')
        except:
            pass

        try:
            os.removedirs('./source/tmp/')
        except:
            pass
