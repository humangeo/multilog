"""Tests for the CLI"""

from nose.tools import raises, eq_

import multilog.scripts.cli as cli
from multilog import IS_PYTHON2

if IS_PYTHON2:
    from mock import patch
else:
    from unittest.mock import patch

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

def test_create_parser_empty():
    parser = cli.create_parser()
    args = parser.parse_args([])
    eq_(args.server, cli.DEFAULT_HOST)
    eq_(args.port, cli.DEFAULT_PORT)
    eq_(args.config_path, "logging.ini")

def test_create_parser_params():
    parser = cli.create_parser()
    args = parser.parse_args(["-s", "127.0.0.1", "-p", "1234", "-c", "logging.cfg"])
    eq_(args.server, "127.0.0.1")
    eq_(args.port, 1234)
    eq_(args.config_path, "logging.cfg")

@patch("multilog.scripts.cli.LogReceiver")
@patch("multilog.scripts.cli.setup_logging")
def test_main(setup_logging, log_receiver):
    import sys
    sys.argv = []
    server = log_receiver.return_value
    cli.main()
    setup_logging.assert_called_with("logging.ini")
    log_receiver.assert_called_with(host=cli.DEFAULT_HOST, port=cli.DEFAULT_PORT)
    server.serve_until_stopped.assert_called_once_with()

@raises(SystemExit)
@patch("multilog.scripts.cli.LogReceiver")
@patch("multilog.scripts.cli.setup_logging")
def test_main_interrupt(setup_logging, log_receiver):
    import sys
    sys.argv = []
    server = log_receiver.return_value
    server.serve_until_stopped.side_effect = SystemExit
    cli.main()
