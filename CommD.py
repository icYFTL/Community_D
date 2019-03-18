import sys

sys.path.append('./source')
import time

from Preview import Preview
from InputWorker import InputWorker
from datetime import datetime
from ApiWorker import ApiWorker

### PREVIEW ###

Preview.do()

### INPUT ###

input = InputWorker()
token = input.WorkOut()

### API WORK ###
ApiW = ApiWorker(token)
Errors = 0

night = [22, 23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

while True:
    if ApiW.post() is False:
        Errors += 1

    if Errors > 0:
        Errors = 0
        continue

    per = 7200
    ctime = datetime.now().time().strftime('%H')

    if int(ctime) in night:
        per = 14400
    else:
        per = 7200

    time.sleep(per)
