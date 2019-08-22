import sys
from tools import BashAPI, getInputs, vim, Directory, Shell, validate

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

def print_example_validation():
	print('#### Print a validation message')
	validate('things are looking good for you')
	print()

def make_symbolic_link():
	print('#### Create a symlink')
	sh.link('example/testFolder/file.txt', 'ex')
	print()

def make_file_executable():
	print('#### Make file executable')
	sh.make_executable('example/testFolder/file.txt')
	print()

def open_file_in_browser():
	print('#### Open file in browser')
	# sh.chrome('example/ex.md')
	sh.chrome('dogs.com')
	print()

get_home_directory()
# remove_file()
create_directory_if_nonexistent()
# open_file_in_editor()
print_example_validation()
# make_symbolic_link()
# make_file_executable()
open_file_in_browser()