#!/usr/bin/env python
# encoding: utf-8

import codecs
import re

from os.path import dirname, join
from setuptools import setup, find_packages


def read(*path_parts):
    file_path = join(dirname(__file__), *path_parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*path_parts):
    version = read(*path_parts)
    match = re.search(r'^__version__ = ["\']([^"\']*)["\']', version, re.M)
    if match:
        return str(match.group(1))

    raise RuntimeError('Unable to find module version.')


setup(
    name='blockchain-api-client',
    verbose_name='Blockchain API Client written in Python 3',
    author='Sergio de Diego',
    version=find_version('blockchainAPI', '__init__.py'),
    description='Blockchain statistics and market data fetcher client',
    long_description=read('README.md'),
    url='https://github.com/sdediego/blockchain-api-client',
    license='MIT',
    requires=read('requirements.txt'),
    packages=find_packages(),
    keywords='Blockchain Bitcoin API client Python',
    entry_points={
        'console_scripts': [
            'run_scheduler = scheduler',
        ],
    },
)
