#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages


setup(
    name='blockchain-api-client',
    author='Sergio de Diego',
    version='1.0',
    description='Blockchain statistics and market data fetcher client',
    url='https://github.com/sdediego/blockchain-api-client',
    license='MIT',
    packages=find_packages(),
    keywords='Blockchain Bitcoin API client Python',
    entry_points={
        'console_scripts': [
            'run_scheduler = scheduler',
        ],
    },
)
