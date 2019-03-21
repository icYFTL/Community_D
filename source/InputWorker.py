import sys

sys.path.append('./source/exceptions/')

from BadIniException import BadIniException


import os
from configparser import ConfigParser
from configparser import ParsingError
from configparser import NoOptionError
from StaticData import StaticData



class InputWorker:
    def __init__(self):
        self.ini = ConfigParser()
        self.path = StaticData.inipath
        self.PathChecker()

    def PathChecker(self):
        try:
            self.ini.read(self.path)
        except ParsingError:
            raise BadIniException


    def WorkOut(self):
        try:
            token = self.ini.get("Data", "Token")
            token_c = self.ini.get("Data", "Token_c")
            return [token, token_c]
        except:
            raise BadIniException


