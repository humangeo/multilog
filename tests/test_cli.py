"""Tests for the CLI"""

from unittest.mock import patch

from nose.tools import raises
import multilog.scripts.cli as cli

@patch("os.path.exists")
@patch("logging.config.fileConfig")
def test_setup_logging(file_config, path_exists):
    path_exists.return_value = True
    cli.setup_logging("/path/to/config")
    path_exists.assert_called_with("/path/to/config")
    file_config.assert_called_with("/path/to/config", defaults={"root_handler": "multilogServerHandler"})

@raises(IOError)
@patch("os.path.exists")
def test_setup_logging_missing_config(path_exists):
    path_exists.return_value = False
    cli.setup_logging("/path/to/config")


