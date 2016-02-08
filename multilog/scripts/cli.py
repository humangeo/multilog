"""Command line logging daemon"""
from __future__ import absolute_import, print_function, unicode_literals

import argparse
import logging
import os.path
import sys

from pkg_resources import get_distribution

from multilog.receivers import DEFAULT_HOST, DEFAULT_PORT, LogReceiver

__version__ = get_distribution('multilog').version # pylint: disable=no-member,maybe-no-member

def setup_logging(config_path):
    """Initialize the logger

    :param config_path: The path to the config file

    """
    if not os.path.exists(config_path):
        raise IOError("Configuration file '{0}' not found. Create it, or pass it in with the '-c' switch.".format(
            config_path))
    logging.config.fileConfig(config_path, defaults={"root_handler": "multilogServerHandler"})

def main():
    """Do the thing"""
    args = parse_args()
    setup_logging(args.config_path)
    tcpserver = LogReceiver(host=args.server, port=args.port)
    print("Starting TCP server '{0}:{1}'...".format(args.server, args.port))
    try:
        tcpserver.serve_until_stopped()
    except KeyboardInterrupt:
        print("Interrupt received. Stopping")
        sys.exit(0)

def parse_args():
    """Parse the thing

    :returns: The parsed arguments

    """
    parser = argparse.ArgumentParser(description="A simple logger for multiple Python processes.", prog="multilog", # pylint: disable=no-member
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--server", dest="server", default=DEFAULT_HOST, help="The server hostname")
    parser.add_argument("-p", "--port", dest="port", default=DEFAULT_PORT, type=int, help="The port to listen on.")
    parser.add_argument("-c", "--config", dest="config_path", default="logging.ini",
                        help="The log configuration to load.")
    return parser.parse_args()

if __name__ == "__main__":
    main()
