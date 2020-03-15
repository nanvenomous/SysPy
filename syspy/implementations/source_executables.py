from ..shell import extend

def remove_unwanted(source_files):
  toRemove = ['__init__.py']
  return [sc for sc in source_files if sc not in toRemove]

def source_executables(sh, extensions):
  binDir = extend(sh.main, 'bin')
  srcDir = extend(sh.main, 'src')

  sh.mkdir(binDir)

  if not sh.exists(srcDir): # no source, can't run
    sh.log.warn('no source to convert to executables at: ' + sh.main)
    return
  sources = remove_unwanted(sh.ls(srcDir))
  executables = sh.ls(binDir)
  unlinked_sources = list(set(sources) - set(executables))

  # get all full executable paths
  exe_paths = [extend(binDir, exe) for exe in executables]
  # remove the exe if the source does not exist
  for exe_path in exe_paths:
    if not sh.readlink(exe_path): sh.rm(exe_path)

  def _get_correct_source(pkg):
    pkgDir = extend(srcDir, pkg)
    for extension in extensions:
      srcFile = pkg + extension
      if (srcFile in sh.ls(pkgDir)):
        return extend(pkgDir, srcFile)
    sh.log.error('could not find correct file type in: \n\t' + pkgDir)

  # make every source file executable
  for pkg in sources:
    source = _get_correct_source(pkg)
    sh.make_executable(source)

  # link all sources to executables
  for pkg in unlinked_sources:
    source = _get_correct_source(pkg)
    destination = extend(binDir, pkg)
    sh.link(source, destination)
    print(source, ' <--> ', destination)

  sh.log.validate('source --> executables at: ' + sh.main)