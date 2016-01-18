"""Multilog command line scripts."""
import sys

if sys.version_info < (3, 0):
    sys.stdout.write("Multilog requires Python 3 or newer.\n")
    sys.exit(-1)
