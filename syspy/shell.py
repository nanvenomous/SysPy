import getopt, os, sys, traceback, shutil
from glob import glob
from subprocess import call, check_output
from select import select

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import Log

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
    # option from command line
    self.verbose = False
    self.log = Log()
    # relevant directories
    self.home = os.path.expanduser('~')
    self.working = os.getcwd()
    self.main = None
    try:
      exeFile = os.path.abspath(sys.modules['__main__'].__file__)
      srcFile = os.path.realpath(exeFile) # resolve symlinks
      self.main = os.path.dirname(srcFile)
    except: self.log.warn('no main file path, interactive interpreter')
    self.find = _Find(self)
    # operating system type
    self.os = _which_os()

  def respond(self, cmd_str_or_lst, shell=False, strip=False):
    cmd = ' '.join(cmd_str_or_lst) if (type(cmd_str_or_lst) == type([])) else cmd_str_or_lst
    if self.verbose: print(cmd)
    byte_output = check_output(cmd, shell=shell)
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
        'google-chrome-stable',
        '--disable-features=NetworkService',
        url,
        '&>/dev/null'
        ])
    elif self.os == 'mac':
      self.command(['open -a', r'Google\ Chrome', url])

  def command(self, cmd_list):
    cmd = ' '.join(cmd_list)
    if self.verbose: print(cmd)
    status = os.system(cmd)
    return status

  def cp(self, from_file, to_file):
    if self.verbose: print('Copying from ', from_file, ' to ', to_file)
    if self.exists(to_file): self.delete(to_file)
    if os.path.isdir(from_file): shutil.copytree(from_file, to_file)
    else: shutil.copyfile(from_file, to_file)

  def rm(self, path):
    if self.verbose: print('Recursively removing: ', path)
    if os.path.isdir(path): shutil.rmtree(path)
    else: os.remove(path)

  def dirname(self, path):
    dirname = os.path.dirname(path)
    if self.verbose: print('Dirname of ', path, ' is ', dirname)
    return dirname

  def exists(self, path): # check for path of directory
    if self.verbose: print('Checking the existance of path: ', path)
    return os.path.exists(path.strip())

  def is_dir(self, path): # check for path of directory
    if self.verbose: print('Checking if is dir, path: ', path)
    return os.path.isdir(path.strip())

  def kill(self, command_name):
    if self.os == 'mac':
      pid = self.pid(command_name)
    else: self.log.error('Shell.kill is not yet implemented for this operating system')
    status = self.command(['kill', '-9', pid])
    if status == 0: self.log.validate('killed ' + command_name + ' running with id ' + pid)

  def link(self, src, dest):
    os.symlink(src, dest)

  def readlink(self, link_path):
    source = os.readlink(link_path)
    if self.exists(source):
      if self.verbose: self.log.validate('the symlink at, ' + link_path + ', resolved')
      return source
    if self.verbose: print('link, ' + link_path + ', exists, but did not resolve')
    return False

  def ls(self, path):
    if self.verbose: print('Listing files in directory: ', path)
    return os.listdir(path)

  def make_executable(self, file):
    self.command(['chmod +x', file])

  def mkdir(self, path):
    if self.is_dir(path):
      self.log.validate('directory, ' + path + ', already exists')
      return
    os.mkdir(path)
    if self.verbose: print('made directory: ', path)

  def mv(self, from_path, to_path):
    try:
      os.rename(from_path, to_path)
      if self.verbose: print('renaming directory: ', from_path, ' to ', to_path)
    except Exception as e:
      raise e

  def pid(self, command_name):
    try: 
      if self.os == 'mac':
        pid = self.respond(['pgrep', command_name], shell=True, strip=True)
      else: self.log.error('Shell.pid is not yet implemented for this operating system')
    except: self.log.error('failed to get a process id for the command name: ' + command_name)
    return pid

  def vim(self, name, SystemEditor=False):
    if SystemEditor: vim = os.environ.get('EDITOR', 'vim') # create editor
    else: vim = 'vim'
    if type(name) == type([]):
      if len(name) > 1: raise TypeError('too many input arguments')
      if len(name) == 0:
        self.command([vim])
        return 0
      else: name = name[0]
    if self.is_dir(name):
      self.command([vim, name])
      return 0
    try:
      open_file_with_vim(vim, name, 'r+') # open file to read
    except:
      open_file_with_vim(vim, name, 'w+') # open file to write
    return 0

def open_file_with_vim(vim, name, permission):
  with open(name, permission) as tf:
    call([vim, tf.name])

# TODO: return aliasable method names for automation
# def get_method_names():
#   [method_name for method_name in dir(Shell) if callable(getattr(Shell, method_name))]