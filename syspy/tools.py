from subprocess import Popen, PIPE, call

from select import select
from os import path, environ, read, mkdir, system, remove, symlink
import sys
import getopt

def fail(): sys.exit(1)

def succeed(): sys.exit(0)

def getInputs(): return sys.argv[1:]

def error(msg):
	context = "\033[91m {}\033[00m".format('[ERROR] ')
	print(context + msg)
	fail()

def warn(msg):
	context = "\033[33m {}\033[00m".format('[WARNING] ')
	print(context + msg)

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

class Shell():
	def __init__(self):
		self.home = path.expanduser('~')
		self.verbose = False

	def command(self, cmd_list):
		cmd = ' '.join(cmd_list)
		if self.verbose: print(cmd)
		system(cmd)

	def rm(self, file):
		if self.verbose: print('removing: ', file)
		remove(file)

	def from_home(self, partPath):
		return path.join(self.home, partPath)

	def mkdir(self, path):
		try:
			mkdir(path)
			if self.verbose: print('made directory: ', path)
		except:
			if self.verbose: print('failed to make directory: ', path)

	def make_executable(self, file):
		system('chmod +x ' + file)

	def link(self, src, dest):
		symlink(src, dest)

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


class BashAPI():
	# input is file (path to shell script)
	def __init__(self, file):
		# get the full executable path of our bash api script
		dir = Directory()
		self.api = dir.to(file)

	# runs a function within a bash script
	def cmd(self, function, args=[''], realTime=False):
		# syntax to run a function within a bash script
		command = ' '.join(['.', self.api, '&&', function] + args)
		# print(command)
		# Popen explanation: https://pypi.org/project/bash/

		# https://stackoverflow.com/questions/31926470/run-command-and-get-its-stdout-stderr-separately-in-near-real-time-like-in-a-te/31953436#31953436
		with Popen(['bash', '-c', command], stdout=PIPE, stderr=PIPE) as p:
			if (realTime):
				readable = {
					p.stdout.fileno(): sys.stdout.buffer, # log separately
					p.stderr.fileno(): sys.stderr.buffer,
				}
				# print(readable) # 3 is a stdout and 5 is a stderr
				while readable:
					for fd in select(readable, [], [])[0]:
							data = read(fd, 1024) # read available
							# print('data: ', data)
							if not data: # handle end of file
								del readable[fd]
							elif (fd == 5): # handle the case of an error
								print('[BASH ERROR]')
								readable[fd].write(data)
								readable[fd].flush()
								fail()
							else: 
								readable[fd].write(data)
								readable[fd].flush()
			else: # not real time output, simple pipe
				# create a pipeline to a subprocess
				# pipe = Popen(['bash', '-c', command], stdout=PIPE, stderr=PIPE)
				# run command and gather output
				byteOutput, byteError = p.communicate()
				output = byteOutput.decode('utf-8')
				error = byteError.decode('utf-8')
				# print output (if there are errors)
				if error == '': return(output)
				else:
					print('[BASH ERROR]')
					print(error)
					fail()

class Message():
	def __init__(self, content, display=False):
		self.display = display
		self.content = content
	def smartPrint(self):
		if self.display == True: print(self.content)
