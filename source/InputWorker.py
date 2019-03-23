import sys

sys.path.append('./source/exceptions/')

from StaticData import StaticData

from configparser import ConfigParser
from configparser import ParsingError


class InputWorker:
    def __init__(self):
        self.ini = ConfigParser()
        self.path = StaticData.inipath
        self.PathChecker()

    def PathChecker(self):
        # Checking ini file path exists
        try:
            self.ini.read(self.path)
        except ParsingError:
            print('Smth went wrong with Data.ini')
            exit()


    def WorkOut(self):
        # Getting tokens from Data.ini
        try:
            token = self.ini.get("Data", "Token")
            token_c = self.ini.get("Data", "Token_c")
            return [token, token_c]
        except:
            print('Smth went wrong with Data.ini')
            exit()
