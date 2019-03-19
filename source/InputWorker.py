import os
from configparser import ConfigParser
from configparser import ParsingError
from StaticData import StaticData
import FileController



class InputWorker:
    def __init__(self):
        self.ini = ConfigParser()
        self.path = StaticData.inipath
        self.PathChecker()

    def PathChecker(self):
        if os.path.exists(self.path):
            try:
                self.ini.read(self.path)
            except ParsingError:
                FileController.RemoveINI()
                self.path = False
        else:
            self.path = False

    def WorkOut(self):
        if self.path:
            token = self.ini.get("Data", "Token")
            token_c = self.ini.get("Data", "Token_c")
            return [token, token_c]
        else:
            print('Bad "Data.ini". Look readme.txt.')
            exit()
