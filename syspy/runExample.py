import sys
from tools import BashAPI, getInputs, editor

api = BashAPI('example/api.sh')

print('#### Check Editor Operation')
editor('example/testFolder/file.txt')
print()


print('#### Copy Filename')
output = api.cmd('copyFile', args=getInputs())
print(output)
print()

print('#### Test Delayed Output with Error')
api.cmd('delayedOutput', realTime=True)