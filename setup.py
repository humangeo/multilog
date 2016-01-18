"""Set up the package."""

import sys
from codecs import open as codecs_open
from setuptools import find_packages, setup

if sys.version_info < (3, 0):
    sys.stdout.write("Multilog requires Python 3 or newer.\n")
    sys.exit(-1)

# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(name='multilog',
      version='0.9.0',
      description="A simple logger for multiple Python processes.",
      long_description=LONG_DESCRIPTION,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: No Input/Output (Daemon)",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX",
          "Programming Language :: Python :: 3 :: Only",
          "Topic :: System :: Logging"
      ],
      keywords='server multiprocess multiproc parallel logger logging logs',
      author="Aru Sahni",
      author_email='aru@thehumangeo.com',
      url='https://github.com/humangeo/multilog',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      extras_require={
          'test': ['nose', 'pylint'],
      },
      entry_points="""
      [console_scripts]
      multilog=multilog.scripts.cli:main
      """)
