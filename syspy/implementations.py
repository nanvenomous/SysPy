from .tools import Shell, error, validate, warn, extend

def source_executables():
	sh = Shell()
	binDir = extend(sh.main, 'bin')
	srcDir = extend(sh.main, 'src')

	sh.mkdir(binDir)

	if not sh.exists(srcDir): # no source, can't run
		warn('no source to convert to executables at: ' + sh.main)
		return
	sources = sh.ls(srcDir)
	executables = sh.ls(binDir)
	unlinked_sources = list(set(sources) - set(executables))

	# get all full executable paths
	exe_paths = [extend(binDir, exe) for exe in executables]
	# remove the exe if the source does not exist
	for exe_path in exe_paths:
		src = sh.respond(['readlink', '-f', exe_path])
		if not sh.exists(src): sh.rm(exe_path)

	# helper
	def get_correct_source(pkg):
		pkgDir = extend(srcDir, pkg)
		srcFile = pkg + '.sh'
		if (srcFile in sh.ls(pkgDir)):
			return extend(pkgDir, srcFile)
		srcFile = pkg + '.py'
		if (srcFile in sh.ls(pkgDir)):
			return extend(pkgDir, srcFile)
		error('could not find correct file type in: \n\t' + pkgDir)

	# make every source file executable
	for pkg in sources:
		source = get_correct_source(pkg)
		sh.make_executable(source)

	# link all sources to executables
	for pkg in unlinked_sources:
		source = get_correct_source(pkg)
		destination = extend(binDir, pkg)
		sh.link(source, destination)
		print(source, ' <--> ', destination)

	validate('source --> executables at: ' + sh.main)