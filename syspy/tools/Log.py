import sys, traceback

class _Error(Exception):
	def __init__(self, message):
		self.type = '\033[91m {}\033[00m'.format('[ERROR] ')
		self.message = message

class Log:
  def __init__(self, layers_to_hide=-3):
    self.layers_to_hide = layers_to_hide

  @staticmethod
  def failure(): sys.exit(1)

  @staticmethod
  def success(): sys.exit(0)

  def _print_stack(self):
    def extract_stack():
      return traceback.format_stack()[:self.layers_to_hide]
    for trace in extract_stack(): print(trace)

  def error(self, message, BaseError=None, stacktrace=True, Fail=True):
    if BaseError: raise BaseError
    try: raise _Error(message)
    except _Error as e:
      if stacktrace: self._print_stack()
      print(e.type, e.message)
      if Fail: self.failure()

  def warn(self, message, stacktrace=False):
    if stacktrace: self._print_stack()
    type = '\033[33m {}\033[00m'.format('[WARNING] ')
    print(type + message)

  @staticmethod
  def validate(message):
    type = '\033[92m {}\033[00m'.format('[LIT] ')
    print(type + message)
