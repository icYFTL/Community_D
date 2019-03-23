import sys

sys.path.append('./source')

from Preview import Preview
from InputWorker import InputWorker
from ApiWorker import ApiWorker
from ExitHandler import ExitHandler
from DataChecker import DataChecker
import atexit

### ATEXIT ###

atexit.register(ExitHandler.bye)

### DATA CHECKER ###

DataChecker.checkout()

### PREVIEW ###

Preview.do()

### INPUT ###

input = InputWorker()
token, token_c = map(str, input.WorkOut())

### API WORK ###

ApiW = ApiWorker(token, token_c)

while True:
    ApiW.post()
