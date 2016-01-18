Multilog
======

.. image:: https://travis-ci.org/humangeo/multilog.svg
   :target: https://travis-ci.org/humangeo/multilog

.. image:: https://coveralls.io/repos/github/humangeo/multilog/badge.svg?branch=master
   :target: https://coveralls.io/github/humangeo/multilog?branch=master

A simple, multiprocess-safe logger for Python

**This requires Python 3+. The future is now.**

Why
---

Python's built-in loggers are pretty handy - they're easily customized and come with useful functionality out
of the box, including things like file rotation. These file handlers are thread-safe, but not process-safe, so, if
you're running a webserver in a pre-forking environment, for example, you run the risk of your workers trampling
over each other when writing to a common log file. File locking is a possible workaround, but that's yucky.

To avoid this, it is recommended that one uses a socket-based logger (`a code sample is helpfully provided in the
Logging Cookbook <https://docs.python.org/3.4/howto/logging-cookbook.html>`_). However, it is just a code snippet.
Multilog is a dependency-free implementation of the sample socket logger with some niceties, like fileConfig
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

For Power Users
---------------

If you want to have Multilog share your application's config, you can do the following:

.. code-block:: ini

    [loggers]
    keys=root,appName

    [handlers]
    keys=multilogClientHandler,multilogServerHandler

    [formatters]
    keys=simpleFormatter

    [logger_root]
    level=NOTSET
    handlers=%(root_handler)s

    [logger_appName]
    level=INFO
    handlers=
    propagate=1
    qualname=appName

    [handler_multilogClientHandler]
    class=handlers.SocketHandler
    level=DEBUG
    formatter=simpleFormatter
    args=('localhost', handlers.DEFAULT_TCP_LOGGING_PORT)

    [handler_multilogServerHandler]
    class=handlers.TimedRotatingFileHandler
    level=DEBUG
    formatter=simpleFormatter
    args=('/var/log/appName/appName.log', 'midnight')

    [formatter_simpleFormatter]
    class=logging.Formatter
    format=%(asctime)s %(levelname)7s: PID: %(process)5s | %(message)s [in %(pathname)s:%(lineno)d]

Then, in your application, pass the root handler name into the logging config:

.. code-block:: python

    import logging
    logging.config.fileConfig(config_path, defaults={"root_handler": "multilogClientHandler"})

Multilog will always load the ``multilogServerHandler`` handler.  If you don't want to run Multilog (if you're running a single-threaded local dev server, for example), simply change your ``root_handler`` value to ``multilogServerHandler`` to write to the handler.
