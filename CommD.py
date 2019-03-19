import sys

sys.path.append('./source')
import time

from Preview import Preview
from InputWorker import InputWorker
from datetime import datetime
from ApiWorker import ApiWorker
from ExitHandler import ExitHandler
import atexit

atexit.register(ExitHandler.bye)



### PREVIEW ###

Preview.do()

### INPUT ###

input = InputWorker()
token = input.WorkOut()

### API WORK ###
ApiW = ApiWorker(token)

while True:
    ApiW.post()
