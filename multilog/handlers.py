"""Logger for multilogging"""

import logging
import logging.config
import logging.handlers
import pickle
import socketserver
import struct

class LogHandler(socketserver.StreamRequestHandler):
    """Handle incoming logs"""

    def handle(self):
        """Deal with the incoming log data"""
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            struct_len = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(struct_len)
            while len(chunk) < struct_len:
                chunk = chunk + self.connection.recv(struct_len - len(chunk))
            obj = self.unpickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handle_log_record(record)

    @staticmethod
    def unpickle(data):
        """Unpack the pickled data

        :param data: The data string to load in
        :returns: The equivalent Python object

        """
        return pickle.loads(data)

    def handle_log_record(self, record):
        """Process incoming log record

        :param record: The record to write

        """
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logging.getLogger(name).handle(record)
