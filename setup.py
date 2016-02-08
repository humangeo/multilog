"""Set up the package."""

import sys
from codecs import open as codecs_open
from setuptools import find_packages, setup

TEST_REQUIREMENTS = []

if sys.version_info < (3, 0):
    TEST_REQUIREMENTS.extend(["astroid==1.2.1", "pylint==1.3.1", "mock==1.3.0", "nose==1.3.7", "coverage==4.0.3"])
else: # New Python
    TEST_REQUIREMENTS.extend(["mock", "nose", "coverage", "pylint"])

# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(name='multilog',
      version='1.1.0',
      description="A simple logger for multiple Python processes.",
      long_description=LONG_DESCRIPTION,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: No Input/Output (Daemon)",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
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
          'test': TEST_REQUIREMENTS,
      },
      entry_points="""
      [console_scripts]
      multilog=multilog.scripts.cli:main
      """)
