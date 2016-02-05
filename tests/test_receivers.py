"""Tests for the Socket Receiver"""

from unittest.mock import patch

from nose.tools import raises, eq_, ok_

import multilog.receivers as receivers
from multilog.handlers import LogHandler

@patch("socketserver.ThreadingTCPServer.__init__")
def test_receiver_init_defaults(tcp_init_mock):
    receiver = receivers.LogReceiver()
    tcp_init_mock.assert_called_with(receiver, (receivers.DEFAULT_HOST, receivers.DEFAULT_PORT), LogHandler)
    eq_(receiver.abort, 0)
    eq_(receiver.timeout, 1)
    eq_(receiver.logname, None)

@patch("socketserver.ThreadingTCPServer.__init__")
def test_receiver_init_params(tcp_init_mock):
    receiver = receivers.LogReceiver(host="HOST", port=1313, handler="HANDLER")
    tcp_init_mock.assert_called_with(receiver, ("HOST", 1313), "HANDLER")
    eq_(receiver.abort, 0)
    eq_(receiver.timeout, 1)
    eq_(receiver.logname, None)

@patch("select.select")
@patch("multilog.receivers.LogReceiver.handle_request")
def test_serve_until_stopped(handle_request, select_mock):
    receiver = receivers.LogReceiver()
    def abort_select(*args):
        receiver.abort = 1
        return ([True], None, None)
    select_mock.side_effect = abort_select
    receiver.serve_until_stopped()
    ok_(select_mock.called)
    handle_request.assert_called_with()
    eq_(receiver.abort, 1)

