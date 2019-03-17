import sys
from PyBash import BashAPI, getInputs

api = BashAPI('exampleApi.sh')

output = api.cmd('copyFile', getInputs())
print(output)