import pytest
from mock import patch
from mock.mock import Mock

call = Mock()

from syspy.tools import Shell

sh = Shell()

def setup_module(module):
  pass

@patch('syspy.tools.os.rename')
def test_moving_a_file(mock_rename):
  sh.mv('ex.txt', 'example')
  mock_rename.assert_called_with('ex.txt', 'example')


@patch('syspy.tools.xsh.vi')
class TestVi:
  def test_editor_cannot_take_2_arguments(self, mock_vi):
    with pytest.raises(TypeError):
      sh.vi(['one', 'two'])
      assert not mock_vi.called

  def test_editor_opens_file_from_list(self, mock_vi):
    ret = sh.vi(['ex.txt'])
    assert ret == 0
    mock_vi.assert_called_with('ex.txt')

  def test_editor_opens_file_from_string(self, mock_vi):
    ret = sh.vi('ex.txt')
    assert ret == 0
    mock_vi.assert_called_with('ex.txt')

  def test_editor_empty_call(self, mock_vi):
    ret = sh.vi([])
    assert ret == 0
    mock_vi.assert_called_with(None)

def teardown_module(module):
  pass
