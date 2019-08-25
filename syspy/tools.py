import getopt, os, sys
from glob import glob
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

def extend(loc, extenstion):
	return os.path.join(loc, extenstion)

def which_os():
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
		# relevant directories
		self.home = os.path.expanduser('~')
		mainFile = os.path.abspath(sys.modules['__main__'].__file__)
		self.main = os.path.dirname(mainFile)
		self.working = os.getcwd()
		# option from command line
		self.verbose = False
		# operating system type
		self.os = which_os()

	def cd(self, path):
		os.chdir(path)

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

	def command(self, cmd_list):
		cmd = ' '.join(cmd_list)
		if self.verbose: print(cmd)
		os.system(cmd)

	def exists(self, path): # check for path of directory
		if self.verbose: print('Checking the existance of path: ', path)
		return os.path.exists(path)

	def find(self, pattern, path=None):
		if path != None: self.cd(path)
		return glob('**/' + pattern, recursive=True)

	def link(self, src, dest):
		os.symlink(src, dest)

	def ls(self, path):
		if self.verbose: print('Listing files in directory: ', path)
		return os.listdir(path)

	def make_executable(self, file):
		self.command(['chmod +x', file])

	def mkdir(self, path):
		try:
			os.mkdir(path)
			if self.verbose: print('made directory: ', path)
		except:
			if self.verbose: print('failed to make directory: ', path)

	def rm(self, file):
		if self.verbose: print('removing: ', file)
		os.remove(file)

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
	vim = os.environ.get('EDITOR', 'vim') # create editor
	def open_file_with_vim(permission):
		with open(name, permission) as tf:
			call([vim, tf.name])
	try:
		open_file_with_vim('r+') # open file to read
	except:
		open_file_with_vim('w+') # open file to write

# supressing stdout
# https://stackoverflow.com/questions/2828953/silence-the-stdout-of-a-function-in-python-without-trashing-sys-stdout-and-resto