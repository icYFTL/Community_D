import sys

sys.path.append('./source')

from Preview import Preview
from ApiWorker import ApiWorker
from ExitHandler import ExitHandler
from DataChecker import DataChecker
from Config import StaticData
import atexit

### ATEXIT ###

atexit.register(ExitHandler.bye)

### DATA CHECKER ###

DataChecker.checkout()

### PREVIEW ###

Preview.do()

### INPUT ###

user_token = StaticData.vk_user_token
community_token = StaticData.vk_community_token

### API WORK ###

ApiW = ApiWorker(user_token, community_token)

while True:
    ApiW.post()
