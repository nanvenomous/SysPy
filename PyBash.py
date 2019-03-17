from subprocess import Popen, PIPE
from os import path
import sys
import getopt

def getInputs():
	return sys.argv[1:]

def parseOptions(args, shortOpts, longOpts):
	# checks that the option exists
	try:
		# returns options and remainder (if success)
		return getopt.getopt(
			args,
			shortOpts,
			longOpts
			)
	except getopt.GetoptError as err:
		print('ERROR:', err)
		sys.exit(1) # exit with error

class Directory():
	def __init__(self):
		mainFile = path.abspath(sys.modules['__main__'].__file__)
		self.mainDir = path.dirname(mainFile)
		# print('MainDir: ', self.mainDir)

	def relPath(self, partPath):
		fullPath = ''.join([self.mainDir, '/', partPath])
		return fullPath

class BashAPI():
	def __init__(self, file):
		# get the full executable path of our bash api script
		dir = Directory()
		self.api = dir.relPath(file)

	# runs a function within a bash script
	def cmd(self, function, args=['']):
		# syntax to run a function within a bash script
		command = ''.join(['. ', self.api, ' && ', function, ' '] + args)
		# print(command)
		# create a pipeline to a subprocess
		pipe = Popen(['bash', '-c', command], stdout=PIPE, stdin=PIPE, stderr=PIPE)
		# run command and gather output
		byteOutput, byteError = pipe.communicate()
		output = byteOutput.decode('utf-8')
		error = byteError.decode('utf-8')
		# print output (if there are errors)
		if error == '': return(output)
		else:
			print('[ERROR]')
			print(error)
			sys.exit(1) # exit with error

class Message():
	def __init__(self, content, display=False):
		self.display = display
		self.content = content
	def smartPrint(self):
		if self.display == True: print(self.content)

