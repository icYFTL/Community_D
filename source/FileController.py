import os
from StaticData import StaticData

class FileController (object):
    def RemoveINI():
        os.remove(StaticData.inipath)