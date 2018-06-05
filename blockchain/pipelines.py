#!/usr/bin/env python
# encoding: utf-8

import os

from dotenv import load_dotenv
from logging.config import fileConfig
from os.path import dirname, join

# Load .env file
dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)


class JSONFileWriterPipeline(object):
    """
    Enable persist data in JSON file.
    """

    def __init__(self, filepath):
        """
        Initialize JSON file writer class config.

        :param str filepath: json file path.
        """
        self._file = path

    def __str__(self):
        """
        Represent class via params string.

        :return str: class representation.
        """
        params = {
            'class': self.__class__.__name__,
            'path': dirname(self._file),
            'filename': basename(self._file),
        }
        return str(params)

    @classmethod
    def config(cls):
        """
        Get JSON file parameters.

        :return cls: JSON file writer class.
        """
        filepath = os.getenv('JSON_FILE_PATH')
        if filepath is not None:
            return cls(filepath)
        else:
            msg = 'Incorrect JSON file configuration: {}'.format(filepath)
            raise ValueError(msg)
