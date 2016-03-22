"""Tests for the Socket Receiver"""

import logging

from nose.tools import raises, eq_, ok_

from multilog.handlers import LogHandler
from multilog import IS_PYTHON2

if IS_PYTHON2:
    from mock import patch, MagicMock
    SOCKETSERVER = "SocketServer"
else:
    from unittest.mock import patch, MagicMock
    SOCKETSERVER = "socketserver"

def mock_streamreqhandler_init(self, *args, **kwargs):
    _logname = kwargs.pop("_logname")
    self.server = MagicMock()
    self.server.logname = _logname

@raises(TypeError)
def test_unpickle_nonetype():
    LogHandler.unpickle(None)

@raises(EOFError)
def test_unpickle_empty_bytestring():
    LogHandler.unpickle(b"")

def test_unpickle():
    import pickle
    test_str = "TESTING PICKLING"
    pickled = pickle.dumps(test_str)
    ok_(test_str != pickled)
    result = LogHandler.unpickle(pickled)
    eq_(result, test_str)

@patch(SOCKETSERVER + ".StreamRequestHandler.__init__", new=mock_streamreqhandler_init)
@patch("logging.getLogger")
def test_handle_log_record_logger(get_logger):
    logger = get_logger.return_value
    handler = LogHandler(_logname="multilog")
    handler.handle_log_record(None)
    get_logger.assert_called_with("multilog")
    logger.handle.assert_called_with(None)

@patch(SOCKETSERVER + ".StreamRequestHandler.__init__", new=mock_streamreqhandler_init)
def test_handle_log_record_valid():
    record_args = ["multilog", logging.DEBUG, "/tmp/test", 13, "Message", None, None, "test_handle_log_record"]
    record = logging.LogRecord(*record_args)
    handler = LogHandler(_logname="multilog")
    handler.handle_log_record(record)

@raises(AttributeError)
@patch(SOCKETSERVER + ".StreamRequestHandler.__init__", new=mock_streamreqhandler_init)
def test_handle_log_record_invalid():
    handler = LogHandler(_logname="multilog")
    handler.handle_log_record(None)
