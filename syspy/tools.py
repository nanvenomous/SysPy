import getopt, os, sys, traceback, shutil
from glob import glob
from subprocess import call, check_output
from select import select

def fail(): sys.exit(1)

def succeed(): sys.exit(0)

def tabPrint(*args, **kwargs): print('\t', *args, **kwargs)

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

def _which_os():
  if sys.platform == 'linux' or sys.platform == 'linux2':
    return 'linux'
  elif sys.platform == 'darwin':
    return 'mac'
  elif sys.platform == 'win32':
    return 'windows'
  else:
    return None

class _Suppressor():
  def __enter__(self):
    self.stdout = sys.stdout
    sys.stdout = self
  def __exit__(self, type, value, traceback):
    sys.stdout = self.stdout
    if type is not None: # Do normal exception handling
      pass
  def write(self, x): pass
suppressor = _Suppressor() # example usage: "with suppressor: my_function()"

class _Find():
  def __init__(self, shell):
    self.sh = shell

  def directories_with(self, pattern, path=None):
    # TODO: increase efficiency, possibly using walk
    all_file_instances = self.recurse(pattern, path=path)
    all_dirs = [self.sh.dirname(p) for p in all_file_instances]
    dirs_without_repeats = list(set(all_dirs))
    return dirs_without_repeats

  def here(self, pattern, path=None):
    if path != None: self.sh.cd(path)
    if self.sh.verbose:
      print('Searching one level in directory: ', path if path else self.sh.working, \
         'for pattern: ', pattern)
    return glob(pattern, recursive=False)

  def recurse(self, pattern, path=None):
    if path != None: self.sh.cd(path)
    if self.sh.verbose:
      print('Searching recursively in directory: ', path if path else self.sh.working, \
         'for pattern: ', pattern)
    return glob('**/' + pattern, recursive=True)


class Shell():
  def __init__(self):
    # relevant directories
    self.home = os.path.expanduser('~')
    self.working = os.getcwd()
    self.main = None
    try:
      exeFile = os.path.abspath(sys.modules['__main__'].__file__)
      srcFile = os.path.realpath(exeFile) # resolve symlinks
      self.main = os.path.dirname(srcFile)
    except: warn('no main file path, interactive interpreter')
    self.find = _Find(self)
    # option from command line
    self.verbose = False
    # operating system type
    self.os = _which_os()

  def respond(self, cmd_list, strip=False):
    if self.verbose: print(' '.join(cmd_list))
    byte_output = check_output(cmd_list)
    string_output = byte_output.decode('utf-8')
    if strip: return string_output.strip()
    return string_output

  def basename(self, path):
    basename = os.path.basename(path)
    if self.verbose: print('Basename of ', path, ' is ', basename)
    return basename

  def cd(self, path):
    if self.verbose: print('Changing directory to: ', path)
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
      self.command(['open -a', '"Google Chrome"', url])

  def command(self, cmd_list):
    cmd = ' '.join(cmd_list)
    if self.verbose: print(cmd)
    os.system(cmd)

  def cp(self, from_file, to_file):
    if self.verbose: print('Copying from ', from_file, ' to ', to_file)
    if self.exists(to_file): self.delete(to_file)
    shutil.copytree(from_file, to_file)

  def delete(self, path):
    if self.verbose: print('Recursively removing: ', path)
    shutil.rmtree(path)

  def dirname(self, path):
    dirname = os.path.dirname(path)
    if self.verbose: print('Dirname of ', path, ' is ', dirname)
    return dirname

  def exists(self, path): # check for path of directory
    if self.verbose: print('Checking the existance of path: ', path)
    return os.path.exists(path.strip())

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
    except Exception:
      print(Exception)
      error('failed to make directory: ' + path)

  def mv(self, from_path, to_path):
    try:
      os.rename(from_path, to_path)
      if self.verbose: print('renaming directory: ', from_path, ' to ', to_path)
    except Exception:
      print(Exception)
      error('failed to rename directory: ' + from_path + ' to ' + to_path)

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