import sys
from tools import BashAPI, getInputs, editor, Directory

api = BashAPI('example/api.sh')

print('#### get home directory')
dir = Directory()
print(dir.mainDir)
print(dir.relPath('fromHere'))
print(dir.homePath)
print(dir.usrPath('fromHOME'))

print('#### Check Editor Operation')
editor('example/testFolder/file.txt')
print()


print('#### Copy Filename')
output = api.cmd('copyFile', args=getInputs())
print(output)
print()

print('#### Test Delayed Output with Error')
api.cmd('delayedOutput', realTime=True)
