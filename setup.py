# -*- coding: utf-8 -*-

import os

from setuptools import setup
from setuptools import find_packages

install_requires = [
    'setuptools',
    'jinja2<2.7',  # 2.7 doesn't support python 3.2
    'six>=1.2.0',  # 1.1.0 release doesn't have six.moves.input
]

try:
    import importlib  # NOQA
except ImportError:
    install_requires.append('importlib')

try:
    from collections import OrderedDict  # NOQA
except ImportError:
    install_requires.append('ordereddict')

try:
    import argparse  # NOQA
except ImportError:
    install_requires.append('argparse')


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(name='mr.bobby',
      version='0.1.dev0',
      description='Bobby renders directory structure templates',
      long_description=read('README.rst') + "\n" + read('HISTORY.rst'),
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
      ],
      author='Jean-Philippe Camguilhem, Cyprien Le Pannérer',
      author_email='',
      url='https://github.com/jpcw/mr.bobby.git',
      license='BSD',
      packages=find_packages(),
      install_requires=install_requires,
      extras_require={
          'test': [
              'nose',
              'coverage<3.6dev',
              'flake8<2.0',
              'mock',
          ],
          'development': [
              'zest.releaser',
              'Sphinx',
          ],
      },
      entry_points="""
      [console_scripts]
      mrbobby = mrbobby.cli:main
      """,
      include_package_data=True,
      zip_safe=False,
      )
