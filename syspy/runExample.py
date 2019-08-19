import sys
from tools import BashAPI, getInputs, vim, Directory, Shell, warn

api = BashAPI('example/api.sh')
sh = Shell()

def get_home_directory():
	print('#### get home directory')
	print(sh.home)
	print(sh.from_home('fromHome'))
	print()

def remove_file():
	print('#### Remove file')
	sh.rm('example/testFolder/file.txt')
	print()

def create_directory_if_nonexistent():
	print('#### create directory if it doesnt exist')
	here = Directory()
	sh.mkdir(here.to('example/testFolder'))
	print()

def open_file_in_editor():
	print('#### Check Editor Operation')
	vim('example/testFolder/file.txt')
	print()

def print_example_warning():
	print('#### Print a warning message')
	warn('you have been warned')
	print()

def make_symbolic_link():
	print('#### Create a symlink')
	sh.link('example/testFolder/file.txt', 'ex')
	print()

def make_file_executable():
	print('#### Make file executable')
	sh.make_executable('example/testFolder/file.txt')
	print()

# def test_gather_inputs():
# 	print('#### Throw error if incorrect number of inputs')
# 	inps = getInputs([1, 2])
# 	print('you gathered these inputs: ', inps)
# 	print()

get_home_directory()
# remove_file()
create_directory_if_nonexistent()
# open_file_in_editor()
print_example_warning()
# make_symbolic_link()
# make_file_executable()