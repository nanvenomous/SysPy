import unittest
import os, sys, shutil, traceback

from .. import source_executables
from .. import Shell, suppressor
sh = Shell()

def quietly_source_executables():
  with suppressor: source_executables()

#__________________________________________________
# Directories
for_testing = os.path.join(sh.main, 'for_testing')
hidden_src = os.path.join(for_testing, 'src')
srcDir = os.path.join(sh.main, 'src')
binDir = os.path.join(sh.main, 'bin')
#__________________________________________________

class Test_Source_Executables(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    sh.cp(hidden_src, srcDir)
    quietly_source_executables()

  def test_src_directory_exists(self):
    self.assertTrue(os.path.exists(srcDir.strip()))

  def test_bin_directory_exists(self):
    self.assertTrue(os.path.exists(binDir.strip()))

  def test_executables_work(self):
    sh_out = sh.respond(['./bin/sh_pkg'], strip=True)
    self.assertEqual(sh_out, 'i am a shell script')
    py_out = sh.respond(['./bin/py_pkg'], strip=True)
    self.assertEqual(py_out, 'i am a python package')

  @classmethod
  def tearDownClass(cls):
    sh.delete(srcDir)
    sh.delete(binDir)

if __name__ == '__main__': unittest.main()
