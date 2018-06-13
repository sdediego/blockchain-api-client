#!/usr/bin/env python
# encoding: utf-8

import json
import os

from dotenv import load_dotenv
from functools import partial
from json import JSONDecoder
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

    def write(self, data):
        """
        Open file connection and write data.
        """
        with open(self._file, 'a') as json_file:
            json.dump(data, json_file, indent=2)
            json.dump('\n\n')

    def read(self):
        """
        Open file connection and read data.

        :return list: list with json objects.
        """
        with open(self._file, 'r') as json_file:
            return list(self._parse(json_file))

    def _parse(self, file, decoder=JSONDecoder(), delimeter='\n', buffer_size=2048):
        """
        Yield complete JSON objects as the parser finds them.

        :param obj file: json file object to parse.
        :param obj decoder: json decoder instance.
        :param str delimeter: json objects delimeter in file.
        :param int buffer_size: buffer size in bytes.
        """
        buffer = ''
        for chunk in iter(partial(file.read, buffer_size), ''):
            buffer += chunk
            while buffer:
                try:
                    stripped = buffer.strip(delimeter)
                    result, index = decoder.raw_decode(stripped)
                    yield result
                    buffer = stripped[index:]
                except ValueError:
                    break


class MongoDBPipeline(object):
    """
    Enable persist data in MongoDB.
    """

    def __init__(self, mongo_url, mongo_db, mongo_collection):
        """
        Initialize MongoDB class config.

        :param str mongo_uri: MongoDB identifier.
        :param str mongo_db: MongoDB name.
        :param str mongo_collection: MongoDB collection name.
        """
        self._mongo_url = mongo_url
        self._mongo_db = mongo_db
        self._mongo_collection = mongo_collection
        self._mongo_uri = self._mongo_url + self._mongo_db
