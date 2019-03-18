import sys
sys.path.append('./source')

from Preview import Preview
from InputWorker import InputWorker
from ApiWorker import ApiWorker

### PREVIEW ###

Preview.do()

### INPUT ###

input = InputWorker()
token = input.WorkOut()

### API WORK ###

ApiW = ApiWorker(token)
ApiW.post()