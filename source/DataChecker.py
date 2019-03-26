import os

class DataChecker(object):
    def checkout():
        try:
            from Config import StaticData
            if len(StaticData.admins) < 1:
                print('There\'re no admins in Config.py . Specify them.')
                exit()
            if len(StaticData.groups) < 1:
                print('There\'re no groups in Config.py from which posts will be steal. Specify them.')
                exit()
            if StaticData.vk_user_token == "":
                print('There\'re no user token in Config.py . Specify it.')
                exit()
            if StaticData.vk_community_token == "":
                print('There\'re no community token in Config.py . Specify it.')
                exit()
            if StaticData.vk_community_id == "":
                print('There\'re no community ID in Config.py . Specify it.')
                exit()
            if os.path.exists('./source/waterx.png') is False:
                print('There\'re no waterx.png in "source" folder. Add it.')
                exit()
        except ModuleNotFoundError:
            print('Can\'t find the Config.py . Where?')
            exit()
        except Exception as e:
            print(str(e))
            print('Error while DataCheck.')
            exit()
