import sys
from tools import BashAPI, getInputs, vim, Directory

api = BashAPI('example/api.sh')

print('#### get home directory')
dir = Directory()
print(dir.here)
print(dir.fromHere('fromHere'))
print(dir.home)
print(dir.fromHome('fromHOME'))
print()

print('#### create directory if it doesnt exist')
dir.make(dir.fromHere('example/testFolder'))
print()

print('#### Check Editor Operation')
vim('example/testFolder/file.txt')
print()


# print('#### Copy Filename')
# output = api.cmd('copyFile', args=getInputs())
# print(output)
# print()

print('#### Test Delayed Output with Error')
api.cmd('delayedOutput', realTime=True)
