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
token, token_c = map(str, input.WorkOut())

### API WORK ###
ApiW = ApiWorker(token, token_c)

while True:
    ApiW.post()
