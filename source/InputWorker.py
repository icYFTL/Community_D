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
            return token
        token = input("Please, give me your VK access token: ")
        while True:
            if len(token) < 85:
                print("Bad access token.")
                token = input("Please, give me your VK access token: ")
            else:
                break
        self.ini.add_section('Data')
        self.ini.set('Data', 'Token', token)
        f = open('source/Data.ini', 'w')
        self.ini.write(f)
        f.close()
        return token
