import os
import hues


class DataChecker:
    @staticmethod
    def checkout():
        try:
            from Config import Config
            if len(Config.admins) < 1:
                hues.error('There\'re no admins in Config.py. Specify them.')
                exit()
            if len(Config.groups) < 1:
                hues.error('There\'re no groups in Config.py from which posts will be steal. Specify them.')
                exit()
            if Config.vk_user_token == "":
                hues.error('There\'re no user token in Config.py. Specify it.')
                exit()
            if Config.vk_community_token == "":
                hues.error('There\'re no community token in Config.py. Specify it.')
                exit()
            if Config.vk_community_id == "":
                hues.error('There\'re no community ID in Config.py. Specify it.')
                exit()
            if os.path.exists('./source/waterx.png') is False:
                hues.error('There\'re no waterx.png in "source" folder. Add it.')
                exit()
        except ImportError:
            hues.error('Can\'t find the Config.py. Where?')
            exit()
        except Exception as e:
            hues.warn(str(e))
            hues.error('Error while DataCheck.')
            exit()
