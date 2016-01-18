Multilog
======

.. image:: https://travis-ci.org/humangeo/multilog.svg
   :target: https://travis-ci.org/humangeo/multilog

.. image:: https://coveralls.io/repos/humangeo/multilog/badge.png
   :target: https://coveralls.io/r/humangeo/multilog

A simple, multiprocess-safe logger for Python

.. image:: https://farm4.staticflickr.com/3951/15672691531_3037819613_o_d.png

Why
---

Python's built-in loggers are pretty handy - they're easily customized and come with useful functionality out
of the box, including things like file rotation. These file handlers are thread-safe, but not process-safe, so, if
you're running a webserver in a pre-forking environment, for example, you run the risk of your workers trampling
over each other in writing to a log file.

To avoid this, it is recommended that one uses a socket-based logger (`a code sample is helpfully provided in the
Logging Cookbook <https://docs.python.org/3.4/howto/logging-cookbook.html>`_). However, it is just a code snippet.
Multilog is a dependency-free implementation of the sample socket loggeri with some niceties, like fileConfig
support, and parameterization.

How
-------------------------

Once installed, the Multilog daemon can be invoked via:

.. code-block:: console

    mutlilog

Usage:

.. code-block:: console

    usage: multilog [-h] [-s SERVER] [-p PORT] [-c CONFIG_PATH]

    A simple logger for multiple Python processes.

    optional arguments:
      -h, --help                    show this help message and exit
      -s SERVER, --server SERVER
                                    The server hostname (default: localhost)
      -p PORT, --port PORT          The port to listen on. (default: 9020)
      -c CONFIG_PATH, --config CONFIG_PATH
                                    The log configuration to load. (default: logging.ini)

By default, it will look for a ``logging.ini`` file in the current directory. If one isn't found, Multilog will
yell at you. A sample configuration file for the server:

.. code-block:: ini

    [loggers]
    keys=root

    [handlers]
    keys=multilogServerHandler

    [formatters]
    keys=simpleFormatter

    [logger_root]
    level=NOTSET
    handlers=multilogServerHandler

    [handler_multilogServerHandler]
    class=handlers.TimedRotatingFileHandler
    level=DEBUG
    formatter=simpleFormatter
    args=('/var/log/appName/appName.log', 'midnight')

    [formatter_simpleFormatter]
    class=logging.Formatter
    format=%(asctime)s %(levelname)7s: PID: %(process)5s | %(message)s [in %(pathname)s:%(lineno)d]

and for your application:

.. code-block:: ini

    [loggers]
    keys=root

    [handlers]
    keys=multilogClientHandler

    [formatters]
    keys=simpleFormatter

    [logger_root]
    level=NOTSET
    handlers=multilogClientHandler

    [handler_multilogClientHandler]
    class=handlers.SocketHandler
    level=DEBUG
    formatter=simpleFormatter
    args=('localhost', handlers.DEFAULT_TCP_LOGGING_PORT)

    [formatter_simpleFormatter]
    class=logging.Formatter
    format=%(asctime)s %(levelname)7s: PID: %(process)5s | %(message)s [in %(pathname)s:%(lineno)d]


The important field is the ``args`` block in the ``handler_multilogClientHandler`` section - those parameters should correspond to the server and ports on which the multilog daemon is listening. By default, the daemon uses ``localhost`` and ``logging.handlers.DEFAULT_TCP_LOGGING_PORT``.
