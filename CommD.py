from source.DataChecker import DataChecker

### DATA CHECKER ###

DataChecker.checkout()

from source.Preview import Preview
from source.ApiWorker import ApiWorker
from source.ExitHandler import ExitHandler
from Config import Config

import atexit

### ATEXIT ###

atexit.register(ExitHandler.bye)

### PREVIEW ###

Preview.do()

### API WORK ###

ApiW = ApiWorker(Config.vk_user_token, Config.vk_community_token)

while True:
    ApiW.post()
