from os import path, environ, read, mkdir, system, remove, symlink, listdir
import sys
import getopt
from subprocess import call
from select import select

def fail(): sys.exit(1)

def succeed(): sys.exit(0)

def getInputs(): return sys.argv[1:]

def error(msg):
	context = '\033[91m {}\033[00m'.format('[ERROR] ')
	print(context + msg)
	fail()

def warn(msg):
	context = '\033[33m {}\033[00m'.format('[WARNING] ')
	print(context + msg)

def validate(msg):
	context = '\033[92m {}\033[00m'.format('[LIT] ')
	print(context + msg)

def os():
	if sys.platform == 'linux' or sys.platform == 'linux2':
		return 'linux'
	elif sys.platform == 'darwin':
		return 'mac'
	elif sys.platform == 'win32':
		return 'windows'
	else:
		return None

class Shell():
	def __init__(self):
		self.home = path.expanduser('~')
		self.verbose = False
		self.os = os()

	def command(self, cmd_list):
		cmd = ' '.join(cmd_list)
		if self.verbose: print(cmd)
		system(cmd)

	def exists(self, pth): # check for path of directory
		if self.verbose: print('Checking the existance of path: ', pth)
		return path.exists(pth)

	def ls(self, pth):
		if self.verbose: print('Listing files in directory: ', pth)
		return listdir(pth)

	def rm(self, file):
		if self.verbose: print('removing: ', file)
		remove(file)

	def from_home(self, partPath):
		return path.join(self.home, partPath)

	def mkdir(self, pth):
		try:
			mkdir(pth)
			if self.verbose: print('made directory: ', pth)
		except:
			if self.verbose: print('failed to make directory: ', pth)

	def make_executable(self, file):
		self.command(['chmod +x', file])

	def link(self, src, dest):
		symlink(src, dest)

	def chrome(self, url):
		if self.os == 'linux':
			self.command([
				'/usr/bin/chromium-browser',
				'--disable-features=NetworkService',
				url,
				'&>/dev/null'
				])
		elif self.os == 'mac':
			error('no mac implementation yet')

def parseOptions(args, shortOpts, longOpts):
	try:
		options, remainder = getopt.getopt(
			args,
			shortOpts,
			longOpts
			)
		command = None
		try:
			command = remainder[0]
			remainder = remainder[1:]
		except:
			remainder = None
		return options, command, remainder
	except getopt.GetoptError as err:
		print(err)
		error('parsing the options failed')

def vim(name):
	vim = environ.get('EDITOR', 'vim') # create editor
	def open_file_with_vim(permission):
		with open(name, permission) as tf:
			call([vim, tf.name])
	try:
		open_file_with_vim('r+') # open file to read
	except:
		open_file_with_vim('w+') # open file to write

class Directory():
	def __init__(self, *args):
		if (len(args) > 1):
			error('too many input arguments')
		if (args):
			self.path = args[0]
		else:
			mainFile = path.abspath(sys.modules['__main__'].__file__)
			self.path = path.dirname(mainFile)

	def to(self, partPath):
		return path.join(self.path, partPath)