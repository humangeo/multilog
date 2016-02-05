"""Accept incoming log message."""

import logging.handlers
import select

from multilog import IS_PYTHON2

if IS_PYTHON2:
    import SocketServer as socketserver
else:
    import socketserver

from .handlers import LogHandler

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = logging.handlers.DEFAULT_TCP_LOGGING_PORT

class LogReceiver(socketserver.ThreadingTCPServer):
    """Simple TCP socket-based logging receiver."""

    allow_reuse_address = True

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, handler=LogHandler):
        """Initialize the log receiver

        :param host: The hostname to bind to
        :param port: The port to listen on
        :param handler: The handler to send received messages to

        """
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        """Run the server foevah"""
        abort = 0
        while not abort:
            read_items, _, _ = select.select([self.socket.fileno()], [], [], self.timeout)
            if read_items:
                self.handle_request()
            abort = self.abort
