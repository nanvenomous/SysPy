import sys
from PyBash.PyBash import BashAPI, getInputs

api = BashAPI('exampleApi.sh')

# output = api.cmd('copyFile', getInputs())
output = api.cmd('falseCommand')


print(output)

print('Made it to end')