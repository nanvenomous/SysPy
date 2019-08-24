from .tools import Shell, Directory, error, validate, warn
sh = Shell()

def source_executables():
	here = Directory()
	binDir = Directory(here.to('bin'))
	srcDir = Directory(here.to('src'))
	sh = Shell()

	sh.mkdir(binDir.path)

	if not sh.exists(srcDir.path): # no source, can't run
		warn('no source to convert to executables at: ' + here.path)
		return
	sources = set(sh.ls(srcDir.path))
	executables = set(sh.ls(binDir.path))
	unlinked_sources = list(sources - executables)
	executables_to_clean = list(executables - sources)

	# remove unecessary executables
	for exe in executables_to_clean:
		sh.rm(binDir.to(exe))

	# helper
	def get_correct_source(pkg):
		pkgDir = Directory(srcDir.to(pkg))
		srcFile = pkg + '.sh'
		if (srcFile in sh.ls(pkgDir.path)):
			return pkgDir.to(srcFile)
		srcFile = pkg + '.py'
		if (srcFile in sh.ls(pkgDir.path)):
			return pkgDir.to(srcFile)
		error('could not find correct file type in: \n\t' + pkgDir.path)

	# make every source file executable
	for pkg in sources:
		source = get_correct_source(pkg)
		sh.make_executable(source)

	# link all sources to executables
	for pkg in unlinked_sources:
		source = get_correct_source(pkg)
		destination = binDir.to(pkg)
		sh.link(source, destination)
		print(source, ' <--> ', destination)

	validate('source --> executables at: ' + here.path)