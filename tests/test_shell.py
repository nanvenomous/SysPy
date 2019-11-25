import pytest
from mock import patch
from mock.mock import Mock

call = Mock()

from syspy import Shell

sh = Shell()

def setup_module(module):
  pass

@patch('syspy.shell.os.rename')
def test_moving_a_file(mock_rename):
  sh.mv('ex.txt', 'example')
  mock_rename.assert_called_with('ex.txt', 'example')


@patch('syspy.shell.Shell.is_dir')
@patch('syspy.shell.Shell.command')
@patch('syspy.shell.open_file_with_vim')
class TestVim:
  def test_editor_cannot_take_2_arguments(self, mock_open_vim, mock_command, mock_is_dir):
    with pytest.raises(TypeError):
      sh.vim(['one', 'two'])
      assert not mock_open_vim.called
      assert not mock_command.called

  def test_editor_opens_file_from_list(self, mock_open_vim, mock_command, mock_is_dir):
    mock_is_dir.return_value = False
    ret = sh.vim(['ex.txt'])
    assert ret == 0
    mock_open_vim.assert_called_with('vim', 'ex.txt', 'r+')
    assert not mock_command.called

  def test_editor_opens_file_from_string(self, mock_open_vim, mock_command, mock_is_dir):
    mock_is_dir.return_value = False
    ret = sh.vim('ex.txt')
    assert ret == 0
    mock_open_vim.assert_called_with('vim', 'ex.txt', 'r+')
    assert not mock_command.called

  @patch('syspy.shell.os.environ.get')
  def test_editor_uses_system_editor(
    self, mock_environment_get, mock_open_vim, mock_command, mock_is_dir
    ):
    mock_is_dir.return_value = False
    ret = sh.vim('ex.txt', SystemEditor=True)
    assert mock_environment_get.called
    assert mock_open_vim.called
    assert ret == 0
    assert not mock_command.called

  def test_editor_empty_call(self, mock_open_vim, mock_command, mock_is_dir):
    ret = sh.vim([])
    assert ret == 0
    mock_command.assert_called_with(['vim'])

def teardown_module(module):
  pass
