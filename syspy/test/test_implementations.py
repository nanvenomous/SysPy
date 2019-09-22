import unittest
import os, sys, shutil

def copy_and_overwrite(from_path, to_path):
	if os.path.exists(to_path): shutil.rmtree(to_path)
	shutil.copytree(from_path, to_path)


main = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))

#__________________________________________________
# Directories
for_testing = os.path.join(main, 'for_testing')
hidden_src = os.path.join(for_testing, 'src')
srcDir = os.path.join(main, 'src')
binDir = os.path.join(main, 'bin')

class Test_Source_Executables(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		from .. import source_executables
		copy_and_overwrite(hidden_src, srcDir)
		source_executables()

	def test_bin_directory_exists(self):
		self.assertTrue(os.path.exists(binDir.strip()))

	def test_src_directory_exists(self):
		self.assertTrue(os.path.exists(srcDir.strip()))

	@classmethod
	def tearDownClass(cls):
		shutil.rmtree(srcDir)
		shutil.rmtree(binDir)

if __name__ == '__main__': unittest.main()
