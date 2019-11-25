import getopt
import sys

def getInputs(): return sys.argv[1:]

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