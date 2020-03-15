import pytest
from mock import patch
from mock.mock import Mock

call = Mock()

# from syspy.implementations.source_executables import remove_unwanted
from ..source_executables import remove_unwanted

with_unwanted_file = ['file1', '__init__.py', 'file2']
sources_only = ['file1', 'file2']

class TestRemoveUnwantedFiles:
	def test_removes_init_py(self):
		assert sources_only == remove_unwanted(with_unwanted_file)

	def test_removes_nothing(self):
		assert sources_only == remove_unwanted(sources_only)
