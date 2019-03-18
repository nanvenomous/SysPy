import sys
from .syspy.tools import BashAPI, getInputs, editor

api = BashAPI('example/api.sh')

# output = api.cmd('copyFile', getInputs())
# output = api.cmd('falseCommand')

editor('example/testFolder/file.txt')

# print(output)

print('Made it to end')