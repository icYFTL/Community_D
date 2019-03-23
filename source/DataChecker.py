import os
import hashlib

class DataChecker(object):
    def checkout():
        DataChecker.check_md5()
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

    def check_md5():
        md5s = {'Preview.py': 'be50193c3eb3b6dcbd276286ef9c69cd',
                'VkApiException.py': '6bb39b798551ad130af6d561fe50d1f6',
                'ApiWorker.py': 'b86b76b1b8a02016554dd19711d77baa',
                'StaticMethods.py': '2dd06bf088c82518f466598fa461921a',
                'UserApi.py': '3d341e3466741710ccaac3df57975be0',
                'ConsoleWorker.py': 'ab0b55981d3d63049f1a5cf678626777',
                'BotApi.py': '3be0bfdeae9fdac8ea019b5add86f665',
                'ExitHandler.py': '5535a510a8544d4fc7b7fe0c127582fb',
                'TimeHandler.py': '7dd230e076e24d6a888671ebee7328f9',
                'ImageHandler.py': 'fabbfa49165226ee9e613fca25e36971', }

        files = DataChecker.get_files()
        for file in files:
            name = file
            md5_original = md5s.get(name)
            f = open('./source/' + file, 'rb')
            file = f.read()
            f.close()
            md5 = hashlib.md5(file).hexdigest()
            if md5 != md5_original:
                print(md5)
                print('Not original file: {}'.format(name))

    def get_files():
        files = []
        allowed_files = ['Preview.py', 'VkApiException.py', 'ApiWorker.py', 'StaticMethods.py',
                         'UserApi.py',
                         'ConsoleWorker.py', 'BotApi.py', 'ExitHandler.py', 'TimeHandler.py',
                         'ImageHandler.py', ]
        try:
            for i in os.walk('./'):
                files.append(i)
            tempmas = []
            for address, dirs, files in files:
                for file in files:
                    if file in allowed_files:
                        tempmas.append(file)
            files = tempmas
        except:
            print(
                'Can\'t find the "source" folder.\n\nTry delete folder with script and make "git clone https://github.com/icYFTL/Community_D" again.')
        if allowed_files != files:
            print(
                'You have missing files.\nTry delete folder with script and make "git clone https://github.com/icYFTL/Community_D"')
        return files
