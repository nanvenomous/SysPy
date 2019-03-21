import sys
from tools import BashAPI, getInputs, editor

api = BashAPI('example/api.sh')

# editor('example/testFolder/file.txt')

# output = api.cmd('copyFile', getInputs())
# output = api.cmd('falseCommand')
output = api.cmd('delayedOutput')

# print(output)