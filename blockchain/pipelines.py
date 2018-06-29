#!/usr/bin/env python
# encoding: utf-8

import json
import logging
import os
import pymongo

from dotenv import load_dotenv
from functools import partial
from json import JSONDecoder
from logging.config import fileConfig
from os.path import dirname, join
from pymongo.errors import ConnectionFailure

# Custom logger
fileConfig(join(dirname(dirname(__file__)), 'logging.cfg'))
logger = logging.getLogger(__name__)

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

    def __str__(self):
        """
        Represent class via params string.

        :return str: class representarion.
        """
        params = {
            'classname': self.__class__.__name__,
            'url': self._mongo_url,
            'db': self._mongo_db,
            'collection': self._mongo_collection,
        }
        return str(params)

    @classmethod
    def config(cls):
        """
        Get MongoDB configuration parameters.

        :return cls: MongoDBPipeline class.
        """
        mongo_config = {
            'mongo_url': os.getenv('MONGO_URL'),
            'mongo_db': os.getenv('MONGO_DB'),
            'mongo_collection': os.getenv('MONGO_COLLECTION'),
        }
        if None not in mongo_config.values():
            return cls(**mongo_config)
        else:
            msg = 'Incorrect MongoDB configuration: {}'.format(mongo_config)
            raise ValueError(msg)

    def open_connection(self):
        """
        Establish MongoDB client connection.
        """
        self.client = pymongo.MongoClient(self._mongo_uri)
        if self.client is None:
            raise ConnectionFailure('No client connection: {}').format(self._mongo_uri)
        self.db = self.client[self._mongo_db]
        self.collection = self.db[self._mongo_collection]

    def close_connection(self):
        """
        Close MongoDB client connection.
        """
        self.client.close()

    def _insert(self, data):
        """
        Insert data in MongoDB.

        :param json data: json data to insert.
        :return json: inserted data in MongoDB.
        """
        self.collection.insert_one(data)
        logger.info('Data inserted to MongoDB: %s', data)
        return data

    def _update(self, data):
        """
        Update data in MongoDB.

        :param json data: json data to update.
        :return json: updated data in MongoDB.
        """
        criteria = data.get('_slug', None)
        if criteria is not None:
            self.collection.update_one({'_slug': criteria}, {'$set': data})
            logger.info('Data updated to MongoDB: %s', data)
            return data.update({'_slug': criteria})

        logger.error('Failed to update data to MongoDB: %s', data)
        return False

    def _delete(self, data):
        """
        Delete data in MongoDB.

        :param json data: json data to delete.
        :return json: deleted data in MongoDB.
        """
        criteria = data.get('_slug')
        if criteria is not None:
            self.collection.delete_one({'_slug': criteria})
            logger.info('Data deleted from MongoDB: %s', data)
            return data

        logger.info('Failed to delete data from MongoDB: %s', data)
        return False

    def persist_data(self, data):
        """
        Persist data in MongoDB.

        :param json data: json data to persist.
        :return json: persisted data in MongoDB.
        """
        for key, value in data.items():
            if not value:
                raise ValueError('Missing value for: {}'.format(key))

        try:
            data_found = self.collection.find_one(
                {'_slug': data.get('_slug')},
                {'_slug': 1, '_id': 0}
            )
            if data_found:
                return self._update(data)
            return self._insert(data)

        except PyMongoError as msg:
            logger.error('Database operation failure: %s', msg)

    @property
    def configuration(self):
        """
        Show database configuration parameters.

        :return dict: MongoDB configuration.
        """
        return {
            'url': self._mongo_url,
            'database': self._mongo_db,
            'collection': self._mongo_collection,
        }


class PostgreSQLPipeline(object):
    """
    Enable persist data in PostgreSQL database.
    """
    pass
