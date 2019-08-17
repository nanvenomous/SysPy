import sys
from tools import BashAPI, getInputs, vim, Directory, Shell, warn

api = BashAPI('example/api.sh')
sh = Shell()

print('#### get home directory')
here = Directory()
print(sh.home)
print(sh.from_home('fromHome'))
print()

# print('#### Remove file')
# sh.rm('example/testFolder/file.txt')
# print()

print('#### create directory if it doesnt exist')
sh.mkdir(here.to('example/testFolder'))
print()

print('#### Check Editor Operation')
vim('example/testFolder/file.txt')
print()

print('#### Print a warning message')
warn('you have been warned')
print()

# print('#### Create a symlink')
# sh.link('example/testFolder/file.txt', 'ex')
# print()

# print('#### Make file executable')
# sh.make_executable('example/testFolder/file.txt')
# print()

# print('#### Copy Filename')
# output = api.cmd('copyFile', args=getInputs())
# print(output)
# print()

# print('#### Test Delayed Output with Error')
# api.cmd('delayedOutput', realTime=True)
# print()