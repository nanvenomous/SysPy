import sys
from syspy import BashAPI, getInputs, editor

api = BashAPI('exampleApi.sh')

# output = api.cmd('copyFile', getInputs())
# output = api.cmd('falseCommand')

editor('testFolder/file.txt')

# print(output)

print('Made it to end')