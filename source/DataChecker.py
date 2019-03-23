import os
import hashlib
import sys

sys.path.append('./source')


class DataChecker(object):
    def checkout():
        try:
            os.path.exists('./source/StaticData.py')
        except:
            pass
        DataChecker.check_md5()
        try:
            from StaticData import StaticData
            if len(StaticData.admins) < 1:
                print('There\'re no admins in StaticData. Specify them.')
                exit()
            if len(StaticData.groups) < 1:
                print('There\'re no groups from which posts will be steal. Specify them.')
                exit()
            if os.path.exists(StaticData.inipath) is not True:
                print('Bad ini file path in StaticData. Correct it.')
                exit()
        except ImportError:
            print('Can\'t find the StaticData.py. Where?')
            exit()
        except Exception as e:
            print(str(e))
            print('Error while DataCheck.')

    def check_md5():
        md5s = {'Preview.py': '6a4e20296821c8ad09921edb342ec9e0',
                'VkApiException.py': '6bb39b798551ad130af6d561fe50d1f6',
                'ApiWorker.py': 'c43e19515567e64eaa8a90e77b1cc4ec',
                'StaticMethods.py': '2dd06bf088c82518f466598fa461921a',
                'InputWorker.py': 'a72020c17f10a3883dc1911af4661622',
                'UserApi.py': '9c26253a2d6966071fed7af258f17d11',
                'ConsoleWorker.py': 'ab0b55981d3d63049f1a5cf678626777',
                'BotApi.py': '3c83fd7cced062c02cdb876cd8634d29',
                'ExitHandler.py': '5535a510a8544d4fc7b7fe0c127582fb',
                'TimeHandler.py': '7018a0d8362d58c849752104d32a4a28',
                'ImageHandler.py': 'fabbfa49165226ee9e613fca25e36971', }

        files = DataChecker.get_files()
        output = []
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
        allowed_files = ['Preview.py', 'VkApiException.py', 'ApiWorker.py', 'StaticMethods.py', 'InputWorker.py',
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
