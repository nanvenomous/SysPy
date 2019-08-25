from tools import getInputs, vim, Shell, validate, extend

sh = Shell()

def get_home_directory():
  print('#### get home directory')
  print(sh.home)
  print(extend(sh.home, 'fromHome'))
  print()

def remove_file():
  print('#### Remove file')
  sh.rm('example/testFolder/file.txt')
  print()

def create_directory_if_nonexistent():
  print('#### create directory if it doesnt exist')
  sh.mkdir(extend(sh.main, 'example/testFolder'))
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

def list_files_in_directory():
  print('#### List all files in a directory')
  dir_files = sh.ls(sh.main)
  print(dir_files)
  print()

def open_file_in_browser():
  print('#### Open file in browser')
  # sh.chrome('example/ex.md')
  sh.chrome('dogs.com')
  print()

def find_pattern_in_directory():
  print('#### find_pattern_in_directory')
  print(sh.find('*.py'))
  print()

get_home_directory()
# remove_file()
create_directory_if_nonexistent()
# open_file_in_editor()
print_example_validation()
# make_symbolic_link()
# make_file_executable()
list_files_in_directory()
# open_file_in_browser()
find_pattern_in_directory()
