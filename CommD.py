import sys

sys.path.append('./source')

from DataChecker import DataChecker

### DATA CHECKER ###

DataChecker.checkout()

from Preview import Preview
from ApiWorker import ApiWorker
from ExitHandler import ExitHandler
from Config import StaticData

import atexit

### ATEXIT ###

atexit.register(ExitHandler.bye)

### PREVIEW ###

Preview.do()

### API WORK ###

ApiW = ApiWorker(StaticData.vk_user_token, StaticData.vk_community_token)

while True:
    ApiW.post()
